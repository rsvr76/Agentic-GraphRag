"""pyTigerGraph connection manager and graph operation helpers for TigerGraph Savanna.

Supports auto-secret/token generation, connection checking, batch upserts capped at 500
records (to prevent HTTP 413 Payload Too Large errors), schema inspection, and query execution.
"""

import logging
import os
import re
from typing import Any, Dict, List, Optional
import pandas as pd
from src.config import settings

logger = logging.getLogger(__name__)


class TigerGraphManager:
    def __init__(self):
        self._conn = None

    def get_connection(self):
        if self._conn is None:
            host = settings.tigergraph_host or os.getenv("TIGERGRAPH_HOST", "")
            if not host or "your-instance" in host:
                return None

            try:
                import pyTigerGraph as tg
                is_cloud = "tgcloud.io" in host or "tigergraph.com" in host or True

                self._conn = tg.TigerGraphConnection(
                    host=host,
                    username=settings.tigergraph_username,
                    password=settings.tigergraph_password,
                    graphname=settings.tigergraph_graph,
                    tgCloud=is_cloud
                )

                # Auto-authenticate via secret/token if not explicitly provided
                if settings.tigergraph_secret:
                    self._conn.getToken(secret=settings.tigergraph_secret)
                else:
                    try:
                        secret = self._conn.createSecret()
                        if secret:
                            self._conn.getToken(secret=secret)
                    except Exception as sec_err:
                        logger.debug(f"Secret generation notice: {sec_err}")

            except Exception as e:
                logger.warning(f"Could not connect to TigerGraph instance at {host}: {e}")
                self._conn = None

        return self._conn

    def is_connected(self) -> bool:
        """Pings the TigerGraph instance to verify connectivity."""
        try:
            conn = self.get_connection()
            if conn:
                return bool(conn.ping())
        except Exception:
            return False
        return False

    def check_gds_installed(self) -> bool:
        """Checks if TigerVector/GDS package is installed on the workspace."""
        conn = self.get_connection()
        if not conn:
            return False
        try:
            res = conn.gsql("SHOW PACKAGE gds")
            return "package gds" in res.lower() or "installed" in res.lower()
        except Exception:
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
        """Run an interpreted GSQL query (fast dev iteration)."""
        conn = self.get_connection()
        if conn:
            return conn.runInterpretedQuery(query_body, params=params or {})
        return []

    def get_neighbors(
        self,
        vertex_type: str,
        vertex_id: str,
        edge_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """1-hop neighbor lookup from a seed vertex."""
        conn = self.get_connection()
        if not conn:
            return []
        try:
            edges = conn.getEdges(vertex_type, vertex_id, edge_type=edge_type)
            return edges if isinstance(edges, list) else []
        except Exception as e:
            logger.debug(f"Neighbor lookup notice for {vertex_type}/{vertex_id}: {e}")
            return []

    def batch_upsert_vertices(
        self,
        vertex_type: str,
        df: pd.DataFrame,
        v_id_col: str,
        attributes: Dict[str, str],
        batch_size: int = 500
    ) -> int:
        """Bulk upserts vertex records in batches capped at batch_size (default 500)."""
        conn = self.get_connection()
        if not conn or df.empty:
            return 0

        total_upserted = 0
        total_rows = len(df)

        for start_idx in range(0, total_rows, batch_size):
            batch_df = df.iloc[start_idx:start_idx + batch_size]
            count = conn.upsertVertexDataFrame(
                df=batch_df,
                vertexType=vertex_type,
                v_id=v_id_col,
                attributes=attributes
            )
            total_upserted += count

        return total_upserted

    def batch_upsert_edges(
        self,
        edge_type: str,
        df: pd.DataFrame,
        from_col: str,
        to_col: str,
        attributes: Optional[Dict[str, str]] = None,
        from_type: Optional[str] = None,
        to_type: Optional[str] = None,
        batch_size: int = 500
    ) -> int:
        """Bulk upserts edge records in batches capped at batch_size (default 500)."""
        conn = self.get_connection()
        if not conn or df.empty:
            return 0

        total_upserted = 0
        total_rows = len(df)

        for start_idx in range(0, total_rows, batch_size):
            batch_df = df.iloc[start_idx:start_idx + batch_size]
            count = conn.upsertEdgeDataFrame(
                df=batch_df,
                sourceVertexType=from_type,
                edgeType=edge_type,
                targetVertexType=to_type,
                from_id=from_col,
                to_id=to_col,
                attributes=attributes or {}
            )
            total_upserted += count

        return total_upserted


graph_manager = TigerGraphManager()
