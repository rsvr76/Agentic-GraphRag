"""Script to deploy the Olympic knowledge graph schema to TigerGraph Savanna."""

import logging
from src.graph.client import tg_manager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def deploy_schema():
    conn = tg_manager.get_connection()
    if not conn:
        logger.error("Could not obtain TigerGraph connection. Verify .env settings.")
        return False

    schema_gsql = """
    USE GRAPH Olympics
    DROP JOB ALL
    CREATE SCHEMA_CHANGE JOB add_olympics_schema FOR GRAPH Olympics {
        ADD VERTEX Document (PRIMARY_ID doc_id STRING, title STRING, raw_text STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Chunk (PRIMARY_ID chunk_id STRING, doc_id STRING, text STRING, start_offset INT, end_offset INT) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Athlete (PRIMARY_ID athlete_id STRING, name STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Event (PRIMARY_ID event_id STRING, name STRING, sport STRING, discipline STRING, gender STRING, competitors INT, nations INT) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Competition (PRIMARY_ID competition_id STRING, name STRING, year INT, season STRING, host_city STRING, host_country STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Venue (PRIMARY_ID venue_id STRING, name STRING, city STRING, country STRING, year_built INT) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Medal (PRIMARY_ID medal_id STRING, medal_type STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Nation (PRIMARY_ID nation_id STRING, name STRING, noc_code STRING) WITH STATS="OUTDEGREE_BY_EDGETYPE";
        ADD VERTEX Date (PRIMARY_ID date_id STRING, date_str STRING, year INT, month INT, day INT) WITH STATS="OUTDEGREE_BY_EDGETYPE";

        ADD DIRECTED EDGE WON_MEDAL (FROM Athlete, TO Medal, event_id STRING, competition_id STRING, date_held STRING) WITH REVERSE_EDGE="MEDAL_WON_BY";
        ADD DIRECTED EDGE COMPETED_IN (FROM Athlete, TO Event) WITH REVERSE_EDGE="HAS_COMPETITOR";
        ADD DIRECTED EDGE HELD_AT (FROM Event, TO Venue) WITH REVERSE_EDGE="HOSTED_EVENT";
        ADD DIRECTED EDGE PART_OF (FROM Event, TO Competition) WITH REVERSE_EDGE="INCLUDES_EVENT";
        ADD DIRECTED EDGE REPRESENTS (FROM Athlete, TO Nation) WITH REVERSE_EDGE="HAS_ATHLETE";
        ADD DIRECTED EDGE HAS_CHUNK (FROM Document, TO Chunk, chunk_index INT) WITH REVERSE_EDGE="CHUNK_OF_DOC";

        ADD DIRECTED EDGE MENTIONS_ATHLETE (FROM Document, TO Athlete, mention_chunk_id STRING) WITH REVERSE_EDGE="MENTIONED_IN_DOC_ATHLETE";
        ADD DIRECTED EDGE MENTIONS_EVENT (FROM Document, TO Event, mention_chunk_id STRING) WITH REVERSE_EDGE="MENTIONED_IN_DOC_EVENT";
        ADD DIRECTED EDGE MENTIONS_COMPETITION (FROM Document, TO Competition, mention_chunk_id STRING) WITH REVERSE_EDGE="MENTIONED_IN_DOC_COMP";
        ADD DIRECTED EDGE MENTIONS_VENUE (FROM Document, TO Venue, mention_chunk_id STRING) WITH REVERSE_EDGE="MENTIONED_IN_DOC_VENUE";
        ADD DIRECTED EDGE MENTIONS_NATION (FROM Document, TO Nation, mention_chunk_id STRING) WITH REVERSE_EDGE="MENTIONED_IN_DOC_NATION";
        ADD DIRECTED EDGE PRECEDES (FROM Competition, TO Competition) WITH REVERSE_EDGE="SUCCEEDS";
    }
    RUN SCHEMA_CHANGE JOB add_olympics_schema
    DROP JOB add_olympics_schema
    """

    logger.info("Executing schema change job on TigerGraph Savanna...")
    res = conn.gsql(schema_gsql)
    logger.info(f"GSQL Response:\n{res}")
    return res


if __name__ == "__main__":
    deploy_schema()
