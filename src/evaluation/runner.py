"""Benchmark Runner: Evaluates questions across Standard RAG, GraphRAG, and Agentic GraphRAG."""

import json
import logging
from typing import Dict, List, Optional
from tqdm import tqdm

from src.pipelines.standard_rag import StandardRAGPipeline
from src.pipelines.graph_rag import GraphRAGPipeline
from src.pipelines.agentic_graphrag import AgenticGraphRAGPipeline
from src.evaluation.metrics import PipelineResult, calculate_token_stats

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, eval_file: str = "Datasets/questions/eval_public.jsonl"):
        self.eval_file = eval_file
        self.p1 = StandardRAGPipeline()
        self.p2 = GraphRAGPipeline()
        self.p3 = AgenticGraphRAGPipeline()

    def load_questions(self, limit: Optional[int] = None) -> List[Dict]:
        questions = []
        with open(self.eval_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
                    if limit and len(questions) >= limit:
                        break
        return questions

    def run_benchmark(self, sample_size: int = 5) -> Dict[str, Dict]:
        questions = self.load_questions(limit=sample_size)
        print(f"Loaded {len(questions)} evaluation questions for 3-way benchmark.")
        
        results_p1: List[PipelineResult] = []
        results_p2: List[PipelineResult] = []
        results_p3: List[PipelineResult] = []
        
        for q in tqdm(questions, desc="Benchmarking"):
            qid = q.get("qid", "")
            query = q.get("question", "")
            gold_answers = q.get("answer", [])
            gold_docs = q.get("gold_doc_ids", [])
            
            # 1. Standard RAG
            results_p1.append(self.p1.run(qid, query, gold_answers, gold_docs))
            
            # 2. GraphRAG
            results_p2.append(self.p2.run(qid, query, gold_answers, gold_docs))
            
            # 3. Agentic GraphRAG
            results_p3.append(self.p3.run(qid, query, gold_answers, gold_docs))
            
        summary = {
            "standard_rag": calculate_token_stats(results_p1),
            "graph_rag": calculate_token_stats(results_p2),
            "agentic_graphrag": calculate_token_stats(results_p3)
        }
        
        return summary


if __name__ == "__main__":
    runner = BenchmarkRunner()
    metrics = runner.run_benchmark(sample_size=3)
    print("\nBenchmark Summary Results:")
    print(json.dumps(metrics, indent=2))
