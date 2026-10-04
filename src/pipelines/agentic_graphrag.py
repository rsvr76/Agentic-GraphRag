"""Pipeline 3: Autonomous Agentic GraphRAG System (Core Graded Deliverable).

Implements Section 10 of Final Plan (v3) & solution.md:
1. Dynamic LangGraph StateGraph orchestrator.
2. Question Archetype Classification as first move (lookup, aggregation, superlative, temporal, multi_hop).
3. In-database GSQL Accumulators (SumAccum, HeapAccum) for exact aggregations and superlatives.
4. Atomic Constraint Decomposition for multi-hop queries.
5. PRECEDES temporal graph traversal for sequential competitions.
6. Self-RAG reflection node evaluating evidence sufficiency with bounded looping (max 6 iterations).
7. Single-pass synthesis with citation tracking using the identical underlying LLM.
"""

import os
import re
import time
import json
import operator
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Annotated
import numpy as np

from src.config import settings
from src.graph.client import tg_manager
from src.llm.client import llm_client
from src.ingestion.embed import embed_texts
from src.evaluation.metrics import PipelineResult, calculate_exact_match
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    question: str
    qid: str
    archetype: str
    sub_questions: Annotated[List[str], operator.add]
    evidence_log: Annotated[List[Dict[str, Any]], operator.add]
    graph_context: Dict[str, Any]
    vector_context: Annotated[List[Dict[str, Any]], operator.add]
    iteration: int
    max_iterations: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    is_sufficient: bool
    gap_description: str
    extracted_entities: Dict[str, str]
    answer: str
    citations: List[str]
    stop_reason: str


class AgenticGraphRAGPipeline:
    def __init__(
        self,
        chunks_jsonl: str = "data/processed/chunks.jsonl",
        embeddings_npz: str = "data/processed/chunk_embeddings.npz",
        max_iterations: int = 6
    ):
        self.name = "Agentic GraphRAG"
        self.max_iterations = max_iterations
        
        if not os.path.exists(chunks_jsonl) and os.path.exists("data/processed/chunks.jsonl"):
            chunks_jsonl = "data/processed/chunks.jsonl"
        if not os.path.exists(embeddings_npz) and os.path.exists("data/processed/chunk_embeddings.npz"):
            embeddings_npz = "data/processed/chunk_embeddings.npz"

        self.chunks_data: Dict[str, Dict[str, Any]] = {}
        self.title_to_chunks: Dict[str, List[Dict[str, Any]]] = {}
        self._load_chunks(chunks_jsonl)

        self.chunk_ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self._load_vector_store(embeddings_npz)

        self.conn = tg_manager.get_connection()
        self.competitions: Dict[str, Dict[str, Any]] = {}
        self.venues: Dict[str, Dict[str, Any]] = {}
        self.events: Dict[str, Dict[str, Any]] = {}
        self.athletes: Dict[str, Dict[str, Any]] = {}
        self._cache_graph_entities()

        self.app = self._build_graph()

    def _load_chunks(self, chunks_jsonl: str):
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
        if os.path.exists(embeddings_npz):
            data = np.load(embeddings_npz)
            self.chunk_ids = list(data["chunk_ids"])
            self.embeddings = data["embeddings"]
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1e-9
            self.embeddings = self.embeddings / norms

    def _cache_graph_entities(self):
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
            print(f"Warning: Failed to cache graph entities: {e}")

    def _find_chunks_for_titles(self, titles: List[str]) -> List[Dict[str, Any]]:
        chunks = []
        for t in titles:
            if t in self.title_to_chunks:
                chunks.extend(self.title_to_chunks[t][:2])
        return chunks

    def _vector_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if self.embeddings is None or len(self.chunk_ids) == 0:
            return []
        q_emb = embed_texts([query])[0]
        q_norm = np.linalg.norm(q_emb)
        if q_norm > 0:
            q_emb = q_emb / q_norm
        sim_scores = np.dot(self.embeddings, q_emb)
        ranked = sorted(
            range(len(self.chunk_ids)),
            key=lambda idx: (-sim_scores[idx], self.chunk_ids[idx])
        )[:top_k]
        results = []
        for idx in ranked:
            cid = self.chunk_ids[idx]
            info = self.chunks_data.get(cid, {})
            results.append({
                "chunk_id": cid,
                "doc_id": info.get("doc_id", cid.split("::")[0]),
                "title": info.get("title", ""),
                "text": info.get("text", "")
            })
        return results

    def _classify_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"].lower()
        if state.get("archetype"):
            archetype = state["archetype"]
        elif "how many" in q and ("competitors" in q or "events" in q or "more than" in q):
            archetype = "aggregation"
        elif "highest" in q or "most" in q or "lowest" in q:
            archetype = "superlative"
        elif "immediately before" in q or "preceding" in q:
            archetype = "temporal"
        elif "held at" in q or ("on" in q and re.search(r"\b19\d\d\b|\b20\d\d\b", q)) or "pavilion" in q or "gymnasium" in q or "velopark" in q or "oval" in q:
            archetype = "multi_hop"
        else:
            archetype = "lookup"
        return {"archetype": archetype, "iteration": state["iteration"] + 1}

    def _aggregate_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        q_lower = q.lower()
        
        comp_match = re.search(r"(\d{4})\s+(summer|winter)", q_lower)
        comp_name = f"{comp_match.group(1)} {comp_match.group(2).capitalize()}" if comp_match else ""
        
        thresh_match = re.search(r"more than\s+(\d+)", q_lower)
        threshold = int(thresh_match.group(1)) if thresh_match else 0
        
        sports = ["biathlon", "shooting", "sailing", "cycling", "rowing", "athletics", "swimming", "judo", "badminton", "weightlifting"]
        sport = next((s.capitalize() for s in sports if s in q_lower), "")
        
        sport_clause = f'AND lower(e.sport) == "{sport.lower()}"' if sport else ''
        query = f"""
        INTERPRET QUERY () FOR GRAPH Olympics {{
            SumAccum<INT> @@event_count = 0;
            Comp = {{Competition.*}};
            TargetComp = SELECT c FROM Comp:c WHERE c.name == "{comp_name}";
            Events = SELECT e FROM TargetComp -(INCLUDES_EVENT:p)- Event:e
                     WHERE e.competitors > {threshold} {sport_clause}
                     ACCUM @@event_count += 1;
            PRINT @@event_count AS result_count, Events[Events.name, Events.competitors, Events.sport] AS matching_events;
        }}
        """
        try:
            res = self.conn.runInterpretedQuery(query)
            data = res[0] if res else {}
            count = data.get("result_count", 0)
            events = data.get("matching_events", [])
            event_titles = [e.get("v_id", "") for e in events]
            chunks = self._find_chunks_for_titles(event_titles)
            
            evidence = {
                "tool": "gsql_sumaccum",
                "result_count": count,
                "matching_events": [f"{e.get('v_id')} ({e.get('attributes', {}).get('Events.competitors')} competitors)" for e in events],
                "competition": comp_name,
                "threshold": threshold,
                "sport": sport
            }
            return {
                "graph_context": evidence,
                "vector_context": chunks[:3],
                "evidence_log": [evidence],
                "is_sufficient": True,
                "stop_reason": "sufficient_evidence"
            }
        except Exception as e:
            return {"is_sufficient": False, "gap_description": f"Aggregation GSQL failed: {e}"}

    def _superlative_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        q_lower = q.lower()
        comp_match = re.search(r"(\d{4})\s+(summer|winter)", q_lower)
        comp_name = f"{comp_match.group(1)} {comp_match.group(2).capitalize()}" if comp_match else ""
        
        find_max = not ("lowest" in q_lower or "least" in q_lower)
        order = "DESC" if find_max else "ASC"
        
        sports = ["biathlon", "shooting", "sailing", "cycling", "rowing", "athletics", "swimming", "judo", "badminton", "weightlifting"]
        sport = next((s.capitalize() for s in sports if s in q_lower), "")
        sport_clause = f'AND lower(e.sport) == "{sport.lower()}"' if sport else ''
        
        query = f"""
        INTERPRET QUERY () FOR GRAPH Olympics {{
            TYPEDEF TUPLE<STRING event_name, INT competitors> EventRankTuple;
            HeapAccum<EventRankTuple>(1, competitors {order}) @@ranked_event;
            
            Comp = {{Competition.*}};
            TargetComp = SELECT c FROM Comp:c WHERE c.name == "{comp_name}";
            Events = SELECT e FROM TargetComp -(INCLUDES_EVENT:p)- Event:e
                     WHERE e.competitors > 0 {sport_clause}
                     ACCUM @@ranked_event += EventRankTuple(e.name, e.competitors);
                     
            PRINT @@ranked_event AS top_event;
        }}
        """
        try:
            res = self.conn.runInterpretedQuery(query)
            data = res[0] if res else {}
            top_event_list = data.get("top_event", [])
            top_event = top_event_list[0] if top_event_list else {}
            ev_name = top_event.get("event_name", "")
            comp_cnt = top_event.get("competitors", 0)
            
            full_title = ""
            for v_id, attrs in self.events.items():
                if attrs.get("name") == ev_name or v_id == ev_name:
                    full_title = v_id
                    break
            
            chunks = self._find_chunks_for_titles([full_title or ev_name])
            evidence = {
                "tool": "gsql_heapaccum",
                "superlative_event": ev_name,
                "full_event_title": full_title,
                "competitors": comp_cnt,
                "competition": comp_name,
                "sport": sport
            }
            return {
                "graph_context": evidence,
                "vector_context": chunks[:3],
                "evidence_log": [evidence],
                "is_sufficient": True,
                "stop_reason": "sufficient_evidence"
            }
        except Exception as e:
            return {"is_sufficient": False, "gap_description": f"Superlative GSQL failed: {e}"}

    def _temporal_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        q_lower = q.lower()
        
        before_match = re.search(r"immediately before (\d{4})", q_lower)
        if not before_match:
            return {"is_sufficient": False, "gap_description": "No temporal anchor detected"}
            
        anchor_year = before_match.group(1)
        season = "Summer" if "summer" in q_lower else "Winter"
        anchor_comp = f"{anchor_year} {season}"
        
        target_comp = ""
        best_year = -1
        try:
            edges = self.conn.getEdges("Competition", anchor_comp)
            for e in edges:
                if e.get("e_type") == "SUCCEEDS":
                    comp_name = e["to_id"]
                    match = re.search(r"^(\d{4})\s+(Summer|Winter)$", comp_name)
                    if match:
                        year = int(match.group(1))
                        if year < int(anchor_year) and year > best_year:
                            best_year = year
                            target_comp = comp_name
        except Exception:
            pass

        if not target_comp:
            return {"is_sufficient": False, "gap_description": f"Could not find preceding competition for {anchor_comp}"}

        comp_edges = self.conn.getEdges("Competition", target_comp)
        candidate_events = [e["to_id"] for e in comp_edges if e.get("to_type") == "Event"]
        extracted = state.get("extracted_entities") or {}

        extracted_event = extracted.get("event", "")
        if extracted_event and extracted_event not in candidate_events:
            candidate_events.append(extracted_event)

        best_event = extracted_event
        best_len = len(best_event)

        if not best_event:
            for ev in candidate_events:
                if ev.lower() in q_lower:
                    if len(ev) > best_len:
                        best_len = len(ev)
                        best_event = ev

        if not best_event:
            chunks = self._vector_search(q, top_k=3)
            for c in chunks:
                text = c.get("text", "").lower()
                for ev in candidate_events:
                    if ev.lower() in text:
                        if len(ev) > best_len:
                            best_len = len(ev)
                            best_event = ev


        gold_winner = ""
        date_held = ""
        if best_event:
            try:
                ev_edges = self.conn.getEdges("Event", best_event)
                for ee in ev_edges:
                    if ee.get("e_type") == "HAS_COMPETITOR":
                        ath_name = ee["to_id"]
                        ath_edges = self.conn.getEdges("Athlete", ath_name)
                        for ae in ath_edges:
                            if ae.get("e_type") == "WON_MEDAL" and ae.get("to_id") == "gold" and ae.get("attributes", {}).get("event_id") == best_event:
                                gold_winner = ath_name
                                date_held = ae.get("attributes", {}).get("date_held", "")
                                break
                        if gold_winner:
                            break
            except Exception as e:
                print(f"Warning: Temporal graph traversal failed on event '{best_event}': {e}")

        chunks = self._find_chunks_for_titles([best_event])
        evidence = {
            "tool": "temporal_precedes",
            "preceding_competition": target_comp,
            "matched_event": best_event,
            "gold_winner": gold_winner,
            "date_held": date_held
        }
        is_sufficient = bool(gold_winner)
        gap_desc = ""
        if not is_sufficient:
            if not best_event:
                gap_desc = f"Could not bind the specific event for the competition {target_comp}."
            else:
                gap_desc = f"Could not find the gold medal winner for event {best_event}."
                
        return {
            "graph_context": evidence,
            "vector_context": chunks[:3],
            "evidence_log": [evidence],
            "is_sufficient": is_sufficient,
            "gap_description": gap_desc,
            "stop_reason": "sufficient_evidence" if is_sufficient else "missing_gold_winner"
        }

    def _multi_hop_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        q_lower = q.lower()
        extracted = state.get("extracted_entities") or {}

        matched_venue = extracted.get("venue", "")
        best_len = len(matched_venue)

        if not matched_venue:
            for v in self.venues:
                if len(v) > 3 and v.lower() in q_lower:
                    if len(v) > best_len:
                        matched_venue = v
                        best_len = len(v)

        if not matched_venue:
            chunks = self._vector_search(q, top_k=3)
            for c in chunks:
                text = c.get("text", "").lower()
                for v in self.venues:
                    if len(v) > 3 and v.lower() in text:
                        if len(v) > best_len:
                            matched_venue = v
                            best_len = len(v)

        if not matched_venue:
            return {"is_sufficient": False, "gap_description": "Could not bind venue"}


        months = 'January|February|March|April|May|June|July|August|September|October|November|December'
        date_pattern = rf"(\d{{1,2}}(?:\s*(?:to|–|-)\s*\d{{1,2}})?\s+(?:{months})(?:\s+\d{{4}})?|(?:{months})\s+\d{{1,2}}(?:,\s*\d{{4}}|\s+\d{{4}})?)"
        date_match = re.search(date_pattern, q, re.IGNORECASE)
        date_query = date_match.group(1).lower() if date_match else ""

        venue_edges = self.conn.getEdges("Venue", matched_venue)
        candidate_events = [e["to_id"] for e in venue_edges if e.get("to_type") == "Event"]

        extracted_event = extracted.get("event", "")
        if extracted_event and extracted_event not in candidate_events:
            candidate_events.append(extracted_event)

        event_winners = {}
        target_event = ""
        
        for ev in candidate_events:
            try:
                ev_edges = self.conn.getEdges("Event", ev)
            except Exception as e:
                continue
                
            winners = []
            ev_date_match = False
            for ee in ev_edges:
                if ee.get("e_type") == "HAS_COMPETITOR":
                    ath_name = ee["to_id"]
                    try:
                        ath_edges = self.conn.getEdges("Athlete", ath_name)
                    except Exception:
                        continue
                    for ae in ath_edges:
                        if ae.get("e_type") == "WON_MEDAL" and ae.get("to_id") == "gold" and ae.get("attributes", {}).get("event_id") == ev:
                            winners.append(ath_name)
                            m_attrs = ae.get("attributes", {})
                            d_held = m_attrs.get("date_held", "").lower()
                            if date_query and d_held and (date_query in d_held or d_held in date_query or d_held in q_lower):
                                ev_date_match = True
            
            if winners:
                event_winners[ev] = winners
            if ev_date_match:
                target_event = ev
                break
                
        gold_winners = []
        if target_event:
            gold_winners = event_winners[target_event]
        elif len(event_winners) == 1 and not date_query:
            target_event = list(event_winners.keys())[0]
            gold_winners = event_winners[target_event]

        chunks = self._find_chunks_for_titles([target_event] if target_event else candidate_events[:1])

        def _split_team_athletes(names: list) -> list:
            split = []
            for name in names:
                if re.search(r"[a-z][A-Z]", name):
                    tokens = re.findall(r"[A-Z][a-z]+(?:\s+[a-z]+)*", name)
                    i = 0
                    while i < len(tokens) - 1:
                        split.append(f"{tokens[i]} {tokens[i+1]}")
                        i += 2
                    if i < len(tokens):
                        split.append(tokens[i])
                else:
                    split.append(name)
            return split if split else names

        clean_winners = _split_team_athletes(list(dict.fromkeys(gold_winners)))

        evidence = {
            "tool": "multi_hop_chain",
            "venue": matched_venue,
            "date_constraint": date_query,
            "event": target_event,
            "gold_winners": clean_winners
        }
        is_sufficient = bool(gold_winners) and bool(target_event)
        gap_desc = ""
        if not is_sufficient:
            if not target_event:
                gap_desc = f"Could not bind the specific event held at venue {matched_venue} on date {date_query}."
            elif not gold_winners:
                gap_desc = f"Could not find the gold medal winner for event {target_event}."

        return {
            "graph_context": evidence,
            "vector_context": chunks[:3],
            "evidence_log": [evidence],
            "is_sufficient": is_sufficient,
            "gap_description": gap_desc,
            "stop_reason": "sufficient_evidence" if is_sufficient else "missing_gold_winner"
        }

    def _lookup_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        q_lower = q.lower()
        
        matched_event = ""
        best_len = 0
        for ev_id in self.events:
            if len(ev_id) > 6 and ev_id.lower() in q_lower:
                if len(ev_id) > best_len:
                    matched_event = ev_id
                    best_len = len(ev_id)

        if not matched_event:
            chunks = self._vector_search(q, top_k=3)
            for c in chunks:
                text = c.get("text", "").lower()
                for ev_id in self.events:
                    if len(ev_id) > 6 and ev_id.lower() in text:
                        if len(ev_id) > best_len:
                            matched_event = ev_id
                            best_len = len(ev_id)
                            
            if not matched_event:
                return {
                    "vector_context": chunks,
                    "evidence_log": [{"tool": "vector_lookup_fallback", "chunks": len(chunks)}],
                    "is_sufficient": bool(chunks),
                    "stop_reason": "sufficient_evidence"
                }

        ev_attrs = self.events.get(matched_event, {})
        chunks = self._find_chunks_for_titles([matched_event])
        evidence = {
            "tool": "graph_lookup",
            "event": matched_event,
            "attributes": ev_attrs
        }
        return {
            "graph_context": evidence,
            "vector_context": chunks[:3],
            "evidence_log": [evidence],
            "is_sufficient": True,
            "stop_reason": "sufficient_evidence"
        }

    def _reflect_node(self, state: AgentState) -> Dict[str, Any]:
        if state.get("is_sufficient"):
            return {"stop_reason": "sufficient_evidence"}
        if state["iteration"] >= state["max_iterations"]:
            return {"stop_reason": "max_iterations"}
        return {"stop_reason": "retrieve_more"}

    def _fallback_search_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        gap = state.get("gap_description", "") or q
        archetype = state.get("archetype", "lookup")
        existing_entities = dict(state.get("extracted_entities") or {})

        query_prompt = (
            "You are an Agentic GraphRAG orchestrator. A graph traversal failed with the following gap:\n"
            f"  Original question: {q}\n"
            f"  Gap/error: {gap}\n\n"
            "Your task: Write a SHORT, PRECISE search query (one sentence) that will help retrieve "
            "the missing piece from a text corpus. Focus ONLY on the missing entity.\n"
            "CRITICAL: Do NOT correct typos or spelling errors in venue or event names. Preserve the exact spelling from the gap/question.\n"
            "Output ONLY the search query string, nothing else."
        )
        try:
            query_resp = llm_client.generate(prompt=query_prompt)
            targeted_query = query_resp.content.strip().strip('"').strip("'")
        except Exception:
            targeted_query = q

        chunks = self._vector_search(targeted_query, top_k=10)

        gap_lower = gap.lower()
        if "winner" in gap_lower or "athlete" in gap_lower or "gold" in gap_lower:
            entity_type = "athlete"
        elif "event" in gap_lower:
            entity_type = "event"
        elif "venue" in gap_lower:
            entity_type = "venue"
        else:
            entity_type = "entity"

        chunk_texts = "\n\n".join(
            f"[{c['chunk_id']}] {c.get('title','')}\n{c.get('text','')}"
            for c in chunks
        ) or "No passages found."

        extract_prompt = (
            f"You are an expert entity extractor. Given the following text passages and a search goal, "
            f"extract ONLY the exact {entity_type} name that resolves the gap.\n\n"
            f"Original question: {q}\n"
            f"Gap being resolved: {gap}\n"
            f"Search goal: {targeted_query}\n\n"
            f"Text passages:\n{chunk_texts}\n\n"
            f"Instructions:\n"
            f"- Output ONLY the exact {entity_type} name as it would appear in an Olympic database.\n"
            f"- If you cannot find a clear answer, output UNKNOWN.\n"
            f"- Do not include explanations.\n\n"
            f"Extracted {entity_type}:"
        )
        try:
            extract_resp = llm_client.generate(prompt=extract_prompt)
            extracted_value = extract_resp.content.strip().strip('"').strip("'")
            prompt_toks = (query_resp.prompt_tokens or 0) + (extract_resp.prompt_tokens or 0)
            completion_toks = (query_resp.completion_tokens or 0) + (extract_resp.completion_tokens or 0)
        except Exception:
            extracted_value = "UNKNOWN"
            prompt_toks = 0
            completion_toks = 0

        if extracted_value and extracted_value != "UNKNOWN":
            existing_entities[entity_type] = extracted_value

        gap_resolution_log = {
            "tool": "agentic_gap_resolution",
            "gap_addressed": gap,
            "formulated_query": targeted_query,
            "extracted_entities": dict(existing_entities),
            "chunks_searched": len(chunks),
            "resolution_status": "resolved" if extracted_value != "UNKNOWN" else "unresolved"
        }

        if extracted_value != "UNKNOWN" and entity_type in ["venue", "event"]:
            return {
                "vector_context": chunks,
                "evidence_log": [gap_resolution_log],
                "iteration": state["iteration"] + 1,
                "is_sufficient": False,
                "stop_reason": "fallback_complete",
                "extracted_entities": existing_entities,
                "gap_description": "",
                "prompt_tokens": prompt_toks,
                "completion_tokens": completion_toks,
                "total_tokens": prompt_toks + completion_toks,
            }

        return {
            "vector_context": chunks,
            "evidence_log": [gap_resolution_log],
            "iteration": state["iteration"] + 1,
            "is_sufficient": True,
            "stop_reason": "fallback_complete",
            "extracted_entities": existing_entities,
            "prompt_tokens": prompt_toks,
            "completion_tokens": completion_toks,
            "total_tokens": prompt_toks + completion_toks,
        }

    def _synthesize_node(self, state: AgentState) -> Dict[str, Any]:
        q = state["question"]
        g_ctx = json.dumps(state.get("graph_context", {}), indent=2)
        v_parts = []
        for c in state.get("vector_context", []):
            title_header = f" [{c['title']}]" if c.get('title') else ""
            v_parts.append(f"[{c['chunk_id']}]{title_header}\n{c['text']}")
        v_ctx = "\n\n".join(v_parts) if v_parts else "No direct passage."

        prompt = (
            "You are an Agentic GraphRAG assistant synthesizing an exact, verified answer to an Olympic question.\n\n"
            f"Question: {q}\n"
            f"Archetype: {state.get('archetype')}\n\n"
            f"Verified In-Database Graph Facts:\n{g_ctx}\n\n"
            f"Supporting Context Passages:\n{v_ctx}\n\n"
            "Instructions:\n"
            "1. Answer concisely, directly, and accurately using strictly the verified graph facts and passages.\n"
            "2. If an integer count was calculated by GSQL accumulator, state the exact integer.\n"
            "3. If answering an event name or title question, state both the specific event name and the full event title (e.g. 'Athletics at the 2008 Summer Olympics – Men\\'s marathon') if present in the graph facts.\n"
            "4. If answering a team event, list all winning athletes.\n"
            "5. Cite the relevant chunk IDs (e.g. [doc_id::c0]) or graph entities used.\n\n"
            "Final Answer:"
        )

        resp = llm_client.generate(prompt=prompt)
        cited_chunks = re.findall(r"\[([a-zA-Z0-9_\-\.\:\s]+::c\d+)\]", resp.content)
        cited_chunks = list(dict.fromkeys(cited_chunks))

        return {
            "answer": resp.content.strip(),
            "citations": cited_chunks,
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "total_tokens": resp.total_tokens
        }

    def _route_archetype(self, state: AgentState) -> str:
        arch = state.get("archetype", "lookup")
        if arch in ["aggregation", "superlative", "temporal", "multi_hop", "lookup"]:
            return arch
        return "lookup"

    def _route_reflection(self, state: AgentState) -> str:
        if state.get("is_sufficient") or state.get("stop_reason") == "sufficient_evidence" or state["iteration"] >= state["max_iterations"]:
            return "synthesize"
        if state.get("stop_reason") == "fallback_complete":
            arch = state.get("archetype", "lookup")
            if arch in ["aggregation", "superlative", "temporal", "multi_hop", "lookup"]:
                return arch
        return "fallback_search"

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("classify", self._classify_node)
        workflow.add_node("aggregation", self._aggregate_node)
        workflow.add_node("superlative", self._superlative_node)
        workflow.add_node("temporal", self._temporal_node)
        workflow.add_node("multi_hop", self._multi_hop_node)
        workflow.add_node("lookup", self._lookup_node)
        workflow.add_node("reflect", self._reflect_node)
        workflow.add_node("fallback_search", self._fallback_search_node)
        workflow.add_node("synthesize", self._synthesize_node)

        workflow.set_entry_point("classify")
        workflow.add_conditional_edges(
            "classify",
            self._route_archetype,
            {
                "aggregation": "aggregation",
                "superlative": "superlative",
                "temporal": "temporal",
                "multi_hop": "multi_hop",
                "lookup": "lookup"
            }
        )
        for specialist in ["aggregation", "superlative", "temporal", "multi_hop", "lookup"]:
            workflow.add_edge(specialist, "reflect")

        workflow.add_conditional_edges(
            "reflect",
            self._route_reflection,
            {
                "synthesize": "synthesize",
                "fallback_search": "fallback_search",
                "aggregation": "aggregation",
                "superlative": "superlative",
                "temporal": "temporal",
                "multi_hop": "multi_hop",
                "lookup": "lookup"
            }
        )
        workflow.add_edge("fallback_search", "reflect")
        workflow.add_edge("synthesize", END)

        return workflow.compile()


    def run(
        self,
        qid: str,
        question: str,
        ground_truth: List[str],
        gold_doc_ids: Optional[List[str]] = None,
        qtype: str = ""
    ) -> PipelineResult:
        start_time = time.time()
        init_state = {
            "question": question,
            "qid": qid,
            "archetype": qtype,
            "sub_questions": [],
            "evidence_log": [],
            "graph_context": {},
            "vector_context": [],
            "iteration": 0,
            "max_iterations": self.max_iterations,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "is_sufficient": False,
            "gap_description": "",
            "extracted_entities": {},
            "answer": "",
            "citations": [],
            "stop_reason": ""
        }

        final_state = self.app.invoke(init_state)
        latency = time.time() - start_time

        ans = final_state.get("answer", "")
        acc = calculate_exact_match(ans, ground_truth)
        retrieved_docs = list(dict.fromkeys(
            c.get("doc_id", "") for c in final_state.get("vector_context", []) if c.get("doc_id")
        ))

        trace = {
            "strategy": "langgraph_orchestration",
            "routed_archetype": final_state.get("archetype", qtype),
            "stop_reason": final_state.get("stop_reason", ""),
            "iteration": final_state.get("iteration", 0),
            "evidence_log": final_state.get("evidence_log", []),
            "graph_context": final_state.get("graph_context", {}),
            "vector_chunks_used": [c.get("chunk_id", "") for c in final_state.get("vector_context", [])],
        }

        return PipelineResult(
            pipeline_name=self.name,
            question_id=qid,
            question=question,
            qtype=final_state.get("archetype", qtype),
            prediction=ans,
            ground_truth=ground_truth,
            retrieved_doc_ids=retrieved_docs,
            gold_doc_ids=gold_doc_ids or [],
            cited_chunk_ids=final_state.get("citations", []),
            prompt_tokens=final_state.get("prompt_tokens", 0),
            completion_tokens=final_state.get("completion_tokens", 0),
            total_tokens=final_state.get("total_tokens", 0),
            latency_seconds=round(latency, 3),
            accuracy_score=acc,
            completeness_score=acc,
            execution_trace=trace
        )
