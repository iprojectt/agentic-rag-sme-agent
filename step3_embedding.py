# step3_embedding.py (Updated for Modular Pipeline)

import json
from pathlib import Path
from typing import List, Dict, Any
import torch
from sentence_transformers import SentenceTransformer
import time
from tqdm import tqdm

class MultiModelEmbedder:
    """
    Generates embeddings for a list of text chunks using multiple SentenceTransformer models.
    This class is designed for comparing the performance and characteristics of different models.
    """
    
    # A curated list of strong candidate models for comparison
    RECOMMENDED_MODELS = {
        "all-mpnet-base-v2": { # Your baseline model
            "dims": 768, "speed": "Medium",
            "description": "Excellent general-purpose model, great for semantic search."
        },
        "BAAI/bge-base-en-v1.5": { # A top-tier alternative from MTEB leaderboard
            "dims": 1024, "speed": "Slow",
            "description": "High-performance model, often a leader on benchmarks."
        },
        "all-MiniLM-L6-v2": { # A fast, lightweight option
            "dims": 384, "speed": "Very Fast",
            "description": "Very fast and lightweight, great for speed-critical tasks."
        }
    }
    
    def __init__(self, model_names: List[str] = None):
        if model_names is None:
            # Default to the recommended set for a robust comparison
            model_names = list(self.RECOMMENDED_MODELS.keys())
        
        self.model_names = model_names
        self.models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f" Initializing Multi-Model Embedder on device: {self.device.upper()}")
        
        for model_name in self.model_names:
            print(f"\n Loading model: {model_name}")
            model = SentenceTransformer(model_name, device=self.device)
            self.models[model_name] = model
            print(f"    Model '{model_name}' loaded successfully.")
    
    def generate_embeddings_for_all_models(self, chunks: List[Dict[str, Any]], batch_size: int = 64) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generates embeddings for the given chunks using all loaded models.

        Args:
            chunks: A list of chunk dictionaries from step2.
            batch_size: The number of chunks to process at once.

        Returns:
            A dictionary where keys are model names and values are lists of chunks with embeddings.
        """
        results = {}
        texts_to_embed = [chunk["text"] for chunk in chunks]
        
        if not texts_to_embed:
            return {}

        for model_name, model in self.models.items():
            print(f"\n--- Generating embeddings with '{model_name}' ---")
            start_time = time.time()
            
            # Use the model's encode method with a progress bar for user feedback
            embeddings = model.encode(
                texts_to_embed,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True # Efficient format
            ).tolist() # Convert to standard Python list for JSON serialization

            elapsed = time.time() - start_time
            
            # Add the generated embedding and model info to each chunk
            chunks_with_embeddings = []
            for i, chunk in enumerate(chunks):
                chunk_copy = chunk.copy()
                chunk_copy["embedding"] = embeddings[i]
                chunk_copy["embedding_model"] = model_name
                chunk_copy["embedding_dim"] = len(embeddings[i])
                chunks_with_embeddings.append(chunk_copy)
            
            results[model_name] = chunks_with_embeddings
            
            print(f"    Completed in {elapsed:.2f} seconds.")
            print(f"   Average time per chunk: {elapsed/len(texts_to_embed)*1000:.2f} ms")
        
        return results

class EmbeddingPipeline:
    """
    Manages the full process of reading chunked data, generating embeddings with multiple
    models, and saving the results for later indexing and evaluation.
    """
    
    def __init__(self, input_dir: str = "output/chunked_data", output_dir: str = "output/embedded_data"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.embedder = MultiModelEmbedder()
        
        print("\n" + "="*60)
        print(f" Input directory (chunks):  {self.input_dir}")
        print(f" Output directory (embeddings): {self.output_dir}")
        print("="*60 + "\n")

    def run_pipeline(self):
        chunk_files = list(self.input_dir.glob("*_chunks.json"))
        if not chunk_files:
            print(f" ERROR: No chunk files ('*_chunks.json') found in '{self.input_dir}'. Run Step 2 first.")
            return

        print(f" Found {len(chunk_files)} chunk files to process.")
        
        all_results_for_report = {}

        for file_path in tqdm(chunk_files, desc="Processing files"):
            with open(file_path, 'r', encoding='-utf-8') as f:
                chunks = json.load(f)
            
            if not chunks:
                continue

            # Generate embeddings for this file's chunks using all models
            embedding_results = self.embedder.generate_embeddings_for_all_models(chunks)
            
            # Save the output for each model into a separate file
            for model_name, embedded_chunks in embedding_results.items():
                safe_model_name = model_name.replace("/", "_") # Make filename safe
                output_filename = f"{file_path.stem}_{safe_model_name}.json"
                output_path = self.output_dir / output_filename
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(embedded_chunks, f, indent=2, ensure_ascii=False)
            
            all_results_for_report[file_path.name] = {m: len(c) for m, c in embedding_results.items()}

        self._generate_comparison_report(all_results_for_report)
        print("\n" + "="*60)
        print(" EMBEDDING GENERATION COMPLETE")
        print("="*60)

    def _generate_comparison_report(self, report_data: Dict):
        report = {
            "models_compared": self.embedder.model_names,
            "files_processed": list(report_data.keys()),
            "total_chunks_processed": sum(next(iter(d.values())) for d in report_data.values() if d),
            "model_details": {}
        }

        for model_name in self.embedder.model_names:
            report["model_details"][model_name] = self.embedder.RECOMMENDED_MODELS.get(model_name, {})
        
        report_path = self.output_dir / "_comparison_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        
        print(f"\n Comparison report saved to: {report_path}")

if __name__ == "__main__":
    pipeline = EmbeddingPipeline()
    pipeline.run_pipeline()

    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. EVALUATE: Use 'test_retrieval.py' with your Golden Set to test the")
    print("   performance of each generated model's embeddings.")
    print("\n2. CHOOSE A WINNER: Based on your evaluation, decide which model is best.")
    print("\n3. INDEX: Run 'step4_indexing.py', making sure to set the")
    print("   'WINNING_MODEL_SUFFIX' variable to your chosen model.")
    print("="*60)