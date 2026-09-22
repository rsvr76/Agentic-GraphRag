"""Parser for Datasets/corpus/corpus.jsonl to extract Olympic graph entities and relationships.

Extracts vertices and edges aligned with Final Plan Section 6:
- Vertices: Document, Athlete, Event, Competition, Venue, Medal, Nation, Date
- Edges: WON_MEDAL, COMPETED_IN, HELD_AT, PART_OF, REPRESENTS, PRECEDES
"""

import json
import re
from typing import Any, Dict, Iterator, List, Optional
import pandas as pd
from pydantic import BaseModel


class ParsedEventDocument(BaseModel):
    doc_id: str
    title: str
    url: str
    wikidata_qid: str
    approx_tokens: int
    text: str

    # Extracted Infobox Metadata
    sport: Optional[str] = None
    event_name: Optional[str] = None
    games: Optional[str] = None
    games_year: Optional[int] = None
    games_season: Optional[str] = None
    venue: Optional[str] = None
    date_held: Optional[str] = None
    competitors: Optional[int] = None
    nations: Optional[int] = None

    # Winners & Medals
    gold_athlete: Optional[str] = None
    gold_noc: Optional[str] = None
    silver_athlete: Optional[str] = None
    silver_noc: Optional[str] = None
    bronze_athlete: Optional[str] = None
    bronze_noc: Optional[str] = None
    win_value: Optional[str] = None

    # Temporal linkages
    prev_year: Optional[int] = None
    next_year: Optional[int] = None


def extract_infobox_field(text: str, key: str) -> Optional[str]:
    pattern = rf"^\s*{re.escape(key)}\s*:\s*(.+)$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if match:
        val = match.group(1).strip()
        return val if val else None
    return None


def parse_document(raw_doc: Dict[str, Any]) -> ParsedEventDocument:
    text = raw_doc.get("text", "")
    title = raw_doc.get("title", "")

    # Extract Sport from Title (e.g., "Canoeing at the 2012 Summer Olympics..." -> "Canoeing")
    sport_match = re.match(r"^([^–\-]+?)\s+at the\s+\d{4}", title)
    sport = sport_match.group(1).strip() if sport_match else None

    # Extract Infobox attributes
    event_name = extract_infobox_field(text, "event") or title
    games = extract_infobox_field(text, "games")
    games_year = None
    games_season = None
    if games:
        year_match = re.search(r"(\d{4})", games)
        if year_match:
            games_year = int(year_match.group(1))
        if "summer" in games.lower():
            games_season = "Summer"
        elif "winter" in games.lower():
            games_season = "Winter"

    venue = extract_infobox_field(text, "venue")
    date_held = extract_infobox_field(text, "date")

    def to_int(s: Optional[str]) -> Optional[int]:
        if not s:
            return None
        m = re.search(r"\d+", s)
        return int(m.group(0)) if m else None

    competitors = to_int(extract_infobox_field(text, "competitors"))
    nations = to_int(extract_infobox_field(text, "nations"))

    gold_athlete = extract_infobox_field(text, "gold")
    gold_noc = extract_infobox_field(text, "goldNOC")
    silver_athlete = extract_infobox_field(text, "silver")
    silver_noc = extract_infobox_field(text, "silverNOC")
    bronze_athlete = extract_infobox_field(text, "bronze")
    bronze_noc = extract_infobox_field(text, "bronzeNOC")
    win_value = extract_infobox_field(text, "win_value")

    prev_year = to_int(extract_infobox_field(text, "prev"))
    next_year = to_int(extract_infobox_field(text, "next"))

    return ParsedEventDocument(
        doc_id=raw_doc.get("doc_id", ""),
        title=title,
        url=raw_doc.get("url", ""),
        wikidata_qid=raw_doc.get("wikidata_qid", ""),
        approx_tokens=raw_doc.get("approx_tokens", 0),
        text=text,
        sport=sport,
        event_name=event_name,
        games=games,
        games_year=games_year,
        games_season=games_season,
        venue=venue,
        date_held=date_held,
        competitors=competitors,
        nations=nations,
        gold_athlete=gold_athlete,
        gold_noc=gold_noc,
        silver_athlete=silver_athlete,
        silver_noc=silver_noc,
        bronze_athlete=bronze_athlete,
        bronze_noc=bronze_noc,
        win_value=win_value,
        prev_year=prev_year,
        next_year=next_year
    )


def extract_graph_dataframes(docs: List[ParsedEventDocument]) -> Dict[str, pd.DataFrame]:
    """Converts a collection of parsed documents into relational DataFrames ready for TigerGraph batch upsert."""
    doc_records = []
    event_records = []
    comp_records = {}
    venue_records = {}
    athlete_records = {}
    nation_records = {}
    date_records = {}

    edge_part_of = []
    edge_held_at = []
    edge_won_medal = []
    edge_represents = []
    edge_competed_in = []

    for d in docs:
        doc_records.append({
            "doc_id": d.doc_id,
            "title": d.title,
            "raw_text": d.text[:1500]
        })

        event_id = d.title
        event_records.append({
            "event_id": event_id,
            "name": d.event_name or d.title,
            "sport": d.sport or "",
            "competitors": d.competitors or 0,
            "nations": d.nations or 0
        })

        if d.games:
            comp_id = d.games
            if comp_id not in comp_records:
                comp_records[comp_id] = {
                    "competition_id": comp_id,
                    "name": comp_id,
                    "year": d.games_year or 0,
                    "season": d.games_season or "",
                    "host_city": "",
                    "host_country": ""
                }
            edge_part_of.append({"from_id": event_id, "to_id": comp_id})

        if d.venue:
            v_id = d.venue
            if v_id not in venue_records:
                venue_records[v_id] = {
                    "venue_id": v_id,
                    "name": v_id,
                    "city": "",
                    "country": "",
                    "year_built": 0
                }
            edge_held_at.append({"from_id": event_id, "to_id": v_id})

        if d.date_held:
            date_id = d.date_held
            if date_id not in date_records:
                date_records[date_id] = {
                    "date_id": date_id,
                    "date_str": date_id,
                    "year": d.games_year or 0,
                    "month": 0,
                    "day": 0
                }

        # Process Medals and Athletes
        medal_tuples = [
            ("gold", d.gold_athlete, d.gold_noc),
            ("silver", d.silver_athlete, d.silver_noc),
            ("bronze", d.bronze_athlete, d.bronze_noc)
        ]

        for medal_type, ath_name, noc in medal_tuples:
            if ath_name:
                ath_id = ath_name.strip()
                if ath_id not in athlete_records:
                    athlete_records[ath_id] = {"athlete_id": ath_id, "name": ath_name}

                edge_won_medal.append({
                    "from_id": ath_id,
                    "to_id": medal_type,
                    "event_id": event_id,
                    "competition_id": d.games or "",
                    "date_held": d.date_held or ""
                })
                edge_competed_in.append({"from_id": ath_id, "to_id": event_id})

                if noc:
                    if noc not in nation_records:
                        nation_records[noc] = {"nation_id": noc, "name": noc, "noc_code": noc}
                    edge_represents.append({"from_id": ath_id, "to_id": noc})

    # Fixed medal records
    medal_records = [
        {"medal_id": "gold", "type": "gold"},
        {"medal_id": "silver", "type": "silver"},
        {"medal_id": "bronze", "type": "bronze"}
    ]

    return {
        "Document": pd.DataFrame(doc_records),
        "Event": pd.DataFrame(event_records),
        "Competition": pd.DataFrame(list(comp_records.values())),
        "Venue": pd.DataFrame(list(venue_records.values())),
        "Athlete": pd.DataFrame(list(athlete_records.values())),
        "Medal": pd.DataFrame(medal_records),
        "Nation": pd.DataFrame(list(nation_records.values())),
        "Date": pd.DataFrame(list(date_records.values())),
        "PART_OF": pd.DataFrame(edge_part_of),
        "HELD_AT": pd.DataFrame(edge_held_at),
        "WON_MEDAL": pd.DataFrame(edge_won_medal),
        "REPRESENTS": pd.DataFrame(edge_represents),
        "COMPETED_IN": pd.DataFrame(edge_competed_in)
    }


def stream_corpus(file_path: str = "Datasets/corpus/corpus.jsonl") -> Iterator[ParsedEventDocument]:
    """Stream parsed records one by one without loading all 23MB at once."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                yield parse_document(data)
