"""
retriever.py

Upgraded Retriever:
- Singleton pattern (model loads once)
- ES client with timeout + version detection
- FAISS fallback if ES offline
- Reranker loaded once
- Embedding caching
"""

import os
import torch
from functools import lru_cache
from typing import Dict, List, Any

from sentence_transformers import SentenceTransformer
from pathlib import Path

# ======================================================
# ES IMPORT & FALLBACK
# ======================================================
try:
    from elasticsearch import Elasticsearch
    ES_AVAILABLE = True
except Exception:
    ES_AVAILABLE = False
    Elasticsearch = None

# FAISS fallback
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False


# ======================================================
# CONFIG
# ======================================================
ES_HOST = "http://localhost:9200"
ES_INDEX = "productivity_sme_index"

EMBED_MODEL_NAME = "BAAI/bge-base-en-v1.5"
RERANK_MODEL_NAME = "BAAI/bge-reranker-v2-m3"

KNN_K = 10
BM25_K = 4
RERANK_K = 4


# ======================================================
# RERANKER (FLAG EMBEDDING)
# ======================================================
try:
    from FlagEmbedding import FlagReranker
    HAS_RERANKER = True
except Exception:
    HAS_RERANKER = False
    FlagReranker = None


# ======================================================
# GLOBAL SINGLETON CACHE
# ======================================================
_GLOBAL_RETRIEVER = None


# ======================================================
# Retriever CLASS
# ======================================================
class Retriever:
    def __new__(cls):
        """
        Enforce singleton (only one instance).
        """
        global _GLOBAL_RETRIEVER
        if _GLOBAL_RETRIEVER is None:
            _GLOBAL_RETRIEVER = super().__new__(cls)
        return _GLOBAL_RETRIEVER

    def __init__(self):
        if hasattr(self, "_initialized"):
            return  # prevent re-init

        print("--- Initializing Retriever ---")

        # -----------------------------------
        # Load Embedding Model Once
        # -----------------------------------
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"--> Loading embedding: {EMBED_MODEL_NAME} on {device}")

        self.embed_model = SentenceTransformer(
            EMBED_MODEL_NAME, device=device, trust_remote_code=True
        )

        # -----------------------------------
        # Load Reranker Once
        # -----------------------------------
        if HAS_RERANKER:
            print(f"--> Loading Reranker: {RERANK_MODEL_NAME}")
            self.reranker = FlagReranker(RERANK_MODEL_NAME, use_fp16=False)
        else:
            print("⚠️ Reranker not installed")
            self.reranker = None

        # -----------------------------------
        # Try Elasticsearch
        # -----------------------------------
        self.es = None
        if ES_AVAILABLE:
            try:
                self.es = Elasticsearch(
                    ES_HOST,
                    request_timeout=30,
                    verify_certs=False,
                    retry_on_timeout=True,
                )

                info = self.es.info()
                version = info["version"]["number"]
                print(f"✅ Connected to Elasticsearch v{version}")

            except Exception as e:
                print(f"⚠️ Elasticsearch not reachable: {e}")
                self.es = None
        else:
            print("⚠️ Elasticsearch library not available")

        # -----------------------------------
        # FAISS fallback
        # -----------------------------------
        self.faiss_index = None
        if not self.es:
            print("→ Using FAISS fallback mode (no ES detected)")
            if FAISS_AVAILABLE:
                self._setup_faiss()
            else:
                print("⚠️ FAISS not installed → fallback disabled")

        self._initialized = True
        print("--- Retriever Initialized ---\n")


    # ======================================================
    # FAISS fallback setup
    # ======================================================
    def _setup_faiss(self):
        """
        Creates a blank FAISS index; user can extend this later.
        """
        dim = self.embed_model.get_sentence_embedding_dimension()
        self.faiss_index = faiss.IndexFlatIP(dim)
        self.faiss_texts = []


    # ======================================================
    # Format document
    # ======================================================
    def _format_doc(self, hit):
        src = hit.get("_source", {})
        return {
            "text": src.get("text", ""),
            "metadata": src.get("metadata", {}),
            "id": hit.get("_id", None),
            "score": hit.get("_score", 0),
        }


    # ======================================================
    # CACHED embedding
    # ======================================================
    @lru_cache(maxsize=512)
    def _encode(self, text: str):
        return self.embed_model.encode(text, normalize_embeddings=True).tolist()


    # ======================================================
    # MAIN RETRIEVAL PIPELINE
    # ======================================================
    def fetch_relevant_chunks(self, query: str) -> List[Dict[str, Any]]:

        # --------------------------------------------------
        # 1. Embed query (cached)
        # --------------------------------------------------
        vector = self._encode(query)

        # --------------------------------------------------
        # 2. Elasticsearch mode
        # --------------------------------------------------
        if self.es:
            try:
                # ---- KNN Search ----
                knn_body = {
                    "knn": {
                        "field": "embedding",
                        "query_vector": vector,
                        "k": KNN_K,
                        "num_candidates": 100,
                    },
                    "_source": True,
                }

                knn_hits = self.es.search(index=ES_INDEX, body=knn_body)["hits"]["hits"]

            except Exception:
                knn_hits = []

            # ---- BM25 Search ----
            try:
                bm25_body = {
                    "size": BM25_K,
                    "query": {"match": {"text": query}},
                    "_source": True,
                }

                bm25_hits = self.es.search(index=ES_INDEX, body=bm25_body)["hits"]["hits"]

            except Exception:
                bm25_hits = []

            # ---- MERGE ----
            merged = {}
            for h in knn_hits + bm25_hits:
                merged[h["_id"]] = h

            docs = [self._format_doc(h) for h in merged.values()]

        else:
            # --------------------------------------------------
            # 3. FAISS fallback mode
            # --------------------------------------------------
            if self.faiss_index and len(self.faiss_texts) > 0:
                qvec = torch.tensor([vector], dtype=torch.float32).numpy()
                scores, ids = self.faiss_index.search(qvec, RERANK_K)
                docs = [{"text": self.faiss_texts[i], "score": float(scores[0][j])}
                        for j, i in enumerate(ids[0])]
            else:
                docs = [{"text": "", "metadata": {"warning": "No documents found"}}]

        # --------------------------------------------------
        # 4. RERANK
        # --------------------------------------------------
        if self.reranker and len(docs) > 1:
            try:
                pairs = [[query, d["text"]] for d in docs]
                scores = self.reranker.compute_score(pairs)

                ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
                return [doc for doc, _ in ranked[:RERANK_K]]

            except Exception as e:
                print("⚠️ Reranker error:", e)

        # fallback
        return docs[:RERANK_K]


# ======================================================
# FOR STANDALONE TEST
# ======================================================
if __name__ == "__main__":
    r = Retriever()
    out = r.fetch_relevant_chunks("What is deep work?")
    for d in out:
        print("-", d["text"][:100], "...")