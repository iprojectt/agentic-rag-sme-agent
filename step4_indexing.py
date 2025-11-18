"""
STEP 4: VECTOR DATABASE INDEXING (Elasticsearch 8.14 Compatible)
================================================================
No deprecated settings.
Uses ES8 automatic HNSW indexing.
"""

import json
import sys
from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

# -------------------------------
# CONFIG
# -------------------------------
ES_HOST = "http://localhost:9200"
ES_INDEX_NAME = "productivity_sme_index"
EMBEDDED_DATA_DIR = "output/embedded_data"
WINNING_MODEL_SUFFIX = "BAAI/bge-base-en-v1.5".replace("/", "_")


# -------------------------------
# CREATE INDEX (correct ES 8.14)
# -------------------------------
def create_es_index(es: Elasticsearch, dim: int):

    # delete old index
    if es.indices.exists(index=ES_INDEX_NAME):
        print(f"--> Index '{ES_INDEX_NAME}' exists. Deleting...")
        es.indices.delete(index=ES_INDEX_NAME)

    print(f"--> Creating new index '{ES_INDEX_NAME}' with dim={dim}")

    mappings = {
        "properties": {
            "embedding": {
                "type": "dense_vector",
                "dims": dim,
                "similarity": "cosine"   # HNSW auto-enabled
            },
            "text": {"type": "text"},
            "metadata": {"type": "object", "enabled": True}
        }
    }

    # NO deprecated settings
    es.indices.create(
        index=ES_INDEX_NAME,
        mappings=mappings
    )

    print("--> Index creation completed.\n")


# -------------------------------
# MAIN
# -------------------------------
def main():
    print("--- STEP 4: Elasticsearch Indexing ---")

    try:
        es = Elasticsearch(ES_HOST, request_timeout=120, verify_certs=False)
        if not es.ping():
            raise ConnectionError("ES Ping failed.")
        print("Connected → Elasticsearch OK.\n")
    except Exception as e:
        print("FATAL: Cannot connect:", e)
        sys.exit(1)

    # find embedded chunks
    embed_dir = Path(EMBEDDED_DATA_DIR)
    safe_suffix = WINNING_MODEL_SUFFIX.replace("/", "_")
    files_to_index = list(embed_dir.glob(f"*_{safe_suffix}.json"))

    if not files_to_index:
        print("ERROR: No embedding files found.")
        sys.exit(1)

    print(f"Found {len(files_to_index)} embedded files.\n")

    # determine dims
    with open(files_to_index[0], "r", encoding="utf-8") as f:
        dim = json.load(f)[0]["embedding_dim"]

    create_es_index(es, dim)

    # Prepare bulk
    actions = []
    print("Preparing bulk actions...")

    for fp in tqdm(files_to_index):
        with open(fp, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        for chunk in chunks:
            actions.append({
                "_index": ES_INDEX_NAME,
                "_id": chunk["chunk_id"],
                "_source": {
                    "text": chunk.get("text", ""),
                    "embedding": chunk.get("embedding", []),
                    "metadata": chunk.get("metadata", {})
                }
            })

    print(f"Prepared {len(actions)} documents.\n")

    # Bulk insert
    print("Executing bulk insert...")
    try:
        success, failed = bulk(
            es, actions,
            chunk_size=500,
            request_timeout=200,
            raise_on_error=False
        )
        print("\n=== INDEXING COMPLETE ===")
        print("Indexed:", success)
        print("Failed:", len(failed))
        print("Elasticsearch vector DB is READY ✔")
    except Exception as e:
        print("FATAL BULK ERROR:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
