# step2_chunking.py (Updated with Manifest and Custom Metadata)

import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

class TextChunker:
    """Breaks text into hierarchical chunks with metadata"""
    
    def __init__(self, chunk_sizes: List[int] = [1024, 512, 256], overlap_tokens: int = 50):
        self.chunk_sizes = sorted(chunk_sizes, reverse=True)
        self.overlap_tokens = overlap_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base") if TIKTOKEN_AVAILABLE else None

    def _split_text_to_chunks(self, text: str, chunk_size: int) -> List[str]:
        tokens = self.tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - self.overlap_tokens):
            chunk_tokens = tokens[i:i + chunk_size]
            chunks.append(self.tokenizer.decode(chunk_tokens))
        return chunks

    def create_hierarchical_chunks(self, text: str, txt_filename: str, doc_metadata: Dict) -> List[Dict[str, Any]]:
        doc_id = hashlib.md5(txt_filename.encode()).hexdigest()[:12]
        all_chunks = []
        
        # Base metadata that is common to all chunks from this document
        base_metadata = {
            "author": doc_metadata.get("author", "Unknown"),
            "source": doc_metadata.get("source", "Unknown"),
            "subject": doc_metadata.get("subject", "Uncategorized"),
            "context": doc_metadata.get("context", "General"),
            "source_document": txt_filename,
            "document_id": doc_id,
            "created_at": datetime.now().isoformat()
        }

        level_0_chunks = self._split_text_to_chunks(text, self.chunk_sizes[0])
        for i, l0_text in enumerate(level_0_chunks):
            l0_id = f"{doc_id}_L0_{i:04d}"
            l0_chunk = {"chunk_id": l0_id, "text": l0_text, "level": 0, "parent_id": None, "metadata": {**base_metadata, "level": 0}}
            all_chunks.append(l0_chunk)

            level_1_chunks = self._split_text_to_chunks(l0_text, self.chunk_sizes[1])
            for j, l1_text in enumerate(level_1_chunks):
                l1_id = f"{l0_id}_L1_{j:04d}"
                l1_chunk = {"chunk_id": l1_id, "text": l1_text, "level": 1, "parent_id": l0_id, "metadata": {**base_metadata, "level": 1, "parent_chunk_id": l0_id}}
                all_chunks.append(l1_chunk)
                
                level_2_chunks = self._split_text_to_chunks(l1_text, self.chunk_sizes[2])
                for k, l2_text in enumerate(level_2_chunks):
                    l2_id = f"{l1_id}_L2_{k:04d}"
                    l2_chunk = {"chunk_id": l2_id, "text": l2_text, "level": 2, "parent_id": l1_id, "metadata": {**base_metadata, "level": 2, "parent_chunk_id": l1_id}}
                    all_chunks.append(l2_chunk)
        return all_chunks

class ChunkingPipeline:
    def __init__(self, input_dir: str = "output/extracted_texts", output_dir: str = "output/chunked_data"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.chunker = TextChunker()
        self.metadata_map = self._load_metadata()
        self.extraction_manifest = self._load_manifest()
        
        print(f"📂 Input directory: {self.input_dir}")
        print(f"📂 Output directory: {self.output_dir}\n")

    def _load_metadata(self) -> Dict[str, Any]:
        metadata_path = Path("metadata.json")
        if not metadata_path.exists():
            print("⚠ WARNING: metadata.json not found.")
            return {}
        with open(metadata_path, 'r', encoding='utf-8') as f:
            print("✅ Metadata catalog loaded.")
            return json.load(f)

    def _load_manifest(self) -> Dict[str, Any]:
        manifest_path = self.input_dir / "_manifest.json"
        if not manifest_path.exists():
            print("❌ ERROR: _manifest.json not found. Run Step 1 first.")
            return {}
        with open(manifest_path, 'r', encoding='utf-8') as f:
            print("✅ Extraction manifest loaded.")
            return json.load(f)

    def chunk_all_texts(self):
        text_files = [f for f in self.input_dir.glob("*.txt") if f.name != "_manifest.json"]
        if not text_files:
            print(f"⚠ No .txt files found in {self.input_dir}")
            return
        
        print(f"📚 Found {len(text_files)} text files to chunk\n")
        
        for idx, text_file in enumerate(text_files, 1):
            print(f"[{idx}/{len(text_files)}] Chunking: {text_file.name}")
            
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()

            # Reliably find the original filename using the manifest
            original_filename = self.extraction_manifest.get(text_file.name)
            if not original_filename:
                print(f"   ⚠ Warning: No original source found for '{text_file.name}' in manifest. Skipping.")
                continue

            doc_metadata = self.metadata_map.get(original_filename, {})
            if not doc_metadata:
                print(f"   ⚠ Warning: No metadata entry found for '{original_filename}'. Using defaults.")
            
            chunks = self.chunker.create_hierarchical_chunks(text, text_file.name, doc_metadata)
            
            output_file = self.output_dir / f"{text_file.stem}_chunks.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            
            print(f"   💾 Saved {len(chunks)} chunks to: {output_file.name}\n")

if __name__ == "__main__":
    if not TIKTOKEN_AVAILABLE:
        print("\n" + "="*60)
        print("WARNING: tiktoken is not installed. Chunk sizes will be approximate.")
        print("For accurate chunking, please install it: pip install tiktoken")
        print("="*60 + "\n")
    
    pipeline = ChunkingPipeline()
    pipeline.chunk_all_texts()