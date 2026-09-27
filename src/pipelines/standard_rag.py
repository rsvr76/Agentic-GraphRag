"""Pipeline 1: Standard Dense Retrieval-Augmented Generation (Baseline).

Implements Section 8 of Final Plan (v3):
1. Embed question using FastEmbed model.
2. Vector similarity search over chunk embeddings, top-k (k=10).
3. Deterministic chunk ordering (descending score, tie-break by chunk_id).
4. Single-pass LLM generation with chunk citations.
5. Structured PipelineResult logging.
"""

import os
import re
import time
import json
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.config import settings
from src.llm.client import llm_client
from src.ingestion.embed import embed_texts
from src.evaluation.metrics import PipelineResult, calculate_exact_match


class StandardRAGPipeline:
    def __init__(
        self,
        embeddings_npz: str = "data/processed/chunk_embeddings.npz",
        chunks_jsonl: str = "data/processed/chunks.jsonl",
        top_k: int = 5
    ):
        self.name = "Standard RAG"
        self.top_k = top_k
        self.chunk_ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self.chunks_data: Dict[str, Dict[str, Any]] = {}
        
        # Fall back to full embeddings if checkpoint not found
        if not os.path.exists(embeddings_npz) and os.path.exists("data/processed/chunk_embeddings.npz"):
            embeddings_npz = "data/processed/chunk_embeddings.npz"
        if not os.path.exists(chunks_jsonl) and os.path.exists("data/processed/chunks.jsonl"):
            chunks_jsonl = "data/processed/chunks.jsonl"
            
        self._load_corpus(embeddings_npz, chunks_jsonl)

    def _load_corpus(self, embeddings_npz: str, chunks_jsonl: str):
        """Loads precomputed chunk embeddings and chunk texts into memory."""
        if os.path.exists(embeddings_npz):
            data = np.load(embeddings_npz)
            self.chunk_ids = list(data["chunk_ids"])
            self.embeddings = data["embeddings"]
            
            # Normalize embeddings for cosine similarity
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1e-9
            self.embeddings = self.embeddings / norms

        if os.path.exists(chunks_jsonl):
            with open(chunks_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        c = json.loads(line)
                        self.chunks_data[c["chunk_id"]] = c

    def retrieve(self, question: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Dense vector retrieval with deterministic ordering."""
        k = top_k or self.top_k
        if self.embeddings is None or len(self.chunk_ids) == 0:
            return []

        # 1. Embed incoming question with same FastEmbed model
        q_emb = embed_texts([question])[0]
        q_norm = np.linalg.norm(q_emb)
        if q_norm > 0:
            q_emb = q_emb / q_norm

        # 2. Vector cosine similarities (dot product since normalized)
        sim_scores = np.dot(self.embeddings, q_emb)

        # 3. Deterministic ranking: sort by (-score, chunk_id)
        ranked_indices = sorted(
            range(len(self.chunk_ids)),
            key=lambda idx: (-sim_scores[idx], self.chunk_ids[idx])
        )[:k]

        retrieved = []
        for idx in ranked_indices:
            cid = self.chunk_ids[idx]
            chunk_info = self.chunks_data.get(cid, {})
            retrieved.append({
                "chunk_id": cid,
                "doc_id": chunk_info.get("doc_id", cid.split("::")[0] if "::" in cid else cid),
                "title": chunk_info.get("title", ""),
                "text": chunk_info.get("text", ""),
                "score": float(sim_scores[idx])
            })
        return retrieved

    def run(
        self,
        qid: str,
        question: str,
        ground_truth: List[str],
        gold_doc_ids: Optional[List[str]] = None,
        qtype: str = ""
    ) -> PipelineResult:
        start_time = time.time()

        # 1. Retrieve top-k chunks
        retrieved_chunks = self.retrieve(question)
        retrieved_doc_ids = list(dict.fromkeys(c["doc_id"] for c in retrieved_chunks))

        # 2. Build deterministic prompt
        context_parts = []
        for c in retrieved_chunks:
            title_header = f" [{c['title']}]" if c.get('title') else ""
            context_parts.append(f"[{c['chunk_id']}]{title_header}\n{c['text']}")
        context_text = "\n\n".join(context_parts)

        prompt = (
            "You are answering an Olympic Games historical question based strictly on the provided context passages.\n\n"
            f"Context Passages:\n{context_text}\n\n"
            f"Question: {question}\n\n"
            "Instructions:\n"
            "1. Answer concisely and accurately based solely on the facts in the context.\n"
            "2. Cite the specific chunk IDs you used to find the answer (e.g. [doc_id::c0]).\n"
            "3. If the answer cannot be determined from the passages, state 'Unknown based on provided context'.\n\n"
            "Answer:"
        )

        # 3. Single-pass LLM call
        response = llm_client.generate(prompt=prompt)
        latency = time.time() - start_time

        # 4. Extract cited chunk IDs
        cited_chunks = re.findall(r"\[([a-zA-Z0-9_\-\.\:\s]+::c\d+)\]", response.content)
        cited_chunks = list(dict.fromkeys(cited_chunks))

        # 5. Calculate Exact Match
        acc = calculate_exact_match(response.content, ground_truth)

        # 6. Build execution trace
        trace = {
            "strategy": "dense_vector_search",
            "model": "sentence-transformers/all-MiniLM-L6-v2 (FastEmbed ONNX)",
            "top_k": len(retrieved_chunks),
            "retrieved_chunks": [
                {
                    "chunk_id": c["chunk_id"],
                    "doc_id": c["doc_id"],
                    "title": c.get("title", ""),
                    "score": round(float(c.get("score", 0.0)), 4)
                }
                for c in retrieved_chunks
            ],
            "context_length_chars": len(context_text)
        }

        return PipelineResult(
            pipeline_name=self.name,
            question_id=qid,
            question=question,
            qtype=qtype,
            prediction=response.content.strip(),
            ground_truth=ground_truth,
            retrieved_doc_ids=retrieved_doc_ids,
            gold_doc_ids=gold_doc_ids or [],
            cited_chunk_ids=cited_chunks,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens,
            latency_seconds=round(latency, 3),
            accuracy_score=acc,
            completeness_score=acc,
            execution_trace=trace
        )
