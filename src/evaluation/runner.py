"""Benchmark Runner: Evaluates questions across Standard RAG, GraphRAG, and Agentic GraphRAG.

Saves structured outputs to JSONL and produces comparative accuracy, token, and latency metrics
broken down by question archetype (lookup, multi_hop, aggregation, superlative, temporal).
"""

import os
import sys
import time
import json
import argparse
import logging
from typing import Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.pipelines.standard_rag import StandardRAGPipeline
from src.pipelines.graph_rag import GraphRAGPipeline
from src.pipelines.agentic_graphrag import AgenticGraphRAGPipeline
from src.evaluation.metrics import PipelineResult, calculate_token_stats, calculate_archetype_breakdown

logger = logging.getLogger(__name__)


class BenchmarkRunner:
    def __init__(self, eval_file: str = "Datasets/questions/eval_public.jsonl"):
        self.eval_file = eval_file
        self.p1: Optional[StandardRAGPipeline] = None
        self.p2: Optional[GraphRAGPipeline] = None
        self.p3: Optional[AgenticGraphRAGPipeline] = None

    def _get_pipeline(self, name: str):
        if name == "standard_rag":
            if self.p1 is None:
                self.p1 = StandardRAGPipeline()
            return self.p1
        elif name == "graph_rag":
            if self.p2 is None:
                self.p2 = GraphRAGPipeline()
            return self.p2
        elif name == "agentic_graphrag":
            if self.p3 is None:
                self.p3 = AgenticGraphRAGPipeline()
            return self.p3
        else:
            raise ValueError(f"Unknown pipeline: {name}")

    def load_questions(self, limit: Optional[int] = None) -> List[Dict]:
        questions = []
        with open(self.eval_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    questions.append(json.loads(line))
                    if limit and len(questions) >= limit:
                        break
        return questions

    def run_benchmark(
        self,
        sample_size: int = 15,
        pipeline_names: Optional[List[str]] = None,
        output_file: Optional[str] = "data/processed/results_checkpoint.jsonl",
        delay_seconds: float = 2.0
    ) -> Dict[str, Dict]:
        selected_pipelines = pipeline_names or ["standard_rag", "graph_rag"]
        questions = self.load_questions(limit=sample_size)
        print(f"Loaded {len(questions)} evaluation questions for benchmark evaluation.")
        print(f"Active pipelines: {', '.join(selected_pipelines)}")
        print(f"Output destination: {output_file}")

        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

        results_by_pipeline: Dict[str, List[PipelineResult]] = {name: [] for name in selected_pipelines}

        for idx, q in enumerate(questions):
            qid = q.get("qid", f"q-{idx+1}")
            query = q.get("question", "")
            qtype = q.get("qtype", "unknown")
            gold_answers = q.get("answer", [])
            gold_docs = q.get("gold_doc_ids", [])

            print(f"\n[{idx+1}/{len(questions)}] ({qtype}) {qid}: {query[:75]}...")
            print(f"   Ground Truth: {gold_answers}")

            for p_name in selected_pipelines:
                pipe = self._get_pipeline(p_name)
                print(f"   Running {pipe.name}...")
                result = pipe.run(
                    qid=qid,
                    question=query,
                    ground_truth=gold_answers,
                    gold_doc_ids=gold_docs,
                    qtype=qtype
                )
                results_by_pipeline[p_name].append(result)
                print(f"   [{pipe.name}] Acc: {result.accuracy_score:.1f} | Tokens: {result.total_tokens} | Latency: {result.latency_seconds:.2f}s")
                print(f"   Pred: {result.prediction[:100]}...")

                # Append result to output file immediately
                if output_file:
                    with open(output_file, "a", encoding="utf-8") as f_out:
                        f_out.write(result.model_dump_json() + "\n")

                if delay_seconds > 0:
                    time.sleep(delay_seconds)

        # Print overall summary table
        print("\n========================================================")
        print("OVERALL BENCHMARK COMPARISON")
        print("========================================================")
        header = f"{'Pipeline':<20} | {'Count':<6} | {'Accuracy':<10} | {'Avg Tokens':<12} | {'Avg Latency (s)':<15}"
        print(header)
        print("-" * len(header))

        summary = {}
        for p_name, p_results in results_by_pipeline.items():
            stats = calculate_token_stats(p_results)
            summary[p_name] = stats
            pipe_display = p_results[0].pipeline_name if p_results else p_name
            print(f"{pipe_display:<20} | {stats['sample_count']:<6} | {stats['accuracy']*100:>8.1f}% | {stats['avg_tokens_per_query']:>12.1f} | {stats.get('avg_latency_seconds', 0.0):>15.2f}")

        # Print archetype breakdown
        print("\n========================================================")
        print("PER-ARCHETYPE ACCURACY BREAKDOWN")
        print("========================================================")
        all_archetypes = sorted(list(set(q.get("qtype", "unknown") for q in questions)))
        arch_header = f"{'Archetype':<15} | {'Count':<6} | " + " | ".join([f"{p_name:<16}" for p_name in selected_pipelines])
        print(arch_header)
        print("-" * len(arch_header))

        breakdowns = {p_name: calculate_archetype_breakdown(p_results) for p_name, p_results in results_by_pipeline.items()}

        for arch in all_archetypes:
            arch_count = sum(1 for q in questions if q.get("qtype") == arch)
            row_items = [f"{arch:<15}", f"{arch_count:<6}"]
            for p_name in selected_pipelines:
                arch_stat = breakdowns[p_name].get(arch, {})
                acc_val = arch_stat.get("accuracy", 0.0) * 100
                row_items.append(f"{acc_val:>14.1f}%")
            print(" | ".join(row_items))

        return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmark comparison across RAG pipelines")
    parser.add_argument("--limit", type=int, default=15, help="Number of questions to evaluate (default: 15)")
    parser.add_argument("--pipelines", nargs="+", default=["standard_rag", "graph_rag"], help="Pipelines to test: standard_rag, graph_rag, agentic_graphrag")
    parser.add_argument("--output", type=str, default="data/processed/results_checkpoint.jsonl", help="Output JSONL destination")
    parser.add_argument("--delay", type=float, default=2.5, help="Delay in seconds between LLM calls to prevent rate limits")
    args = parser.parse_args()

    runner = BenchmarkRunner()
    runner.run_benchmark(
        sample_size=args.limit,
        pipeline_names=args.pipelines,
        output_file=args.output,
        delay_seconds=args.delay
    )
