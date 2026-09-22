# TigerGraph Agentic GraphRAG: Autonomous Knowledge Navigator

[![TigerGraph](https://img.shields.io/badge/Graph_Database-TigerGraph_Savanna-FF6B00?logo=tigergraph&logoColor=white)](https://www.tigergraph.com/)
[![MCP](https://img.shields.io/badge/Protocol-Model_Context_Protocol_(MCP)-8A2BE2)](https://modelcontextprotocol.io/)
[![Google GenAI](https://img.shields.io/badge/LLM-Google_Gemini_2.5-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![xAI Grok](https://img.shields.io/badge/LLM-xAI_Grok-000000?logo=x&logoColor=white)](https://x.ai/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

An autonomous Agentic GraphRAG investigation system built on TigerGraph Savanna. It coordinates graph traversal, vector similarity search, and temporal reasoning to resolve complex multi-hop, aggregation, and superlative inquiries over unstructured and semi-structured corpora.

## Executive Summary

Standard Retrieval-Augmented Generation (RAG) architectures fail when queries require synthesizing facts across dispersed documents, calculating aggregations, or resolving temporal sequences. TigerGraph Agentic GraphRAG replaces rigid, single-pass retrieval pipelines with an autonomous agent orchestrator powered by the TigerGraph Model Context Protocol (MCP).

The system decomposes complex user queries into discrete exploration plans, interrogates structured entity relationships via GSQL, executes vector similarity searches across document embeddings, identifies evidentiary gaps, and iterates until establishing a verified, grounded answer.

In accordance with the TigerGraph Agentic GraphRAG Hackathon specifications, this repository provides an empirical, side-by-side comparative benchmark of three distinct retrieval architectures:
1. Standard RAG: Dense vector similarity search baseline.
2. GraphRAG: Static knowledge graph subgraph retrieval baseline.
3. Agentic GraphRAG: Dynamic orchestrator with MCP tool dispatch and temporal reasoning.

## System Architecture

The following diagram illustrates the multi-tier interaction between the agent harness, the MCP tool abstraction layer, and the TigerGraph Savanna backend:

```mermaid
flowchart TD
    UserQuery["User / Benchmark Query"] --> Orchestrator["Agent Orchestrator<br>(Gemini 2.5 Flash / Grok)"]

    subgraph AgentHarness["Agent Harness & State Manager"]
        Orchestrator --> Loop{"Sufficient<br>Evidence?"}
        Loop -- No --> ActionPlanner["Query Decomposition & Action Planner"]
        Loop -- Yes --> AnswerSynthesis["Evidence Evaluator & Answer Synthesis"]
    end

    subgraph MCPInterface["TigerGraph Model Context Protocol (MCP) Interface"]
        ActionPlanner --> T1["tg_get_schema()"]
        ActionPlanner --> T2["tg_get_neighbors()"]
        ActionPlanner --> T3["tg_run_query()"]
        ActionPlanner --> T4["tg_vector_search()"]
    end

    subgraph TigerGraphBackend["TigerGraph Savanna Cloud Engine"]
        T1 & T2 & T3 --> GraphDB[("Graph DB<br>(GSQL Schema & Algorithms)")]
        T4 --> VectorDB[("TigerGraph Vector DB<br>(Corpus Embeddings)")]
    end

    GraphDB & VectorDB --> EvidenceStore["Observation & Context Buffer"]
    EvidenceStore --> Orchestrator
    AnswerSynthesis --> FinalOutput["Final Answer + Grounded Citations"]
```

## Knowledge Graph and Temporal Reasoning Schema

The graph schema is modeled specifically around the Olympic benchmark corpus (2,951 Wikipedia documents, ~5.47M tokens):

### Vertex Types
- Document: Complete article text, source URL, Wikidata QID, and token length.
- OlympicGame: Event iteration defined by year and season (e.g., `2012 Summer`, `2010 Winter`).
- Sport: Athletic discipline classification (e.g., `Athletics`, `Canoeing`, `Biathlon`).
- Event: Specific competition instance (e.g., `Men's 20km walk`).
- Athlete: Participating competitors and medal recipients.
- Country: National Olympic Committees (NOC) identifiers (e.g., `USA`, `NED`, `HUN`).
- Venue: Host facility and geographic location.

### Edges and Relational Topology
- Structural: `PART_OF_GAME`, `IN_SPORT`, `HELD_AT_VENUE`, `WON_GOLD`, `WON_SILVER`, `WON_BRONZE`, `REPRESENTS_NOC`, `DOCUMENT_COVERS`.
- Temporal Precedence:
  - `PRECEDING_GAME`: Chronological ordering between Olympiads, enabling resolution of relative temporal queries (e.g., *"held immediately before 2016"*).
  - `PREVIOUS_EVENT` and `NEXT_EVENT`: Direct linkages across consecutive historical editions of specific events.

## Empirical Benchmark Evaluation

The three retrieval pipelines are evaluated across the 100 questions in `Datasets/questions/eval_public.jsonl`, covering five query archetypes: aggregation, superlative, temporal, multi-hop, and direct lookup.

Metrics are computed via the automated evaluation harness (`python -m src.evaluation.runner`), which logs prompt tokens, completion tokens, latency, accuracy against ground truth, and completeness score.

| Pipeline | Accuracy (%) | Completeness (%) | Avg Tokens / Query | Avg Latency (s) | Evaluation Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Standard RAG | Pending run | Pending run | Pending run | Pending run | Awaiting full-corpus benchmark run |
| GraphRAG | Pending run | Pending run | Pending run | Pending run | Awaiting full-corpus benchmark run |
| Agentic GraphRAG | Pending run | Pending run | Pending run | Pending run | Awaiting full-corpus benchmark run |

Note: Benchmark metrics will be populated strictly following completion and logging of the full verification run across the entire evaluation set. Unverified or estimated numbers are omitted to preserve benchmark integrity.

## Getting Started

### Prerequisites
- Python 3.11 or higher
- TigerGraph Savanna cloud instance (or local TigerGraph 3.x / 4.x enterprise deployment)
- API key for Google Gemini (`GEMINI_API_KEY`) or xAI Grok (`XAI_API_KEY`)

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/tigergraph-agentic-graphrag.git
cd tigergraph-agentic-graphrag

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Configure the connection parameters in `.env`:
```ini
# TigerGraph Savanna Credentials
TIGERGRAPH_HOST=https://your-instance.i.tgcloud.io
TIGERGRAPH_USERNAME=tigergraph
TIGERGRAPH_PASSWORD=your_password
TIGERGRAPH_GRAPH=OlympicsCorpus

# LLM Providers
GEMINI_API_KEY=your_gemini_api_key
XAI_API_KEY=your_xai_grok_api_key
PRIMARY_LLM_PROVIDER=gemini
```

### 3. Running the Benchmark Evaluation

Execute the automated test suite across all three pipelines to log verifiable performance metrics:
```bash
python -m src.evaluation.runner
```

### 4. Interactive Dashboard

Launch the metrics visualization and real-time query investigator interface:
```bash
streamlit run dashboard/app.py
```

## Repository Structure

```text
tigergraph-agentic-graphrag/
├── Datasets/                     # Official Olympic corpus and evaluation question sets
│   ├── corpus/corpus.jsonl       # 2,951 Wikipedia articles (~5.47M tokens)
│   └── questions/                # eval_public.jsonl & eval_hidden.jsonl
├── dashboard/
│   └── app.py                    # Streamlit metrics dashboard & query visualizer
├── docs/                         # Specifications and source-of-truth project reference documents
│   ├── plan.md                   # Concrete technical implementation plan
│   ├── project.md                # Problem analysis, design decisions, and research reference
│   ├── implementation-plan.md    # Multi-phase execution roadmap
│   ├── overview.md               # Hackathon overview, eligibility, and prize breakdown
│   └── ps.md                     # Detailed problem statement, rubric, and dataset specs
├── src/
│   ├── config.py                 # Pydantic Settings configuration manager
│   ├── evaluation/
│   │   ├── metrics.py            # Accuracy, completeness, and token accounting
│   │   └── runner.py             # Automated 3-way evaluation harness
│   ├── graph/
│   │   ├── client.py             # pyTigerGraph connection manager
│   │   └── schema.gsql           # GSQL schema with entity and temporal edges
│   ├── ingestion/
│   │   └── parser.py             # Infobox and document parser for corpus.jsonl
│   ├── llm/
│   │   └── client.py             # Unified Gemini & Grok client with token accounting
│   ├── mcp/
│   │   └── server.py             # TigerGraph Model Context Protocol (MCP) tools
│   └── pipelines/
│       ├── standard_rag.py       # Pipeline 1: Dense vector baseline
│       ├── graph_rag.py          # Pipeline 2: Static GraphRAG baseline
│       └── agentic_graphrag.py   # Pipeline 3: Autonomous Orchestrator Agent
├── requirements.txt              # Production dependencies
├── .env.example                  # Environment configuration template
└── .gitignore                    # Professional git exclusion rules
```

## Hackathon Rubric Alignment

This implementation maps directly to the official scoring criteria:

- Investigation Accuracy (30%): Empirical validation against held-out ground truth for complex multi-hop, aggregation, and temporal questions.
- Evidence Quality and Explainability (15%): Unbroken citation trail grounded strictly in `corpus.jsonl` with structured step logs.
- Agentic Effectiveness and Efficiency (15%): Dynamic stopping criteria balancing token expenditure with evidentiary sufficiency.
- Engineering and Code Quality (15%): Production-grade Python packaging, typing, decoupled MCP architecture, and automated evaluation scripts.
- Innovation (15%): Graph-native temporal edges (`PRECEDING_GAME`, `PREVIOUS_EVENT`) enabling non-linear historical reasoning.
- Presentation and Visualization (10%): Interactive Streamlit dashboard for comparative evaluation and live auditability.

## License and Attribution

This project is distributed under the Apache License 2.0. The underlying corpus text is derived from English Wikipedia under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
