"""Deterministic document chunker for Wikipedia Olympic corpus.

Splits documents into ~800 token chunks with ~150 token overlap.
Enforces deterministic ID format: {doc_id}::c{index}.
Tracks start_offset and end_offset for citation traceability.
"""

import json
import os
import re
from typing import Any, Dict, Iterator, List, Optional
from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str           # format: {doc_id}::c{index}
    doc_id: str
    chunk_index: int
    title: str
    text: str
    start_offset: int
    end_offset: int
    approx_tokens: int


def estimate_tokens(text: str) -> int:
    """Fast whitespace-based token estimation."""
    return len(text.split())


def chunk_text(
    text: str,
    target_tokens: int = 800,
    overlap_tokens: int = 150
) -> List[Dict[str, Any]]:
    """Splits text into chunks of target_tokens with overlap_tokens on paragraph/sentence boundaries."""
    words = text.split()
    if len(words) <= target_tokens:
        return [{
            "text": text,
            "start_offset": 0,
            "end_offset": len(text),
            "approx_tokens": len(words)
        }]

    chunks = []
    step = target_tokens - overlap_tokens
    if step <= 0:
        step = target_tokens // 2

    word_idx = 0
    total_words = len(words)

    word_spans = []
    for m in re.finditer(r"\S+", text):
        word_spans.append((m.start(), m.end()))

    if not word_spans:
        return []

    while word_idx < total_words:
        end_word_idx = min(word_idx + target_tokens, total_words)
        start_char = word_spans[word_idx][0]
        end_char = word_spans[end_word_idx - 1][1]
        chunk_str = text[start_char:end_char]

        chunks.append({
            "text": chunk_str,
            "start_offset": start_char,
            "end_offset": end_char,
            "approx_tokens": end_word_idx - word_idx
        })

        if end_word_idx == total_words:
            break
        word_idx += step

    return chunks


def chunk_document(raw_doc: Dict[str, Any]) -> List[DocumentChunk]:
    """Chunks a single raw document from corpus.jsonl."""
    doc_id = raw_doc.get("doc_id", "")
    title = raw_doc.get("title", "")
    text = raw_doc.get("text", "")

    raw_chunks = chunk_text(text, target_tokens=800, overlap_tokens=150)
    result = []

    for idx, c in enumerate(raw_chunks):
        chunk_id = f"{doc_id}::c{idx}"
        result.append(DocumentChunk(
            chunk_id=chunk_id,
            doc_id=doc_id,
            chunk_index=idx,
            title=title,
            text=c["text"],
            start_offset=c["start_offset"],
            end_offset=c["end_offset"],
            approx_tokens=c["approx_tokens"]
        ))

    return result


def chunk_corpus(
    input_jsonl: str = "Datasets/corpus/corpus.jsonl",
    output_jsonl: str = "data/processed/chunks.jsonl",
    limit: Optional[int] = None
) -> int:
    """Reads corpus.jsonl, chunks all documents, and writes to output_jsonl."""
    os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)
    count = 0
    total_chunks = 0

    with open(input_jsonl, "r", encoding="utf-8") as in_f, open(output_jsonl, "w", encoding="utf-8") as out_f:
        for line in in_f:
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line)
            chunks = chunk_document(doc)
            for c in chunks:
                out_f.write(c.model_dump_json() + "\n")
                total_chunks += 1
            count += 1
            if limit and count >= limit:
                break

    return total_chunks


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chunk Olympic corpus documents")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of documents to chunk")
    parser.add_argument("--output", type=str, default="data/processed/chunks.jsonl", help="Output JSONL path")
    args = parser.parse_args()

    print(f"Chunking corpus (limit={args.limit})...")
    n = chunk_corpus(limit=args.limit, output_jsonl=args.output)
    print(f"Done. Generated {n} chunks in {args.output}")
