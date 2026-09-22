"""Benchmark evaluation metrics: Accuracy, Completeness, and Token Cost tracking."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class PipelineResult(BaseModel):
    pipeline_name: str
    question_id: str
    question: str
    prediction: str
    ground_truth: List[str]
    retrieved_doc_ids: List[str] = []
    gold_doc_ids: List[str] = []
    
    # Metrics
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_seconds: float = 0.0
    accuracy_score: float = 0.0
    completeness_score: float = 0.0


def calculate_exact_match(prediction: str, ground_truth: List[str]) -> float:
    """Exact string or substring match against any accepted ground-truth variant."""
    pred_clean = prediction.strip().lower()
    for gold in ground_truth:
        gold_clean = gold.strip().lower()
        if gold_clean in pred_clean or pred_clean in gold_clean:
            return 1.0
    return 0.0


def calculate_token_stats(results: List[PipelineResult]) -> Dict[str, Any]:
    """Aggregate token usage and performance across a pipeline run."""
    if not results:
        return {"count": 0, "avg_accuracy": 0.0, "avg_tokens": 0, "total_tokens": 0}
    
    total_tokens = sum(r.total_tokens for r in results)
    avg_accuracy = sum(r.accuracy_score for r in results) / len(results)
    avg_completeness = sum(r.completeness_score for r in results) / len(results)
    avg_tokens = total_tokens / len(results)
    
    return {
        "pipeline": results[0].pipeline_name if results else "unknown",
        "sample_count": len(results),
        "accuracy": round(avg_accuracy, 4),
        "completeness": round(avg_completeness, 4),
        "avg_tokens_per_query": round(avg_tokens, 1),
        "total_tokens": total_tokens
    }
