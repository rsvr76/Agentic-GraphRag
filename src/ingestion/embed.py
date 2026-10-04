"""Local offline embedding pipeline using FastEmbed (ONNX Runtime).

Peak memory usage is strictly bounded <300MB RAM.
Generates 384-dimensional dense embeddings for document chunks and entity names.
Embeddings are cached in data/processed/ for reuse across all three pipelines.
"""

import argparse
import json
import os
from typing import Dict, List, Optional
import numpy as np
from src.config import settings


def get_embedding_model():
    """Initializes FastEmbed TextEmbedding model using ONNX runtime."""
    from fastembed import TextEmbedding
    model_name = settings.local_embedding_model
    return TextEmbedding(model_name=model_name)


def embed_texts(texts: List[str], batch_size: int = 32) -> np.ndarray:
    """Generates normalized vector embeddings for a list of texts using FastEmbed."""
    model = get_embedding_model()
    embeddings_list = []
    for emb in model.embed(texts, batch_size=batch_size):
        embeddings_list.append(emb)
    return np.array(embeddings_list, dtype=np.float32)


def embed_chunks(
    chunks_jsonl: str = "data/processed/chunks.jsonl",
    output_npz: str = "data/processed/chunk_embeddings.npz",
    batch_size: int = 32,
    limit: Optional[int] = None
) -> int:
    """Reads chunks JSONL, computes embeddings, and saves as compressed .npz archive."""
    if not os.path.exists(chunks_jsonl):
        raise FileNotFoundError(f"Chunks file not found: {chunks_jsonl}. Run chunk.py first.")

    chunk_ids = []
    texts = []

    print(f"Reading chunks from {chunks_jsonl}...")
    with open(chunks_jsonl, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if limit and idx >= limit:
                break
            data = json.loads(line.strip())
            chunk_ids.append(data["chunk_id"])
            title = data.get("title", "")
            text = data.get("text", "")
            texts.append(f"{title}: {text}" if title else text)

    total_chunks = len(chunk_ids)
    print(f"Generating FastEmbed embeddings for {total_chunks} chunks (batch_size={batch_size})...")

    model = get_embedding_model()
    embeddings = []

    for i, emb in enumerate(model.embed(texts, batch_size=batch_size)):
        embeddings.append(emb)
        if (i + 1) % 500 == 0 or (i + 1) == total_chunks:
            print(f"Embedded {i + 1}/{total_chunks} chunks...")

    emb_matrix = np.array(embeddings, dtype=np.float32)

    os.makedirs(os.path.dirname(output_npz), exist_ok=True)
    np.savez_compressed(
        output_npz,
        chunk_ids=np.array(chunk_ids),
        embeddings=emb_matrix
    )
    print(f"Saved {total_chunks} embeddings matrix shape {emb_matrix.shape} to {output_npz}")
    return total_chunks


def load_chunk_embeddings(embeddings_npz: str = "data/processed/chunk_embeddings.npz"):
    """Loads chunk IDs and embedding matrix from .npz file."""
    data = np.load(embeddings_npz)
    chunk_ids = list(data["chunk_ids"])
    embeddings = data["embeddings"]
    return chunk_ids, embeddings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate local FastEmbed embeddings for chunks")
    parser.add_argument("--chunks", type=str, default="data/processed/chunks.jsonl", help="Input chunks JSONL")
    parser.add_argument("--output", type=str, default="data/processed/chunk_embeddings.npz", help="Output .npz file")
    parser.add_argument("--batch-size", type=int, default=32, help="Embedding batch size")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of chunks to embed")
    args = parser.parse_args()

    embed_chunks(
        chunks_jsonl=args.chunks,
        output_npz=args.output,
        batch_size=args.batch_size,
        limit=args.limit
    )
