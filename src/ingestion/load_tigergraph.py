"""Bulk loader streaming parsed Olympic entities, chunks, and edges into TigerGraph Savanna.

Enforces batch sizing capped at 500 vertices/edges per call to avoid HTTP 413 Payload Too Large.
Derives sequential PRECEDES edges between Olympic competitions ordered by (year, season).
"""

import argparse
import json
import logging
from typing import Dict, List, Optional
import pandas as pd
from src.graph.client import graph_manager
from src.ingestion.parser import stream_corpus, extract_graph_dataframes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def derive_precedes_edges(df_comp: pd.DataFrame) -> pd.DataFrame:
    """Derives directed PRECEDES edges connecting sequential Olympic Games.
    
    Example: 2012 Summer -> 2016 Summer (or Summer -> next Summer, Winter -> next Winter).
    """
    if df_comp.empty:
        return pd.DataFrame()

    precedes_records = []

    # Sort separately by season to connect Summer -> next Summer and Winter -> next Winter
    for season in ["Summer", "Winter"]:
        season_df = df_comp[df_comp["season"] == season].sort_values(by="year").reset_index(drop=True)
        for i in range(len(season_df) - 1):
            curr_id = season_df.iloc[i]["competition_id"]
            next_id = season_df.iloc[i + 1]["competition_id"]
            # curr_id PRECEDES next_id
            precedes_records.append({"from_id": curr_id, "to_id": next_id})

    return pd.DataFrame(precedes_records)


def load_corpus_into_tigergraph(
    corpus_path: str = "Datasets/corpus/corpus.jsonl",
    limit: Optional[int] = None,
    batch_size: int = 500,
    target_doc_ids: Optional[set] = None
) -> Dict[str, int]:
    """Streams corpus documents, extracts graph tables, and bulk loads into TigerGraph Savanna."""
    conn = graph_manager.get_connection()
    if not conn:
        logger.error("Cannot load data: Not connected to TigerGraph Savanna. Please configure .env.")
        return {}

    logger.info(f"Streaming corpus documents from {corpus_path} (limit={limit}, target_docs={len(target_doc_ids) if target_doc_ids else 'all'})...")
    docs = []
    for idx, doc in enumerate(stream_corpus(corpus_path)):
        if target_doc_ids and doc.doc_id not in target_doc_ids:
            continue
        docs.append(doc)
        if limit and len(docs) >= limit:
            break

    logger.info(f"Extracting graph DataFrames for {len(docs)} documents...")
    tables = extract_graph_dataframes(docs)

    # Derive PRECEDES edges from competitions
    df_precedes = derive_precedes_edges(tables["Competition"])
    tables["PRECEDES"] = df_precedes

    results = {}

    # 1. Upsert Vertices
    logger.info("Upserting vertices...")

    vertex_configs = [
        ("Document", "doc_id", {"title": "title", "raw_text": "raw_text"}),
        ("Competition", "competition_id", {"name": "name", "year": "year", "season": "season"}),
        ("Venue", "venue_id", {"name": "name"}),
        ("Event", "event_id", {"name": "name", "sport": "sport", "competitors": "competitors", "nations": "nations"}),
        ("Athlete", "athlete_id", {"name": "name"}),
        ("Medal", "medal_id", {"medal_type": "medal_type"}),
        ("Nation", "nation_id", {"name": "name", "noc_code": "noc_code"}),
        ("Date", "date_id", {"date_str": "date_str", "year": "year"})
    ]

    for v_type, v_id, attrs in vertex_configs:
        df = tables.get(v_type)
        if df is not None and not df.empty:
            count = graph_manager.batch_upsert_vertices(
                vertex_type=v_type,
                df=df,
                v_id_col=v_id,
                attributes=attrs,
                batch_size=batch_size
            )
            results[f"vertex_{v_type}"] = count
            logger.info(f"Upserted {count} {v_type} vertices.")

    # 2. Upsert Edges
    logger.info("Upserting edges...")

    edge_configs = [
        ("PART_OF", "from_id", "to_id", {}, "Event", "Competition"),
        ("HELD_AT", "from_id", "to_id", {}, "Event", "Venue"),
        ("WON_MEDAL", "from_id", "to_id", {"event_id": "event_id", "competition_id": "competition_id", "date_held": "date_held"}, "Athlete", "Medal"),
        ("REPRESENTS", "from_id", "to_id", {}, "Athlete", "Nation"),
        ("COMPETED_IN", "from_id", "to_id", {}, "Athlete", "Event"),
        ("PRECEDES", "from_id", "to_id", {}, "Competition", "Competition")
    ]

    for e_type, from_col, to_col, attrs, from_t, to_t in edge_configs:
        df = tables.get(e_type)
        if df is not None and not df.empty:
            count = graph_manager.batch_upsert_edges(
                edge_type=e_type,
                df=df,
                from_col=from_col,
                to_col=to_col,
                attributes=attrs,
                from_type=from_t,
                to_type=to_t,
                batch_size=batch_size
            )
            results[f"edge_{e_type}"] = count
            logger.info(f"Upserted {count} {e_type} edges.")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Olympic corpus into TigerGraph Savanna")
    parser.add_argument("--limit", type=int, default=None, help="Number of documents to test")
    parser.add_argument("--checkpoint-questions", type=int, default=None, help="Load gold documents for first N checkpoint questions")
    parser.add_argument("--batch-size", type=int, default=500, help="Batch size (max 500)")
    args = parser.parse_args()

    targets = None
    if args.checkpoint_questions:
        targets = set()
        with open("Datasets/questions/eval_public.jsonl", "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= args.checkpoint_questions:
                    break
                data = json.loads(line)
                targets.update(data.get("gold_doc_ids", []))
        print(f"Extracted {len(targets)} unique gold doc IDs for first {args.checkpoint_questions} questions.")

    load_corpus_into_tigergraph(limit=args.limit, batch_size=args.batch_size, target_doc_ids=targets)
