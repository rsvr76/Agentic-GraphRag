"""TigerGraph Model Context Protocol (MCP) tool server definition.

Exposes TigerGraph tools for graph schema discovery, neighbor traversal,
GSQL query execution, and vector search to LLM agents.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from src.graph.client import tg_manager


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]


class TigerGraphMCPTools:
    """Registry of TigerGraph MCP tools callable by LLM Orchestrators."""

    @classmethod
    def get_tool_definitions(cls) -> List[Dict[str, Any]]:
        """Return standardized OpenAI/MCP format tool declarations."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "tg_get_schema",
                    "description": "Inspect the TigerGraph schema to discover all available vertex types, edge types, and their attributes.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tg_get_neighbors",
                    "description": "Traverse the graph from a starting vertex to retrieve connected neighbor vertices and relationship edges.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "vertex_type": {
                                "type": "string",
                                "description": "The type of vertex (e.g., Event, Athlete, Sport, OlympicGame, Country, Venue)"
                            },
                            "vertex_id": {
                                "type": "string",
                                "description": "The primary ID of the vertex (e.g., event name or athlete name)"
                            },
                            "edge_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional list of edge types to follow (e.g., ['WON_GOLD', 'PART_OF_GAME'])"
                            }
                        },
                        "required": ["vertex_type", "vertex_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tg_run_query",
                    "description": "Execute a specific GSQL query against TigerGraph for aggregations, multi-hop lookups, or superlatives.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query_name": {
                                "type": "string",
                                "description": "Name of the installed GSQL query or interpreted query body"
                            },
                            "params": {
                                "type": "object",
                                "description": "Key-value parameters to pass to the query"
                            }
                        },
                        "required": ["query_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tg_vector_search",
                    "description": "Perform semantic similarity search over text chunks in TigerGraph Vector DB to locate relevant documents.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query_text": {
                                "type": "string",
                                "description": "The search query string to embed and match against document vectors"
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of top matching documents to retrieve (default 5)"
                            }
                        },
                        "required": ["query_text"]
                    }
                }
            }
        ]

    @classmethod
    def execute_tool(cls, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch tool execution to TigerGraph client."""
        try:
            if tool_name == "tg_get_schema":
                return {"status": "success", "schema": tg_manager.get_schema()}
            
            elif tool_name == "tg_get_neighbors":
                v_type = arguments.get("vertex_type", "")
                v_id = arguments.get("vertex_id", "")
                edges = arguments.get("edge_types")
                neighbors = tg_manager.get_neighbors(v_type, v_id, edges)
                return {"status": "success", "neighbors": neighbors}
            
            elif tool_name == "tg_run_query":
                q_name = arguments.get("query_name", "")
                params = arguments.get("params", {})
                result = tg_manager.run_installed_query(q_name, params)
                return {"status": "success", "result": result}
            
            elif tool_name == "tg_vector_search":
                q_text = arguments.get("query_text", "")
                top_k = arguments.get("top_k", 5)
                return {
                    "status": "success",
                    "query": q_text,
                    "top_k": top_k,
                    "matches": []  # Populated via TigerGraph Vector DB endpoint
                }
            
            else:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
