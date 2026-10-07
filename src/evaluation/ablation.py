"""Agentic Component Ablation Framework.

Defines ablation experiments to isolate causal attribution between:
1. Graph-native GSQL accumulators (SumAccum, HeapAccum) vs. LangGraph orchestration.
2. Deterministic graph traversal vs. targeted vector fallback.
3. Single-pass fallback vs. multi-turn Self-RAG reflection.

All experiments are registered with strict status tracking:
If an experiment has not been executed, status is 'NOT RUN / FRAMEWORK READY'
and results are marked 'Ablation not yet executed' with zero invented numbers.
"""

import os
import re
import json
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from src.config import settings
from src.graph.client import tg_manager
from src.llm.client import llm_client
from src.evaluation.metrics import PipelineResult, calculate_exact_match


class AblationExperimentSpec(BaseModel):
    experiment_id: str
    archetype: str
    component_ablated: str
    description: str
    baseline_pipeline: str
    baseline_accuracy: float
    ablated_pipeline_name: str
    ablated_accuracy: Optional[float] = None
    full_pipeline_name: str
    full_accuracy: float
    status: str = "NOT RUN / FRAMEWORK READY"
    scientific_hypothesis: str
    interpretation: str


ABLATION_REGISTRY: Dict[str, AblationExperimentSpec] = {
    "aggregation_sumaccum": AblationExperimentSpec(
        experiment_id="aggregation_sumaccum",
        archetype="aggregation",
        component_ablated="LangGraph Orchestrator (Isolated GSQL SumAccum)",
        description="Executes GSQL SumAccum directly in a static single-pass pipeline without LangGraph StateGraph, classifier node, or reflection loops.",
        baseline_pipeline="Static GraphRAG",
        baseline_accuracy=4.8,
        ablated_pipeline_name="Static Graph + GSQL SumAccum (No Agent)",
        ablated_accuracy=None,
        full_pipeline_name="Agentic GraphRAG + SumAccum",
        full_accuracy=100.0,
        status="NOT RUN / FRAMEWORK READY",
        scientific_hypothesis="If Static Graph + GSQL SumAccum achieves ~100% accuracy, the accuracy gain is driven by in-database GSQL computation rather than agentic orchestration.",
        interpretation="Determines whether LangGraph orchestration is causal or if graph-native computation alone resolves aggregation."
    ),
    "superlative_heapaccum": AblationExperimentSpec(
        experiment_id="superlative_heapaccum",
        archetype="superlative",
        component_ablated="LangGraph Orchestrator (Isolated GSQL HeapAccum)",
        description="Executes GSQL HeapAccum(1) directly in a static single-pass pipeline without LangGraph StateGraph or reflection loops.",
        baseline_pipeline="Static GraphRAG",
        baseline_accuracy=50.0,
        ablated_pipeline_name="Static Graph + GSQL HeapAccum (No Agent)",
        ablated_accuracy=None,
        full_pipeline_name="Agentic GraphRAG + HeapAccum",
        full_accuracy=100.0,
        status="NOT RUN / FRAMEWORK READY",
        scientific_hypothesis="If Static Graph + HeapAccum achieves ~100% accuracy, extreme ranking is solved entirely by the priority queue accumulator.",
        interpretation="Determines whether ranking accuracy stems from graph accumulators or agentic loop coordination."
    ),
    "multihop_datespan": AblationExperimentSpec(
        experiment_id="multihop_datespan",
        archetype="multi_hop",
        component_ablated="Vector Fallback & Reflection (Isolated Date-Span Overlap)",
        description="Executes graph traversal with deterministic date-span overlap ranking to resolve venue collisions, but disables vector fallback and reflection.",
        baseline_pipeline="Static GraphRAG",
        baseline_accuracy=53.6,
        ablated_pipeline_name="Graph + Date-Span Resolution (No Fallback)",
        ablated_accuracy=None,
        full_pipeline_name="Agentic GraphRAG (Full Adaptive)",
        full_accuracy=96.4,
        status="NOT RUN / FRAMEWORK READY",
        scientific_hypothesis="Measures what fraction of multi-hop improvement is explained by deterministic date matching vs adaptive fallback retrieval.",
        interpretation="Isolates the accuracy contribution of venue-date disambiguation from vector fallback recovery."
    ),
    "multihop_vector_fallback": AblationExperimentSpec(
        experiment_id="multihop_vector_fallback",
        archetype="multi_hop",
        component_ablated="Self-RAG Multi-Turn Reflection (Single-Pass Fallback)",
        description="Executes graph traversal with targeted vector fallback on gap, but allows only 1 single pass without iterative Self-RAG reflection loops.",
        baseline_pipeline="Static GraphRAG",
        baseline_accuracy=53.6,
        ablated_pipeline_name="Graph + Single-Pass Vector Fallback",
        ablated_accuracy=None,
        full_pipeline_name="Agentic GraphRAG (Full Adaptive)",
        full_accuracy=96.4,
        status="NOT RUN / FRAMEWORK READY",
        scientific_hypothesis="Measures whether single-pass fallback suffices or if multi-turn self-reflection is required to resolve multi-hop entities.",
        interpretation="Isolates the value of iterative Self-RAG state looping vs simple static fallback."
    )
}


def get_ablation_status_rows() -> List[Dict[str, Any]]:
    """Returns formatted rows for the Streamlit dashboard ablation table."""
    rows = []
    for exp_id, spec in ABLATION_REGISTRY.items():
        ablated_display = (
            f"{spec.ablated_accuracy:.1f}%"
            if spec.ablated_accuracy is not None
            else "Ablation not yet executed"
        )
        delta_display = (
            f"+{spec.ablated_accuracy - spec.baseline_accuracy:.1f}%"
            if spec.ablated_accuracy is not None
            else "Pending execution"
        )
        rows.append({
            "Archetype": spec.archetype.capitalize(),
            "Component Tested": spec.component_ablated,
            "Ablation Status": spec.status,
            "Baseline Acc (%)": f"{spec.baseline_accuracy:.1f}% ({spec.baseline_pipeline})",
            "Ablated Acc (%)": ablated_display,
            "Full Acc (%)": f"{spec.full_accuracy:.1f}% ({spec.full_pipeline_name})",
            "Δ Accuracy": delta_display,
            "Scientific Interpretation": spec.interpretation
        })
    return rows


class StaticGraphSumAccumPipeline:
    """Ablation A: Direct GSQL SumAccum without LangGraph StateGraph orchestration."""
    def __init__(self):
        self.name = "Static Graph + GSQL SumAccum (No Agent)"
        self.conn = tg_manager.get_connection()

    def run(self, qid: str, question: str, ground_truth: List[str], qtype: str = "aggregation") -> PipelineResult:
        start_time = time.time()
        q_lower = question.lower()
        comp_match = re.search(r"(\d{4})\s+(summer|winter)", q_lower)
        comp_name = f"{comp_match.group(1)} {comp_match.group(2).capitalize()}" if comp_match else ""
        thresh_match = re.search(r"more than\s+(\d+)", q_lower)
        threshold = int(thresh_match.group(1)) if thresh_match else 0
        
        sport = ""
        sport_clause = f'AND lower(e.sport) == "{sport.lower()}"' if sport else ''

        query = f"""
        INTERPRET QUERY () FOR GRAPH Olympics {{
            SumAccum<INT> @@event_count = 0;
            Comp = {{Competition.*}};
            TargetComp = SELECT c FROM Comp:c WHERE c.name == "{comp_name}";
            Events = SELECT e FROM TargetComp -(INCLUDES_EVENT:p)- Event:e
                     WHERE e.competitors > {threshold} {sport_clause}
                     ACCUM @@event_count += 1;
            PRINT @@event_count AS result_count;
        }}
        """
        try:
            res = self.conn.runInterpretedQuery(query)
            count = res[0].get("result_count", 0) if res else 0
        except Exception:
            count = 0

        prompt = (
            f"Question: {question}\n"
            f"Computed Database Count: {count}\n"
            "State the exact integer count concisely."
        )
        resp = llm_client.generate(prompt=prompt)
        ans = resp.content.strip()
        latency = time.time() - start_time
        acc = calculate_exact_match(ans, ground_truth)

        return PipelineResult(
            pipeline_name=self.name,
            question_id=qid,
            question=question,
            qtype=qtype,
            prediction=ans,
            ground_truth=ground_truth,
            prompt_tokens=resp.prompt_tokens or 0,
            completion_tokens=resp.completion_tokens or 0,
            total_tokens=resp.total_tokens or 0,
            latency_seconds=round(latency, 3),
            accuracy_score=acc,
            completeness_score=acc,
            execution_trace={
                "strategy": "static_gsql_sumaccum_ablation",
                "actual_llm_calls": 1,
                "actual_graph_calls": 1,
                "actual_vector_calls": 0,
                "reflection_iterations": 0,
                "fallback_triggered": False,
                "gsql_operation": "SumAccum",
                "stop_reason": "single_pass_gsql_complete"
            }
        )
