# Comparative 3-Pipeline Benchmark Traces and Agent Execution Analysis (Public 100)

## Overview

This report documents the detailed comparative execution traces, reasoning paths, tool interactions, and synthesized outputs for all 100 public benchmark questions across all three benchmarked pipelines:

1. **Pipeline 1: Standard RAG** (Vector Search over document chunks)

2. **Pipeline 2: GraphRAG** (Entity Linking + 1-2 hop neighborhood traversal)

3. **Pipeline 3: Autonomous Agentic GraphRAG** (Dynamic LangGraph StateGraph + In-Database GSQL Accumulators + Self-RAG Reflection)

## Public 100 3-Pipeline Benchmark Summary

| Pipeline | Question Count | Accuracy | Avg Tokens / Query | Avg Latency (s) | Evaluation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Standard RAG | 100 | 47.0% | 6344.9 | 16.83 | Official Public Benchmark |
| GraphRAG | 100 | 62.0% | 5319.9 | 15.18 | Official Public Benchmark |
| Agentic GraphRAG | 100 | 99.0% | 5250.2 | 11.38 | Official Public Benchmark |

## Per-Archetype Performance Distribution

| Archetype | Questions | Standard RAG Acc | GraphRAG Acc | Agentic GraphRAG Acc |
| :--- | :--- | :--- | :--- | :--- |
| aggregation | 21 | 4.8% | 4.8% | 100.0% |
| lookup | 19 | 100.0% | 100.0% | 100.0% |
| multi_hop | 28 | 42.9% | 53.6% | 96.4% |
| superlative | 10 | 40.0% | 50.0% | 100.0% |
| temporal | 22 | 50.0% | 100.0% | 100.0% |


## Question-by-Question 3-Pipeline Comparative Traces and Outputs

### Question [1/100] — pub-001

- Query: "According to the provided corpus, how many biathlon events at the 2018 Winter Olympics had more than 73 competitors?"
- Archetype: `aggregation`
- Ground Truth: `5`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 74.13 seconds
- Tokens Used: 7097 (Prompt: 7044, Completion: 53)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context passages, there is no mention of the total number of competitors in the biathlon events at the 2018 Winter Olympics to determine which events had more than 73 competitors. 

Answer: Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 31.68 seconds
- Tokens Used: 7759 (Prompt: 7630, Completion: 129)
- Retrieved Subgraph Chunks: `Q47155408::c0, Q47155541::c0, Q47155371::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there is only **1** biathlon event at the 2018 Winter Olympics that had more than 73 competitors:

* **Men's individual** with 86 competitors [Q47155408::c0]. 

The other listed events have 73 or fewer competitors (Men's relay has 73 [Q47155541::c0], Men's pursuit has 60 [Q47155371::c0], and Men's mass start has 30)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 5.31 seconds
- Tokens Used: 209 (Prompt: 178, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Biathlon at the 2018 Winter Olympics – Mixed relay (80 competitors)", "Biathlon at the 2018 Winter Olympics – Men's sprint (87 competitors)", "Biathlon at the 2018 Winter Olympics – Women's sprint (87 competitors)", "Biathlon at the 2018 Winter Olympics – Women's individual (87 competitors)", "Biathlon at the 2018 Winter Olympics – Men's individual (86 competitors)"], "competition": "2018 Winter", "threshold": 73, "sport": "Biathlon"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Biathlon at the 2018 Winter Olympics – Mixed relay (80 competitors)", "Biathlon at the 2018 Winter Olympics – Men's sprint (87 competitors)", "Biathlon at the 2018 Winter Olympics – Women's sprint (87 competitors)", "Biathlon at the 2018 Winter Olympics – Women's individual (87 competitors)", "Biathlon at the 2018 Winter Olympics – Men's individual (86 competitors)"], "competition": "2018 Winter", "threshold": 73, "sport": "Biathlon"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 5 biathlon events at the 2018 Winter Olympics that had more than 73 competitors."

### Question [2/100] — pub-002

- Query: "Who won the gold medal in the men's 20 kilometres walk athletics event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Chen Ding`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 54.45 seconds
- Tokens Used: 5198 (Prompt: 5151, Completion: 47)
- Retrieved Context Chunks: `Q26233122::c0`
- Synthesized Prediction:
  > "Based on the provided context, the defending 2012 Olympic champion for the men's 20 kilometres walk was Chen Ding. 

Sources: [Q26233122::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 30.14 seconds
- Tokens Used: 5479 (Prompt: 5418, Completion: 61)
- Retrieved Subgraph Chunks: `Q1050909::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, **Chen Ding** won the gold medal in the men's 20 kilometres walk athletics event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) [Q1050909::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 23.31 seconds
- Tokens Used: 8685 (Prompt: 8549, Completion: 136)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Athletics at the 2012 Summer Olympics – Men's 20 kilometres walk", "gold_winner": "Chen Ding", "date_held": "4 August 2012"}`
  - Supporting Document Chunks: `Q1050909::c0`
- Synthesized Prediction:
  > "**Chen Ding** won the gold medal in the men's 20 kilometres walk athletics event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics) [Q1050909::c0]. 

* **Event Name:** Men's 20 kilometres walk
* **Full Event Title:** Athletics at the 2012 Summer Olympics – Men's 20 kilometres walk [Q1050909::c0]
* **Date Held:** 4 August 2012 [Q1050909::c0]"

### Question [3/100] — pub-003

- Query: "According to the provided corpus, how many shooting events at the 2004 Summer Olympics had more than 37 competitors?"
- Archetype: `aggregation`
- Ground Truth: `8`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 42.40 seconds
- Tokens Used: 7995 (Prompt: 7674, Completion: 321)
- Retrieved Context Chunks: `Q7500840::c0, Q7500838::c0, Q4354074::c0`
- Synthesized Prediction:
  > "To find the number of shooting events at the 2004 Summer Olympics with more than 37 competitors, we can examine the competitor counts given in the infoboxes of the provided context passages:

* **Women's 50 metre rifle three positions**: 32 competitors ([Q7500840::c0])
* **Women's 25 metre pistol**: 37 competitors ([Q7500838::c0])
* **Women's 10 metre air rifle**: 44 competitors ([Q4354074::c0])
* **Men's 25 metre rapid fire pistol**: 17 competitors ([Q7500830::c0])
* **Men's 50 metre pistol**: 42 competitors ([Q7500827::c0])

Out of these events, only **2** events had more than 37 competitors: the Women's 10 metre air rifle (44 competitors) and the Men's 50 metre pistol (42 competitors).

**Sources:** 
- [Q4354074::c0]
- [Q7500827::c0]
- [Q7500830::c0]
- [Q7500838::c0]
- [Q7500840::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 37.26 seconds
- Tokens Used: 5685 (Prompt: 5603, Completion: 82)
- Retrieved Subgraph Chunks: `Q4354615::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are **2** shooting events at the 2004 Summer Olympics that had more than 37 competitors:

1. **Men's 10 metre air pistol** with 47 competitors [Q4354615::c0]
2. **Men's 10 metre air rifle** with 47 competitors"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 3.92 seconds
- Tokens Used: 212 (Prompt: 182, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 8, "matching_events": ["Shooting at the 2004 Summer Olympics – Men's 50 metre rifle prone (46 competitors)", "Shooting at the 2004 Summer Olympics – Men's skeet (41 competitors)", "Shooting at the 2004 Summer Olympics – Women's 10 metre air pistol (41 competitors)", "Shooting at the 2004 Summer Olympics – Women's 10 metre air rifle (44 competitors)", "Shooting at the 2004 Summer Olympics – Men's 10 metre air pistol (47 competitors)", "Shooting at the 2004 Summer Olympics – Men's 50 metre pistol (42 competitors)", "Shooting at the 2004 Summer Olympics – Men's 50 metre rifle three positions (40 competitors)", "Shooting at the 2004 Summer Olympics – Men's 10 metre air rifle (47 competitors)"], "competition": "2004 Summer", "threshold": 37, "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 8, "matching_events": ["Shooting at the 2004 Summer Olympics – Men's 50 metre rifle prone (46 competitors)", "Shooting at the 2004 Summer Olympics – Men's skeet (41 competitors)", "Shooting at the 2004 Summer Olympics – Women's 10 metre air pistol (41 competitors)", "Shooting at the 2004 Summer Olympics – Women's 10 metre air rifle (44 competitors)", "Shooting at the 2004 Summer Olympics – Men's 10 metre air pistol (47 competitors)", "Shooting at the 2004 Summer Olympics – Men's 50 metre pistol (42 competitors)", "Shooting at the 2004 Summer Olympics – Men's 50 metre rifle three positions (40 competitors)", "Shooting at the 2004 Summer Olympics – Men's 10 metre air rifle (47 competitors)"], "competition": "2004 Summer", "threshold": 37, "sport": "Shooting"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database, there were 8 shooting events at the 2004 Summer Olympics that had more than 37 competitors."

### Question [4/100] — pub-004

- Query: "According to the provided corpus, which athletics event at the 2008 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Athletics at the 2008 Summer Olympics – Men's marathon`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 41.09 seconds
- Tokens Used: 7152 (Prompt: 7054, Completion: 98)
- Retrieved Context Chunks: `Q693595::c1, Q677027::c2`
- Synthesized Prediction:
  > "Based on the provided context passages, the athletics event with the highest number of competitors listed is the **Men's marathon** (with at least 60 runners finishing, as indicated by rank numbers up to 60) and the **Men's 800 metres** (which also lists participants up to rank 58). 

Sources: [Q693595::c1], [Q677027::c2]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 99.49 seconds
- Tokens Used: 5250 (Prompt: 5142, Completion: 108)
- Retrieved Subgraph Chunks: `Q754844::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the athletics event at the 2008 Summer Olympics with the highest number of competitors was the **Men's 100 metres**, which had **80 competitors** [Q754844::c0] (compared to 39 for the 10,000 metres, 43 for the 110 metres hurdles, 48 for the 1500 metres, and 51 for the 20 kilometres walk)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 5.40 seconds
- Tokens Used: 2011 (Prompt: 1929, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's marathon", "full_event_title": "Athletics at the 2008 Summer Olympics – Men's marathon", "competitors": 95, "competition": "2008 Summer", "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's marathon", "full_event_title": "Athletics at the 2008 Summer Olympics – Men's marathon", "competitors": 95, "competition": "2008 Summer", "sport": "Athletics"}`
  - Supporting Document Chunks: `Q693595::c0`
- Synthesized Prediction:
  > "According to the provided database facts and corpus, the athletics event at the 2008 Summer Olympics with the highest number of competitors was the **Men's marathon** (full title: *Athletics at the 2008 Summer Olympics – Men's marathon*), featuring **95** competitors from 56 nations [Q693595::c0]."

### Question [5/100] — pub-005

- Query: "Who won the gold medal in the event held at Olympic Weightlifting Gymnasium on 20 September 1988?"
- Archetype: `multi_hop`
- Ground Truth: `Naim Süleymanoğlu`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 39.98 seconds
- Tokens Used: 8782 (Prompt: 8648, Completion: 134)
- Retrieved Context Chunks: `Q25239533::c0, Q25239316::c0`
- Synthesized Prediction:
  > "Based on the provided context, two weightlifting events took place on 20 September 1988 at the Olympic Weightlifting Gymnasium:

1. **Men's 67.5 kg event**: Joachim Kunz won the gold medal [Q25239533::c0].
2. **Men's 60 kg event**: Naim Süleymanoğlu won the gold medal [Q25239316::c0].

Sources: [Q25239533::c0], [Q25239316::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 32.27 seconds
- Tokens Used: 6485 (Prompt: 6416, Completion: 69)
- Retrieved Subgraph Chunks: `Q25239316::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph and context passages, the gold medal for the men's 60 kg weightlifting event held at the Olympic Weightlifting Gymnasium on 20 September 1988 was won by **Naim Süleymanoğlu** [Q25239316::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 101.06 seconds
- Tokens Used: 21686 (Prompt: 21567, Completion: 119)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Olympic Weightlifting Gymnasium", "date_constraint": "20 september 1988", "year_filter": "1988", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 5}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Weightlifting Gymnasium", "date_constraint": "20 september 1988", "year_filter": "1988", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 5}`
  - Supporting Document Chunks: `Q25239316::c0`
- Synthesized Prediction:
  > "Based on the verified context passages, the gold medal in the event held at the **Olympic Weightlifting Gymnasium** on **20 September 1988** (Men's 60 kg weightlifting event) was won by:

* **Naim Süleymanoğlu** (representing Turkey, TUR) [Q25239316::c0].

**Full Event Title:** Weightlifting at the 1988 Summer Olympics – Men's 60 kg [Q25239316::c0]"

### Question [6/100] — pub-006

- Query: "Who won the gold medal in the women's 57 kg judo event at the Summer Olympics held immediately before 2020?"
- Archetype: `temporal`
- Ground Truth: `Rafaela Silva`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 32.75 seconds
- Tokens Used: 1716 (Prompt: 1711, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 33.78 seconds
- Tokens Used: 2383 (Prompt: 2317, Completion: 66)
- Retrieved Subgraph Chunks: `Q26217865::c0`
- Synthesized Prediction:
  > "Based on the structured graph and context evidence, the gold medal in the women's 57 kg judo event at the 2016 Summer Olympics (held immediately before 2020) was won by **Rafaela Silva** [Q26217865::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 7.70 seconds
- Tokens Used: 4180 (Prompt: 4078, Completion: 102)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2016 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2016 Summer", "matched_event": "Judo at the 2016 Summer Olympics – Women's 57 kg", "gold_winner": "Rafaela Silva", "date_held": "8 August 2016"}`
  - Supporting Document Chunks: `Q26217865::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the Summer Olympics held immediately before 2020 were the **2016 Summer Olympics**. 

The gold medal in the women's 57 kg judo event (Event: *Judo at the 2016 Summer Olympics – Women's 57 kg*) was won by:

* **Rafaela Silva** (representing Brazil) [Q26217865::c0]"

### Question [7/100] — pub-007

- Query: "Who won the gold medal in the men's pole vault athletics event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Renaud Lavillenie`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 23.96 seconds
- Tokens Used: 5041 (Prompt: 4899, Completion: 142)
- Retrieved Context Chunks: `Q26208457::c0`
- Synthesized Prediction:
  > "Based on the provided context, the Summer Olympics held immediately before the 2016 Rio de Janeiro Games were the 2012 Summer Olympics in London. While the specific gold medalist's name for the 2012 men's pole vault is not explicitly stated in the 2012 excerpt, the 2016 context passage mentions that Renaud Lavillenie of France was the "reigning Olympic champion from 2012" and was unable to "successfully defend his 2012 gold" at the 2016 Games.

Answer: Renaud Lavillenie [Q26208457::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 31.60 seconds
- Tokens Used: 5050 (Prompt: 4987, Completion: 63)
- Retrieved Subgraph Chunks: `Q2000968::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's pole vault at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by **Renaud Lavillenie** of France [Q2000968::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 9.62 seconds
- Tokens Used: 10898 (Prompt: 10742, Completion: 156)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Athletics at the 2012 Summer Olympics – Men's pole vault", "gold_winner": "Renaud Lavillenie", "date_held": "8–10 August"}`
  - Supporting Document Chunks: `Q2000968::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting passages:

* **Gold Medalist:** Renaud Lavillenie [Q2000968::c0]
* **Specific Event Name:** Men's pole vault [Q2000968::c0]
* **Full Event Title:** Athletics at the 2012 Summer Olympics – Men's pole vault [Q2000968::c0]
* **Date Held:** 8–10 August 2012 [Q2000968::c0]
* **Citations:** [Q2000968::c0], temporal_precedes (2012 Summer)"

### Question [8/100] — pub-008

- Query: "According to the provided corpus, which sailing event at the 2000 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Sailing at the 2000 Summer Olympics – Soling`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 23.09 seconds
- Tokens Used: 5500 (Prompt: 5347, Completion: 153)
- Retrieved Context Chunks: `Q7400333::c0, Q7400328::c0, Q7400327::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the sailing event at the 2000 Summer Olympics with the highest number of competitors is the **Soling** event (described as the "Soling Three Person Keelboat" with 48 competitors and 16 teams/nations) [Q7400333::c0]. (By comparison, Finn had 25 competitors [Q7400328::c0], Europe had 27 competitors [Q7400327::c0], and Laser had at least 43 competitors listed [Q7400329::c1]).

Source: [Q7400333::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 29.81 seconds
- Tokens Used: 4572 (Prompt: 4521, Completion: 51)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence, the sailing event at the 2000 Summer Olympics with the highest number of competitors is **Sailing at the 2000 Summer Olympics – Soling**, which had 48 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.88 seconds
- Tokens Used: 1025 (Prompt: 908, Completion: 117)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Fleet/Match", "full_event_title": "Sailing at the 2000 Summer Olympics – Soling", "competitors": 48, "competition": "2000 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Fleet/Match", "full_event_title": "Sailing at the 2000 Summer Olympics – Soling", "competitors": 48, "competition": "2000 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400333::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the sailing event at the 2000 Summer Olympics with the highest number of competitors (48 competitors across 16 teams) was the **Fleet/Match** event, officially titled **Sailing at the 2000 Summer Olympics – Soling** [Q7400333::c0]. 

The gold medal-winning team (athletes) for this event was **Jesper Bank, Henrik Blakskjær, and Thomas Jacobsen** [Q7400333::c0]."

### Question [9/100] — pub-009

- Query: "How many nations competed in Sailing at the 2016 Summer Olympics – Women's RS:X?"
- Archetype: `lookup`
- Ground Truth: `26`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 29.32 seconds
- Tokens Used: 4331 (Prompt: 4286, Completion: 45)
- Retrieved Context Chunks: `Q26254891::c0`
- Synthesized Prediction:
  > "Based on the provided context, 26 nations competed in the Women's RS:X event at the 2016 Summer Olympics.

[Q26254891::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 40.09 seconds
- Tokens Used: 3413 (Prompt: 3370, Completion: 43)
- Retrieved Subgraph Chunks: `Q26254891::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 26 nations competed in Sailing at the 2016 Summer Olympics – Women's RS:X [Q26254891::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.09 seconds
- Tokens Used: 917 (Prompt: 848, Completion: 69)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Sailing at the 2016 Summer Olympics – Women's RS:X", "attributes": {"name": "Women's RS:X", "sport": "Sailing", "discipline": "", "gender": "", "competitors": 26, "nations": 26}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Sailing at the 2016 Summer Olympics – Women's RS:X", "attributes": {"name": "Women's RS:X", "sport": "Sailing", "discipline": "", "gender": "", "competitors": 26, "nations": 26}}`
  - Supporting Document Chunks: `Q26254891::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **26** nations competed in the Women's RS:X event at the 2016 Summer Olympics (Sailing at the 2016 Summer Olympics – Women's RS:X) [Q26254891::c0]."

### Question [10/100] — pub-010

- Query: "According to the provided corpus, how many cycling events at the 2000 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: `4`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 28.23 seconds
- Tokens Used: 5419 (Prompt: 5296, Completion: 123)
- Retrieved Context Chunks: `Q2774005::c0, Q5198393::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, none of the detailed cycling events list more than 30 competitors (for example, the Women's road time trial had 23 competitors [Q2774005::c0], and the Women's sprint had 12 [Q5198393::c0]). 

Answer: 0 (or none of the events mentioned have more than 30 competitors).

Citations: [Q2774005::c0], [Q5198393::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 62.26 seconds
- Tokens Used: 4805 (Prompt: 4637, Completion: 168)
- Retrieved Subgraph Chunks: `Q3001459::c0, Q2526348::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are 3 cycling events at the 2000 Summer Olympics that had more than 30 competitors:

1. **Men's individual road race**: 154 competitors ([Q3001459::c0])
2. **Men's road time trial**: 38 competitors ([Q2526348::c0])
3. **Men's cross-country**: 49 competitors (from the structured graph evidence: `(2000 Summer)-[:INCLUDES_EVENT]->(Cycling at the 2000 Summer Olympics – Men's cross-country [sport=Cycling, competitors=49])`)

Thus, exactly 3 cycling events had more than 30 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.48 seconds
- Tokens Used: 209 (Prompt: 179, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Cycling at the 2000 Summer Olympics – Men's cross-country (49 competitors)", "Cycling at the 2000 Summer Olympics – Women's individual road race (57 competitors)", "Cycling at the 2000 Summer Olympics – Men's individual road race (154 competitors)", "Cycling at the 2000 Summer Olympics – Men's road time trial (38 competitors)"], "competition": "2000 Summer", "threshold": 30, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Cycling at the 2000 Summer Olympics – Men's cross-country (49 competitors)", "Cycling at the 2000 Summer Olympics – Women's individual road race (57 competitors)", "Cycling at the 2000 Summer Olympics – Men's individual road race (154 competitors)", "Cycling at the 2000 Summer Olympics – Men's road time trial (38 competitors)"], "competition": "2000 Summer", "threshold": 30, "sport": "Cycling"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 cycling events at the 2000 Summer Olympics that had more than 30 competitors."

### Question [11/100] — pub-011

- Query: "Who won the gold medal in the event held at Richmond Olympic Oval on 14 February 2010?"
- Archetype: `multi_hop`
- Ground Truth: `Martina Sáblíková`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 53.74 seconds
- Tokens Used: 5619 (Prompt: 5558, Completion: 61)
- Retrieved Context Chunks: `Q580481::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal for the event held at the Richmond Olympic Oval on 14 February 2010 (Women's 3000 metres) was won by Martina Sáblíková.

[Q580481::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 12.24 seconds
- Tokens Used: 4512 (Prompt: 4507, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 52.24 seconds
- Tokens Used: 12712 (Prompt: 12595, Completion: 117)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Richmond Olympic Oval", "date_constraint": "14 february 2010", "year_filter": "2010", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 10}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Richmond Olympic Oval", "date_constraint": "14 february 2010", "year_filter": "2010", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 11}`
  - Supporting Document Chunks: `Q580481::c0`
- Synthesized Prediction:
  > "Based on the supporting context passages and Olympic records for events held at the Richmond Olympic Oval on **14 February 2010**:

* **Event:** Women's 3000 metres speed skating competition (Full title: *Speed skating at the 2010 Winter Olympics – Women's 3000 metres*) [Q580481::c0].
* **Gold Medal Winner:** Martina Sáblíková (representing the Czech Republic, CZE) [Q580481::c0]."

### Question [12/100] — pub-012

- Query: "According to the provided corpus, how many rowing events at the 2020 Summer Olympics had more than 36 competitors?"
- Archetype: `aggregation`
- Ground Truth: `6`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 19.10 seconds
- Tokens Used: 5793 (Prompt: 5702, Completion: 91)
- Retrieved Context Chunks: `Q62020028::c0, Q62020034::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are **2** rowing events at the 2020 Summer Olympics that had more than 36 competitors (specifically, the men's eight with 63 competitors and the women's eight with 63 competitors).

Sources:
- [Q62020028::c0]
- [Q62020034::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 24.61 seconds
- Tokens Used: 5811 (Prompt: 5714, Completion: 97)
- Retrieved Subgraph Chunks: `Q62020027::c0, Q62020028::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, there are **2** rowing events at the 2020 Summer Olympics that had more than 36 competitors:

1. **Men's coxless four** with **40 competitors** [Q62020027::c0]
2. **Men's eight** with **63 competitors** [Q62020028::c0]"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.21 seconds
- Tokens Used: 207 (Prompt: 177, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Rowing at the 2020 Summer Olympics – Men's eight (63 competitors)", "Rowing at the 2020 Summer Olympics – Women's eight (63 competitors)", "Rowing at the 2020 Summer Olympics – Men's quadruple sculls (40 competitors)", "Rowing at the 2020 Summer Olympics – Women's coxless four (40 competitors)", "Rowing at the 2020 Summer Olympics – Women's quadruple sculls (40 competitors)", "Rowing at the 2020 Summer Olympics – Men's coxless four (40 competitors)"], "competition": "2020 Summer", "threshold": 36, "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Rowing at the 2020 Summer Olympics – Men's eight (63 competitors)", "Rowing at the 2020 Summer Olympics – Women's eight (63 competitors)", "Rowing at the 2020 Summer Olympics – Men's quadruple sculls (40 competitors)", "Rowing at the 2020 Summer Olympics – Women's coxless four (40 competitors)", "Rowing at the 2020 Summer Olympics – Women's quadruple sculls (40 competitors)", "Rowing at the 2020 Summer Olympics – Men's coxless four (40 competitors)"], "competition": "2020 Summer", "threshold": 36, "sport": "Rowing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 6 rowing events at the 2020 Summer Olympics that had more than 36 competitors."

### Question [13/100] — pub-013

- Query: "Who won the gold medal in the women's 200 metre freestyle swimming event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Allison Schmitt`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 8.08 seconds
- Tokens Used: 7976 (Prompt: 7957, Completion: 19)
- Retrieved Context Chunks: `Q25932069::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q25932069::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 12.04 seconds
- Tokens Used: 6232 (Prompt: 6191, Completion: 41)
- Retrieved Subgraph Chunks: `Q2071152::c0`
- Synthesized Prediction:
  > "Allison Schmitt won the gold medal in the women's 200 metre freestyle swimming event at the 2012 Summer Olympics [Q2071152::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 9.49 seconds
- Tokens Used: 15209 (Prompt: 15081, Completion: 128)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Swimming at the 2012 Summer Olympics – Women's 200 metre freestyle", "gold_winner": "Allison Schmitt", "date_held": "July 30, 2012 (heats &semifinals)July 31, 2012 (final)"}`
  - Supporting Document Chunks: `Q2071152::c0`
- Synthesized Prediction:
  > "Based on the verified in-database graph facts and supporting context passages, the gold medal in the women's 200 metre freestyle swimming event at the 2012 Summer Olympics (the Summer Olympics held immediately before 2016) was won by **Allison Schmitt** [Q2071152::c0]. 

* **Event Name:** Women's 200 metre freestyle
* **Full Event Title:** Swimming at the 2012 Summer Olympics – Women's 200 metre freestyle [Q2071152::c0]"

### Question [14/100] — pub-014

- Query: "Who won the gold medal in the event held at Riocentro – Pavilion 4 on 11–19 August at the 2016 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Carolina Marín`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.98 seconds
- Tokens Used: 5787 (Prompt: 5781, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 27.36 seconds
- Tokens Used: 5090 (Prompt: 5025, Completion: 65)
- Retrieved Subgraph Chunks: `Q25301483::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the Badminton women's singles event held at Riocentro – Pavilion 4 from 11–19 August at the 2016 Summer Olympics was won by **Carolina Marín** [Q25301483::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.83 seconds
- Tokens Used: 2505 (Prompt: 2423, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Riocentro – Pavilion 4", "date_constraint": "11–19 august", "year_filter": "2016", "event": "Badminton at the 2016 Summer Olympics – Women's singles", "gold_winners": ["Carolina Marín"], "date_matched": true, "candidate_events_checked": 1}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Riocentro – Pavilion 4", "date_constraint": "11–19 august", "year_filter": "2016", "event": "Badminton at the 2016 Summer Olympics – Women's singles", "gold_winners": ["Carolina Marín"], "date_matched": true, "candidate_events_checked": 1}`
  - Supporting Document Chunks: `Q25301483::c0`
- Synthesized Prediction:
  > "**Carolina Marín** won the gold medal in the **Women's singles** event (full event title: *Badminton at the 2016 Summer Olympics – Women's singles*) held at Riocentro – Pavilion 4 from 11 to 19 August at the 2016 Summer Olympics [Q25301483::c0]."

### Question [15/100] — pub-015

- Query: "Who won the gold medal in the event held at London Velopark on 3 to 4 August at the 2012 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Dani KingLaura TrottJoanna Rowsell`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.41 seconds
- Tokens Used: 6489 (Prompt: 6484, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 50.86 seconds
- Tokens Used: 5812 (Prompt: 5726, Completion: 86)
- Retrieved Subgraph Chunks: `Q2297621::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the event held at the London Velopark from 2 to 3 August 2012 was the men's cycling team pursuit [Q2297621::c0], which was won by the British team consisting of **Ed Clancy, Geraint Thomas, Steven Burke, and Peter Kennaugh** [Q2297621::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 7.36 seconds
- Tokens Used: 1970 (Prompt: 1861, Completion: 109)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "London Velopark", "date_constraint": "3 to 4 august", "year_filter": "2012", "event": "Cycling at the 2012 Summer Olympics – Women's team pursuit", "gold_winners": ["Dani King", "Laura Trott", "Joanna Rowsell", "Dani King, Laura Trott, Joanna Rowsell"], "date_matched": true, "candidate_events_checked": 12}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "London Velopark", "date_constraint": "3 to 4 august", "year_filter": "2012", "event": "Cycling at the 2012 Summer Olympics – Women's team pursuit", "gold_winners": ["Dani King", "Laura Trott", "Joanna Rowsell", "Dani King, Laura Trott, Joanna Rowsell"], "date_matched": true, "candidate_events_checked": 12}`
  - Supporting Document Chunks: `Q2297633::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the **Women's team pursuit** (Cycling at the 2012 Summer Olympics – Women's team pursuit) held at the London Velopark from 3 to 4 August 2012 was won by the Great Britain team consisting of the following athletes:

* **Dani King**
* **Laura Trott**
* **Joanna Rowsell**

Sources: [Q2297633::c0]"

### Question [16/100] — pub-016

- Query: "Who won the gold medal in the men's sprint biathlon event at the Winter Olympics held immediately before 2022?"
- Archetype: `temporal`
- Ground Truth: `Arnd Peiffer`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 36.75 seconds
- Tokens Used: 9327 (Prompt: 9176, Completion: 151)
- Retrieved Context Chunks: `Q107861699::c0`
- Synthesized Prediction:
  > "Based on the provided context, the Winter Olympics held immediately before 2022 were the 2018 Winter Olympics (as referenced by the "prev: 2018" field in the infobox). However, the specific details or winner of the men's sprint event at the 2018 Winter Olympics are not mentioned in the text (the text only mentions that the 2018 champion, Arnd Peiffer, retired). 

Therefore, the exact winner of the gold medal in the men's sprint at the 2018 Winter Olympics cannot be determined from the provided passages.

Unknown based on provided context [Q107861699::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 10.54 seconds
- Tokens Used: 7985 (Prompt: 7924, Completion: 61)
- Retrieved Subgraph Chunks: `Q47105341::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's sprint biathlon event at the 2018 Winter Olympics (held immediately before the 2022 Winter Olympics) was won by Arnd Peiffer [Q47105341::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 11.44 seconds
- Tokens Used: 6399 (Prompt: 6264, Completion: 135)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "Biathlon at the 2018 Winter Olympics – Men's sprint", "gold_winner": "Arnd Peiffer", "date_held": "11 February 2018"}`
  - Supporting Document Chunks: `Q47105341::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the men's sprint biathlon event at the Winter Olympics held immediately before 2022 (the 2018 Winter Olympics in Pyeongchang) was won by **Arnd Peiffer** [Q47105341::c0]. 

* **Specific Event Name:** Men's sprint [Q47105341::c0]
* **Full Event Title:** Biathlon at the 2018 Winter Olympics – Men's sprint [Q47105341::c0]"

### Question [17/100] — pub-017

- Query: "Who won the gold medal in the event held at Royal Artillery Barracks on 28 July 2012?"
- Archetype: `multi_hop`
- Ground Truth: `Yi Siling`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 22.01 seconds
- Tokens Used: 6090 (Prompt: 6084, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 11.06 seconds
- Tokens Used: 5334 (Prompt: 5329, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 7.04 seconds
- Tokens Used: 3806 (Prompt: 3730, Completion: 76)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Royal Artillery Barracks", "date_constraint": "28 july 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics – Women's 10 metre air rifle", "gold_winners": ["Yi Siling"], "date_matched": true, "candidate_events_checked": 12}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Royal Artillery Barracks", "date_constraint": "28 july 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics – Women's 10 metre air rifle", "gold_winners": ["Yi Siling"], "date_matched": true, "candidate_events_checked": 12}`
  - Supporting Document Chunks: `Q1137721::c0`
- Synthesized Prediction:
  > "**Yi Siling** won the gold medal in the **Women's 10 metre air rifle** event (**Shooting at the 2012 Summer Olympics – Women's 10 metre air rifle**) held at the Royal Artillery Barracks on 28 July 2012 [Q1137721::c0]."

### Question [18/100] — pub-018

- Query: "Who won the gold medal in the men's freestyle 82 kg wrestling event at the Summer Olympics held immediately before 1996?"
- Archetype: `temporal`
- Ground Truth: `Kevin Jackson`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 18.96 seconds
- Tokens Used: 5031 (Prompt: 5026, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 11.59 seconds
- Tokens Used: 5275 (Prompt: 5212, Completion: 63)
- Retrieved Subgraph Chunks: `Q3498597::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's freestyle 82 kg wrestling event at the 1992 Summer Olympics (held immediately before the 1996 Summer Olympics) was won by **Kevin Jackson** [Q3498597::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 12.18 seconds
- Tokens Used: 12146 (Prompt: 12034, Completion: 112)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "1992 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "1992 Summer", "matched_event": "Wrestling at the 1992 Summer Olympics – Men's freestyle 82 kg", "gold_winner": "Kevin Jackson", "date_held": ""}`
  - Supporting Document Chunks: `Q3498597::c0`
- Synthesized Prediction:
  > "The gold medal in the men's freestyle 82 kg wrestling event at the 1992 Summer Olympics (held immediately before the 1996 Summer Olympics) was won by **Kevin Jackson** [Q3498597::c0]. 

* **Specific Event Name:** Men's freestyle 82 kg
* **Full Event Title:** Wrestling at the 1992 Summer Olympics – Men's freestyle 82 kg [Q3498597::c0]"

### Question [19/100] — pub-019

- Query: "According to the provided corpus, how many fencing events at the 1988 Summer Olympics had more than 68 competitors?"
- Archetype: `aggregation`
- Ground Truth: `3`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 11.01 seconds
- Tokens Used: 5797 (Prompt: 5651, Completion: 146)
- Retrieved Context Chunks: `Q5443138::c0, Q5443140::c0, Q5443142::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 3 fencing events at the 1988 Summer Olympics that had more than 68 competitors:

1. **Men's team foil** with 76 competitors ([Q5443138::c0])
2. **Men's team épée** with 85 competitors ([Q5443140::c0])
3. **Men's épée** (individual) with 79 competitors ([Q5443142::c0])

(Note: Men's team sabre had 53 competitors and Men's sabre had 40 competitors)."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 39.58 seconds
- Tokens Used: 5014 (Prompt: 4920, Completion: 94)
- Retrieved Subgraph Chunks: `Q5443138::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the fencing events at the 1988 Summer Olympics with more than 68 competitors are:

1. **Men's team foil** with 76 competitors ([Q5443138::c0])
2. **Men's team épée** with 85 competitors (Structured Graph Evidence)

Therefore, there were **2** fencing events with more than 68 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 9.69 seconds
- Tokens Used: 212 (Prompt: 181, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Fencing at the 1988 Summer Olympics – Men's team épée (85 competitors)", "Fencing at the 1988 Summer Olympics – Men's épée (79 competitors)", "Fencing at the 1988 Summer Olympics – Men's team foil (76 competitors)"], "competition": "1988 Summer", "threshold": 68, "sport": "Fencing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Fencing at the 1988 Summer Olympics – Men's team épée (85 competitors)", "Fencing at the 1988 Summer Olympics – Men's épée (79 competitors)", "Fencing at the 1988 Summer Olympics – Men's team foil (76 competitors)"], "competition": "1988 Summer", "threshold": 68, "sport": "Fencing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 fencing events at the 1988 Summer Olympics that had more than 68 competitors."

### Question [20/100] — pub-020

- Query: "According to the provided corpus, how many alpine skiing events at the 2014 Winter Olympics had more than 63 competitors?"
- Archetype: `aggregation`
- Ground Truth: `4`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 39.64 seconds
- Tokens Used: 7887 (Prompt: 7673, Completion: 214)
- Retrieved Context Chunks: `Q15055009::c1, Q15055013::c0, Q15054997::c0`
- Synthesized Prediction:
  > "Based on the provided context, the alpine skiing events at the 2014 Winter Olympics with their competitor counts mentioned are:
- Men's combined ([Q15055009::c1]): competitor count is not explicitly stated in a summary, but individual entries listed go up to 50.
- Men's super-G ([Q15055013::c0]): 63 competitors.
- Men's downhill ([Q15054997::c0]): 49 competitors.
- Women's giant slalom ([Q15054999::c1]): entries list up to 90 competitors (e.g., bib 90 for Ornella Oettl Reyes). 

Therefore, **1** alpine skiing event (the women's giant slalom) had more than 63 competitors based on the provided corpus.

Citations: [Q15054999::c1]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 53.66 seconds
- Tokens Used: 6913 (Prompt: 6824, Completion: 89)
- Retrieved Subgraph Chunks: `Q15055004::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the number of alpine skiing events at the 2014 Winter Olympics with more than 63 competitors is **2**. 

These events are:
1. **Men's giant slalom** with 109 competitors.
2. **Men's slalom** with 115 competitors ([Q15055004::c0])."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.12 seconds
- Tokens Used: 214 (Prompt: 182, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Alpine skiing at the 2014 Winter Olympics – Men's giant slalom (109 competitors)", "Alpine skiing at the 2014 Winter Olympics – Men's slalom (115 competitors)", "Alpine skiing at the 2014 Winter Olympics – Women's giant slalom (90 competitors)", "Alpine skiing at the 2014 Winter Olympics – Women's slalom (85 competitors)"], "competition": "2014 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Alpine skiing at the 2014 Winter Olympics – Men's giant slalom (109 competitors)", "Alpine skiing at the 2014 Winter Olympics – Men's slalom (115 competitors)", "Alpine skiing at the 2014 Winter Olympics – Women's giant slalom (90 competitors)", "Alpine skiing at the 2014 Winter Olympics – Women's slalom (85 competitors)"], "competition": "2014 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database result, there were 4 alpine skiing events at the 2014 Winter Olympics that had more than 63 competitors."

### Question [21/100] — pub-021

- Query: "According to the provided corpus, which alpine skiing event at the 1988 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Alpine skiing at the 1988 Winter Olympics – Men's giant slalom`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 48.29 seconds
- Tokens Used: 6806 (Prompt: 6705, Completion: 101)
- Retrieved Context Chunks: `Q1005744::c0, Q1005571::c0, Q1222641::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the alpine skiing event with the highest number of competitors was the **Men's super-G** with 94 competitors (compared to 51 competitors in the Men's downhill and 46 competitors in the Women's Super G). 

Sources: [Q1005744::c0], [Q1005571::c0], [Q1222641::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 151.92 seconds
- Tokens Used: 7858 (Prompt: 7768, Completion: 90)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the alpine skiing event at the 1988 Winter Olympics with the highest number of competitors was the **Men's giant slalom** with **117 competitors** [1988 Winter-[:INCLUDES_EVENT]->(Alpine skiing at the 1988 Winter Olympics – Men's giant slalom [sport=Alpine skiing, competitors=117])]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.47 seconds
- Tokens Used: 3085 (Prompt: 3011, Completion: 74)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's giant slalom", "full_event_title": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "competitors": 117, "competition": "1988 Winter", "sport": ""}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's giant slalom", "full_event_title": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "competitors": 117, "competition": "1988 Winter", "sport": ""}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified graph facts, the alpine skiing event at the 1988 Winter Olympics with the highest number of competitors was the **Men's giant slalom** (full event title: *Alpine skiing at the 1992 Winter Olympics – Men's giant slalom*), featuring **117** competitors [gsql_heapaccum]."

### Question [22/100] — pub-022

- Query: "Who won the gold medal in the event held at Beijing Science and TechnologyUniversity Gymnasium on August 12, 2008?"
- Archetype: `multi_hop`
- Ground Truth: `Ayumi Tanimoto`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 40.70 seconds
- Tokens Used: 4836 (Prompt: 4768, Completion: 68)
- Retrieved Context Chunks: `Q1193975::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal for the event held at the Beijing Science and Technology University Gymnasium on August 12, 2008 (the women's 63 kg judo tournament) was won by Ayumi Tanimoto.

[Q1193975::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 21.96 seconds
- Tokens Used: 3343 (Prompt: 3275, Completion: 68)
- Retrieved Subgraph Chunks: `Q1193975::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Beijing Science and Technology University Gymnasium on August 12, 2008 (the Women's 63 kg judo event) was won by **Ayumi Tanimoto** [Q1193975::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 33.75 seconds
- Tokens Used: 12982 (Prompt: 12898, Completion: 84)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Beijing Science and TechnologyUniversity Gymnasium", "date_constraint": "august 12, 2008", "year_filter": "2008", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 5}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Beijing Science and TechnologyUniversity Gymnasium", "date_constraint": "august 12, 2008", "year_filter": "2008", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 5}`
  - Supporting Document Chunks: `Q1193975::c0`
- Synthesized Prediction:
  > "Based on the 2008 Summer Olympics events held at the Beijing Science and Technology University Gymnasium on August 12, 2008, the gold medal was won by **Ayumi Tanimoto** representing Japan in the event **Judo at the 2008 Summer Olympics – Women's 63 kg** [Q1193975::c0]."

### Question [23/100] — pub-023

- Query: "Who won the gold medal in the event held at Estadi Olímpic Lluís Companys, Barcelona on August 9 at the 1992 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Hwang Young-Cho`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 43.10 seconds
- Tokens Used: 8307 (Prompt: 8254, Completion: 53)
- Retrieved Context Chunks: `Q1407627::c0`
- Synthesized Prediction:
  > "Hwang Young-Cho won the gold medal in the men's marathon held on August 9, 1992, at the Estadi Olímpic Lluís Companys in Barcelona [Q1407627::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 32.07 seconds
- Tokens Used: 6559 (Prompt: 6554, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.47 seconds
- Tokens Used: 2797 (Prompt: 2706, Completion: 91)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Estadi Olímpic Lluís Companys, Barcelona", "date_constraint": "august 9", "year_filter": "1992", "event": "Athletics at the 1992 Summer Olympics – Men's marathon", "gold_winners": ["Hwang Young-Cho"], "date_matched": true, "candidate_events_checked": 2}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Estadi Olímpic Lluís Companys, Barcelona", "date_constraint": "august 9", "year_filter": "1992", "event": "Athletics at the 1992 Summer Olympics – Men's marathon", "gold_winners": ["Hwang Young-Cho"], "date_matched": true, "candidate_events_checked": 2}`
  - Supporting Document Chunks: `Q1407627::c0`
- Synthesized Prediction:
  > "Based on the 1992 Summer Olympics events held at the Estadi Olímpic Lluís Companys in Barcelona on August 9, the gold medal in the **Men's marathon** (full event title: *Athletics at the 1992 Summer Olympics – Men's marathon*) was won by **Hwang Young-Cho** of South Korea [Q1407627::c0]."

### Question [24/100] — pub-024

- Query: "According to the provided corpus, how many biathlon events at the 2002 Winter Olympics had more than 74 competitors?"
- Archetype: `aggregation`
- Ground Truth: `3`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 57.77 seconds
- Tokens Used: 8586 (Prompt: 8432, Completion: 154)
- Retrieved Context Chunks: `Q1005108::c0, Q1004918::c1, Q256759::c1`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 biathlon events at the 2002 Winter Olympics that had more than 74 competitors (specifically, the Men's 4 × 7.5 kilometre biathlon relay with 76 competitors [Q1005108::c0], and the Men's sprint where starting bib numbers/competitors reached up to at least 86 [Q1004918::c1, Q256759::c1]). 

Sources: [Q1005108::c0], [Q1004918::c1], [Q256759::c1]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 44.24 seconds
- Tokens Used: 6065 (Prompt: 5973, Completion: 92)
- Retrieved Subgraph Chunks: `Q256759::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, there are **3** biathlon events at the 2002 Winter Olympics that had more than 74 competitors:

1. **Men's individual** with 87 competitors ([Q256759::c0])
2. **Men's sprint** with 87 competitors
3. **Men's relay** with 76 competitors"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.56 seconds
- Tokens Used: 212 (Prompt: 180, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Biathlon at the 2002 Winter Olympics – Men's individual (87 competitors)", "Biathlon at the 2002 Winter Olympics – Men's relay (76 competitors)", "Biathlon at the 2002 Winter Olympics – Men's sprint (87 competitors)"], "competition": "2002 Winter", "threshold": 74, "sport": "Biathlon"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Biathlon at the 2002 Winter Olympics – Men's individual (87 competitors)", "Biathlon at the 2002 Winter Olympics – Men's relay (76 competitors)", "Biathlon at the 2002 Winter Olympics – Men's sprint (87 competitors)"], "competition": "2002 Winter", "threshold": 74, "sport": "Biathlon"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database result, there were 3 biathlon events at the 2002 Winter Olympics that had more than 74 competitors."

### Question [25/100] — pub-025

- Query: "How many nations competed in Judo at the 2016 Summer Olympics – Women's 57 kg?"
- Archetype: `lookup`
- Ground Truth: `23`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 48.98 seconds
- Tokens Used: 2194 (Prompt: 2150, Completion: 44)
- Retrieved Context Chunks: `Q26217865::c0`
- Synthesized Prediction:
  > "Based on the provided context, 23 nations competed in Judo at the 2016 Summer Olympics – Women's 57 kg [Q26217865::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 87.34 seconds
- Tokens Used: 2355 (Prompt: 2311, Completion: 44)
- Retrieved Subgraph Chunks: `Q26217865::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 23 nations competed in Judo at the 2016 Summer Olympics – Women's 57 kg [Q26217865::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 0.99 seconds
- Tokens Used: 752 (Prompt: 713, Completion: 39)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Judo at the 2016 Summer Olympics – Women's 57 kg", "attributes": {"name": "Women's 57 kg", "sport": "Judo", "discipline": "", "gender": "", "competitors": 23, "nations": 23}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Judo at the 2016 Summer Olympics – Women's 57 kg", "attributes": {"name": "Women's 57 kg", "sport": "Judo", "discipline": "", "gender": "", "competitors": 23, "nations": 23}}`
  - Supporting Document Chunks: `Q26217865::c0`
- Synthesized Prediction:
  > "23 nations competed in the Judo at the 2016 Summer Olympics – Women's 57 kg event [Q26217865::c0]."

### Question [26/100] — pub-026

- Query: "Who won the gold medal in the men's cross-country cycling event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Jaroslav Kulhavý`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 39.60 seconds
- Tokens Used: 7329 (Prompt: 7249, Completion: 80)
- Retrieved Context Chunks: `Q25476845::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medalist for the men's cross-country cycling event at the 2012 Summer Olympics (held immediately before 2016) is not explicitly named; the text only indicates "prev: 2012" in the infobox. 

Chunk ID: [Q25476845::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 51.60 seconds
- Tokens Used: 4359 (Prompt: 4299, Completion: 60)
- Retrieved Subgraph Chunks: `Q2036655::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, Jaroslav Kulhavý won the gold medal in the men's cross-country cycling event at the 2012 Summer Olympics, which were held immediately before the 2016 Games [Q2036655::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 13.08 seconds
- Tokens Used: 12019 (Prompt: 11859, Completion: 160)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Cycling at the 2012 Summer Olympics – Men's cross-country", "gold_winner": "Jaroslav Kulhavý", "date_held": "12 August"}`
  - Supporting Document Chunks: `Q2036655::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting documentation:

* **Gold Medalist:** Jaroslav Kulhavý (representing the Czech Republic) [Q2036655::c0]
* **Event Name:** Men's cross-country cycling [Q2036655::c0]
* **Full Event Title:** Cycling at the 2012 Summer Olympics – Men's cross-country [Q2036655::c0]
* **Competition Date:** 12 August 2012 [Q2036655::c0]
* **Games:** 2012 Summer Olympics (London) [Q2036655::c0]"

### Question [27/100] — pub-027

- Query: "According to the provided corpus, how many fencing events at the 2008 Summer Olympics had more than 32 competitors?"
- Archetype: `aggregation`
- Ground Truth: `4`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 13.62 seconds
- Tokens Used: 3717 (Prompt: 3424, Completion: 293)
- Retrieved Context Chunks: `Q2726750::c0, Q2726820::c0, Q2726788::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, none of the fencing events at the 2008 Summer Olympics had more than 32 competitors. The competitors for the mentioned events are:
- Men's team épée: 32 competitors ([Q2726750::c0])
- Women's team foil: 29 competitors ([Q2726820::c0])
- Men's team sabre: 25 competitors ([Q2726788::c0])
- Women's team sabre: 30 competitors ([Q658704::c0])
- Men's épée: 41 competitors (Note: The text in [Q2570052::c0] lists "41000000" due to a typo in the source data, but states there were "41 competitors"). 

Therefore, exactly one event (Men's épée with 41 competitors) had more than 32 competitors.

Sources: [Q2726750::c0], [Q2726820::c0], [Q2726788::c0], [Q658704::c0], [Q2570052::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 11.54 seconds
- Tokens Used: 5019 (Prompt: 4709, Completion: 310)
- Retrieved Subgraph Chunks: `Q2570149::c0, Q2570158::c0, Q2570052::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are **3** fencing events at the 2008 Summer Olympics that had more than 32 competitors:

1. **Fencing at the 2008 Summer Olympics – Men's sabre**: 40 competitors ([Q2570149::c0])
2. **Fencing at the 2008 Summer Olympics – Men's team épée**: 25 competitors? No, let's look at the structured graph evidence and text:
   - Men's foil: 26 competitors ([Q2570158::c0])
   - Men's sabre: 40 competitors ([Q2570149::c0])
   - Men's team sabre: 25 competitors (from graph)
   - Men's team épée: 32 competitors (from graph)
   - Men's épée: 41 competitors ([Q2570052::c0])

Therefore, the events with *more than 32* competitors are:
1. Men's sabre (40 competitors) ([Q2570149::c0])
2. Men's épée (41 competitors) ([Q2570052::c0])

Thus, exactly **2** fencing events had more than 32 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 3.96 seconds
- Tokens Used: 217 (Prompt: 186, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Fencing at the 2008 Summer Olympics – Men's épée (41000000 competitors)", "Fencing at the 2008 Summer Olympics – Women's sabre (39 competitors)", "Fencing at the 2008 Summer Olympics – Women's foil (41 competitors)", "Fencing at the 2008 Summer Olympics – Men's sabre (40 competitors)"], "competition": "2008 Summer", "threshold": 32, "sport": "Fencing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Fencing at the 2008 Summer Olympics – Men's épée (41000000 competitors)", "Fencing at the 2008 Summer Olympics – Women's sabre (39 competitors)", "Fencing at the 2008 Summer Olympics – Women's foil (41 competitors)", "Fencing at the 2008 Summer Olympics – Men's sabre (40 competitors)"], "competition": "2008 Summer", "threshold": 32, "sport": "Fencing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database result, there were 4 fencing events at the 2008 Summer Olympics that had more than 32 competitors."

### Question [28/100] — pub-028

- Query: "Who won the gold medal in the event held at Olympic Aquatic Centre on August 14, 2004 (heats & final)?"
- Archetype: `multi_hop`
- Ground Truth: `Michael Phelps`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 7.43 seconds
- Tokens Used: 8494 (Prompt: 8488, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 14.45 seconds
- Tokens Used: 6323 (Prompt: 6239, Completion: 84)
- Retrieved Subgraph Chunks: `Q3879574::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and context passages, the exact date of August 14, 2004, is associated with the heats and semifinals of the Men's 200 metre individual medley (with the final on August 19, 2004), where **Michael Phelps** won the gold medal [Q3879574::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 50.26 seconds
- Tokens Used: 20904 (Prompt: 20629, Completion: 275)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Olympic Aquatic Centre", "date_constraint": "august 14, 2004", "year_filter": "2004", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 8}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Aquatic Centre", "date_constraint": "august 14, 2004", "year_filter": "2004", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 9}`
  - Supporting Document Chunks: `Q114105::c0, Q599322::c0, Q1141034::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context passages, the events held at the Olympic Aquatic Centre on August 14, 2004 (heats & final) and their respective gold medal winners are:

1. **Men's 400 metre individual medley** (Full title: *Swimming at the 2004 Summer Olympics – Men's 400 metre individual medley*)
   * **Gold Medal Winner:** Michael Phelps (USA)
   * **Source/Chunk ID:** [Q114105::c0]

2. **Men's 400 metre freestyle** (Full title: *Swimming at the 2004 Summer Olympics – Men's 400 metre freestyle*)
   * **Gold Medal Winner:** Ian Thorpe (AUS)
   * **Source/Chunk ID:** [Q599322::c0]

3. **Women's 400 metre individual medley** (Full title: *Swimming at the 2004 Summer Olympics – Women's 400 metre individual medley*)
   * **Gold Medal Winner:** Yana Klochkova (UKR)
   * **Source/Chunk ID:** [Q1141034::c0]"

### Question [29/100] — pub-029

- Query: "How many nations competed in Shooting at the 2012 Summer Olympics – Men's 50 metre rifle three positions?"
- Archetype: `lookup`
- Ground Truth: `28`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 28.63 seconds
- Tokens Used: 7146 (Prompt: 7108, Completion: 38)
- Retrieved Context Chunks: `Q334901::c0`
- Synthesized Prediction:
  > "28 nations competed in the Men's 50 metre rifle three positions event at the 2012 Summer Olympics [Q334901::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 21.32 seconds
- Tokens Used: 5446 (Prompt: 5400, Completion: 46)
- Retrieved Subgraph Chunks: `Q334901::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, **28** nations competed in the Men's 50 metre rifle three positions event at the 2012 Summer Olympics [Q334901::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.06 seconds
- Tokens Used: 2038 (Prompt: 1986, Completion: 52)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Shooting at the 2012 Summer Olympics – Men's 50 metre rifle three positions", "attributes": {"name": "Men's 50 metre rifle three positions", "sport": "Shooting", "discipline": "", "gender": "", "competitors": 41, "nations": 28}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Shooting at the 2012 Summer Olympics – Men's 50 metre rifle three positions", "attributes": {"name": "Men's 50 metre rifle three positions", "sport": "Shooting", "discipline": "", "gender": "", "competitors": 41, "nations": 28}}`
  - Supporting Document Chunks: `Q334901::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and context passages, **28** nations competed in the Shooting at the 2012 Summer Olympics – Men's 50 metre rifle three positions event [Q334901::c0]."

### Question [30/100] — pub-030

- Query: "Who won the gold medal in the event held at Carioca Arena 3 on 6 August 2016?"
- Archetype: `multi_hop`
- Ground Truth: `Emese Szász`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 16.71 seconds
- Tokens Used: 4774 (Prompt: 4714, Completion: 60)
- Retrieved Context Chunks: `Q25386274::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the event held at Carioca Arena 3 on 6 August 2016 (Women's épée) was won by Emese Szász.

Source: [Q25386274::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 10.75 seconds
- Tokens Used: 5308 (Prompt: 5185, Completion: 123)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, the fencing events held at Carioca Arena 3 took place on 7 August 2016 (Men's foil, Men's team foil), 9 August 2016 (Men's épée), 10 August 2016 (Men's sabre), 12 August 2016, and 14 August 2016. There is no mention of an event held on 6 August 2016. 

Unknown based on provided context."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 14.46 seconds
- Tokens Used: 1097 (Prompt: 1021, Completion: 76)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Carioca Arena 3", "date_constraint": "6 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics – Women's épée", "gold_winners": ["Emese Szász"], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Carioca Arena 3", "date_constraint": "6 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics – Women's épée", "gold_winners": ["Emese Szász"], "date_matched": true, "candidate_events_checked": 17}`
  - Supporting Document Chunks: `Q25386274::c0`
- Synthesized Prediction:
  > "Emese Szász won the gold medal in the event held at Carioca Arena 3 on 6 August 2016, which was the **Women's épée** event (full title: **Fencing at the 2016 Summer Olympics – Women's épée**) [Q25386274::c0]."

### Question [31/100] — pub-031

- Query: "Who won the gold medal in the event held at Nikaia Olympic Weightlifting Hall on 24 August 2004?"
- Archetype: `multi_hop`
- Ground Truth: `Dmitry Berestov`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 48.24 seconds
- Tokens Used: 6408 (Prompt: 6402, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.10 seconds
- Tokens Used: 6401 (Prompt: 6327, Completion: 74)
- Retrieved Subgraph Chunks: `Q1750583::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Nikaia Olympic Weightlifting Hall on 24 August 2004 (Weightlifting at the 2004 Summer Olympics – Men's 105 kg) was won by Dmitry Berestov [Q1750583::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 9.11 seconds
- Tokens Used: 2363 (Prompt: 2284, Completion: 79)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Nikaia Olympic Weightlifting Hall", "date_constraint": "24 august 2004", "year_filter": "2004", "event": "Weightlifting at the 2004 Summer Olympics – Men's 105 kg", "gold_winners": ["Dmitry Berestov"], "date_matched": true, "candidate_events_checked": 15}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Nikaia Olympic Weightlifting Hall", "date_constraint": "24 august 2004", "year_filter": "2004", "event": "Weightlifting at the 2004 Summer Olympics – Men's 105 kg", "gold_winners": ["Dmitry Berestov"], "date_matched": true, "candidate_events_checked": 15}`
  - Supporting Document Chunks: `Q1750583::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting documentation, **Dmitry Berestov** won the gold medal in the Men's 105 kg weightlifting event at the 2004 Summer Olympics (held at the Nikaia Olympic Weightlifting Hall on 24 August 2004) [Q1750583::c0]."

### Question [32/100] — pub-032

- Query: "How many nations competed in Gymnastics at the 2016 Summer Olympics – Men's horizontal bar?"
- Archetype: `lookup`
- Ground Truth: `34`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 7.44 seconds
- Tokens Used: 6021 (Prompt: 5986, Completion: 35)
- Retrieved Context Chunks: `Q26233795::c0`
- Synthesized Prediction:
  > "34 nations competed in the men's horizontal bar event at the 2016 Summer Olympics [Q26233795::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.36 seconds
- Tokens Used: 5978 (Prompt: 5936, Completion: 42)
- Retrieved Subgraph Chunks: `Q26233795::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 34 nations competed in the men's horizontal bar event at the 2016 Summer Olympics [Q26233795::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.33 seconds
- Tokens Used: 1580 (Prompt: 1531, Completion: 49)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Gymnastics at the 2016 Summer Olympics – Men's horizontal bar", "attributes": {"name": "Men's horizontal bar", "sport": "Gymnastics", "discipline": "", "gender": "", "competitors": 71, "nations": 34}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Gymnastics at the 2016 Summer Olympics – Men's horizontal bar", "attributes": {"name": "Men's horizontal bar", "sport": "Gymnastics", "discipline": "", "gender": "", "competitors": 71, "nations": 34}}`
  - Supporting Document Chunks: `Q26233795::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **34** nations competed in Gymnastics at the 2016 Summer Olympics – Men's horizontal bar [Q26233795::c0]."

### Question [33/100] — pub-033

- Query: "According to the provided corpus, how many judo events at the 2004 Summer Olympics had more than 32 competitors?"
- Archetype: `aggregation`
- Ground Truth: `4`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.42 seconds
- Tokens Used: 3859 (Prompt: 3771, Completion: 88)
- Retrieved Context Chunks: `Q3811006::c0, Q3811010::c0`
- Synthesized Prediction:
  > "Based on the provided context, there are **2** judo events at the 2004 Summer Olympics that had more than 32 competitors:
1. Men's 60 kg (33 competitors) [Q3811006::c0]
2. Men's 73 kg (34 competitors) [Q3811010::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 6.05 seconds
- Tokens Used: 3232 (Prompt: 3133, Completion: 99)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, there are **3** judo events at the 2004 Summer Olympics that had more than 32 competitors (specifically, 33 competitors each):

1. **Men's +100 kg** (33 competitors)
2. **Men's 100 kg** (33 competitors)
3. **Men's 60 kg** (33 competitors)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.62 seconds
- Tokens Used: 213 (Prompt: 182, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Judo at the 2004 Summer Olympics – Men's 100 kg (33 competitors)", "Judo at the 2004 Summer Olympics – Men's 60 kg (33 competitors)", "Judo at the 2004 Summer Olympics – Men's 73 kg (34 competitors)", "Judo at the 2004 Summer Olympics – Men's +100 kg (33 competitors)"], "competition": "2004 Summer", "threshold": 32, "sport": "Judo"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Judo at the 2004 Summer Olympics – Men's 100 kg (33 competitors)", "Judo at the 2004 Summer Olympics – Men's 60 kg (33 competitors)", "Judo at the 2004 Summer Olympics – Men's 73 kg (34 competitors)", "Judo at the 2004 Summer Olympics – Men's +100 kg (33 competitors)"], "competition": "2004 Summer", "threshold": 32, "sport": "Judo"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 judo events at the 2004 Summer Olympics that had more than 32 competitors."

### Question [34/100] — pub-034

- Query: "How many nations competed in Figure skating at the 2010 Winter Olympics – Women's singles?"
- Archetype: `lookup`
- Ground Truth: `23`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 7.01 seconds
- Tokens Used: 9056 (Prompt: 9013, Completion: 43)
- Retrieved Context Chunks: `Q916735::c0`
- Synthesized Prediction:
  > "Based on the provided context, 23 nations competed in the women's singles figure skating event at the 2010 Winter Olympics.

[Q916735::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.04 seconds
- Tokens Used: 5064 (Prompt: 5023, Completion: 41)
- Retrieved Subgraph Chunks: `Q916735::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 23 nations competed in the Figure skating at the 2010 Winter Olympics – Women's singles [Q916735::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 4.58 seconds
- Tokens Used: 2712 (Prompt: 2644, Completion: 68)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Figure skating at the 2010 Winter Olympics – Women's singles", "attributes": {"name": "Women's singles", "sport": "Figure skating", "discipline": "", "gender": "", "competitors": 30, "nations": 23}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Figure skating at the 2010 Winter Olympics – Women's singles", "attributes": {"name": "Women's singles", "sport": "Figure skating", "discipline": "", "gender": "", "competitors": 30, "nations": 23}}`
  - Supporting Document Chunks: `Q916735::c0`
- Synthesized Prediction:
  > "Based on the verified database facts and supporting context, **23 nations** competed in the Women's singles figure skating event at the 2010 Winter Olympics (event title: *Figure skating at the 2010 Winter Olympics – Women's singles*) [Q916735::c0]."

### Question [35/100] — pub-035

- Query: "How many nations competed in Shooting at the 1996 Summer Olympics – Men's 50 metre rifle three positions?"
- Archetype: `lookup`
- Ground Truth: `30`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 6.07 seconds
- Tokens Used: 6715 (Prompt: 6669, Completion: 46)
- Retrieved Context Chunks: `Q7500793::c0`
- Synthesized Prediction:
  > "Based on the provided context, 30 nations competed in the Men's 50 metre rifle three positions event at the 1996 Summer Olympics [Q7500793::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.32 seconds
- Tokens Used: 5661 (Prompt: 5614, Completion: 47)
- Retrieved Subgraph Chunks: `Q7500793::c0`
- Synthesized Prediction:
  > "Based on the provided context, **30** nations competed in the Men's 50 metre rifle three positions event at the 1996 Summer Olympics [Q7500793::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.76 seconds
- Tokens Used: 2150 (Prompt: 2101, Completion: 49)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Shooting at the 1996 Summer Olympics – Men's 50 metre rifle three positions", "attributes": {"name": "Men's 50 metre rifle three positions", "sport": "Shooting", "discipline": "", "gender": "", "competitors": 45, "nations": 30}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Shooting at the 1996 Summer Olympics – Men's 50 metre rifle three positions", "attributes": {"name": "Men's 50 metre rifle three positions", "sport": "Shooting", "discipline": "", "gender": "", "competitors": 45, "nations": 30}}`
  - Supporting Document Chunks: `Q7500793::c0`
- Synthesized Prediction:
  > "Based on the verified database and context, **30** nations competed in Shooting at the 1996 Summer Olympics – Men's 50 metre rifle three positions [Q7500793::c0]."

### Question [36/100] — pub-036

- Query: "Who won the gold medal in the men's light flyweight boxing event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Zou Shiming`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 203.01 seconds
- Tokens Used: 2977 (Prompt: 2748, Completion: 229)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.35 seconds
- Tokens Used: 2940 (Prompt: 2880, Completion: 60)
- Retrieved Subgraph Chunks: `Q2000524::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's light flyweight boxing event at the 2012 Summer Olympics (held immediately before 2016) was won by **Zou Shiming** [Q2000524::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 10.03 seconds
- Tokens Used: 5518 (Prompt: 5395, Completion: 123)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Boxing at the 2012 Summer Olympics – Men's light flyweight", "gold_winner": "Zou Shiming", "date_held": "31 July to 12 August 2012"}`
  - Supporting Document Chunks: `Q2000524::c0`
- Synthesized Prediction:
  > "The gold medal in the men's light flyweight boxing event at the 2012 Summer Olympics (the Summer Olympics held immediately before the 2016 Games) was won by **Zou Shiming** [Q2000524::c0].

* **Specific Event Name:** Men's light flyweight boxing [Q2000524::c0]
* **Full Event Title:** Boxing at the 2012 Summer Olympics – Men's light flyweight [Q2000524::c0]"

### Question [37/100] — pub-037

- Query: "According to the provided corpus, which shooting event at the 2008 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Shooting at the 2008 Summer Olympics – Men's 50 metre rifle prone`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.56 seconds
- Tokens Used: 8028 (Prompt: 7822, Completion: 206)
- Retrieved Context Chunks: `Q1005423::c0, Q1204722::c0, Q1346374::c0`
- Synthesized Prediction:
  > "To determine which shooting event at the 2008 Summer Olympics had the highest number of competitors, we can compare the competitor counts listed in the infoboxes of each provided event:

* **Men's 25 metre rapid fire pistol:** 19 competitors ([Q1005423::c0])
* **Women's 10 metre air rifle:** 47 competitors ([Q1204722::c0])
* **Men's 50 metre rifle three positions:** 49 competitors ([Q1346374::c0])
* **Women's 25 metre pistol:** 41 competitors ([Q1360895::c0])

Based on these passages, the Men's 50 metre rifle three positions event had the highest number of competitors (49).

**Sources:**
* [Q1346374::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.28 seconds
- Tokens Used: 5243 (Prompt: 5149, Completion: 94)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the shooting event at the 2008 Summer Olympics with the highest number of competitors was the **Men's 10 metre air rifle** with **51 competitors** (2008 Summer-[:INCLUDES_EVENT]->(Shooting at the 2008 Summer Olympics – Men's 10 metre air rifle [sport=Shooting, competitors=51]))."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.69 seconds
- Tokens Used: 2061 (Prompt: 1976, Completion: 85)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 2008 Summer Olympics – Men's 50 metre rifle prone", "competitors": 56, "competition": "2008 Summer", "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 2008 Summer Olympics – Men's 50 metre rifle prone", "competitors": 56, "competition": "2008 Summer", "sport": "Shooting"}`
  - Supporting Document Chunks: `Q1005722::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the shooting event at the 2008 Summer Olympics with the highest number of competitors was the **Men's 50 metre rifle prone** (full title: **Shooting at the 2008 Summer Olympics – Men's 50 metre rifle prone**), which featured **56** competitors [Q1005722::c0]."

### Question [38/100] — pub-038

- Query: "Who won the gold medal in the event held at Sydney Convention and Exhibition Centre on 23 September 2000?"
- Archetype: `multi_hop`
- Ground Truth: `Pyrros Dimas`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.06 seconds
- Tokens Used: 4192 (Prompt: 4020, Completion: 172)
- Retrieved Context Chunks: `Q4951847::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the events held at the Sydney Convention and Exhibition Centre that included competitions on September 23, 2000, are:

1. **Men's freestyle 97 kg wrestling** (held September 28–30, 2000, though wrestling matches occurred during that window; however, September 23 is specifically noted for boxing preliminary rounds). 
2. **Men's super heavyweight boxing** (held from 23 September to 1 October 2000, with the preliminary Round of 16 taking place on September 23, 2000). The gold medal for this event was won by **Audley Harrison** (representing Great Britain).

Sources: [Q4951847::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.65 seconds
- Tokens Used: 3157 (Prompt: 3047, Completion: 110)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context and structured knowledge graph evidence, the events held at the Sydney Convention and Exhibition Centre during the 2000 Summer Olympics (such as the bantamweight, featherweight, flyweight, heavyweight, and light flyweight boxing competitions) span multiple dates rather than a single specific gold medal match identified solely for 23 September 2000 in the given text. Therefore, the specific gold medalist for an event exclusively on that date cannot be determined from the provided context. 

Unknown based on provided context."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 31.56 seconds
- Tokens Used: 2254 (Prompt: 2173, Completion: 81)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Sydney Convention and Exhibition Centre", "date_constraint": "23 september 2000", "year_filter": "2000", "event": "Weightlifting at the 2000 Summer Olympics – Men's 85 kg", "gold_winners": ["Pyrros Dimas"], "date_matched": true, "candidate_events_checked": 57}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sydney Convention and Exhibition Centre", "date_constraint": "23 september 2000", "year_filter": "2000", "event": "Weightlifting at the 2000 Summer Olympics – Men's 85 kg", "gold_winners": ["Pyrros Dimas"], "date_matched": true, "candidate_events_checked": 57}`
  - Supporting Document Chunks: `Q7979999::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting documentation, the gold medal in the event held at the Sydney Convention and Exhibition Centre on 23 September 2000 (Weightlifting at the 2000 Summer Olympics – Men's 85 kg) was won by **Pyrros Dimas** (representing Greece) [Q7979999::c0]."

### Question [39/100] — pub-039

- Query: "Who won the gold medal in the women's discus throw athletics event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Sandra Perković`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.01 seconds
- Tokens Used: 6133 (Prompt: 6114, Completion: 19)
- Retrieved Context Chunks: `Q26234091::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q26234091::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.95 seconds
- Tokens Used: 5297 (Prompt: 5247, Completion: 50)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and context passages, Sandra Perković won the gold medal in the women's discus throw at the 2012 Summer Olympics, which were held immediately before the 2016 Summer Olympics."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 14.96 seconds
- Tokens Used: 12219 (Prompt: 12107, Completion: 112)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Athletics at the 2012 Summer Olympics – Women's discus throw", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q1771958::c0`
- Synthesized Prediction:
  > "Based on the verified in-database graph facts and supporting context passages, the Summer Olympics held immediately before 2016 was the **2012 Summer** Olympics [Q1771958::c0]. 

The winner of the gold medal in the **Women's discus throw** event (full event title: **Athletics at the 2012 Summer Olympics – Women's discus throw**) was **Sandra Perković** of Croatia [Q1771958::c0]."

### Question [40/100] — pub-040

- Query: "Who won the gold medal in the individual normal hill/10 km nordic combined event at the Winter Olympics held immediately before 2014?"
- Archetype: `temporal`
- Ground Truth: `Jason Lamy Chappuis`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 5.49 seconds
- Tokens Used: 9019 (Prompt: 8962, Completion: 57)
- Retrieved Context Chunks: `Q303268::c0`
- Synthesized Prediction:
  > "Jason Lamy Chappuis won the gold medal in the individual normal hill/10 km Nordic combined event at the 2010 Winter Olympics, which was held immediately before the 2014 Winter Olympics [Q303268::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.98 seconds
- Tokens Used: 5585 (Prompt: 5524, Completion: 61)
- Retrieved Subgraph Chunks: `Q303268::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the individual normal hill/10 km Nordic combined event at the 2010 Winter Olympics (held immediately before 2014) was won by Jason Lamy Chappuis [Q303268::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 18.98 seconds
- Tokens Used: 11884 (Prompt: 11753, Completion: 131)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "Nordic combined at the 2010 Winter Olympics – Individual normal hill/10 km", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q303268::c0`
- Synthesized Prediction:
  > "Based on the supporting context and graph facts, the Winter Olympics held immediately before 2014 were the 2010 Winter Olympics. 

The gold medal winner of the individual normal hill/10 km nordic combined event at the 2010 Winter Olympics was **Jason Lamy Chappuis** (representing France).

* **Specific Event Name:** Men's individual normal hill/10 km
* **Full Event Title:** Nordic combined at the 2010 Winter Olympics – Individual normal hill/10 km

**Sources:**
* [Q303268::c0]"

### Question [41/100] — pub-041

- Query: "Who won the gold medal in the event held at Mountain Bike Centre on 21 August at the 2016 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Nino Schurter`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 28.66 seconds
- Tokens Used: 7145 (Prompt: 7083, Completion: 62)
- Retrieved Context Chunks: `Q25476845::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the men's cross-country cycling event held at the Mountain Bike Centre on 21 August 2016 was won by Nino Schurter.

**Source Citation:**
[Q25476845::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 35.17 seconds
- Tokens Used: 4541 (Prompt: 4479, Completion: 62)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the structured graph evidence, **Nino Schurter** won the gold medal in the event held at the Mountain Bike Centre on 21 August at the 2016 Summer Olympics (in the Cycling at the 2016 Summer Olympics – Men's cross-country event)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.66 seconds
- Tokens Used: 2008 (Prompt: 1939, Completion: 69)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Mountain Bike Centre", "date_constraint": "21 august", "year_filter": "2016", "event": "Cycling at the 2016 Summer Olympics – Men's cross-country", "gold_winners": ["Nino Schurter"], "date_matched": true, "candidate_events_checked": 2}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Mountain Bike Centre", "date_constraint": "21 august", "year_filter": "2016", "event": "Cycling at the 2016 Summer Olympics – Men's cross-country", "gold_winners": ["Nino Schurter"], "date_matched": true, "candidate_events_checked": 2}`
  - Supporting Document Chunks: `Q25476845::c0`
- Synthesized Prediction:
  > "**Nino Schurter** won the gold medal in the men's cross-country cycling event (Cycling at the 2016 Summer Olympics – Men's cross-country) held at the Mountain Bike Centre on 21 August 2016 [Q25476845::c0]."

### Question [42/100] — pub-042

- Query: "How many nations competed in Alpine skiing at the 1992 Winter Olympics – Men's giant slalom?"
- Archetype: `lookup`
- Ground Truth: `47`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 5.67 seconds
- Tokens Used: 6660 (Prompt: 6620, Completion: 40)
- Retrieved Context Chunks: `Q1005805::c0`
- Synthesized Prediction:
  > "Based on the provided context, 47 nations competed in the Men's giant slalom at the 1992 Winter Olympics [Q1005805::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.33 seconds
- Tokens Used: 9114 (Prompt: 9072, Completion: 42)
- Retrieved Subgraph Chunks: `Q1005805::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 47 nations competed in Alpine skiing at the 1992 Winter Olympics – Men's giant slalom [Q1005805::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.72 seconds
- Tokens Used: 3065 (Prompt: 3019, Completion: 46)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "attributes": {"name": "Men's giant slalom", "sport": "Alpine skiing", "discipline": "", "gender": "", "competitors": 131, "nations": 47}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "attributes": {"name": "Men's giant slalom", "sport": "Alpine skiing", "discipline": "", "gender": "", "competitors": 131, "nations": 47}}`
  - Supporting Document Chunks: `Q1005805::c0`
- Synthesized Prediction:
  > "Based on the verified database and event records, **47** nations competed in Alpine skiing at the 1992 Winter Olympics – Men's giant slalom [Q1005805::c0]."

### Question [43/100] — pub-043

- Query: "Who won the gold medal in the event held at Val-d'Isère on 16 February 1992?"
- Archetype: `multi_hop`
- Ground Truth: `Kjetil André Aamodt`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.08 seconds
- Tokens Used: 10605 (Prompt: 10599, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.67 seconds
- Tokens Used: 3135 (Prompt: 3075, Completion: 60)
- Retrieved Subgraph Chunks: `Q1534918::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, **Kjetil André Aamodt** won the gold medal in the men's super-G event held at Val-d'Isère on February 16, 1992 [Q1534918::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 46.01 seconds
- Tokens Used: 26847 (Prompt: 26731, Completion: 116)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Val-d'Isère", "date_constraint": "16 february 1992", "year_filter": "1992", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 1}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Val-d'Isère", "date_constraint": "16 february 1992", "year_filter": "1992", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 2}`
  - Supporting Document Chunks: `Q1534918::c0`
- Synthesized Prediction:
  > "The gold medal in the event held at Val-d'Isère on 16 February 1992 was won by **Kjetil André Aamodt** of Norway [Q1534918::c0]. 

* **Specific Event Name:** Men's super-G [Q1534918::c0]
* **Full Event Title:** Alpine skiing at the 1992 Winter Olympics – Men's super-G [Q1534918::c0]"

### Question [44/100] — pub-044

- Query: "According to the provided corpus, which fencing event at the 2008 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Fencing at the 2008 Summer Olympics – Men's épée`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.92 seconds
- Tokens Used: 2716 (Prompt: 2654, Completion: 62)
- Retrieved Context Chunks: `Q2726750::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the fencing event at the 2008 Summer Olympics with the highest number of competitors was the **Men's team épée** event, which had 32 competitors.

Sources:
- [Q2726750::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 7.26 seconds
- Tokens Used: 4787 (Prompt: 4707, Completion: 80)
- Retrieved Subgraph Chunks: `Q2570052::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the fencing event at the 2008 Summer Olympics with the highest number of competitors was the **Men's épée**, which had 41,000,000 competitors (as recorded in the structured evidence) / 41 competitors (as noted in the text passage [Q2570052::c0])."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 6.35 seconds
- Tokens Used: 1828 (Prompt: 1762, Completion: 66)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's épée", "full_event_title": "Fencing at the 2016 Summer Olympics – Men's épée", "competitors": 41000000, "competition": "2008 Summer", "sport": ""}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's épée", "full_event_title": "Fencing at the 2016 Summer Olympics – Men's épée", "competitors": 41000000, "competition": "2008 Summer", "sport": ""}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database facts and corpus, the fencing event at the 2008 Summer Olympics with the highest number of competitors was **Men's épée** (full event title: *Fencing at the 2016 Summer Olympics – Men's épée*) [gsql_heapaccum]."

### Question [45/100] — pub-045

- Query: "According to the provided corpus, how many athletics events at the 2004 Summer Olympics had more than 41 competitors?"
- Archetype: `aggregation`
- Ground Truth: `20`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.51 seconds
- Tokens Used: 5688 (Prompt: 5682, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.00 seconds
- Tokens Used: 4745 (Prompt: 4655, Completion: 90)
- Retrieved Subgraph Chunks: `Q220855::c0`
- Synthesized Prediction:
  > "Based on the provided context, there are **2** athletics events at the 2004 Summer Olympics that had more than 41 competitors:

1. **Men's 100 metres** with **82** competitors [Q220855::c0]
2. **Men's 110 metres hurdles** with **47** competitors (referenced in the structured graph evidence)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.46 seconds
- Tokens Used: 213 (Prompt: 182, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 20, "matching_events": ["Athletics at the 2004 Summer Olympics – Men's 800 metres (72 competitors)", "Athletics at the 2004 Summer Olympics – Men's 110 metres hurdles (47 competitors)", "Athletics at the 2004 Summer Olympics – Men's 4 × 100 metres relay (65 competitors)", "Athletics at the 2004 Summer Olympics – Men's triple jump (47 competitors)", "Athletics at the 2004 Summer Olympics – Men's marathon (101 competitors)", "Athletics at the 2004 Summer Olympics – Men's 400 metres (62 competitors)", "Athletics at the 2004 Summer Olympics – Women's 20 kilometres walk (57 competitors)", "Athletics at the 2004 Summer Olympics – Men's 100 metres (82 competitors)", "Athletics at the 2004 Summer Olympics – Women's javelin throw (45 competitors)", "Athletics at the 2004 Summer Olympics – Women's 200 metres (44 competitors)", "Athletics at the 2004 Summer Olympics – Women's hammer throw (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 400 metres (42 competitors)", "Athletics at the 2004 Summer Olympics – Men's 200 metres (54 competitors)", "Athletics at the 2004 Summer Olympics – Men's 20 kilometres walk (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 1500 metres (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 100 metres (63 competitors)", "Athletics at the 2004 Summer Olympics – Men's 50 kilometres walk (54 competitors)", "Athletics at the 2004 Summer Olympics – Women's marathon (82 competitors)", "Athletics at the 2004 Summer Olympics – Women's 800 metres (43 competitors)", "Athletics at the 2004 Summer Olympics – Women's discus throw (42 competitors)"], "competition": "2004 Summer", "threshold": 41, "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 20, "matching_events": ["Athletics at the 2004 Summer Olympics – Men's 800 metres (72 competitors)", "Athletics at the 2004 Summer Olympics – Men's 110 metres hurdles (47 competitors)", "Athletics at the 2004 Summer Olympics – Men's 4 × 100 metres relay (65 competitors)", "Athletics at the 2004 Summer Olympics – Men's triple jump (47 competitors)", "Athletics at the 2004 Summer Olympics – Men's marathon (101 competitors)", "Athletics at the 2004 Summer Olympics – Men's 400 metres (62 competitors)", "Athletics at the 2004 Summer Olympics – Women's 20 kilometres walk (57 competitors)", "Athletics at the 2004 Summer Olympics – Men's 100 metres (82 competitors)", "Athletics at the 2004 Summer Olympics – Women's javelin throw (45 competitors)", "Athletics at the 2004 Summer Olympics – Women's 200 metres (44 competitors)", "Athletics at the 2004 Summer Olympics – Women's hammer throw (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 400 metres (42 competitors)", "Athletics at the 2004 Summer Olympics – Men's 200 metres (54 competitors)", "Athletics at the 2004 Summer Olympics – Men's 20 kilometres walk (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 1500 metres (48 competitors)", "Athletics at the 2004 Summer Olympics – Women's 100 metres (63 competitors)", "Athletics at the 2004 Summer Olympics – Men's 50 kilometres walk (54 competitors)", "Athletics at the 2004 Summer Olympics – Women's marathon (82 competitors)", "Athletics at the 2004 Summer Olympics – Women's 800 metres (43 competitors)", "Athletics at the 2004 Summer Olympics – Women's discus throw (42 competitors)"], "competition": "2004 Summer", "threshold": 41, "sport": "Athletics"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database, there were 20 athletics events at the 2004 Summer Olympics that had more than 41 competitors."

### Question [46/100] — pub-046

- Query: "How many nations competed in Cross-country skiing at the 2010 Winter Olympics – Men's 15 kilometre freestyle?"
- Archetype: `lookup`
- Ground Truth: `50`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.96 seconds
- Tokens Used: 7644 (Prompt: 7595, Completion: 49)
- Retrieved Context Chunks: `Q384953::c0`
- Synthesized Prediction:
  > "Based on the provided context, 50 nations competed in the Men's 15 kilometre freestyle cross-country skiing competition at the 2010 Winter Olympics.

[Q384953::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.00 seconds
- Tokens Used: 7296 (Prompt: 7249, Completion: 47)
- Retrieved Subgraph Chunks: `Q384953::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 50 nations competed in the cross-country skiing men's 15 kilometre freestyle event at the 2010 Winter Olympics [Q384953::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.41 seconds
- Tokens Used: 2975 (Prompt: 2922, Completion: 53)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2010 Winter Olympics – Men's 15 kilometre freestyle", "attributes": {"name": "Men's 15 kilometre freestyle", "sport": "", "discipline": "", "gender": "", "competitors": 96, "nations": 50}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2010 Winter Olympics – Men's 15 kilometre freestyle", "attributes": {"name": "Men's 15 kilometre freestyle", "sport": "", "discipline": "", "gender": "", "competitors": 96, "nations": 50}}`
  - Supporting Document Chunks: `Q384953::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **50** nations competed in the Cross-country skiing at the 2010 Winter Olympics – Men's 15 kilometre freestyle event [Q384953::c0]."

### Question [47/100] — pub-047

- Query: "How many nations competed in Athletics at the 1992 Summer Olympics – Men's 3000 metres steeplechase?"
- Archetype: `lookup`
- Ground Truth: `24`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 6.47 seconds
- Tokens Used: 4979 (Prompt: 4924, Completion: 55)
- Retrieved Context Chunks: `Q1409048::c0`
- Synthesized Prediction:
  > "Based on the provided context, there were 24 nations that competed in the men's 3000 metres steeplechase event at the 1992 Summer Olympics.

Citation: [Q1409048::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.02 seconds
- Tokens Used: 5672 (Prompt: 5625, Completion: 47)
- Retrieved Subgraph Chunks: `Q1409048::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 24 nations competed in the Men's 3000 metres steeplechase at the 1992 Summer Olympics [Q1409048::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.64 seconds
- Tokens Used: 2171 (Prompt: 2084, Completion: 87)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Athletics at the 1992 Summer Olympics – Men's 3000 metres steeplechase", "attributes": {"name": "Men's 3000 metres steeplechase", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 32, "nations": 24}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Athletics at the 1992 Summer Olympics – Men's 3000 metres steeplechase", "attributes": {"name": "Men's 3000 metres steeplechase", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 32, "nations": 24}}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "Based on the verified graph facts and context, **24** nations competed in the Men's 3000 metres steeplechase at the 1992 Summer Olympics (specifically, the event *Athletics at the 1992 Summer Olympics – Men's 3000 metres steeplechase*) [graph_lookup, Q1409048::c0]."

### Question [48/100] — pub-048

- Query: "Who won the gold medal in the men's 68 kg taekwondo event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Servet Tazegül`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.59 seconds
- Tokens Used: 3393 (Prompt: 3374, Completion: 19)
- Retrieved Context Chunks: `Q26219849::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q26219849::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.51 seconds
- Tokens Used: 2489 (Prompt: 2428, Completion: 61)
- Retrieved Subgraph Chunks: `Q2142977::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's 68 kg taekwondo event at the 2012 Summer Olympics (held immediately before 2016) was won by Servet Tazegül [Q2142977::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 15.61 seconds
- Tokens Used: 5239 (Prompt: 5080, Completion: 159)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Taekwondo at the 2012 Summer Olympics – Men's 68 kg", "gold_winner": "Servet Tazegül", "date_held": "9 August"}`
  - Supporting Document Chunks: `Q2142977::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the Summer Olympics held immediately before 2016 was the 2012 Summer Olympics. 

The gold medal in the men's 68 kg taekwondo event at the 2012 Summer Olympics was won by **Servet Tazegül** [Q2142977::c0].

* **Specific Event Name:** Men's 68 kg
* **Full Event Title:** Taekwondo at the 2012 Summer Olympics – Men's 68 kg [Q2142977::c0]
* **Gold Medalist:** Servet Tazegül [Q2142977::c0]"

### Question [49/100] — pub-049

- Query: "Who won the gold medal in the men's pursuit biathlon event at the Winter Olympics held immediately before 2022?"
- Archetype: `temporal`
- Ground Truth: `Martin Fourcade`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 5.58 seconds
- Tokens Used: 9487 (Prompt: 9405, Completion: 82)
- Retrieved Context Chunks: `Q107861704::c0`
- Synthesized Prediction:
  > "Based on the provided context, Martin Fourcade was the 2014 and 2018 champion of the men's pursuit biathlon event (held immediately before the 2022 Winter Olympics) [Q107861704::c0]. 

Answer: Martin Fourcade [Q107861704::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.09 seconds
- Tokens Used: 7686 (Prompt: 7629, Completion: 57)
- Retrieved Subgraph Chunks: `Q47155371::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's pursuit biathlon event at the 2018 Winter Olympics (held immediately before 2022) was won by Martin Fourcade [Q47155371::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 13.43 seconds
- Tokens Used: 8740 (Prompt: 8611, Completion: 129)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "Biathlon at the 2018 Winter Olympics – Men's pursuit", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q47155371::c0`
- Synthesized Prediction:
  > "Based on the Winter Olympics held immediately before 2022 (the 2018 Winter Olympics in Pyeongchang, South Korea), the gold medal in the men's pursuit biathlon event was won by **Martin Fourcade** of France [Q47155371::c0]. 

* **Specific Event Name:** Men's pursuit [Q47155371::c0]
* **Full Event Title:** Biathlon at the 2018 Winter Olympics – Men's pursuit [Q47155371::c0]"

### Question [50/100] — pub-050

- Query: "Who won the gold medal in the event held at Adler Arena Skating Center on 11 February 2014?"
- Archetype: `multi_hop`
- Ground Truth: `Lee Sang-hwa`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.00 seconds
- Tokens Used: 7417 (Prompt: 7411, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.29 seconds
- Tokens Used: 5961 (Prompt: 5888, Completion: 73)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting context passages, there is no event listed as taking place on 11 February 2014 at the Adler Arena Skating Center (events mentioned took place on 8, 10, 12, and 15 February 2014). 

Unknown based on provided context."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 3.88 seconds
- Tokens Used: 3349 (Prompt: 3277, Completion: 72)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Adler Arena Skating Center", "date_constraint": "11 february 2014", "year_filter": "2014", "event": "Speed skating at the 2014 Winter Olympics – Women's 500 metres", "gold_winners": ["Lee Sang-hwa"], "date_matched": true, "candidate_events_checked": 5}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Adler Arena Skating Center", "date_constraint": "11 february 2014", "year_filter": "2014", "event": "Speed skating at the 2014 Winter Olympics – Women's 500 metres", "gold_winners": ["Lee Sang-hwa"], "date_matched": true, "candidate_events_checked": 5}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "**Lee Sang-hwa** won the gold medal in the **Speed skating at the 2014 Winter Olympics – Women's 500 metres** event held at the Adler Arena Skating Center on 11 February 2014 [multi_hop_chain, Q15056224::c0]."

### Question [51/100] — pub-051

- Query: "According to the provided corpus, how many canoeing events at the 2012 Summer Olympics had more than 25 competitors?"
- Archetype: `aggregation`
- Ground Truth: `6`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 15.05 seconds
- Tokens Used: 7074 (Prompt: 6597, Completion: 477)
- Retrieved Context Chunks: `Q1042705::c0, Q539696::c0, Q919261::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 4 canoeing events at the 2012 Summer Olympics that had more than 25 competitors:

1. **Women's canoe sprint K-4 500 metres** with 44 competitors [Q1042705::c0].
2. **Men's canoe sprint K-4 1,000 metres** with 40 competitors [Q539696::c0].
3. **Women's K-2 500 metres** with 34 competitors [Q919261::c0].
4. **Men's K-2 1,000 metres** with 24 competitors? Wait, let's check: 24 competitors is *not* more than 25. 
Let's re-verify the competitor counts for all events:
- Women's K-4 500 metres: 44 competitors [Q1042705::c0] (> 25)
- Men's K-4 1,000 metres: 40 competitors [Q539696::c0] (> 25)
- Women's K-2 500 metres: 34 competitors [Q919261::c0] (> 25)
- Men's C-2 1,000 metres: 24 competitors [Q2494175::c0] (not > 25)
- Men's K-2 1,000 metres: 24 competitors [Q303623::c0] (not > 25)

Therefore, exactly 3 canoeing events had more than 25 competitors.

**Citations:**
- [Q1042705::c0]
- [Q539696::c0]
- [Q919261::c0]
- [Q2494175::c0]
- [Q303623::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.93 seconds
- Tokens Used: 5657 (Prompt: 5451, Completion: 206)
- Retrieved Subgraph Chunks: `Q2390636::c0, Q2494175::c0, Q1005434::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the number of competitors for each mentioned canoeing event at the 2012 Summer Olympics is as follows:
- Men's C-1 1000 metres: 17 competitors
- Men's C-1 200 metres: 25 competitors [Q2390636::c0]
- Men's C-2 1000 metres: 24 competitors [Q2494175::c0]
- Men's K-1 1000 metres: 22 competitors
- Men's K-1 200 metres: 20 competitors [Q1005434::c0]

None of the events had *more than* 25 competitors (the maximum was 25 in the Men's C-1 200 metres). 

Answer: 0"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 6.18 seconds
- Tokens Used: 212 (Prompt: 182, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Canoeing at the 2012 Summer Olympics – Men's slalom C-2 (28 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-2 500 metres (34 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-4 500 metres (44 competitors)", "Canoeing at the 2012 Summer Olympics – Men's K-4 1000 metres (40 competitors)", "Canoeing at the 2012 Summer Olympics – Men's K-2 200 metres (28 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-1 200 metres (29 competitors)"], "competition": "2012 Summer", "threshold": 25, "sport": "Canoeing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Canoeing at the 2012 Summer Olympics – Men's slalom C-2 (28 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-2 500 metres (34 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-4 500 metres (44 competitors)", "Canoeing at the 2012 Summer Olympics – Men's K-4 1000 metres (40 competitors)", "Canoeing at the 2012 Summer Olympics – Men's K-2 200 metres (28 competitors)", "Canoeing at the 2012 Summer Olympics – Women's K-1 200 metres (29 competitors)"], "competition": "2012 Summer", "threshold": 25, "sport": "Canoeing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database, there were 6 canoeing events at the 2012 Summer Olympics that had more than 25 competitors."

### Question [52/100] — pub-052

- Query: "How many nations competed in Biathlon at the 2022 Winter Olympics – Women's relay?"
- Archetype: `lookup`
- Ground Truth: `20`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.25 seconds
- Tokens Used: 9858 (Prompt: 9825, Completion: 33)
- Retrieved Context Chunks: `Q107861706::c0`
- Synthesized Prediction:
  > "Based on the provided context, 20 nations competed in the Women's relay event [Q107861706::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.67 seconds
- Tokens Used: 7864 (Prompt: 7820, Completion: 44)
- Retrieved Subgraph Chunks: `Q107861706::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 20 nations competed in the Biathlon at the 2022 Winter Olympics – Women's relay [Q107861706::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.74 seconds
- Tokens Used: 2379 (Prompt: 2330, Completion: 49)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Biathlon at the 2022 Winter Olympics – Women's relay", "attributes": {"name": "Women’s relay", "sport": "Biathlon", "discipline": "", "gender": "", "competitors": 80, "nations": 20}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Biathlon at the 2022 Winter Olympics – Women's relay", "attributes": {"name": "Women’s relay", "sport": "Biathlon", "discipline": "", "gender": "", "competitors": 80, "nations": 20}}`
  - Supporting Document Chunks: `Q107861706::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **20** nations competed in the Biathlon at the 2022 Winter Olympics – Women's relay [Q107861706::c0]."

### Question [53/100] — pub-053

- Query: "According to the provided corpus, which shooting event at the 2016 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Shooting at the 2016 Summer Olympics – Women's 10 metre air rifle`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.49 seconds
- Tokens Used: 8547 (Prompt: 8384, Completion: 163)
- Retrieved Context Chunks: `Q26219824::c0, Q26220718::c0, Q26218171::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the shooting event at the 2016 Summer Olympics with the highest number of competitors was the **Women's 10 metre air rifle** event, which had 51 competitors (compared to 44 competitors in the Women's 10 metre air pistol and Men's 50 metre rifle three positions events, and 26 competitors in the Men's 25 metre rapid fire pistol event).

Sources:
- [Q26219824::c0]
- [Q26220718::c0]
- [Q26218171::c0]
- [Q26237418::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 3.93 seconds
- Tokens Used: 5398 (Prompt: 5266, Completion: 132)
- Retrieved Subgraph Chunks: `Q25396733::c0, Q26237421::c0, Q26219824::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the shooting event at the 2016 Summer Olympics with the highest number of competitors was the **Men's 50 metre rifle prone**, which had **47 competitors**. 

(For comparison: Men's 10 metre air pistol had 46 [Q25396733::c0], Men's 50 metre pistol had 41 [Q26237421::c0], and Men's 25 metre rapid fire pistol had 26 [Q26219824::c0])."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.58 seconds
- Tokens Used: 1526 (Prompt: 1443, Completion: 83)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Women's 10 metre air rifle", "full_event_title": "Shooting at the 1996 Summer Olympics – Women's 10 metre air rifle", "competitors": 51, "competition": "2016 Summer", "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Women's 10 metre air rifle", "full_event_title": "Shooting at the 1996 Summer Olympics – Women's 10 metre air rifle", "competitors": 51, "competition": "2016 Summer", "sport": "Shooting"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database and corpus, the shooting event with the highest number of competitors is the **Women's 10 metre air rifle**, with the full event title **Shooting at the 1996 Summer Olympics – Women's 10 metre air rifle**, featuring **51** competitors [gsql_heapaccum, Q7500799::c0]."

### Question [54/100] — pub-054

- Query: "How many nations competed in Marathon swimming at the 2016 Summer Olympics – Women's 10 kilometre?"
- Archetype: `lookup`
- Ground Truth: `24`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.51 seconds
- Tokens Used: 5180 (Prompt: 5131, Completion: 49)
- Retrieved Context Chunks: `Q25991470::c0`
- Synthesized Prediction:
  > "Based on the provided context, 24 nations competed in the Women's 10 kilometre marathon swimming at the 2016 Summer Olympics.

Source: [Q25991470::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 5.80 seconds
- Tokens Used: 5267 (Prompt: 5221, Completion: 46)
- Retrieved Subgraph Chunks: `Q25991470::c0`
- Synthesized Prediction:
  > "Based on the provided context, 24 nations competed in the Women's 10 kilometre marathon swimming event at the 2016 Summer Olympics [Q25991470::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.77 seconds
- Tokens Used: 1612 (Prompt: 1551, Completion: 61)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Marathon swimming at the 2016 Summer Olympics – Women's 10 kilometre", "attributes": {"name": "Women's marathon 10 kilometre", "sport": "Marathon swimming", "discipline": "", "gender": "", "competitors": 26, "nations": 24}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Marathon swimming at the 2016 Summer Olympics – Women's 10 kilometre", "attributes": {"name": "Women's marathon 10 kilometre", "sport": "Marathon swimming", "discipline": "", "gender": "", "competitors": 26, "nations": 24}}`
  - Supporting Document Chunks: `Q25991470::c0`
- Synthesized Prediction:
  > "Based on the verified database and supporting context, **24** nations competed in the Women's marathon 10 kilometre (Marathon swimming at the 2016 Summer Olympics – Women's 10 kilometre) [Q25991470::c0]."

### Question [55/100] — pub-055

- Query: "Who won the gold medal in the men's 80 kg taekwondo event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Sebastián Crismanich`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.15 seconds
- Tokens Used: 3462 (Prompt: 3374, Completion: 88)
- Retrieved Context Chunks: `Q26219850::c0`
- Synthesized Prediction:
  > "Based on the provided context, the Summer Olympics held immediately before 2016 is not explicitly detailed with the 2012 gold medalist for the men's 80 kg event (the text only provides details for the 2016 Summer Olympics). Therefore, the exact answer cannot be determined from the passages.

Unknown based on provided context [Q26219850::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.81 seconds
- Tokens Used: 2487 (Prompt: 2428, Completion: 59)
- Retrieved Subgraph Chunks: `Q934172::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, Sebastián Crismanich won the gold medal in the men's 80 kg taekwondo event at the 2012 Summer Olympics (held immediately before the 2016 Games) [Q934172::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 20.03 seconds
- Tokens Used: 5479 (Prompt: 5299, Completion: 180)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Taekwondo at the 2012 Summer Olympics – Men's 80 kg", "gold_winner": "Sebastián Crismanich", "date_held": "10 August"}`
  - Supporting Document Chunks: `Q934172::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the Summer Olympics held immediately before 2016 was the 2012 Summer Olympics. 

The gold medal in the men's 80 kg taekwondo event at those games was won by **Sebastián Crismanich** (representing Argentina) [Q934172::c0].

* **Specific Event Name:** Men's 80 kg
* **Full Event Title:** Taekwondo at the 2012 Summer Olympics – Men's 80 kg [Q934172::c0]
* **Gold Winner:** Sebastián Crismanich [Q934172::c0]
* **Date Held:** 10 August 2012 [Q934172::c0]"

### Question [56/100] — pub-056

- Query: "Who won the gold medal in the men's 30 kilometre pursuit cross-country skiing event at the Winter Olympics held immediately before 2010?"
- Archetype: `temporal`
- Ground Truth: `Yevgeny Dementyev`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.27 seconds
- Tokens Used: 8571 (Prompt: 8497, Completion: 74)
- Retrieved Context Chunks: `Q848689::c0, Q824803::c0`
- Synthesized Prediction:
  > "Yevgeny Dementyev won the gold medal in the men's 30 kilometre pursuit cross-country skiing event at the 2006 Winter Olympics (held immediately before the 2010 Games).

Sources: [Q848689::c0], [Q824803::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.24 seconds
- Tokens Used: 6504 (Prompt: 6436, Completion: 68)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence, the gold medal in the men's 30 kilometre pursuit cross-country skiing event at the 2006 Winter Olympics (held immediately before the 2010 Winter Olympics) was won by **Yevgeny Dementyev** and **Frode Estil**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 14.02 seconds
- Tokens Used: 17193 (Prompt: 17051, Completion: 142)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2006 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2006 Winter", "matched_event": "Cross-country skiing at the 2006 Winter Olympics – Men's 30 kilometre pursuit", "gold_winner": "Yevgeny Dementyev", "date_held": ""}`
  - Supporting Document Chunks: `Q824803::c0`
- Synthesized Prediction:
  > "Based on the verified in-database graph facts and supporting context, the gold medal in the men's 30 kilometre pursuit cross-country skiing event at the 2006 Winter Olympics (the Winter Olympics held immediately before 2010) was won by **Yevgeny Dementyev**.

* **Specific Event Name:** Men's 30 kilometre pursuit
* **Full Event Title:** Cross-country skiing at the 2006 Winter Olympics – Men's 30 kilometre pursuit
* **Gold Medalist:** Yevgeny Dementyev

**Citations:**
* [Q824803::c0]"

### Question [57/100] — pub-057

- Query: "Who won the gold medal in the women's 200 metres athletics event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Allyson Felix`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.95 seconds
- Tokens Used: 7499 (Prompt: 7318, Completion: 181)
- Retrieved Context Chunks: `Q26219842::c0`
- Synthesized Prediction:
  > "Based on the provided context, the athlete who won the gold medal in the 2012 Olympic 200 metres is not explicitly named as the winner of the 2012 event, but the passages mention that "The 2012 Olympic champion Allyson Felix was absent..." in the context of the 200 metres event [Q26219842::c0]. However, looking at the previous event history references, the 2012 winner is not explicitly stated as winning gold by name for 2012, though Allyson Felix is identified as the "2012 Olympic champion" for the women's 200 metres [Q26219842::c0]. 

Answer: Allyson Felix [Q26219842::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.31 seconds
- Tokens Used: 5272 (Prompt: 5216, Completion: 56)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the gold medal in the Women's 200 metres athletics event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by **Allyson Felix**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 16.56 seconds
- Tokens Used: 10155 (Prompt: 10007, Completion: 148)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Athletics at the 2012 Summer Olympics – Women's 200 metres", "gold_winner": "Allyson Felix", "date_held": "6–8 August"}`
  - Supporting Document Chunks: `Q1798867::c0`
- Synthesized Prediction:
  > "The gold medal in the women's 200 metres athletics event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics) was won by **Allyson Felix** [Q1798867::c0].

* **Specific Event Name:** Women's 200 metres [Q1798867::c0]
* **Full Event Title:** Athletics at the 2012 Summer Olympics – Women's 200 metres [Q1798867::c0]
* **Gold Medalist:** Allyson Felix [Q1798867::c0]"

### Question [58/100] — pub-058

- Query: "According to the provided corpus, how many rowing events at the 1996 Summer Olympics had more than 39 competitors?"
- Archetype: `aggregation`
- Ground Truth: `5`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.85 seconds
- Tokens Used: 4221 (Prompt: 4115, Completion: 106)
- Retrieved Context Chunks: `Q22964454::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there is only one rowing event (Women's eight) that explicitly mentions the total number of competitors (72 competitors), which is more than 39 [Q22964454::c0]. The other provided passages do not specify the total number of competitors for their respective events. Therefore, based strictly on the provided text, the number of such events is 1.

Source cited: [Q22964454::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.10 seconds
- Tokens Used: 5993 (Prompt: 5847, Completion: 146)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, the rowing events at the 1996 Summer Olympics with their number of competitors are:

* **Men's coxless four**: 56 competitors
* **Men's lightweight coxless four**: 68 competitors
* **Men's coxless pair**: 36 competitors
* **Men's double sculls**: 39 competitors
* **Men's lightweight double sculls**: 38 competitors

Out of these events, **2** events had more than 39 competitors (Men's coxless four with 56 competitors and Men's lightweight coxless four with 68 competitors)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.22 seconds
- Tokens Used: 209 (Prompt: 179, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Rowing at the 1996 Summer Olympics – Men's coxless four (56 competitors)", "Rowing at the 1996 Summer Olympics – Men's lightweight coxless four (68 competitors)", "Rowing at the 1996 Summer Olympics – Women's eight (72 competitors)", "Rowing at the 1996 Summer Olympics – Women's quadruple sculls (40 competitors)", "Rowing at the 1996 Summer Olympics – Men's quadruple sculls (56 competitors)"], "competition": "1996 Summer", "threshold": 39, "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Rowing at the 1996 Summer Olympics – Men's coxless four (56 competitors)", "Rowing at the 1996 Summer Olympics – Men's lightweight coxless four (68 competitors)", "Rowing at the 1996 Summer Olympics – Women's eight (72 competitors)", "Rowing at the 1996 Summer Olympics – Women's quadruple sculls (40 competitors)", "Rowing at the 1996 Summer Olympics – Men's quadruple sculls (56 competitors)"], "competition": "1996 Summer", "threshold": 39, "sport": "Rowing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database, there were 5 rowing events at the 1996 Summer Olympics that had more than 39 competitors."

### Question [59/100] — pub-059

- Query: "Who won the gold medal in the women's sprint biathlon event at the Winter Olympics held immediately before 2022?"
- Archetype: `temporal`
- Ground Truth: `Laura Dahlmeier`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.81 seconds
- Tokens Used: 10112 (Prompt: 10058, Completion: 54)
- Retrieved Context Chunks: `Q107861710::c0`
- Synthesized Prediction:
  > "Based on the provided context, the 2018 champion (the Winter Olympics held immediately before 2022) in the women's sprint biathlon event was Laura Dahlmeier [Q107861710::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 7.41 seconds
- Tokens Used: 6730 (Prompt: 6673, Completion: 57)
- Retrieved Subgraph Chunks: `Q47091419::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the women's sprint biathlon event at the 2018 Winter Olympics (held immediately before 2022) was won by Laura Dahlmeier [Q47091419::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 15.70 seconds
- Tokens Used: 12910 (Prompt: 12793, Completion: 117)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2018 Winter", "matched_event": "Biathlon at the 2018 Winter Olympics – Women's sprint", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q47091419::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the women's sprint biathlon event at the Winter Olympics held immediately before 2022 (the 2018 Winter Olympics) was won by **Laura Dahlmeier** of Germany [Q47091419::c0]. 

* **Specific Event Name:** Women's sprint [Q47091419::c0]
* **Full Event Title:** Biathlon at the 2018 Winter Olympics – Women's sprint"

### Question [60/100] — pub-060

- Query: "Who won the gold medal in the event held at ExCeL Exhibition Centre on 30 July at the 2012 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Yana Shemyakina`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.35 seconds
- Tokens Used: 3067 (Prompt: 2982, Completion: 85)
- Retrieved Context Chunks: `Q348720::c0`
- Synthesized Prediction:
  > "Based on the provided context, the men's light heavyweight boxing competition was held at the ExCeL Exhibition Centre starting on 30 July 2012, and the gold medal in that event was won by Egor Mekhontsev [Q348720::c0]. 

Answer: Egor Mekhontsev [Q348720::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 3.85 seconds
- Tokens Used: 2951 (Prompt: 2832, Completion: 119)
- Retrieved Subgraph Chunks: `Q332673::c0, Q348720::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph and text passages, multiple boxing events were held at the ExCeL Exhibition Centre starting on 30 July 2012 during the 2012 Summer Olympics. The gold medalists for those specific events are:

* **Men's flyweight:** Robeisy Ramírez [Q332673::c0]
* **Men's heavyweight:** Oleksandr Usyk
* **Men's light heavyweight:** Egor Mekhontsev [Q348720::c0]"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: FAILED
- Latency: 27.85 seconds
- Tokens Used: 976 (Prompt: 893, Completion: 83)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "ExCeL Exhibition Centre", "date_constraint": "30 july", "year_filter": "2012", "event": "Boxing at the 2012 Summer Olympics – Men's light heavyweight", "gold_winners": ["Egor Mekhontsev"], "date_matched": true, "candidate_events_checked": 37}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "ExCeL Exhibition Centre", "date_constraint": "30 july", "year_filter": "2012", "event": "Boxing at the 2012 Summer Olympics – Men's light heavyweight", "gold_winners": ["Egor Mekhontsev"], "date_matched": true, "candidate_events_checked": 37}`
  - Supporting Document Chunks: `Q348720::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal for the event held at the ExCeL Exhibition Centre starting on 30 July at the 2012 Summer Olympics (specifically, **Boxing at the 2012 Summer Olympics – Men's light heavyweight**) was won by **Egor Mekhontsev** [Q348720::c0]."

### Question [61/100] — pub-061

- Query: "How many nations competed in Boxing at the 1988 Summer Olympics – Light flyweight?"
- Archetype: `lookup`
- Ground Truth: `34`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 15.71 seconds
- Tokens Used: 7197 (Prompt: 7163, Completion: 34)
- Retrieved Context Chunks: `Q10572416::c0`
- Synthesized Prediction:
  > "34 nations competed in the light flyweight boxing event at the 1988 Summer Olympics [Q10572416::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.14 seconds
- Tokens Used: 5364 (Prompt: 5323, Completion: 41)
- Retrieved Subgraph Chunks: `Q10572416::c0`
- Synthesized Prediction:
  > "Based on the provided context, 34 nations competed in the Light flyweight boxing event at the 1988 Summer Olympics [Q10572416::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.79 seconds
- Tokens Used: 1709 (Prompt: 1657, Completion: 52)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Boxing at the 1988 Summer Olympics – Light flyweight", "attributes": {"name": "Light flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 34, "nations": 34}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Boxing at the 1988 Summer Olympics – Light flyweight", "attributes": {"name": "Light flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 34, "nations": 34}}`
  - Supporting Document Chunks: `Q10572416::c0`
- Synthesized Prediction:
  > "34 nations competed in the Light flyweight boxing event at the 1988 Summer Olympics (Event: Boxing at the 1988 Summer Olympics – Light flyweight) [Q10572416::c0]."

### Question [62/100] — pub-062

- Query: "Who won the gold medal in the women's 10,000 metres athletics event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Tirunesh Dibaba`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.39 seconds
- Tokens Used: 7565 (Prompt: 7480, Completion: 85)
- Retrieved Context Chunks: `Q26233297::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the women's 10,000 metres event at the 2012 Summer Olympics (held immediately before 2016) was won by Tirunesh Dibaba of Ethiopia (who entered the 2016 Games as the defending champion). 

Sources: [Q26233297::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.20 seconds
- Tokens Used: 5357 (Prompt: 5290, Completion: 67)
- Retrieved Subgraph Chunks: `Q1799275::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the women's 10,000 metres athletics event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by Tirunesh Dibaba [Q1799275::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 16.60 seconds
- Tokens Used: 16164 (Prompt: 15980, Completion: 184)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Athletics at the 2012 Summer Olympics – Women's 10,000 metres", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q1799275::c0`
- Synthesized Prediction:
  > "Based on the verified database facts and supporting context passages, the gold medal in the women's 10,000 metres athletics event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics) was won by **Tirunesh Dibaba** representing Ethiopia [Q1799275::c0]. 

* **Specific Event Name:** Women's 10,000 metres
* **Full Event Title:** Athletics at the 2012 Summer Olympics – Women's 10,000 metres [Q1799275::c0]
* **Gold Medal Winner:** Tirunesh Dibaba (ETH) [Q1799275::c0]
* **Citation:** [Q1799275::c0]"

### Question [63/100] — pub-063

- Query: "How many nations competed in Swimming at the 1988 Summer Olympics – Men's 200 metre freestyle?"
- Archetype: `lookup`
- Ground Truth: `41`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.20 seconds
- Tokens Used: 7236 (Prompt: 7187, Completion: 49)
- Retrieved Context Chunks: `Q7656692::c0`
- Synthesized Prediction:
  > "Based on the provided context, 41 nations competed in the men's 200 metre freestyle event at the 1988 Summer Olympics.

Sources: [Q7656692::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.40 seconds
- Tokens Used: 5450 (Prompt: 5402, Completion: 48)
- Retrieved Subgraph Chunks: `Q7656692::c0`
- Synthesized Prediction:
  > "Based on the provided context, there were 41 nations that competed in the Men's 200 metre freestyle event at the 1988 Summer Olympics [Q7656692::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.99 seconds
- Tokens Used: 3317 (Prompt: 3262, Completion: 55)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Swimming at the 1988 Summer Olympics – Men's 200 metre freestyle", "attributes": {"name": "Men's 200 metre freestyle", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 63, "nations": 41}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Swimming at the 1988 Summer Olympics – Men's 200 metre freestyle", "attributes": {"name": "Men's 200 metre freestyle", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 63, "nations": 41}}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **41** nations competed in Swimming at the 1988 Summer Olympics – Men's 200 metre freestyle [graph_lookup, Q7656692::c0]."

### Question [64/100] — pub-064

- Query: "Who won the gold medal in the event held at ANZ Stadium on 22 September 2000 (heats)25 September 2000 (final)?"
- Archetype: `multi_hop`
- Ground Truth: `Gabriela Szabo`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.58 seconds
- Tokens Used: 7763 (Prompt: 7686, Completion: 77)
- Retrieved Context Chunks: `Q3628769::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the event held at ANZ Stadium with heats on 22 September 2000 and the final on 25 September 2000 (Women's 5000 metres) was won by Gabriela Szabo of Romania.

Sources: [Q3628769::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 20.99 seconds
- Tokens Used: 5688 (Prompt: 5615, Completion: 73)
- Retrieved Subgraph Chunks: `Q3628769::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the Women's 5000 metres held at ANZ Stadium on 22 September 2000 (heats) and 25 September 2000 (final) was won by **Gabriela Szabo** [Q3628769::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 7.70 seconds
- Tokens Used: 3965 (Prompt: 3884, Completion: 81)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "ANZ Stadium", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics – Women's 5000 metres", "gold_winners": ["Gabriela Szabo"], "date_matched": true, "candidate_events_checked": 4}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "ANZ Stadium", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics – Women's 5000 metres", "gold_winners": ["Gabriela Szabo"], "date_matched": true, "candidate_events_checked": 4}`
  - Supporting Document Chunks: `Q3628769::c0`
- Synthesized Prediction:
  > "**Gabriela Szabo** won the gold medal in the **Athletics at the 2000 Summer Olympics – Women's 5000 metres** event held at ANZ Stadium on 22 September 2000 (heats) and 25 September 2000 (final) [Q3628769::c0]."

### Question [65/100] — pub-065

- Query: "According to the provided corpus, how many biathlon events at the 2014 Winter Olympics had more than 68 competitors?"
- Archetype: `aggregation`
- Ground Truth: `5`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 74.77 seconds
- Tokens Used: 9519 (Prompt: 8714, Completion: 805)
- Retrieved Context Chunks: `Q15052014::c0, Q15052026::c0, Q15052025::c0`
- Synthesized Prediction:
  > "1. Cite: [Q15052014::c0] (Men's relay – 76 competitors), [Q15052026::c0] (Mixed relay – 64 competitors), [Q15052025::c0] (Women's relay – 68 competitors)."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 3.53 seconds
- Tokens Used: 6766 (Prompt: 6640, Completion: 126)
- Retrieved Subgraph Chunks: `Q15021060::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are **2** biathlon events at the 2014 Winter Olympics that had more than 68 competitors:

1. **Men's individual** with 89 competitors [Q15021060::c0]
2. **Men's relay** with 76 competitors (as indicated in the structured graph evidence: `(2014 Winter)-[:INCLUDES_EVENT]->(Biathlon at the 2014 Winter Olympics – Men's relay [sport=Biathlon, competitors=76])`)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.41 seconds
- Tokens Used: 211 (Prompt: 180, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Biathlon at the 2014 Winter Olympics – Men's sprint (87 competitors)", "Biathlon at the 2014 Winter Olympics – Women's individual (82 competitors)", "Biathlon at the 2014 Winter Olympics – Women's sprint (84 competitors)", "Biathlon at the 2014 Winter Olympics – Men's relay (76 competitors)", "Biathlon at the 2014 Winter Olympics – Men's individual (89 competitors)"], "competition": "2014 Winter", "threshold": 68, "sport": "Biathlon"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Biathlon at the 2014 Winter Olympics – Men's sprint (87 competitors)", "Biathlon at the 2014 Winter Olympics – Women's individual (82 competitors)", "Biathlon at the 2014 Winter Olympics – Women's sprint (84 competitors)", "Biathlon at the 2014 Winter Olympics – Men's relay (76 competitors)", "Biathlon at the 2014 Winter Olympics – Men's individual (89 competitors)"], "competition": "2014 Winter", "threshold": 68, "sport": "Biathlon"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 5 biathlon events at the 2014 Winter Olympics that had more than 68 competitors."

### Question [66/100] — pub-066

- Query: "According to the provided corpus, which weightlifting event at the 1992 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Weightlifting at the 1992 Summer Olympics – Men's 75 kg`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 9.31 seconds
- Tokens Used: 8671 (Prompt: 8606, Completion: 65)
- Retrieved Context Chunks: `Q7979977::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the weightlifting event at the 1992 Summer Olympics with the highest number of competitors is the **Men's 82.5 kg** event, which had 31 competitors.

Source chunk: [Q7979977::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 6.51 seconds
- Tokens Used: 5971 (Prompt: 5784, Completion: 187)
- Retrieved Subgraph Chunks: `Q7979967::c0, Q7979968::c0, Q7979971::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the weightlifting events at the 1992 Summer Olympics listed in the structured graph and context have the following competitor counts:
- Men's +110 kg: 20 competitors [Q7979967::c0]
- Men's 100 kg: 25 competitors [Q7979968::c0]
- Men's 110 kg: 24 competitors
- Men's 52 kg: 17 competitors [Q7979971::c0]
- Men's 56 kg: 22 competitors

Therefore, the **Men's 100 kg** weightlifting event had the highest number of competitors (25) among those listed [Q7979968::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.47 seconds
- Tokens Used: 2706 (Prompt: 2620, Completion: 86)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 75 kg", "full_event_title": "Weightlifting at the 1992 Summer Olympics – Men's 75 kg", "competitors": 34, "competition": "1992 Summer", "sport": "Weightlifting"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 75 kg", "full_event_title": "Weightlifting at the 1992 Summer Olympics – Men's 75 kg", "competitors": 34, "competition": "1992 Summer", "sport": "Weightlifting"}`
  - Supporting Document Chunks: `Q7979975::c0`
- Synthesized Prediction:
  > "Based on the provided corpus and graph facts, the weightlifting event at the 1992 Summer Olympics with the highest number of competitors was the **Men's 75 kg** event (full title: **Weightlifting at the 1992 Summer Olympics – Men's 75 kg**), which featured **34** competitors [Q7979975::c0]."

### Question [67/100] — pub-067

- Query: "Who won the gold medal in the event held at North Greenwich Arena on 4 August at the 2012 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Rosannagh MacLennan`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.47 seconds
- Tokens Used: 6881 (Prompt: 6838, Completion: 43)
- Retrieved Context Chunks: `Q284413::c0`
- Synthesized Prediction:
  > "Rosannagh MacLennan won the gold medal in the event held at the North Greenwich Arena on 4 August at the 2012 Summer Olympics [Q284413::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.16 seconds
- Tokens Used: 4966 (Prompt: 4909, Completion: 57)
- Retrieved Subgraph Chunks: `Q284413::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the North Greenwich Arena on 4 August at the 2012 Summer Olympics (Women's trampoline) was won by Rosannagh MacLennan [Q284413::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.91 seconds
- Tokens Used: 1564 (Prompt: 1440, Completion: 124)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "North Greenwich Arena", "date_constraint": "4 august", "year_filter": "2012", "event": "Gymnastics at the 2012 Summer Olympics – Women's trampoline", "gold_winners": ["Rosannagh Mac, Lennan"], "date_matched": true, "candidate_events_checked": 2}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "North Greenwich Arena", "date_constraint": "4 august", "year_filter": "2012", "event": "Gymnastics at the 2012 Summer Olympics – Women's trampoline", "gold_winners": ["Rosannagh Mac, Lennan"], "date_matched": true, "candidate_events_checked": 2}`
  - Supporting Document Chunks: `Q284413::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the women's trampoline event held at the North Greenwich Arena on 4 August at the 2012 Summer Olympics was won by **Rosannagh MacLennan** (representing Canada) [Q284413::c0]. 

* **Event Name:** Women's trampoline [Q284413::c0]
* **Full Event Title:** Gymnastics at the 2012 Summer Olympics – Women's trampoline [Q284413::c0]"

### Question [68/100] — pub-068

- Query: "How many nations competed in Cycling at the 2012 Summer Olympics – Women's cross-country?"
- Archetype: `lookup`
- Ground Truth: `24`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.50 seconds
- Tokens Used: 5567 (Prompt: 5524, Completion: 43)
- Retrieved Context Chunks: `Q2269155::c0`
- Synthesized Prediction:
  > "Based on the provided context, 24 nations competed in the Women's cross-country cycling event at the 2012 Summer Olympics [Q2269155::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.42 seconds
- Tokens Used: 4584 (Prompt: 4540, Completion: 44)
- Retrieved Subgraph Chunks: `Q2269155::c0`
- Synthesized Prediction:
  > "Based on the provided context, **24** nations competed in the Women's cross-country cycling event at the 2012 Summer Olympics [Q2269155::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.89 seconds
- Tokens Used: 1254 (Prompt: 1207, Completion: 47)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Cycling at the 2012 Summer Olympics – Women's cross-country", "attributes": {"name": "Women's cross-country cycling", "sport": "Cycling", "discipline": "", "gender": "", "competitors": 30, "nations": 24}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Cycling at the 2012 Summer Olympics – Women's cross-country", "attributes": {"name": "Women's cross-country cycling", "sport": "Cycling", "discipline": "", "gender": "", "competitors": 30, "nations": 24}}`
  - Supporting Document Chunks: `Q2269155::c0`
- Synthesized Prediction:
  > "Based on the verified database and supporting context, **24** nations competed in the Women's cross-country cycling event at the 2012 Summer Olympics [Q2269155::c0]."

### Question [69/100] — pub-069

- Query: "According to the provided corpus, how many fencing events at the 2000 Summer Olympics had more than 39 competitors?"
- Archetype: `aggregation`
- Ground Truth: `3`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.58 seconds
- Tokens Used: 2960 (Prompt: 2710, Completion: 250)
- Retrieved Context Chunks: `Q5443153::c0, Q647750::c0, Q5443155::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, none of the fencing events at the 2000 Summer Olympics had more than 39 competitors. The competitor counts for the events mentioned are as follows:
- Women's team épée: 26 competitors [Q5443153::c0]
- Men's team foil: 28 competitors [Q647750::c0]
- Women's team foil: 29 competitors [Q5443155::c0]
- Men's sabre: 39 competitors [Q647742::c0]
- Men's team sabre: 29 competitors [Q5443151::c0]

Therefore, the number of events with more than 39 competitors is **0**.

Citations: [Q5443153::c0], [Q647750::c0], [Q5443155::c0], [Q647742::c0], [Q5443151::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.55 seconds
- Tokens Used: 3656 (Prompt: 3509, Completion: 147)
- Retrieved Subgraph Chunks: `Q632472::c0, Q647742::c0, Q632754::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the fencing events at the 2000 Summer Olympics with their number of competitors are:

* Men's foil: 40 competitors [Q632472::c0]
* Men's sabre: 39 competitors [Q647742::c0]
* Men's team foil: 28 competitors
* Men's team sabre: 29 competitors
* Men's team épée: 33 competitors [Q632754::c0]

Only **1** event (Men's foil) had more than 39 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.19 seconds
- Tokens Used: 209 (Prompt: 179, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Fencing at the 2000 Summer Olympics – Men's foil (40 competitors)", "Fencing at the 2000 Summer Olympics – Men's épée (42 competitors)", "Fencing at the 2000 Summer Olympics – Women's foil (40 competitors)"], "competition": "2000 Summer", "threshold": 39, "sport": "Fencing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Fencing at the 2000 Summer Olympics – Men's foil (40 competitors)", "Fencing at the 2000 Summer Olympics – Men's épée (42 competitors)", "Fencing at the 2000 Summer Olympics – Women's foil (40 competitors)"], "competition": "2000 Summer", "threshold": 39, "sport": "Fencing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 3 fencing events at the 2000 Summer Olympics that had more than 39 competitors."

### Question [70/100] — pub-070

- Query: "According to the provided corpus, how many speed skating events at the 2010 Winter Olympics had more than 36 competitors?"
- Archetype: `aggregation`
- Ground Truth: `3`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.85 seconds
- Tokens Used: 6800 (Prompt: 6662, Completion: 138)
- Retrieved Context Chunks: `Q848666::c1, Q841942::c1, Q595972::c0`
- Synthesized Prediction:
  > "Based on the provided context, the exact number of speed skating events at the 2010 Winter Olympics with more than 36 competitors cannot be determined, as the corpus only provides detailed participant listings for specific events (such as the Men's and Women's 500 metres and the Men's 10,000 metres, which had 15 competitors) and does not list the total competitor counts for all speed skating events. 

Unknown based on provided context [Q848666::c1], [Q841942::c1], [Q595972::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 3.64 seconds
- Tokens Used: 4895 (Prompt: 4795, Completion: 100)
- Retrieved Subgraph Chunks: `Q905485::c0, Q614894::c0, Q379473::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are no speed skating events at the 2010 Winter Olympics with more than 36 competitors. The listed events have 36 ([Q905485::c0]), 32 ([Q614894::c0]), and 32 ([Q379473::c0]) competitors. 

Therefore, the number of events with more than 36 competitors is 0."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.66 seconds
- Tokens Used: 217 (Prompt: 185, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Speed skating at the 2010 Winter Olympics – Men's 1500 metres (37 competitors)", "Speed skating at the 2010 Winter Olympics – Men's 1000 metres (38 competitors)", "Speed skating at the 2010 Winter Olympics – Men's 500 metres (39 competitors)"], "competition": "2010 Winter", "threshold": 36, "sport": "Speed skating"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Speed skating at the 2010 Winter Olympics – Men's 1500 metres (37 competitors)", "Speed skating at the 2010 Winter Olympics – Men's 1000 metres (38 competitors)", "Speed skating at the 2010 Winter Olympics – Men's 500 metres (39 competitors)"], "competition": "2010 Winter", "threshold": 36, "sport": "Speed skating"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 speed skating events at the 2010 Winter Olympics that had more than 36 competitors."

### Question [71/100] — pub-071

- Query: "How many nations competed in Biathlon at the 2018 Winter Olympics – Women's pursuit?"
- Archetype: `lookup`
- Ground Truth: `24`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 16.08 seconds
- Tokens Used: 7307 (Prompt: 7260, Completion: 47)
- Retrieved Context Chunks: `Q47155365::c0`
- Synthesized Prediction:
  > "Based on the provided context, 24 nations competed in the Women's pursuit biathlon at the 2018 Winter Olympics.

Source chunk: [Q47155365::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.21 seconds
- Tokens Used: 7784 (Prompt: 7741, Completion: 43)
- Retrieved Subgraph Chunks: `Q47155365::c0`
- Synthesized Prediction:
  > "Based on the provided context, 24 nations competed in the Biathlon at the 2018 Winter Olympics – Women's pursuit [Q47155365::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.31 seconds
- Tokens Used: 2279 (Prompt: 2233, Completion: 46)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Biathlon at the 2018 Winter Olympics – Women's pursuit", "attributes": {"name": "Women's pursuit", "sport": "Biathlon", "discipline": "", "gender": "", "competitors": 58, "nations": 24}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Biathlon at the 2018 Winter Olympics – Women's pursuit", "attributes": {"name": "Women's pursuit", "sport": "Biathlon", "discipline": "", "gender": "", "competitors": 58, "nations": 24}}`
  - Supporting Document Chunks: `Q47155365::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and context passages, **24** nations competed in the Women's pursuit at the 2018 Winter Olympics [Q47155365::c0]."

### Question [72/100] — pub-072

- Query: "Who won the gold medal in the women's 500 metres speed skating event at the Winter Olympics held immediately before 2014?"
- Archetype: `temporal`
- Ground Truth: `Lee Sang-hwa`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.70 seconds
- Tokens Used: 6598 (Prompt: 6497, Completion: 101)
- Retrieved Context Chunks: `Q15056224::c0, Q586729::c0`
- Synthesized Prediction:
  > "Based on the provided context, the Winter Olympics held immediately before 2014 was the 2010 Winter Olympics in Vancouver. The gold medal in the women's 500 metres speed skating event was won by Lee Sang-hwa (who won it at the 2010 Olympics, as noted in the text). 

Sources: [Q15056224::c0], [Q586729::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.89 seconds
- Tokens Used: 4825 (Prompt: 4707, Completion: 118)
- Retrieved Subgraph Chunks: `Q938779::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence, the gold medal in the Speed skating at the 2010 Winter Olympics – Women's 500 metres event (held immediately before the 2014 Winter Olympics) was won by Lee Sang-hwa (on 11 February 2014). 

*(Note: In short-track speed skating, the gold medal for the women's 500 metres at the 2010 Winter Olympics was won by Wang Meng [Q938779::c0].)*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 19.63 seconds
- Tokens Used: 10194 (Prompt: 10094, Completion: 100)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 3)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "Speed skating at the 2010 Winter Olympics – Women's 500 metres", "gold_winner": "", "date_held": ""}`
  - Supporting Document Chunks: `Q848666::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting passages, the Winter Olympics held immediately before 2014 was the 2010 Winter Olympics. 

* **Event Name:** Women's 500 metres
* **Full Event Title:** Speed skating at the 2010 Winter Olympics – Women's 500 metres
* **Gold Medal Winner:** Lee Sang-hwa (South Korea) [Q848666::c0]"

### Question [73/100] — pub-073

- Query: "Who won the gold medal in the event held at Sydney International Shooting Centre on 21 September 2000 (slow)22 September 2000 (fast)?"
- Archetype: `multi_hop`
- Ground Truth: `Yang Ling`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.57 seconds
- Tokens Used: 6553 (Prompt: 6490, Completion: 63)
- Retrieved Context Chunks: `Q7500807::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal for the event held at the Sydney International Shooting Centre on 21 September 2000 (slow) and 22 September 2000 (fast) was won by Yang Ling [Q7500807::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.55 seconds
- Tokens Used: 4561 (Prompt: 4483, Completion: 78)
- Retrieved Subgraph Chunks: `Q7500807::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Sydney International Shooting Centre on 21 September 2000 (slow) and 22 September 2000 (fast)—which was the Men's 10 metre running target—was won by **Yang Ling** [Q7500807::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 11.04 seconds
- Tokens Used: 13502 (Prompt: 13319, Completion: 183)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Sydney International Shooting Centre", "date_constraint": "21 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics – Men's 10 metre running target", "gold_winners": [], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sydney International Shooting Centre", "date_constraint": "21 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics – Men's 10 metre running target", "gold_winners": [], "date_matched": true, "candidate_events_checked": 17}`
  - Supporting Document Chunks: `Q7500807::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal for the event held at the Sydney International Shooting Centre with the date schedule "21 September 2000 (slow)22 September 2000 (fast)" was won by **Yang Ling** (representing China) [Q7500807::c0].

* **Specific Event Name:** Men's 10 metre running target [Q7500807::c0]
* **Full Event Title:** Shooting at the 2000 Summer Olympics – Men's 10 metre running target [Q7500807::c0]
* **Gold Medalist:** Yang Ling [Q7500807::c0]

**Citation:** [Q7500807::c0]"

### Question [74/100] — pub-074

- Query: "How many nations competed in Cross-country skiing at the 2006 Winter Olympics – Women's 4 × 5 kilometre relay?"
- Archetype: `lookup`
- Ground Truth: `17`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 4.32 seconds
- Tokens Used: 5776 (Prompt: 5723, Completion: 53)
- Retrieved Context Chunks: `Q827175::c0`
- Synthesized Prediction:
  > "Based on the provided context, 17 nations competed in the Women's 4 × 5 kilometre relay cross-country skiing competition at the 2006 Winter Olympics.

Source: [Q827175::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.44 seconds
- Tokens Used: 5555 (Prompt: 5511, Completion: 44)
- Retrieved Subgraph Chunks: `Q827175::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 17 nations competed in the Women's 4 × 5 kilometre relay at the 2006 Winter Olympics [Q827175::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.81 seconds
- Tokens Used: 1695 (Prompt: 1601, Completion: 94)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2006 Winter Olympics – Women's 4 × 5 kilometre relay", "attributes": {"name": "Women's 4 × 5 kilometre relay", "sport": "", "discipline": "", "gender": "", "competitors": 68, "nations": 17}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2006 Winter Olympics – Women's 4 × 5 kilometre relay", "attributes": {"name": "Women's 4 × 5 kilometre relay", "sport": "", "discipline": "", "gender": "", "competitors": 68, "nations": 17}}`
  - Supporting Document Chunks: `Q827175::c0`
- Synthesized Prediction:
  > "Based on the verified database facts and supporting context, **17** nations competed in the Women's 4 × 5 kilometre relay at the 2006 Winter Olympics (Event: *Women's 4 × 5 kilometre relay* / Full title: *Cross-country skiing at the 2006 Winter Olympics – Women's 4 × 5 kilometre relay*) [Q827175::c0]."

### Question [75/100] — pub-075

- Query: "How many nations competed in Swimming at the 2000 Summer Olympics – Men's 1500 metre freestyle?"
- Archetype: `lookup`
- Ground Truth: `32`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.94 seconds
- Tokens Used: 4850 (Prompt: 4800, Completion: 50)
- Retrieved Context Chunks: `Q3879590::c0`
- Synthesized Prediction:
  > "Based on the provided context, 32 nations competed in the men's 1500 metre freestyle event at the 2000 Summer Olympics.

Citation: [Q3879590::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 2.85 seconds
- Tokens Used: 5609 (Prompt: 5560, Completion: 49)
- Retrieved Subgraph Chunks: `Q3879590::c0`
- Synthesized Prediction:
  > "Based on the provided context, there were 32 nations that competed in the Men's 1500 metre freestyle event at the 2000 Summer Olympics [Q3879590::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.28 seconds
- Tokens Used: 2046 (Prompt: 1994, Completion: 52)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Swimming at the 2000 Summer Olympics – Men's 1500 metre freestyle", "attributes": {"name": "Men's 1500 metre freestyle", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 41, "nations": 32}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Swimming at the 2000 Summer Olympics – Men's 1500 metre freestyle", "attributes": {"name": "Men's 1500 metre freestyle", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 41, "nations": 32}}`
  - Supporting Document Chunks: `Q3879590::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **32** nations competed in Swimming at the 2000 Summer Olympics – Men's 1500 metre freestyle [Q3879590::c0]."

### Question [76/100] — pub-076

- Query: "Who won the gold medal in the event held at Sestriere on February 24, 2006?"
- Archetype: `multi_hop`
- Ground Truth: `Julia Mancuso`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.11 seconds
- Tokens Used: 6632 (Prompt: 6627, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 3.17 seconds
- Tokens Used: 7100 (Prompt: 7095, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 10.87 seconds
- Tokens Used: 2468 (Prompt: 2396, Completion: 72)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Sestriere", "date_constraint": "february 24, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics – Women's giant slalom", "gold_winners": ["Julia Mancuso"], "date_matched": true, "candidate_events_checked": 7}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sestriere", "date_constraint": "february 24, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics – Women's giant slalom", "gold_winners": ["Julia Mancuso"], "date_matched": true, "candidate_events_checked": 7}`
  - Supporting Document Chunks: `Q2574045::c0`
- Synthesized Prediction:
  > "**Julia Mancuso** won the gold medal in the **Women's giant slalom** event (full event title: *Alpine skiing at the 2006 Winter Olympics – Women's giant slalom*) held at Sestriere on February 24, 2006 [Q2574045::c0]."

### Question [77/100] — pub-077

- Query: "Who won the gold medal in the event held at Xiaohaituo Bobsleigh and Luge TrackBeijing on 13, 14 February 2022?"
- Archetype: `multi_hop`
- Ground Truth: `Kaillie Humphries`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.16 seconds
- Tokens Used: 8877 (Prompt: 8824, Completion: 53)
- Retrieved Context Chunks: `Q110264144::c0`
- Synthesized Prediction:
  > "Kaillie Humphries won the gold medal in the event held on 13, 14 February 2022 (the women's monobob competition).

Sources: [Q110264144::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.56 seconds
- Tokens Used: 6784 (Prompt: 6714, Completion: 70)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence, **Kaillie Humphries** won the gold medal in the event held at the Xiaohaituo Bobsleigh and Luge Track on 13, 14 February 2022 (Bobsleigh at the 2022 Winter Olympics – Women's monobob)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.66 seconds
- Tokens Used: 3213 (Prompt: 3122, Completion: 91)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Xiaohaituo Bobsleigh and Luge TrackBeijing", "date_constraint": "14 february 2022", "year_filter": "2022", "event": "Bobsleigh at the 2022 Winter Olympics – Women's monobob", "gold_winners": ["Kaillie Humphries"], "date_matched": true, "candidate_events_checked": 4}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Xiaohaituo Bobsleigh and Luge TrackBeijing", "date_constraint": "14 february 2022", "year_filter": "2022", "event": "Bobsleigh at the 2022 Winter Olympics – Women's monobob", "gold_winners": ["Kaillie Humphries"], "date_matched": true, "candidate_events_checked": 4}`
  - Supporting Document Chunks: `Q110264144::c0`
- Synthesized Prediction:
  > "**Kaillie Humphries** won the gold medal in the **Women's monobob** event (full event title: *Bobsleigh at the 2022 Winter Olympics – Women's monobob*) held at the Xiaohaituo Bobsleigh and Luge Track in Beijing on 13 and 14 February 2022 [Q110264144::c0]."

### Question [78/100] — pub-078

- Query: "According to the provided corpus, how many athletics events at the 1996 Summer Olympics had more than 49 competitors?"
- Archetype: `aggregation`
- Ground Truth: `7`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.54 seconds
- Tokens Used: 7087 (Prompt: 6989, Completion: 98)
- Retrieved Context Chunks: `Q942846::c0`
- Synthesized Prediction:
  > "Based on the provided context, the Women's 400 metres event at the 1996 Summer Olympics had a total of 49 competitors [Q942846::c0]. The context does not provide the total number of competitors for any other athletics events, so the number of events with more than 49 competitors is unknown based on the provided context.

Sources:
- [Q942846::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 10.30 seconds
- Tokens Used: 5464 (Prompt: 5285, Completion: 179)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and text passages, there are **5** athletics events at the 1996 Summer Olympics listed with more than 49 competitors:

1. **Men's 10,000 metres** – 46 competitors *(Note: 46 is not > 49)*
2. **Men's 100 metres** – 106 competitors
3. **Men's 110 metres hurdles** – 62 competitors
4. **Men's 20 kilometres walk** – 53 competitors
5. **Men's 400 metres** – 62 competitors

Excluding the 10,000 metres (which had 46 competitors), the remaining **4** events each had more than 49 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.15 seconds
- Tokens Used: 211 (Prompt: 181, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 7, "matching_events": ["Athletics at the 1996 Summer Olympics – Men's 20 kilometres walk (53 competitors)", "Athletics at the 1996 Summer Olympics – Men's 800 metres (56 competitors)", "Athletics at the 1996 Summer Olympics – Women's 100 metres (56 competitors)", "Athletics at the 1996 Summer Olympics – Men's 100 metres (106 competitors)", "Athletics at the 1996 Summer Olympics – Men's 400 metres (62 competitors)", "Athletics at the 1996 Summer Olympics – Men's long jump (52 competitors)", "Athletics at the 1996 Summer Olympics – Men's 110 metres hurdles (62 competitors)"], "competition": "1996 Summer", "threshold": 49, "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 7, "matching_events": ["Athletics at the 1996 Summer Olympics – Men's 20 kilometres walk (53 competitors)", "Athletics at the 1996 Summer Olympics – Men's 800 metres (56 competitors)", "Athletics at the 1996 Summer Olympics – Women's 100 metres (56 competitors)", "Athletics at the 1996 Summer Olympics – Men's 100 metres (106 competitors)", "Athletics at the 1996 Summer Olympics – Men's 400 metres (62 competitors)", "Athletics at the 1996 Summer Olympics – Men's long jump (52 competitors)", "Athletics at the 1996 Summer Olympics – Men's 110 metres hurdles (62 competitors)"], "competition": "1996 Summer", "threshold": 49, "sport": "Athletics"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 7 athletics events at the 1996 Summer Olympics that had more than 49 competitors."

### Question [79/100] — pub-079

- Query: "Who won the gold medal in the event held at Centennial Parklands, Sydney on 26 September at the 2000 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: `Leontien Zijlaard`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.08 seconds
- Tokens Used: 6609 (Prompt: 6604, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.70 seconds
- Tokens Used: 5132 (Prompt: 5069, Completion: 63)
- Retrieved Subgraph Chunks: `Q2133123::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the women's individual road race (held at Centennial Parklands, Sydney on 26 September 2000) was won by **Leontien Zijlaard** of the Netherlands [Q2133123::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 40.74 seconds
- Tokens Used: 26424 (Prompt: 26291, Completion: 133)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Centennial Parklands, Sydney", "date_constraint": "26 september", "year_filter": "2000", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 2}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Centennial Parklands, Sydney", "date_constraint": "26 september", "year_filter": "2000", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 2}`
  - Supporting Document Chunks: `Q2133123::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context passages, the gold medal for the event held at Centennial Parklands, Sydney on 26 September at the 2000 Summer Olympics was won by:

* **Athlete:** Leontien Zijlaard (representing the Netherlands) [Q2133123::c0]
* **Event Name:** Women's cycling road race [Q2133123::c0]
* **Full Event Title:** Cycling at the 2000 Summer Olympics – Women's individual road race [Q2133123::c0]"

### Question [80/100] — pub-080

- Query: "How many nations competed in Beach volleyball at the 2008 Summer Olympics – Women's tournament?"
- Archetype: `lookup`
- Ground Truth: `17`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.52 seconds
- Tokens Used: 5770 (Prompt: 5730, Completion: 40)
- Retrieved Context Chunks: `Q977229::c0`
- Synthesized Prediction:
  > "Based on the provided context, 17 nations competed in the women's beach volleyball tournament at the 2008 Summer Olympics [Q977229::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 7.83 seconds
- Tokens Used: 5154 (Prompt: 5114, Completion: 40)
- Retrieved Subgraph Chunks: `Q977229::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 17 nations competed in the women's beach volleyball tournament at the 2008 Summer Olympics [Q977229::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 5.92 seconds
- Tokens Used: 3236 (Prompt: 2834, Completion: 402)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Beach volleyball at the 2008 Summer Olympics – Women's tournament", "attributes": {"name": "Women's beach volleyball", "sport": "Beach volleyball", "discipline": "", "gender": "", "competitors": 48, "nations": 17}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Beach volleyball at the 2008 Summer Olympics – Women's tournament", "attributes": {"name": "Women's beach volleyball", "sport": "Beach volleyball", "discipline": "", "gender": "", "competitors": 48, "nations": 17}}`
  - Supporting Document Chunks: `Q977229::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **17** nations competed in the Women's beach volleyball tournament at the 2008 Summer Olympics (Event name: *Women's beach volleyball*, Full event title: *Beach volleyball at the 2008 Summer Olympics – Women's tournament*) [graph_lookup, Q977229::c0].

**Participating nations (17):**
- Australia (AUS) [Q977229::c0]
- Austria (AUT) [Q977229::c0]
- Belgium (BEL) [Q977229::c0]
- Brazil (BRA) [Q977229::c0]
- China (CHN) [Q977229::c0]
- Cuba (CUB) [Q977229::c0]
- Georgia (GEO) [Q977229::c0]
- Germany (GER) [Q977229::c0]
- Greece (GRE) [Q977229::c0]
- Japan (JPN) [Q977229::c0]
- Mexico (MEX) [Q977229::c0]
- Netherlands (NED) [Q977229::c0]
- Norway (NOR) [Q977229::c0]
- South Africa (RSA) [Q977229::c0]
- Russia (RUS) [Q977229::c0]
- Switzerland (SUI) [Q977229::c0]
- United States (USA) [Q977229::c0]"

### Question [81/100] — pub-081

- Query: "Who won the gold medal in the event held at Beijing Shooting Range Hall on August 10, 2008?"
- Archetype: `multi_hop`
- Ground Truth: `Guo Wenjun`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 17.43 seconds
- Tokens Used: 7487 (Prompt: 7428, Completion: 59)
- Retrieved Context Chunks: `Q736527::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal for the event held at the Beijing Shooting Range Hall on August 10, 2008 (Women's 10 metre air pistol) was won by Guo Wenjun [Q736527::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.43 seconds
- Tokens Used: 5907 (Prompt: 5621, Completion: 286)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and context passages, the shooting event held at the Beijing Shooting Range Hall on August 10, 2008, was the **Women's 10 metre air pistol**. 

The medalists for this event were:
* **Gold:** Natalia Paderina won the silver medal, while the gold medal for the event is not explicitly listed in the text chunk for August 10, but the structured graph confirms **Guo Wenjun** and others. Wait, let's look closer at the graph evidence for August 10, 2008:
  `(Nino Salukvadze)-[:WON_MEDAL bronze (date: August 10, 2008)]->(Shooting at the 2008 Summer Olympics – Women's 10 metre air pistol)`
  `(Natalia Paderina)-[:WON_MEDAL silver (date: August 10, 2008)]->(Shooting at the 2008 Summer Olympics – Women's 10 metre air pistol)`

*(Note: The provided context does not explicitly name the gold medalist on August 10, 2008, within the text passages, though Natalia Paderina won silver and Nino Salukvadze won bronze on that date.)*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 52.54 seconds
- Tokens Used: 17619 (Prompt: 17459, Completion: 160)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Beijing Shooting Range Hall", "date_constraint": "august 10, 2008", "year_filter": "2008", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 9}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Beijing Shooting Range Hall", "date_constraint": "august 10, 2008", "year_filter": "2008", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 10}`
  - Supporting Document Chunks: `Q736527::c0, Q775967::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medalists for the events held at the **Beijing Shooting Range Hall** on **August 10, 2008** are:

1. **Guo Wenjun** (China) – **Shooting at the 2008 Summer Olympics – Women's 10 metre air pistol** [Q736527::c0]
2. **David Kostelecký** (Czech Republic) – **Shooting at the 2008 Summer Olympics – Men's trap** (Note: This event took place across August 9 and August 10 at the *Beijing Shooting Range Clay Target Field*) [Q775967::c0]"

### Question [82/100] — pub-082

- Query: "According to the provided corpus, how many swimming events at the 1996 Summer Olympics had more than 42 competitors?"
- Archetype: `aggregation`
- Ground Truth: `12`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.11 seconds
- Tokens Used: 4163 (Prompt: 4157, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 6.05 seconds
- Tokens Used: 6013 (Prompt: 5864, Completion: 149)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, there are 4 swimming events at the 1996 Summer Olympics listed with the number of competitors, all of which had more than 42 competitors:

1. **Men's 100 metre backstroke**: 52 competitors ([Structured Graph Evidence])
2. **Men's 100 metre breaststroke**: 45 competitors ([Structured Graph Evidence])
3. **Men's 100 metre butterfly**: 61 competitors ([Structured Graph Evidence])
4. **Men's 100 metre freestyle**: 61 competitors ([Structured Graph Evidence])

Thus, **4** swimming events had more than 42 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 2.23 seconds
- Tokens Used: 215 (Prompt: 183, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 12, "matching_events": ["Swimming at the 1996 Summer Olympics – Men's 100 metre butterfly (61 competitors)", "Swimming at the 1996 Summer Olympics – Women's 50 metre freestyle (56 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre backstroke (52 competitors)", "Swimming at the 1996 Summer Olympics – Men's 200 metre freestyle (43 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre breaststroke (45 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre breaststroke (46 competitors)", "Swimming at the 1996 Summer Olympics – Women's 200 metre individual medley (43 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre freestyle (61 competitors)", "Swimming at the 1996 Summer Olympics – Men's 200 metre butterfly (43 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre freestyle (48 competitors)", "Swimming at the 1996 Summer Olympics – Men's 50 metre freestyle (65 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre butterfly (44 competitors)"], "competition": "1996 Summer", "threshold": 42, "sport": "Swimming"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 12, "matching_events": ["Swimming at the 1996 Summer Olympics – Men's 100 metre butterfly (61 competitors)", "Swimming at the 1996 Summer Olympics – Women's 50 metre freestyle (56 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre backstroke (52 competitors)", "Swimming at the 1996 Summer Olympics – Men's 200 metre freestyle (43 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre breaststroke (45 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre breaststroke (46 competitors)", "Swimming at the 1996 Summer Olympics – Women's 200 metre individual medley (43 competitors)", "Swimming at the 1996 Summer Olympics – Men's 100 metre freestyle (61 competitors)", "Swimming at the 1996 Summer Olympics – Men's 200 metre butterfly (43 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre freestyle (48 competitors)", "Swimming at the 1996 Summer Olympics – Men's 50 metre freestyle (65 competitors)", "Swimming at the 1996 Summer Olympics – Women's 100 metre butterfly (44 competitors)"], "competition": "1996 Summer", "threshold": 42, "sport": "Swimming"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database result, there were 12 swimming events at the 1996 Summer Olympics that had more than 42 competitors."

### Question [83/100] — pub-083

- Query: "Who won the gold medal in the event held at Kvitfjell and Hafjell on February 20–21, 1994?"
- Archetype: `multi_hop`
- Ground Truth: `Pernilla Wiberg`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 8.13 seconds
- Tokens Used: 9920 (Prompt: 9860, Completion: 60)
- Retrieved Context Chunks: `Q1222212::c0`
- Synthesized Prediction:
  > "Based on the provided context, Pernilla Wiberg won the gold medal in the event held at Kvitfjell and Hafjell on February 20–21, 1994 (Women's combined).

[Q1222212::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.19 seconds
- Tokens Used: 6524 (Prompt: 6385, Completion: 139)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence, Vreni Schneider won the silver medal (on February 20–21, 1994) in the Alpine skiing at the 1994 Winter Olympics – Women's giant slalom. However, the context does not explicitly state who won the gold medal for the specific event on February 20–21, 1994 (though Deborah Compagnoni won the gold on February 24, 1994). 

Therefore, stating the exact gold medalist for the event dated February 20–21, 1994, is **Unknown based on provided context**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 35.58 seconds
- Tokens Used: 24278 (Prompt: 24172, Completion: 106)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Kvitfjell and Hafjell", "date_constraint": "february 20", "year_filter": "1994", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 2}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Kvitfjell and Hafjell", "date_constraint": "february 20", "year_filter": "1994", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 3}`
  - Supporting Document Chunks: `Q1222212::c0`
- Synthesized Prediction:
  > "Based on the verified supporting documents and graph facts, the event held at Kvitfjell and Hafjell on February 20–21, 1994, was the **Women's combined** event (**Alpine skiing at the 1994 Winter Olympics – Women's combined**) [Q1222212::c0]. 

The gold medal was won by **Pernilla Wiberg** representing Sweden [Q1222212::c0]."

### Question [84/100] — pub-084

- Query: "According to the provided corpus, which fencing event at the 1992 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Fencing at the 1992 Summer Olympics – Men's épée`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.63 seconds
- Tokens Used: 3984 (Prompt: 3817, Completion: 167)
- Retrieved Context Chunks: `Q38407::c0, Q38605::c0, Q38601::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, both the **Men's team sabre** (59 competitors) [Q38407::c0], the **Men's team foil** (59 competitors) [Q38605::c0], and the **Men's team épée** (60 competitors) [Q38601::c0] list their competitor numbers. 

Comparing these events, the **Men's team épée** had the highest number of competitors with 60 [Q38601::c0].

Sources used:
- [Q38407::c0]
- [Q38601::c0]
- [Q38605::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 6.89 seconds
- Tokens Used: 4561 (Prompt: 4441, Completion: 120)
- Retrieved Subgraph Chunks: `Q38599::c0, Q38407::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, the fencing events at the 1992 Summer Olympics with the highest number of competitors (59 competitors each) are:

* **Men's foil** [sport=Fencing, competitors=59] ([Q38599::c0])
* **Men's team foil** [sport=Fencing, competitors=59]
* **Men's team sabre** [sport=Fencing, competitors=59] ([Q38407::c0])"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 5.40 seconds
- Tokens Used: 1840 (Prompt: 1759, Completion: 81)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's épée", "full_event_title": "Fencing at the 2016 Summer Olympics – Men's épée", "competitors": 70, "competition": "1992 Summer", "sport": "Fencing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's épée", "full_event_title": "Fencing at the 2016 Summer Olympics – Men's épée", "competitors": 70, "competition": "1992 Summer", "sport": "Fencing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified graph facts and corpus, the fencing event at the 1992 Summer Olympics with the highest number of competitors was the **Men's épée** (full title: **Fencing at the 2016 Summer Olympics – Men's épée** based on the linked database entity context), which featured **70** competitors [gsql_heapaccum]."

### Question [85/100] — pub-085

- Query: "According to the provided corpus, which sailing event at the 2008 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Sailing at the 2008 Summer Olympics – Men's 470`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.33 seconds
- Tokens Used: 4560 (Prompt: 4387, Completion: 173)
- Retrieved Context Chunks: `Q2634280::c0, Q2563962::c0, Q2566720::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the sailing events with the highest number of competitors at the 2008 Summer Olympics were:

* **Women's Yngling** with 45 competitors [Q2634280::c0].
* **Women's 470** with 38 competitors [Q2563962::c0].
* **Mixed 49er** with 38 competitors [Q2566720::c0].

Thus, the Women's Yngling had the highest number of competitors (45).

Sources: [Q2634280::c0], [Q2563962::c0], [Q2566720::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.57 seconds
- Tokens Used: 3865 (Prompt: 3764, Completion: 101)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the structured graph evidence and supporting passages, the sailing event at the 2008 Summer Olympics with the highest number of competitors was the **Men's 470**, which had 58 competitors [2008 Summer -[:INCLUDES_EVENT]->(Sailing at the 2008 Summer Olympics – Men's 470 [sport=Sailing, competitors=58]), Q2564420::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.43 seconds
- Tokens Used: 735 (Prompt: 650, Completion: 85)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 58, "competition": "2008 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 58, "competition": "2008 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "According to the verified graph facts, the sailing event at the 2008 Summer Olympics with the highest number of competitors was the **Men's 470** (full event title: *Sailing at the 2004 Summer Olympics – Men's 470*), with a total of **58** competitors [Q7400344::c0]."

### Question [86/100] — pub-086

- Query: "Who won the gold medal in the event held at Richmond Olympic Oval on 17 February 2010?"
- Archetype: `multi_hop`
- Ground Truth: `Shani Davis`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.94 seconds
- Tokens Used: 5563 (Prompt: 5558, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.08 seconds
- Tokens Used: 4564 (Prompt: 4507, Completion: 57)
- Retrieved Subgraph Chunks: `Q848696::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's 1000 metres speed skating event held at the Richmond Olympic Oval on 17 February 2010 was won by Shani Davis [Q848696::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 50.59 seconds
- Tokens Used: 15063 (Prompt: 14953, Completion: 110)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Richmond Olympic Oval", "date_constraint": "17 february 2010", "year_filter": "2010", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 10}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Richmond Olympic Oval", "date_constraint": "17 february 2010", "year_filter": "2010", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 10}`
  - Supporting Document Chunks: `Q848696::c0`
- Synthesized Prediction:
  > "Based on the supporting context passages and venue details for the 2010 Winter Olympics:

The event held at the **Richmond Olympic Oval** on **17 February 2010** was the **Men's 1000 metres** (*Speed skating at the 2010 Winter Olympics – Men's 1000 metres*). 

The gold medal in this event was won by **Shani Davis** representing the United States [Q848696::c0]."

### Question [87/100] — pub-087

- Query: "According to the provided corpus, how many athletics events at the 1988 Summer Olympics had more than 41 competitors?"
- Archetype: `aggregation`
- Ground Truth: `17`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.99 seconds
- Tokens Used: 6592 (Prompt: 6485, Completion: 107)
- Retrieved Context Chunks: `Q3628688::c0, Q3628708::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 athletics events that explicitly list the number of competitors as greater than 41:

1. **Women's 400 metres** (1988 Summer) – 46 competitors ([Q3628688::c0]).
2. **Men's 4 × 400 metres relay** (1988 Summer) – 99 competitors ([Q3628708::c0])."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.28 seconds
- Tokens Used: 5538 (Prompt: 5335, Completion: 203)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the athletics events at the 1988 Summer Olympics that had more than 41 competitors are:

1. **Men's 10,000 metres** with 51 competitors [sport=Athletics, competitors=51]
2. **Men's 100 metres** with 102 competitors [sport=Athletics, competitors=102]
3. **Men's 1500 metres** with 59 competitors [sport=Athletics, competitors=59]
4. **Men's 20 kilometres walk** with 53 competitors [sport=Athletics, competitors=53]

*(Note: The Men's 110 metres hurdles had 41 competitors, so it is excluded).* 

Therefore, there were **4** athletics events with more than 41 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.26 seconds
- Tokens Used: 211 (Prompt: 179, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 17, "matching_events": ["Athletics at the 1988 Summer Olympics – Men's triple jump (43 competitors)", "Athletics at the 1988 Summer Olympics – Men's 800 metres (70 competitors)", "Athletics at the 1988 Summer Olympics – Men's 10,000 metres (51 competitors)", "Athletics at the 1988 Summer Olympics – Women's marathon (70 competitors)", "Athletics at the 1988 Summer Olympics – Men's 4 × 400 metres relay (99 competitors)", "Athletics at the 1988 Summer Olympics – Women's 10,000 metres (42 competitors)", "Athletics at the 1988 Summer Olympics – Men's 100 metres (102 competitors)", "Athletics at the 1988 Summer Olympics – Men's 400 metres (75 competitors)", "Athletics at the 1988 Summer Olympics – Women's 400 metres (46 competitors)", "Athletics at the 1988 Summer Olympics – Men's 1500 metres (59 competitors)", "Athletics at the 1988 Summer Olympics – Men's 200 metres (72 competitors)", "Athletics at the 1988 Summer Olympics – Men's marathon (118 competitors)", "Athletics at the 1988 Summer Olympics – Men's 20 kilometres walk (53 competitors)", "Athletics at the 1988 Summer Olympics – Women's 100 metres (64 competitors)", "Athletics at the 1988 Summer Olympics – Men's 5000 metres (56 competitors)", "Athletics at the 1988 Summer Olympics – Men's 50 kilometres walk (42 competitors)", "Athletics at the 1988 Summer Olympics – Women's 200 metres (59 competitors)"], "competition": "1988 Summer", "threshold": 41, "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 17, "matching_events": ["Athletics at the 1988 Summer Olympics – Men's triple jump (43 competitors)", "Athletics at the 1988 Summer Olympics – Men's 800 metres (70 competitors)", "Athletics at the 1988 Summer Olympics – Men's 10,000 metres (51 competitors)", "Athletics at the 1988 Summer Olympics – Women's marathon (70 competitors)", "Athletics at the 1988 Summer Olympics – Men's 4 × 400 metres relay (99 competitors)", "Athletics at the 1988 Summer Olympics – Women's 10,000 metres (42 competitors)", "Athletics at the 1988 Summer Olympics – Men's 100 metres (102 competitors)", "Athletics at the 1988 Summer Olympics – Men's 400 metres (75 competitors)", "Athletics at the 1988 Summer Olympics – Women's 400 metres (46 competitors)", "Athletics at the 1988 Summer Olympics – Men's 1500 metres (59 competitors)", "Athletics at the 1988 Summer Olympics – Men's 200 metres (72 competitors)", "Athletics at the 1988 Summer Olympics – Men's marathon (118 competitors)", "Athletics at the 1988 Summer Olympics – Men's 20 kilometres walk (53 competitors)", "Athletics at the 1988 Summer Olympics – Women's 100 metres (64 competitors)", "Athletics at the 1988 Summer Olympics – Men's 5000 metres (56 competitors)", "Athletics at the 1988 Summer Olympics – Men's 50 kilometres walk (42 competitors)", "Athletics at the 1988 Summer Olympics – Women's 200 metres (59 competitors)"], "competition": "1988 Summer", "threshold": 41, "sport": "Athletics"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database results, there were 17 athletics events at the 1988 Summer Olympics that had more than 41 competitors."

### Question [88/100] — pub-088

- Query: "According to the provided corpus, which alpine skiing event at the 1992 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: `Alpine skiing at the 1992 Winter Olympics – Men's giant slalom`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.90 seconds
- Tokens Used: 5051 (Prompt: 4941, Completion: 110)
- Retrieved Context Chunks: `Q1534918::c0`
- Synthesized Prediction:
  > "Based on the provided context, the men's super-G competition at the 1992 Winter Olympics had 118 competitors [Q1534918::c0]. The context does not provide the total number of competitors for the other mentioned alpine skiing events, so it is unknown based on the provided context which event strictly had the overall highest number compared to all others, though super-G is explicitly stated to have had 118 competitors [Q1534918::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.07 seconds
- Tokens Used: 8267 (Prompt: 8224, Completion: 43)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, the alpine skiing event at the 1992 Winter Olympics with the highest number of competitors was the **Men's giant slalom**, which had **131** competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.25 seconds
- Tokens Used: 3096 (Prompt: 3014, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's giant slalom", "full_event_title": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "competitors": 131, "competition": "1992 Winter", "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's giant slalom", "full_event_title": "Alpine skiing at the 1992 Winter Olympics – Men's giant slalom", "competitors": 131, "competition": "1992 Winter", "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1005805::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the alpine skiing event at the 1992 Winter Olympics with the highest number of competitors was the **Men's giant slalom** (full event title: *Alpine skiing at the 1992 Winter Olympics – Men's giant slalom*), with a total of **131** competitors [Q1005805::c0]."

### Question [89/100] — pub-089

- Query: "According to the provided corpus, how many boxing events at the 1988 Summer Olympics had more than 39 competitors?"
- Archetype: `aggregation`
- Ground Truth: `5`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.83 seconds
- Tokens Used: 6456 (Prompt: 6334, Completion: 122)
- Retrieved Context Chunks: `Q10497007::c0, Q10719573::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 boxing events at the 1988 Summer Olympics that had more than 39 competitors (44 competitors each):

1. **Flyweight boxing** ([Q10497007::c0]) - 44 competitors
2. **Welterweight boxing** ([Q10719573::c0]) - 44 competitors

Sources used: [Q10497007::c0], [Q10719573::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.42 seconds
- Tokens Used: 5993 (Prompt: 5871, Completion: 122)
- Retrieved Subgraph Chunks: `Q10426128::c0, Q10495988::c0, Q10497007::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are 3 boxing events at the 1988 Summer Olympics that had more than 39 competitors:

1. **Bantamweight** with 48 competitors ([Q10426128::c0])
2. **Featherweight** with 48 competitors ([Q10495988::c0])
3. **Flyweight** with 44 competitors ([Q10497007::c0])

Thus, the total number of events is **3**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.14 seconds
- Tokens Used: 206 (Prompt: 176, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Boxing at the 1988 Summer Olympics – Bantamweight (48 competitors)", "Boxing at the 1988 Summer Olympics – Featherweight (48 competitors)", "Boxing at the 1988 Summer Olympics – Flyweight (44 competitors)", "Boxing at the 1988 Summer Olympics – Welterweight (44 competitors)", "Boxing at the 1988 Summer Olympics – Light welterweight (45 competitors)"], "competition": "1988 Summer", "threshold": 39, "sport": "Boxing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 5, "matching_events": ["Boxing at the 1988 Summer Olympics – Bantamweight (48 competitors)", "Boxing at the 1988 Summer Olympics – Featherweight (48 competitors)", "Boxing at the 1988 Summer Olympics – Flyweight (44 competitors)", "Boxing at the 1988 Summer Olympics – Welterweight (44 competitors)", "Boxing at the 1988 Summer Olympics – Light welterweight (45 competitors)"], "competition": "1988 Summer", "threshold": 39, "sport": "Boxing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided database, there were 5 boxing events at the 1988 Summer Olympics that had more than 39 competitors."

### Question [90/100] — pub-090

- Query: "Who won the gold medal in the men's greco-roman 96 kg wrestling event at the Summer Olympics held immediately before 2012?"
- Archetype: `temporal`
- Ground Truth: `Aslanbek Khushtov`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.83 seconds
- Tokens Used: 2395 (Prompt: 2377, Completion: 18)
- Retrieved Context Chunks: `Q2358254::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q2358254::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.33 seconds
- Tokens Used: 2669 (Prompt: 2602, Completion: 67)
- Retrieved Subgraph Chunks: `Q1005294::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's Greco-Roman 96 kg wrestling event at the 2008 Summer Olympics (held immediately before 2012) was won by **Aslanbek Khushtov** [Q1005294::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 7.47 seconds
- Tokens Used: 7433 (Prompt: 7261, Completion: 172)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2008 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2008 Summer", "matched_event": "Wrestling at the 2008 Summer Olympics – Men's Greco-Roman 96 kg", "gold_winner": "Aslanbek Khushtov", "date_held": "14 August 2008"}`
  - Supporting Document Chunks: `Q1005294::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the men's Greco-Roman 96 kg wrestling event at the Summer Olympics immediately preceding 2012 (the 2008 Summer Olympics) was won by **Aslanbek Khushtov** [Q1005294::c0]. 

* **Specific Event:** Men's Greco-Roman 96 kg [Q1005294::c0]
* **Full Event Title:** Wrestling at the 2008 Summer Olympics – Men's Greco-Roman 96 kg [Q1005294::c0]
* **Gold Medal Winner:** Aslanbek Khushtov [Q1005294::c0]"

### Question [91/100] — pub-091

- Query: "How many nations competed in Wrestling at the 1992 Summer Olympics – Men's freestyle 100 kg?"
- Archetype: `lookup`
- Ground Truth: `18`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 18.33 seconds
- Tokens Used: 6287 (Prompt: 6242, Completion: 45)
- Retrieved Context Chunks: `Q3498987::c0`
- Synthesized Prediction:
  > "Based on the provided context, 18 nations competed in the Men's freestyle 100 kg event at the 1992 Summer Olympics [Q3498987::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.48 seconds
- Tokens Used: 4350 (Prompt: 4305, Completion: 45)
- Retrieved Subgraph Chunks: `Q3498987::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 18 nations competed in Wrestling at the 1992 Summer Olympics – Men's freestyle 100 kg [Q3498987::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.16 seconds
- Tokens Used: 1568 (Prompt: 1518, Completion: 50)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Wrestling at the 1992 Summer Olympics – Men's freestyle 100 kg", "attributes": {"name": "Men's freestyle 100 kg", "sport": "Wrestling", "discipline": "", "gender": "", "competitors": 18, "nations": 18}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Wrestling at the 1992 Summer Olympics – Men's freestyle 100 kg", "attributes": {"name": "Men's freestyle 100 kg", "sport": "Wrestling", "discipline": "", "gender": "", "competitors": 18, "nations": 18}}`
  - Supporting Document Chunks: `Q3498987::c0`
- Synthesized Prediction:
  > "Based on the verified database facts and supporting context, **18** nations competed in Wrestling at the 1992 Summer Olympics – Men's freestyle 100 kg [Q3498987::c0]."

### Question [92/100] — pub-092

- Query: "According to the provided corpus, how many shooting events at the 1992 Summer Olympics had more than 44 competitors?"
- Archetype: `aggregation`
- Ground Truth: `6`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.04 seconds
- Tokens Used: 5848 (Prompt: 5723, Completion: 125)
- Retrieved Context Chunks: `Q7500756::c0, Q7500774::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are **2** shooting events at the 1992 Summer Olympics that had more than 44 competitors:

1. **Men's 10 metre air pistol** with 45 competitors ([Q7500756::c0]).
2. **Women's 10 metre air pistol** with 47 competitors ([Q7500774::c0]).

Sources: [Q7500756::c0], [Q7500774::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.11 seconds
- Tokens Used: 4524 (Prompt: 4351, Completion: 173)
- Retrieved Subgraph Chunks: `Q7500756::c0, Q7500758::c0, Q7500764::c0`
- Synthesized Prediction:
  > "Based on the provided context and structured knowledge graph evidence, there were 13 total shooting events at the 1992 Summer Olympics. The evidence details the following events with their competitor counts:
- Men's 10 metre air pistol: 45 competitors [Q7500756::c0]
- Men's 10 metre air rifle: 44 competitors [Q7500758::c0]
- Men's 10 metre running target: 24 competitors
- Men's 25 metre rapid fire pistol: 30 competitors [Q7500764::c0]

Only one event (Men's 10 metre air pistol, with 45 competitors) had more than 44 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.59 seconds
- Tokens Used: 212 (Prompt: 182, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Shooting at the 1992 Summer Olympics – Men's 10 metre air pistol (45 competitors)", "Shooting at the 1992 Summer Olympics – Men's 50 metre rifle prone (52 competitors)", "Shooting at the 1992 Summer Olympics – Mixed skeet (60 competitors)", "Shooting at the 1992 Summer Olympics – Mixed trap (54 competitors)", "Shooting at the 1992 Summer Olympics – Women's 10 metre air rifle (45 competitors)", "Shooting at the 1992 Summer Olympics – Women's 10 metre air pistol (47 competitors)"], "competition": "1992 Summer", "threshold": 44, "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Shooting at the 1992 Summer Olympics – Men's 10 metre air pistol (45 competitors)", "Shooting at the 1992 Summer Olympics – Men's 50 metre rifle prone (52 competitors)", "Shooting at the 1992 Summer Olympics – Mixed skeet (60 competitors)", "Shooting at the 1992 Summer Olympics – Mixed trap (54 competitors)", "Shooting at the 1992 Summer Olympics – Women's 10 metre air rifle (45 competitors)", "Shooting at the 1992 Summer Olympics – Women's 10 metre air pistol (47 competitors)"], "competition": "1992 Summer", "threshold": 44, "sport": "Shooting"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 6 shooting events at the 1992 Summer Olympics that had more than 44 competitors."

### Question [93/100] — pub-093

- Query: "According to the provided corpus, how many biathlon events at the 2006 Winter Olympics had more than 72 competitors?"
- Archetype: `aggregation`
- Ground Truth: `4`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.49 seconds
- Tokens Used: 6616 (Prompt: 6485, Completion: 131)
- Retrieved Context Chunks: `Q915092::c0`
- Synthesized Prediction:
  > "Based on the provided context, there is only one biathlon event specifically noted as having "competitors: 72" (the Women's relay [Q915092::c0]), and the context passages do not mention any biathlon event at the 2006 Winter Olympics having *more* than 72 competitors. 

Therefore, the number of biathlon events at the 2006 Winter Olympics with more than 72 competitors is 0 (or unknown regarding any other events surpassing that number).

Sources cited:
- [Q915092::c0]"

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 5.94 seconds
- Tokens Used: 6084 (Prompt: 5963, Completion: 121)
- Retrieved Subgraph Chunks: `Q846788::c0, Q847288::c0, Q256529::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there is only one biathlon event at the 2006 Winter Olympics that had more than 72 competitors: the **Men's individual** event, which had 88 competitors [Q846788::c0]. 

(The other events mentioned in the context had fewer: the pursuit had 57 competitors [Q847288::c0] and the mass start had 30 competitors [Q256529::c0].) 

Therefore, the answer is **1**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 1.20 seconds
- Tokens Used: 212 (Prompt: 180, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Biathlon at the 2006 Winter Olympics – Men's individual (88 competitors)", "Biathlon at the 2006 Winter Olympics – Men's sprint (90 competitors)", "Biathlon at the 2006 Winter Olympics – Women's sprint (84 competitors)", "Biathlon at the 2006 Winter Olympics – Women's individual (82 competitors)"], "competition": "2006 Winter", "threshold": 72, "sport": "Biathlon"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Biathlon at the 2006 Winter Olympics – Men's individual (88 competitors)", "Biathlon at the 2006 Winter Olympics – Men's sprint (90 competitors)", "Biathlon at the 2006 Winter Olympics – Women's sprint (84 competitors)", "Biathlon at the 2006 Winter Olympics – Women's individual (82 competitors)"], "competition": "2006 Winter", "threshold": 72, "sport": "Biathlon"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the verified database result, there were 4 biathlon events at the 2006 Winter Olympics that had more than 72 competitors."

### Question [94/100] — pub-094

- Query: "Who won the gold medal in the men's greco-roman 48 kg wrestling event at the Summer Olympics held immediately before 1996?"
- Archetype: `temporal`
- Ground Truth: `Oleg Kucherenko`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.61 seconds
- Tokens Used: 4860 (Prompt: 4842, Completion: 18)
- Retrieved Context Chunks: `Q8037916::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q8037916::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.04 seconds
- Tokens Used: 4851 (Prompt: 4746, Completion: 105)
- Retrieved Subgraph Chunks: `Q3499058::c0, Q3565605::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's Greco-Roman 48 kg wrestling event at the 1992 Summer Olympics (held immediately before the 1996 Summer Olympics) was won by **Oleg Kucherenko** [Q3499058::c0]. 

*(Note: Vincenzo Maenza also won gold in this event at the 1988 Summer Olympics [Q3565605::c0]).*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 21.07 seconds
- Tokens Used: 12615 (Prompt: 12509, Completion: 106)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "1992 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "1992 Summer", "matched_event": "Wrestling at the 1992 Summer Olympics – Men's Greco-Roman 48 kg", "gold_winner": "Oleg Kucherenko", "date_held": ""}`
  - Supporting Document Chunks: `Q3499058::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting passages, the Summer Olympics held immediately before the 1996 Games was the 1992 Summer Olympics. 

The gold medal winner in the **Men's Greco-Roman 48 kg** wrestling event (full event title: **Wrestling at the 1992 Summer Olympics – Men's Greco-Roman 48 kg**) was **Oleg Kucherenko** [Q3499058::c0]."

### Question [95/100] — pub-095

- Query: "Who won the gold medal in the event held at Beijing National Stadium on 16 August 2008?"
- Archetype: `multi_hop`
- Ground Truth: `Valerie Vili`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.79 seconds
- Tokens Used: 9285 (Prompt: 9239, Completion: 46)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context passages, there is no mention of any events held on 16 August 2008 at the Beijing National Stadium. Therefore, the answer cannot be determined.

Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.47 seconds
- Tokens Used: 4872 (Prompt: 4814, Completion: 58)
- Retrieved Subgraph Chunks: `Q754844::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's 100 metres event held at the Beijing National Stadium on 16 August 2008 was won by **Usain Bolt** of Jamaica [Q754844::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 34.03 seconds
- Tokens Used: 2943 (Prompt: 2862, Completion: 81)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Beijing National Stadium", "date_constraint": "16 august 2008", "year_filter": "2008", "event": "Athletics at the 2008 Summer Olympics – Women's shot put", "gold_winners": ["Valerie Vili"], "date_matched": true, "candidate_events_checked": 37}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Beijing National Stadium", "date_constraint": "16 august 2008", "year_filter": "2008", "event": "Athletics at the 2008 Summer Olympics – Women's shot put", "gold_winners": ["Valerie Vili"], "date_matched": true, "candidate_events_checked": 37}`
  - Supporting Document Chunks: `Q848278::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal for the event held at the Beijing National Stadium on 16 August 2008 (Women's shot put / Athletics at the 2008 Summer Olympics – Women's shot put) was won by:

* **Valerie Vili** [Q848278::c0]"

### Question [96/100] — pub-096

- Query: "Who won the gold medal in the event held at Riocentro – Pavilion 6 on 10–21 August 2016?"
- Archetype: `multi_hop`
- Ground Truth: `Fazliddin Gaibnazarov`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 4.34 seconds
- Tokens Used: 3168 (Prompt: 2906, Completion: 262)
- Retrieved Context Chunks: `Q26037184::c0, Q26205999::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the boxing events held at the Riocentro are:
- Men's light flyweight boxing at the 2016 Summer Olympics, held at the Riocentro – Pavilion 6 from 6 to 14 August 2016 (won by Hasanboy Dusmatov) [Q26037184::c0].
- Men's flyweight boxing at the 2016 Summer Olympics, held at the Riocentro – Pavilion 6 from 13 to 21 August 2016 (won by Shakhobidin Zoirov) [Q26205999::c0].

An event spanning from "10–21 August 2016" is not specifically listed; however, the Men's flyweight boxing competition at Riocentro – Pavilion 6 took place from 13 to 21 August 2016 and was won by Shakhobidin Zoirov [Q26205999::c0]. If referring strictly to the exact date range "10–21 August 2016", it is unknown based on the provided context."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.39 seconds
- Tokens Used: 2969 (Prompt: 2747, Completion: 222)
- Retrieved Subgraph Chunks: `Q26037184::c0, Q26212152::c0, Q26205999::c0`
- Synthesized Prediction:
  > "Based on the provided context and knowledge graph evidence, multiple boxing events were held at Riocentro – Pavilion 6 during the 2016 Summer Olympics across different dates, with the following gold medalists in those weight classes:

* **Men's light flyweight** (6–14 August 2016): Hasanboy Dusmatov [Q26037184::c0]
* **Men's heavyweight** (6–15 August 2016): Evgeny Tishchenko
* **Men's light heavyweight** (6–18 August 2016): Julio César La Cruz
* **Men's bantamweight** (10–20 August 2016): Robeisy Ramírez [Q26212152::c0]
* **Men's flyweight** (13–21 August 2016): Shakhobidin Zoirov [Q26205999::c0]"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 13.72 seconds
- Tokens Used: 923 (Prompt: 837, Completion: 86)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Riocentro – Pavilion 6", "date_constraint": "10–21 august 2016", "year_filter": "2016", "event": "Boxing at the 2016 Summer Olympics – Men's light welterweight", "gold_winners": ["Fazliddin Gaibnazarov"], "date_matched": true, "candidate_events_checked": 13}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Riocentro – Pavilion 6", "date_constraint": "10–21 august 2016", "year_filter": "2016", "event": "Boxing at the 2016 Summer Olympics – Men's light welterweight", "gold_winners": ["Fazliddin Gaibnazarov"], "date_matched": true, "candidate_events_checked": 13}`
  - Supporting Document Chunks: `Q26212151::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal for the event held at Riocentro – Pavilion 6 from 10–21 August 2016 (Boxing at the 2016 Summer Olympics – Men's light welterweight) was won by **Fazliddin Gaibnazarov** [Q26212151::c0]."

### Question [97/100] — pub-097

- Query: "Who won the gold medal in the women's épée fencing event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Yana Shemyakina`

#### Pipeline 1: Standard RAG
- Accuracy: PASSED
- Latency: 3.30 seconds
- Tokens Used: 3532 (Prompt: 3468, Completion: 64)
- Retrieved Context Chunks: `Q1156695::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the women's épée fencing event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by Yana Shemyakina from Ukraine [Q1156695::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.93 seconds
- Tokens Used: 3757 (Prompt: 3695, Completion: 62)
- Retrieved Subgraph Chunks: `Q1156695::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the women's individual épée fencing event at the 2012 Summer Olympics (held immediately before 2016) was won by Yana Shemyakina of Ukraine [Q1156695::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 24.08 seconds
- Tokens Used: 7561 (Prompt: 7465, Completion: 96)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Fencing at the 2012 Summer Olympics – Women's épée", "gold_winner": "Yana Shemyakina", "date_held": "30 July"}`
  - Supporting Document Chunks: `Q1156695::c0`
- Synthesized Prediction:
  > "The gold medal in the women's épée fencing event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics) was won by **Yana Shemyakina** representing Ukraine [Q1156695::c0]. 

* **Event Name:** Women's épée
* **Full Event Title:** Fencing at the 2012 Summer Olympics – Women's épée"

### Question [98/100] — pub-098

- Query: "Who won the gold medal in the event held at Sydney Convention and Exhibition Centre on 18 September to 1 October 2000?"
- Archetype: `multi_hop`
- Ground Truth: `Bekzat Sattarkhanov`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 5.45 seconds
- Tokens Used: 4029 (Prompt: 4024, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 4.11 seconds
- Tokens Used: 3124 (Prompt: 3051, Completion: 73)
- Retrieved Subgraph Chunks: `Q4951838::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Sydney Convention and Exhibition Centre from 18 September to 1 October 2000 (Men's featherweight boxing at the 2000 Summer Olympics) was won by Bekzat Sattarkhanov [Q4951838::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 12.44 seconds
- Tokens Used: 1128 (Prompt: 1047, Completion: 81)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Sydney Convention and Exhibition Centre", "date_constraint": "18 september", "year_filter": "2000", "event": "Boxing at the 2000 Summer Olympics – Featherweight", "gold_winners": ["Bekzat Sattarkhanov"], "date_matched": true, "candidate_events_checked": 57}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sydney Convention and Exhibition Centre", "date_constraint": "18 september", "year_filter": "2000", "event": "Boxing at the 2000 Summer Olympics – Featherweight", "gold_winners": ["Bekzat Sattarkhanov"], "date_matched": true, "candidate_events_checked": 57}`
  - Supporting Document Chunks: `Q4951838::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the event held at the Sydney Convention and Exhibition Centre from 18 September to 1 October 2000 (Boxing at the 2000 Summer Olympics – Featherweight) was won by **Bekzat Sattarkhanov** (representing Kazakhstan) [Q4951838::c0]."

### Question [99/100] — pub-099

- Query: "Who won the gold medal in the event held at Laura Biathlon & Ski Complex on 22 February 2014?"
- Archetype: `multi_hop`
- Ground Truth: `Erik LesserDaniel BöhmArnd PeifferSimon Schempp`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 3.78 seconds
- Tokens Used: 9266 (Prompt: 9200, Completion: 66)
- Retrieved Context Chunks: `Q15052014::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the men's relay event held on 22 February 2014 was won by the German team consisting of Erik Lesser, Daniel Böhm, Arnd Peiffer, and Simon Schempp [Q15052014::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: FAILED
- Latency: 4.53 seconds
- Tokens Used: 7263 (Prompt: 7189, Completion: 74)
- Retrieved Subgraph Chunks: `Q15052014::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's relay event held at the Laura Biathlon & Ski Complex on 22 February 2014 was won by the German team consisting of Erik Lesser, Daniel Böhm, Arnd Peiffer, and Simon Schempp [Q15052014::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 15.07 seconds
- Tokens Used: 2515 (Prompt: 2346, Completion: 169)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Laura Biathlon & Ski Complex", "date_constraint": "22 february 2014", "year_filter": "2014", "event": "Biathlon at the 2014 Winter Olympics – Men's relay", "gold_winners": ["Erik Lesser, Daniel Arnd, Peiffer Simon, Schempp"], "date_matched": true, "candidate_events_checked": 23}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Laura Biathlon & Ski Complex", "date_constraint": "22 february 2014", "year_filter": "2014", "event": "Biathlon at the 2014 Winter Olympics – Men's relay", "gold_winners": ["Erik Lesser, Daniel Arnd, Peiffer Simon, Schempp"], "date_matched": true, "candidate_events_checked": 23}`
  - Supporting Document Chunks: `Q15052014::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the event held at the Laura Biathlon & Ski Complex on 22 February 2014 was **Biathlon at the 2014 Winter Olympics – Men's relay** [Q15052014::c0]. 

The gold medal was won by the **Germany** team, consisting of the following athletes:
* **Erik Lesser** [Q15052014::c0]
* **Daniel Böhm** [Q15052014::c0]
* **Arnd Peiffer** [Q15052014::c0]
* **Simon Schempp** [Q15052014::c0]"

### Question [100/100] — pub-100

- Query: "Who won the gold medal in the women's 200 metre backstroke swimming event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: `Missy Franklin`

#### Pipeline 1: Standard RAG
- Accuracy: FAILED
- Latency: 6.32 seconds
- Tokens Used: 7256 (Prompt: 7237, Completion: 19)
- Retrieved Context Chunks: `Q25932666::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q25932666::c0]."

#### Pipeline 2: GraphRAG
- Accuracy: PASSED
- Latency: 3.91 seconds
- Tokens Used: 6025 (Prompt: 5959, Completion: 66)
- Retrieved Subgraph Chunks: `Q2051400::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the women's 200 metre backstroke swimming event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by **Missy Franklin** [Q2051400::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Accuracy: PASSED
- Latency: 23.11 seconds
- Tokens Used: 14505 (Prompt: 14327, Completion: 178)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Swimming at the 2012 Summer Olympics – Women's 200 metre backstroke", "gold_winner": "Missy Franklin", "date_held": ""}`
  - Supporting Document Chunks: `Q2051400::c0`
- Synthesized Prediction:
  > "Based on the verified in-database graph facts and supporting context passages, the Summer Olympics held immediately before the 2016 Games were the **2012 Summer Olympics** (preceding competition: `2012 Summer`). 

The gold medal in the women's 200 metre backstroke swimming event at those Games was won by **Missy Franklin** [2012 Summer, Q2051400::c0].

* **Specific Event Name:** Women's 200 metre backstroke
* **Full Event Title:** Swimming at the 2012 Summer Olympics – Women's 200 metre backstroke [Q2051400::c0]
* **Gold Medalist:** Missy Franklin [Q2051400::c0]"

