"""Parser for Datasets/corpus/corpus.jsonl to extract graph entities and relationships."""

import json
import re
from typing import Any, Dict, Iterator, List, Optional
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


def stream_corpus(file_path: str = "Datasets/corpus/corpus.jsonl") -> Iterator[ParsedEventDocument]:
    """Stream parsed records one by one without loading all 23MB at once."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                yield parse_document(data)
