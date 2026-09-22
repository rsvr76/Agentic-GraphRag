"""pyTigerGraph connection manager and graph operation helpers."""

import logging
from typing import Any, Dict, List, Optional
from src.config import settings

logger = logging.getLogger(__name__)


class TigerGraphManager:
    def __init__(self):
        self._conn = None

    def get_connection(self):
        if self._conn is None:
            try:
                import pyTigerGraph as tg
                self._conn = tg.TigerGraphConnection(
                    host=settings.tigergraph_host,
                    username=settings.tigergraph_username,
                    password=settings.tigergraph_password,
                    graphname=settings.tigergraph_graph
                )
                if settings.tigergraph_secret:
                    self._conn.getToken(settings.tigergraph_secret)
            except Exception as e:
                logger.warning(f"Could not connect to TigerGraph instance at {settings.tigergraph_host}: {e}")
                self._conn = None
        return self._conn

    def is_connected(self) -> bool:
        try:
            conn = self.get_connection()
            if conn:
                return conn.ping()
        except Exception:
            return False
        return False

    def get_schema(self) -> Dict[str, Any]:
        """Fetch schema metadata (vertices, edges)."""
        conn = self.get_connection()
        if conn:
            try:
                return conn.getSchema()
            except Exception as e:
                logger.error(f"Failed to fetch schema: {e}")
        return {"vertices": [], "edges": []}

    def run_installed_query(self, query_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Run an installed GSQL query."""
        conn = self.get_connection()
        if conn:
            return conn.runInstalledQuery(query_name, params=params or {})
        return []

    def run_interpreted_query(self, query_body: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Run an interpreted GSQL query."""
        conn = self.get_connection()
        if conn:
            return conn.runInterpretedQuery(query_body, params=params or {})
        return []

    def get_neighbors(self, vertex_type: str, vertex_id: str, edge_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve 1-hop connected neighbors for a given vertex."""
        conn = self.get_connection()
        if conn:
            try:
                edges = ",".join(edge_types) if edge_types else ""
                return conn.getNeighbors(vertex_type, vertex_id, edge_types=edges)
            except Exception as e:
                logger.error(f"Neighbor lookup error: {e}")
        return []


tg_manager = TigerGraphManager()
