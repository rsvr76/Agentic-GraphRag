"""Pipeline 1: Standard Dense Retrieval-Augmented Generation (Baseline)."""

import time
from typing import List
from src.llm.client import llm_client
from src.evaluation.metrics import PipelineResult, calculate_exact_match


class StandardRAGPipeline:
    def __init__(self):
        self.name = "Standard RAG"

    def run(self, qid: str, question: str, ground_truth: List[str], gold_doc_ids: List[str] = None) -> PipelineResult:
        start_time = time.time()
        
        # 1. Dense retrieval simulation / Vector DB lookup
        # In full production, this calls TigerGraph Vector DB search
        retrieved_context = (
            f"[Passage retrieved via Vector Similarity for query '{question}']\n"
            f"Olympic Games historical records contain events, participating nations, and medalists."
        )
        
        prompt = (
            f"You are answering a question based solely on the provided context.\n"
            f"Context:\n{retrieved_context}\n\n"
            f"Question: {question}\n"
            f"Provide a concise, direct answer based strictly on the text above."
        )
        
        # 2. Single-pass LLM generation
        response = llm_client.generate(prompt=prompt)
        latency = time.time() - start_time
        
        acc = calculate_exact_match(response.content, ground_truth)
        
        return PipelineResult(
            pipeline_name=self.name,
            question_id=qid,
            question=question,
            prediction=response.content.strip(),
            ground_truth=ground_truth,
            retrieved_doc_ids=[],
            gold_doc_ids=gold_doc_ids or [],
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
            total_tokens=response.total_tokens,
            latency_seconds=round(latency, 3),
            accuracy_score=acc,
            completeness_score=acc  # Initial baseline estimate
        )
