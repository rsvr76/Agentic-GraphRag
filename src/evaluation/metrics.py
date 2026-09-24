"""Benchmark evaluation metrics: Accuracy, Completeness, and Token Cost tracking."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class PipelineResult(BaseModel):
    pipeline_name: str
    question_id: str
    question: str
    qtype: str = ""
    prediction: str
    ground_truth: List[str]
    retrieved_doc_ids: List[str] = []
    gold_doc_ids: List[str] = []
    cited_chunk_ids: List[str] = []
    
    # Metrics
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_seconds: float = 0.0
    accuracy_score: float = 0.0
    completeness_score: float = 0.0
    execution_trace: Optional[Dict[str, Any]] = None


import unicodedata
import re


def normalize_text(s: str) -> str:
    """Normalizes text for evaluation: NFKC unicode, lowercase, collapses spaces and strips markdown."""
    s = unicodedata.normalize("NFKC", str(s))
    # Normalize typographic curly apostrophes and quotation marks to standard ASCII
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("`", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    # Normalize dashes (en-dash, em-dash, minus) to standard hyphen
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    s = s.lower()
    # Remove markdown bold/italic markers
    s = re.sub(r"[*_~`]+", " ", s)
    # Replace citation brackets and punctuation (except hyphens)
    s = re.sub(r"[\[\]【】\(\)\"\'\:\,\.\;]", " ", s)
    # Collapse multiple whitespaces
    s = re.sub(r"\s+", " ", s).strip()
    return s


NUMBER_WORDS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    "10": "ten", "11": "eleven", "12": "twelve", "13": "thirteen", "14": "fourteen",
    "15": "fifteen", "16": "sixteen", "17": "seventeen", "18": "eighteen", "19": "nineteen",
    "20": "twenty", "26": "twenty-six"
}


def calculate_exact_match(prediction: str, ground_truth: List[str]) -> float:
    """Exact string or substring match against any accepted ground-truth variant.
    
    Enforces word boundary matching for numbers to avoid false positives (e.g. '8' matching '2008').
    """
    pred_clean = normalize_text(prediction)
    for gold in ground_truth:
        gold_clean = normalize_text(gold)
        if not gold_clean:
            continue

        # Numeric ground truth: enforce standalone number or written-out number match
        if gold_clean.isdigit():
            if re.search(r"\b" + re.escape(gold_clean) + r"\b", pred_clean):
                return 1.0
            word_form = NUMBER_WORDS.get(gold_clean)
            if word_form and re.search(r"\b" + re.escape(word_form) + r"\b", pred_clean):
                return 1.0
            continue

        # Non-numeric string match
        if gold_clean in pred_clean:
            return 1.0

        # Space-stripped containment for concatenated names (e.g. "Dani KingLaura TrottJoanna Rowsell")
        gold_no_space = gold_clean.replace(" ", "")
        pred_no_space = pred_clean.replace(" ", "")
        if gold_no_space and gold_no_space in pred_no_space:
            return 1.0

        # Word set containment for multi-token entities (e.g. "Chen Ding")
        gold_words = set(gold_clean.split())
        pred_words = set(pred_clean.split())
        if gold_words and gold_words.issubset(pred_words):
            return 1.0

        # CamelCase team-name split for concatenated athlete strings
        # e.g. "Dani KingLaura TrottJoanna Rowsell" -> ["dani", "king", "laura", "trott", "joanna", "rowsell"]
        # The gold string has no separator at last-name/first-name boundaries between team members.
        raw_gold = str(gold)
        camel_tokens = re.findall(r"[A-Z][a-z]+|[a-z]+", raw_gold)
        if len(camel_tokens) >= 4:
            camel_lower = {t.lower() for t in camel_tokens}
            if camel_lower and camel_lower.issubset(pred_words):
                return 1.0

    return 0.0


def calculate_token_stats(results: List[PipelineResult]) -> Dict[str, Any]:
    """Aggregate token usage and performance across a pipeline run."""
    if not results:
        return {"count": 0, "avg_accuracy": 0.0, "avg_tokens": 0, "total_tokens": 0}
    
    total_tokens = sum(r.total_tokens for r in results)
    avg_tokens = total_tokens / len(results)
    avg_accuracy = sum(r.accuracy_score for r in results) / len(results)
    avg_completeness = sum(r.completeness_score for r in results) / len(results)
    total_latency = sum(r.latency_seconds for r in results)
    avg_latency = total_latency / len(results)
    
    return {
        "pipeline": results[0].pipeline_name if results else "unknown",
        "sample_count": len(results),
        "accuracy": round(avg_accuracy, 4),
        "completeness": round(avg_completeness, 4),
        "avg_tokens_per_query": round(avg_tokens, 1),
        "total_tokens": total_tokens,
        "avg_latency_seconds": round(avg_latency, 2)
    }


def calculate_archetype_breakdown(results: List[PipelineResult]) -> Dict[str, Dict[str, Any]]:
    """Computes performance metrics grouped by question archetype."""
    breakdown: Dict[str, List[PipelineResult]] = {}
    for r in results:
        qt = r.qtype or "unknown"
        breakdown.setdefault(qt, []).append(r)
        
    stats = {}
    for qt, q_results in breakdown.items():
        stats[qt] = {
            "count": len(q_results),
            "accuracy": round(sum(r.accuracy_score for r in q_results) / len(q_results), 4),
            "avg_tokens": round(sum(r.total_tokens for r in q_results) / len(q_results), 1),
            "avg_latency": round(sum(r.latency_seconds for r in q_results) / len(q_results), 2)
        }
    return stats
