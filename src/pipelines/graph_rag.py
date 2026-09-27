"""Pipeline 2: Static Knowledge Graph-Augmented Generation (GraphRAG Baseline).

Implements Section 9 of Final Plan (v3):
1. Entity linking: extracts candidate mentions from question, resolves to canonical vertices.
2. Fixed-depth traversal: 1-2 hops along domain edges (PART_OF, HELD_AT, WON_MEDAL, COMPETED_IN, PRECEDES).
3. HeapAccum relevance capping: caps expansion by query relevance to prevent hub entity flooding.
4. Fallback: if entity linking is weak/empty, falls back to dense vector retrieval.
5. Single-pass LLM generation: identical underlying model with structured graph evidence and text chunks.
6. Structured PipelineResult logging: tracks citations, tokens, latency, and exact match.
"""

import os
import re
import time
import json
import heapq
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.config import settings
from src.graph.client import tg_manager
from src.llm.client import llm_client
from src.ingestion.embed import embed_texts
from src.evaluation.metrics import PipelineResult, calculate_exact_match


class GraphRAGPipeline:
    def __init__(
        self,
        chunks_jsonl: str = "data/processed/chunks.jsonl",
        embeddings_npz: str = "data/processed/chunk_embeddings.npz",
        max_triples: int = 20,
        top_k_chunks: int = 3
    ):
        self.name = "GraphRAG"
        self.max_triples = max_triples
        self.top_k_chunks = top_k_chunks
        
        # Fall back to full corpus if checkpoint paths not found
        if not os.path.exists(chunks_jsonl) and os.path.exists("data/processed/chunks.jsonl"):
            chunks_jsonl = "data/processed/chunks.jsonl"
        if not os.path.exists(embeddings_npz) and os.path.exists("data/processed/chunk_embeddings.npz"):
            embeddings_npz = "data/processed/chunk_embeddings.npz"

        self.chunks_data: Dict[str, Dict[str, Any]] = {}
        self.title_to_chunks: Dict[str, List[Dict[str, Any]]] = {}
        self._load_chunks(chunks_jsonl)

        # Fallback vector retrieval store
        self.chunk_ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self._load_vector_store(embeddings_npz)

        # Connect to TigerGraph and cache canonical entities
        self.conn = tg_manager.get_connection()
        self.competitions: Dict[str, Dict[str, Any]] = {}
        self.venues: Dict[str, Dict[str, Any]] = {}
        self.events: Dict[str, Dict[str, Any]] = {}
        self.athletes: Dict[str, Dict[str, Any]] = {}
        self._cache_graph_entities()

    def _load_chunks(self, chunks_jsonl: str):
        """Loads chunks and builds title-to-chunk index for fast lookup."""
        if os.path.exists(chunks_jsonl):
            with open(chunks_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        c = json.loads(line)
                        cid = c["chunk_id"]
                        self.chunks_data[cid] = c
                        title = c.get("title", "")
                        if title:
                            self.title_to_chunks.setdefault(title, []).append(c)

    def _load_vector_store(self, embeddings_npz: str):
        """Loads normalized embeddings for fallback vector search."""
        if os.path.exists(embeddings_npz):
            data = np.load(embeddings_npz)
            self.chunk_ids = list(data["chunk_ids"])
            self.embeddings = data["embeddings"]
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1e-9
            self.embeddings = self.embeddings / norms

    def _cache_graph_entities(self):
        """Caches canonical vertex sets from TigerGraph for low-latency entity linking."""
        if not self.conn:
            return
        try:
            comps = self.conn.getVertices("Competition", limit=100000)
            self.competitions = {c["v_id"]: c.get("attributes", {}) for c in comps}
            
            venues = self.conn.getVertices("Venue", limit=100000)
            self.venues = {v["v_id"]: v.get("attributes", {}) for v in venues}
            
            events = self.conn.getVertices("Event", limit=100000)
            self.events = {e["v_id"]: e.get("attributes", {}) for e in events}
            
            athletes = self.conn.getVertices("Athlete", limit=100000)
            self.athletes = {a["v_id"]: a.get("attributes", {}) for a in athletes}
        except Exception as e:
            print(f"Warning: Failed to cache graph entities from TigerGraph: {e}")

    def link_entities(self, question: str) -> Dict[str, List[str]]:
        """Resolves question mentions to canonical TigerGraph vertex IDs."""
        linked = {
            "Competition": [],
            "Venue": [],
            "Event": [],
            "Athlete": []
        }
        q_lower = question.lower()

        # 1. Temporal Resolution: 'immediately before <year>'
        before_match = re.search(r"immediately before (\d{4})", q_lower)
        if before_match and self.conn:
            anchor_year = before_match.group(1)
            season = "Summer" if "summer" in q_lower else "Winter"
            anchor_comp = f"{anchor_year} {season}"
            try:
                edges = self.conn.getEdges("Competition", anchor_comp)
                for e in edges:
                    if e.get("e_type") == "SUCCEEDS":
                        linked["Competition"].append(e["to_id"])
            except Exception:
                pass

        # 2. Competitions (e.g. 2018 Winter, 2008 Summer)
        if not linked["Competition"]:
            for c in self.competitions:
                if c.lower() in q_lower:
                    linked["Competition"].append(c)

        # 3. Venues (e.g. Olympic Weightlifting Gymnasium, London Velopark)
        for v in self.venues:
            if len(v) > 3 and v.lower() in q_lower:
                linked["Venue"].append(v)

        # 4. Athletes
        for a in self.athletes:
            if len(a) > 4 and a.lower() in q_lower:
                linked["Athlete"].append(a)

        # 5. Events
        for e in self.events:
            if len(e) > 5 and e.lower() in q_lower:
                linked["Event"].append(e)

        return linked

    def traverse(
        self,
        linked: Dict[str, List[str]],
        question: str
    ) -> Tuple[List[str], List[str]]:
        """Executes 1-2 hop static traversal with HeapAccum relevance capping."""
        if not self.conn:
            return [], []

        triples: List[str] = []
        selected_events: List[str] = []
        q_tokens = set(re.findall(r"\w+", question.lower()))

        def score_relevance(text: str) -> int:
            t_tokens = set(re.findall(r"\w+", text.lower()))
            return len(t_tokens.intersection(q_tokens))

        heap: List[Tuple[int, str, str]] = []

        # Hop 1: Competitions -> INCLUDES_EVENT -> Event
        for comp in linked.get("Competition", []):
            try:
                edges = self.conn.getEdges("Competition", comp)
                for e in edges:
                    if e.get("to_type") == "Event":
                        ev_name = e["to_id"]
                        score = score_relevance(ev_name)
                        ev_attrs = self.events.get(ev_name, {})
                        comp_cnt = ev_attrs.get("competitors", 0)
                        sport = ev_attrs.get("sport", "")
                        triple = f"({comp})-[:INCLUDES_EVENT]->({ev_name} [sport={sport}, competitors={comp_cnt}])"
                        heapq.heappush(heap, (-score, triple, ev_name))
            except Exception:
                pass

        # Hop 1: Venues -> HOSTED_EVENT -> Event
        for venue in linked.get("Venue", []):
            try:
                edges = self.conn.getEdges("Venue", venue)
                for e in edges:
                    if e.get("to_type") == "Event":
                        ev_name = e["to_id"]
                        score = score_relevance(ev_name) + 5
                        triple = f"({venue})-[:HOSTED_EVENT]->({ev_name})"
                        heapq.heappush(heap, (-score, triple, ev_name))
            except Exception:
                pass

        # Hop 1: Athletes -> WON_MEDAL, COMPETED_IN
        for ath in linked.get("Athlete", []):
            try:
                edges = self.conn.getEdges("Athlete", ath)
                for e in edges:
                    if e.get("e_type") == "WON_MEDAL":
                        m_type = e["to_id"]
                        attrs = e.get("attributes", {})
                        ev_name = attrs.get("event_id", "")
                        d_held = attrs.get("date_held", "")
                        triple = f"({ath})-[:WON_MEDAL {m_type} (date: {d_held})]->({ev_name})"
                        heapq.heappush(heap, (-10, triple, ev_name))
            except Exception:
                pass

        # Extract top-ranked entities via HeapAccum pattern
        visited_evs = set()
        while heap and len(triples) < self.max_triples:
            neg_score, triple, ev_name = heapq.heappop(heap)
            triples.append(triple)
            if ev_name and ev_name not in visited_evs:
                visited_evs.add(ev_name)
                selected_events.append(ev_name)
                
                # Hop 2: Event -> HAS_COMPETITOR -> Athlete -> WON_MEDAL
                try:
                    ev_edges = self.conn.getEdges("Event", ev_name)
                    for ee in ev_edges:
                        if ee.get("e_type") == "HAS_COMPETITOR":
                            ath_name = ee["to_id"]
                            ath_edges = self.conn.getEdges("Athlete", ath_name)
                            for ae in ath_edges:
                                if ae.get("e_type") == "WON_MEDAL":
                                    m_attrs = ae.get("attributes", {})
                                    m_type = ae["to_id"]
                                    d_held = m_attrs.get("date_held", "")
                                    ath_triple = f"({ath_name})-[:WON_MEDAL {m_type} (date: {d_held})]->({ev_name})"
                                    triples.append(ath_triple)
                                    if len(triples) >= self.max_triples:
                                        break
                            if len(triples) >= self.max_triples:
                                break
                except Exception:
                    pass

        return triples, selected_events

    def get_associated_chunks(self, event_names: List[str], question: str) -> List[Dict[str, Any]]:
        """Retrieves and ranks supporting document chunks for traversed events."""
        candidate_chunks = []
        for ev in event_names:
            if ev in self.title_to_chunks:
                candidate_chunks.extend(self.title_to_chunks[ev])

        if not candidate_chunks:
            return []

        # Deduplicate by chunk_id
        unique_chunks = {}
        for c in candidate_chunks:
            unique_chunks[c["chunk_id"]] = c

        # Rank by question token overlap
        q_tokens = set(re.findall(r"\w+", question.lower()))
        ranked = sorted(
            unique_chunks.values(),
            key=lambda c: (-len(set(re.findall(r"\w+", c["text"].lower())).intersection(q_tokens)), c["chunk_id"])
        )
        return ranked[:self.top_k_chunks]

    def fallback_vector_retrieve(self, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Dense vector retrieval fallback when graph entity linking yields zero matches."""
        if self.embeddings is None or len(self.chunk_ids) == 0:
            return []

        q_emb = embed_texts([question])[0]
        q_norm = np.linalg.norm(q_emb)
        if q_norm > 0:
            q_emb = q_emb / q_norm

        sim_scores = np.dot(self.embeddings, q_emb)
        ranked_indices = sorted(
            range(len(self.chunk_ids)),
            key=lambda idx: (-sim_scores[idx], self.chunk_ids[idx])
        )[:top_k]

        retrieved = []
        for idx in ranked_indices:
            cid = self.chunk_ids[idx]
            info = self.chunks_data.get(cid, {})
            retrieved.append({
                "chunk_id": cid,
                "doc_id": info.get("doc_id", cid.split("::")[0] if "::" in cid else cid),
                "title": info.get("title", ""),
                "text": info.get("text", "")
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

        # 1. Entity linking
        linked = self.link_entities(question)
        has_entities = any(len(v) > 0 for v in linked.values())

        # 2. Subgraph traversal with HeapAccum capping
        triples, events = [], []
        if has_entities:
            triples, events = self.traverse(linked, question)

        # 3. Supporting chunk retrieval
        supporting_chunks = []
        if events:
            supporting_chunks = self.get_associated_chunks(events, question)

        # 4. Fallback if graph evidence is empty
        if not triples and not supporting_chunks:
            supporting_chunks = self.fallback_vector_retrieve(question, top_k=self.top_k_chunks)

        retrieved_doc_ids = list(dict.fromkeys(c.get("doc_id", "") for c in supporting_chunks if c.get("doc_id")))

        # 5. Build prompt
        graph_section = "\n".join(triples) if triples else "No direct entity triples identified."
        chunk_parts = []
        for c in supporting_chunks:
            title_header = f" [{c['title']}]" if c.get('title') else ""
            chunk_parts.append(f"[{c['chunk_id']}]{title_header}\n{c['text']}")
        chunks_section = "\n\n".join(chunk_parts) if chunk_parts else "No direct context passages."

        prompt = (
            "You are answering an Olympic Games historical question using structured knowledge graph evidence and supporting passages.\n\n"
            f"Structured Graph Evidence:\n{graph_section}\n\n"
            f"Supporting Context Passages:\n{chunks_section}\n\n"
            f"Question: {question}\n\n"
            "Instructions:\n"
            "1. Answer concisely and accurately based solely on the facts in the evidence above.\n"
            "2. If citing text passages, include the chunk IDs (e.g. [doc_id::c0]).\n"
            "3. If the answer cannot be determined from the evidence, state 'Unknown based on provided context'.\n\n"
            "Answer:"
        )

        # 6. Single-pass LLM call
        response = llm_client.generate(prompt=prompt)
        latency = time.time() - start_time

        # 7. Extract citations
        cited_chunks = re.findall(r"\[([a-zA-Z0-9_\-\.\:\s]+::c\d+)\]", response.content)
        cited_chunks = list(dict.fromkeys(cited_chunks))

        # 8. Compute Exact Match
        acc = calculate_exact_match(response.content, ground_truth)

        # 9. Build execution trace
        trace = {
            "strategy": "entity_linking_and_static_traversal",
            "linked_entities": [f"{vtype}:{vid}" for vtype, vlist in linked.items() for vid in vlist],
            "triples_count": len(triples),
            "triples_sample": triples[:5],
            "supporting_chunks_count": len(supporting_chunks),
            "supporting_chunk_ids": [c.get("chunk_id", "") for c in supporting_chunks],
            "graph_evidence_length_chars": len(graph_section)
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
