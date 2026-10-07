# Comparative 3-Pipeline Benchmark Traces and Agent Execution Analysis

## Overview

This report documents the detailed comparative execution traces, reasoning paths, tool interactions, and synthesized outputs for all 50 held-out evaluation questions across all three benchmarked pipelines:

1. **Pipeline 1: Standard RAG** (Vector Search over document chunks)

2. **Pipeline 2: GraphRAG** (Entity Linking + 1-2 hop neighborhood traversal)

3. **Pipeline 3: Autonomous Agentic GraphRAG** (Dynamic LangGraph StateGraph + In-Database GSQL Accumulators + Multi-tier Fallback)

All questions were evaluated using the primary model configured in `.env`: Google Gemini (`gemini-3.5-flash-lite`).

## Held-Out 3-Pipeline Benchmark Summary

| Pipeline | Question Count | Model | Avg Tokens / Query | Avg Latency (s) | Evaluation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Standard RAG | 50 | gemini-3.5-flash-lite | 6048.2 | 3.10 | Raw Outputs Logged (Held-Out Benchmark Set) |
| GraphRAG | 50 | gemini-3.5-flash-lite | 5113.3 | 4.18 | Raw Outputs Logged (Held-Out Benchmark Set) |
| Agentic GraphRAG | 50 | gemini-3.5-flash-lite | 2929.7 | 6.07 | Raw Outputs Logged (Held-Out Benchmark Set) |

## Per-Archetype Question Distribution

| Archetype | Question Count | Evaluation Status |
| :--- | :--- | :--- |
| aggregation | 15 | Official Held-Out Evaluation |
| lookup | 7 | Official Held-Out Evaluation |
| multi_hop | 10 | Official Held-Out Evaluation |
| superlative | 10 | Official Held-Out Evaluation |
| temporal | 8 | Official Held-Out Evaluation |


## Question-by-Question 3-Pipeline Comparative Traces and Outputs

### Question [1/50] — eval-001

- Query: "Who won the gold medal in the event held at Olympic Tennis Centre on 15 to 22 August 2004?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 13.49 seconds
- Tokens Used: 5329 (Prompt: 5220, Completion: 109)
- Retrieved Context Chunks: `Q942805::c0, Q734997::c0`
- Synthesized Prediction:
  > "Based on the provided context, there are two events that took place at the Olympic Tennis Centre from 15 to 22 August 2004:

1. **Women's Doubles tennis:** The gold medal was won by China's **Li Ting and Sun Tiantian** [Q942805::c0].
2. **Men's Singles tennis:** The gold medal was won by Chile's **Nicolás Massú** [Q734997::c0]."

#### Pipeline 2: GraphRAG
- Latency: 7.22 seconds
- Tokens Used: 3718 (Prompt: 3640, Completion: 78)
- Retrieved Subgraph Chunks: `Q942805::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Olympic Tennis Centre from 15 to 22 August 2004 (Tennis at the 2004 Summer Olympics – Women's doubles) was won by **Li Ting** and **Sun Tiantian** (representing China) [Q942805::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.29 seconds
- Tokens Used: 910 (Prompt: 758, Completion: 152)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Olympic Tennis Centre", "date_constraint": "15 to 22 august 2004", "year_filter": "2004", "event": "Tennis at the 2004 Summer Olympics – Women's doubles", "gold_winners": ["Li Ting, Sun Tiantian"], "date_matched": true, "candidate_events_checked": 1}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Tennis Centre", "date_constraint": "15 to 22 august 2004", "year_filter": "2004", "event": "Tennis at the 2004 Summer Olympics – Women's doubles", "gold_winners": ["Li Ting, Sun Tiantian"], "date_matched": true, "candidate_events_checked": 1}`
  - Supporting Document Chunks: `Q942805::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the Women's doubles tennis event held at the Olympic Tennis Centre from 15 to 22 August 2004 was won by **Li Ting** and **Sun Tiantian** (representing China) [Q942805::c0]. 

* **Event:** Women's doubles tennis [Q942805::c0]
* **Full Event Title:** Tennis at the 2004 Summer Olympics – Women's doubles [Q942805::c0]
* **Gold Medalists:** Li Ting and Sun Tiantian [Q942805::c0]"

### Question [2/50] — eval-002

- Query: "How many nations competed in Fencing at the 1988 Summer Olympics – Men's foil?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 4.21 seconds
- Tokens Used: 5241 (Prompt: 5196, Completion: 45)
- Retrieved Context Chunks: `Q5443136::c0`
- Synthesized Prediction:
  > "Based on the provided context, 29 nations competed in the men's foil event at the 1988 Summer Olympics.

Source chunk: [Q5443136::c0]"

#### Pipeline 2: GraphRAG
- Latency: 2.75 seconds
- Tokens Used: 4955 (Prompt: 4915, Completion: 40)
- Retrieved Subgraph Chunks: `Q5443136::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 29 nations competed in the Men's foil event at the 1988 Summer Olympics [Q5443136::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.39 seconds
- Tokens Used: 2431 (Prompt: 2384, Completion: 47)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Fencing at the 1988 Summer Olympics – Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 68, "nations": 29}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Fencing at the 1988 Summer Olympics – Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 68, "nations": 29}}`
  - Supporting Document Chunks: `Q5443136::c0, Q5443136::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **29** nations competed in Fencing at the 1988 Summer Olympics – Men's foil [Q5443136::c0]."

### Question [3/50] — eval-003

- Query: "According to the provided corpus, how many cycling events at the 2008 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.29 seconds
- Tokens Used: 4669 (Prompt: 4564, Completion: 105)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context, the exact number of cycling events at the 2008 Summer Olympics that had more than 30 competitors cannot be explicitly determined, as the passages only provide full or partial start/results lists for specific events (such as the Men's individual road race, Women's individual road race, Men's sprint, and Women's BMX) without detailing the total number of events or their complete competitor counts across the entire Olympic cycling program. 

Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 2.99 seconds
- Tokens Used: 4824 (Prompt: 4688, Completion: 136)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the structured graph evidence, there are 3 cycling events at the 2008 Summer Olympics that had more than 30 competitors:

1. **Cycling at the 2008 Summer Olympics – Men's BMX** (32 competitors)
2. **Cycling at the 2008 Summer Olympics – Men's Madison** (32 competitors)
3. **Cycling at the 2008 Summer Olympics – Men's cross-country** (50 competitors)

*(Note: The Men's individual road race also had 143 competitors, as shown in the supporting text and graph).*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 3.83 seconds
- Tokens Used: 208 (Prompt: 178, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 8, "matching_events": ["Cycling at the 2008 Summer Olympics – Men's team sprint (39 competitors)", "Cycling at the 2008 Summer Olympics – Men's Madison (32 competitors)", "Cycling at the 2008 Summer Olympics – Men's team pursuit (44 competitors)", "Cycling at the 2008 Summer Olympics – Women's individual road race (66 competitors)", "Cycling at the 2008 Summer Olympics – Men's individual road race (143 competitors)", "Cycling at the 2008 Summer Olympics – Men's cross-country (50 competitors)", "Cycling at the 2008 Summer Olympics – Men's BMX (32 competitors)", "Cycling at the 2008 Summer Olympics – Men's road time trial (39 competitors)"], "competition": "2008 Summer", "threshold": 30, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 8, "matching_events": ["Cycling at the 2008 Summer Olympics – Men's team sprint (39 competitors)", "Cycling at the 2008 Summer Olympics – Men's Madison (32 competitors)", "Cycling at the 2008 Summer Olympics – Men's team pursuit (44 competitors)", "Cycling at the 2008 Summer Olympics – Women's individual road race (66 competitors)", "Cycling at the 2008 Summer Olympics – Men's individual road race (143 competitors)", "Cycling at the 2008 Summer Olympics – Men's cross-country (50 competitors)", "Cycling at the 2008 Summer Olympics – Men's BMX (32 competitors)", "Cycling at the 2008 Summer Olympics – Men's road time trial (39 competitors)"], "competition": "2008 Summer", "threshold": 30, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q1005322::c0, Q1005614::c0, Q635304::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 8 cycling events at the 2008 Summer Olympics that had more than 30 competitors."

### Question [4/50] — eval-004

- Query: "Who won the gold medal in the event held at Sydney International Shooting Centre on 22 September 2000?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.88 seconds
- Tokens Used: 6291 (Prompt: 6158, Completion: 133)
- Retrieved Context Chunks: `Q7500817::c0, Q7500807::c0`
- Synthesized Prediction:
  > "Based on the provided context, multiple shooting events were held on 22 September 2000 at the Sydney International Shooting Centre. The gold medalists for those events are:

* **Mariya Grozdeva** (BUL) won the gold medal in the Women's 25 metre pistol event [Q7500817::c0].
* **Yang Ling** (CHN) successfully defended his title to win the gold medal in the Men's 10 metre running target event (held on 21 and 22 September) [Q7500807::c0]."

#### Pipeline 2: GraphRAG
- Latency: 3.23 seconds
- Tokens Used: 4539 (Prompt: 4470, Completion: 69)
- Retrieved Subgraph Chunks: `Q7500807::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting context passages, **Yang Ling** won the gold medal in the men's 10 metre running target event held at the Sydney International Shooting Centre, which concluded on 22 September 2000 (fast run) [Q7500807::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.67 seconds
- Tokens Used: 1891 (Prompt: 1809, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Sydney International Shooting Centre", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics – Women's 25 metre pistol", "gold_winners": ["Mariya Grozdeva"], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sydney International Shooting Centre", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics – Women's 25 metre pistol", "gold_winners": ["Mariya Grozdeva"], "date_matched": true, "candidate_events_checked": 17}`
  - Supporting Document Chunks: `Q7500817::c0`
- Synthesized Prediction:
  > "**Mariya Grozdeva** won the gold medal in the **Women's 25 metre pistol** event (full event title: *Shooting at the 2000 Summer Olympics – Women's 25 metre pistol*) held at the Sydney International Shooting Centre on 22 September 2000 [Q7500817::c0]."

### Question [5/50] — eval-005

- Query: "According to the provided corpus, which sailing event at the 2016 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 4.36 seconds
- Tokens Used: 2957 (Prompt: 2898, Completion: 59)
- Retrieved Context Chunks: `Q26263261::c0`
- Synthesized Prediction:
  > "Based on the provided context, the sailing event at the 2016 Summer Olympics with the highest number of competitors was the **Men's 470**, which had 52 competitors.

Sources: [Q26263261::c0]"

#### Pipeline 2: GraphRAG
- Latency: 2.50 seconds
- Tokens Used: 2578 (Prompt: 2497, Completion: 81)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, the sailing events at the 2016 Summer Olympics with the highest number of competitors are the **Men's 49er** and the **Women's 49er FX**, both with **40 competitors** [Q26262259::c0, Q26262261::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.46 seconds
- Tokens Used: 741 (Prompt: 650, Completion: 91)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 52, "competition": "2016 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 52, "competition": "2016 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "Based on the provided graph facts and supporting context, the sailing event at the 2016 Summer Olympics with the highest number of competitors was the **Men's 470** (full event title: *Sailing at the 2004 Summer Olympics – Men's 470*), featuring **52** competitors [gsql_heapaccum, Q7400344::c0]."

### Question [6/50] — eval-006

- Query: "According to the provided corpus, how many cross-country skiing events at the 2010 Winter Olympics had more than 62 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.49 seconds
- Tokens Used: 7943 (Prompt: 7857, Completion: 86)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context passages, there is no mention of the total number of competitors in all cross-country skiing events that would allow determining how many events had more than 62 competitors (the provided snippets only list results for specific events and do not provide total competitor counts above 62 for each event as a whole, except for listing individual athletes up to certain ranks or numbers). 

Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 3.25 seconds
- Tokens Used: 7477 (Prompt: 7131, Completion: 346)
- Retrieved Subgraph Chunks: `Q384953::c0, Q848689::c0, Q843851::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there is **1** cross-country skiing event at the 2010 Winter Olympics that had more than 62 competitors:

* **Men's 15 kilometre freestyle**, which had **96 competitors** [Q384953::c0]. 

(For comparison, the Men's 30 kilometre pursuit had 64 competitors [Q848689::c0], but the prompt asks for events with *more than* 62 competitors—meaning both the Men's 15 kilometre freestyle and Men's 30 kilometre pursuit exceed 62, making a total of 2 events. Wait, let's verify: 96 > 62 and 64 > 62. Both exceed 62.)

Let's re-verify the competitor counts from the structured graph evidence and passages:
- Men's 15 kilometre freestyle: 96 competitors [Q384953::c0]
- Men's 30 kilometre pursuit: 64 competitors [Q848689::c0]
- Men's 50 kilometre classical: 55 competitors (from graph evidence)
- Men's sprint: 62 competitors [Q848689::c0] / [Q843851::c0]

Therefore, **2** events had more than 62 competitors (the Men's 15 kilometre freestyle with 96 and the Men's 30 kilometre pursuit with 64)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.78 seconds
- Tokens Used: 223 (Prompt: 0, Completion: 0)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 0, "matching_events": [], "competition": "2010 Winter", "threshold": 62, "sport": "Cross-country skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 0, "matching_events": [], "competition": "2010 Winter", "threshold": 62, "sport": "Cross-country skiing"}`
  - Supporting Document Chunks: `None`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 cross-country skiing events at the 2010 Winter Olympics that had more than 62 competitors."

### Question [7/50] — eval-007

- Query: "Who won the gold medal in the men's heavyweight boxing event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.62 seconds
- Tokens Used: 2613 (Prompt: 2607, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 2.97 seconds
- Tokens Used: 2907 (Prompt: 2859, Completion: 48)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's heavyweight boxing event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by Oleksandr Usyk."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 10.63 seconds
- Tokens Used: 5709 (Prompt: 5607, Completion: 102)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Boxing at the 2012 Summer Olympics – Men's heavyweight", "gold_winner": "Oleksandr Usyk", "date_held": "1–11 August 2012"}`
  - Supporting Document Chunks: `Q348720::c0, Q326382::c0, Q326384::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting documentation, the gold medal in the men's heavyweight boxing event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics in London) was won by **Oleksandr Usyk** [Q326384::c0]. 

* **Specific Event Name:** Men's heavyweight boxing
* **Full Event Title:** Boxing at the 2012 Summer Olympics – Men's heavyweight"

### Question [8/50] — eval-008

- Query: "According to the provided corpus, how many sailing events at the 1996 Summer Olympics had more than 46 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.47 seconds
- Tokens Used: 5880 (Prompt: 5874, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 3.66 seconds
- Tokens Used: 6687 (Prompt: 6333, Completion: 354)
- Retrieved Subgraph Chunks: `Q7400318::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and text passages, there are **3** sailing events at the 1996 Summer Olympics that had more than 46 competitors:

1. **Sailing at the 1996 Summer Olympics – Laser** – 56 competitors
2. **Sailing at the 1996 Summer Olympics – Men's 470** – 72 competitors
3. **Sailing at the 1996 Summer Olympics – Europe** – 28 competitors (Wait, 28 is not > 46, let's re-check the graph)

Let's check the competitor counts from the structured graph evidence:
* `Sailing at the 1996 Summer Olympics – Europe` : competitors = 28
* `Sailing at the 1996 Summer Olympics – Finn` : competitors = 31
* `Sailing at the 1996 Summer Olympics – Laser` : competitors = 56 (also in [Q7400318::c0])
* `Sailing at the 1996 Summer Olympics – Men's 470` : competitors = 72
* `Sailing at the 1996 Summer Olympics – Men's Mistral One Design` : competitors = 46 (not *more* than 46)

Thus, the events with *more* than 46 competitors are **Laser** (56) and **Men's 470** (72). 

Answer: **2** (Laser and Men's 470)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.54 seconds
- Tokens Used: 205 (Prompt: 175, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Sailing at the 1996 Summer Olympics – Soling (66 competitors)", "Sailing at the 1996 Summer Olympics – Men's 470 (72 competitors)", "Sailing at the 1996 Summer Olympics – Laser (56 competitors)", "Sailing at the 1996 Summer Olympics – Star (50 competitors)"], "competition": "1996 Summer", "threshold": 46, "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Sailing at the 1996 Summer Olympics – Soling (66 competitors)", "Sailing at the 1996 Summer Olympics – Men's 470 (72 competitors)", "Sailing at the 1996 Summer Olympics – Laser (56 competitors)", "Sailing at the 1996 Summer Olympics – Star (50 competitors)"], "competition": "1996 Summer", "threshold": 46, "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400322::c0, Q7400319::c0, Q7400319::c1`
- Synthesized Prediction:
  > "According to the provided database, there were 4 sailing events at the 1996 Summer Olympics that had more than 46 competitors."

### Question [9/50] — eval-009

- Query: "According to the provided corpus, which sailing event at the 2004 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 6.72 seconds
- Tokens Used: 1819 (Prompt: 1754, Completion: 65)
- Retrieved Context Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the sailing event at the 2004 Summer Olympics with the highest number of competitors was the **Men's 470**, which had 54 competitors (54 sailors).

Sources:
- [Q7400344::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.12 seconds
- Tokens Used: 1801 (Prompt: 1763, Completion: 38)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, the sailing event at the 2004 Summer Olympics with the highest number of competitors was the **Laser** event, which had 42 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.28 seconds
- Tokens Used: 734 (Prompt: 650, Completion: 84)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 54, "competition": "2004 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics – Men's 470", "competitors": 54, "competition": "2004 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the sailing event at the 2004 Summer Olympics with the highest number of competitors was the **Men's 470** (full event title: *Sailing at the 2004 Summer Olympics – Men's 470*), with a total of **54** competitors [Q7400344::c0]."

### Question [10/50] — eval-010

- Query: "How many nations competed in Boxing at the 1996 Summer Olympics – Flyweight?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.81 seconds
- Tokens Used: 2464 (Prompt: 2422, Completion: 42)
- Retrieved Context Chunks: `Q10497009::c0`
- Synthesized Prediction:
  > "Based on the provided context, 32 nations competed in the Flyweight boxing event at the 1996 Summer Olympics.

[Q10497009::c0]"

#### Pipeline 2: GraphRAG
- Latency: 2.92 seconds
- Tokens Used: 1796 (Prompt: 1755, Completion: 41)
- Retrieved Subgraph Chunks: `Q10497009::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 32 nations competed in the Boxing at the 1996 Summer Olympics – Flyweight event [Q10497009::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.08 seconds
- Tokens Used: 643 (Prompt: 572, Completion: 71)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Boxing at the 1996 Summer Olympics – Flyweight", "attributes": {"name": "Flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 32, "nations": 32}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Boxing at the 1996 Summer Olympics – Flyweight", "attributes": {"name": "Flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 32, "nations": 32}}`
  - Supporting Document Chunks: `Q10497009::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, 32 nations competed in the Flyweight boxing event at the 1996 Summer Olympics (Event name: *Flyweight boxing*, Full title: *Boxing at the 1996 Summer Olympics – Flyweight*) [Q10497009::c0]."

### Question [11/50] — eval-011

- Query: "According to the provided corpus, how many weightlifting events at the 1992 Summer Olympics had more than 24 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 4.41 seconds
- Tokens Used: 9557 (Prompt: 9016, Completion: 541)
- Retrieved Context Chunks: `Q7979977::c0, Q7979973::c0, Q7979974::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are **3** weightlifting events at the 1992 Summer Olympics that had more than 24 competitors:

1. **Men's 82.5 kg** with 31 competitors [Q7979977::c0]
2. **Men's 60 kg** with 31 competitors [Q7979973::c0]
3. **Men's 90 kg** with 23 competitors? Wait, let's check:
   - Men's 67.5 kg: 18 competitors [Q7979974::c0]
   - Men's 90 kg: 23 competitors [Q797998::c0]
   - Men's 56 kg: 22 competitors [Q7979972::c0]
   - Men's 82.5 kg: 31 competitors [Q7979977::c0]
   - Men's 60 kg: 31 competitors [Q7979973::c0]

Let's re-verify the count of events with *more than 24* competitors from the provided texts:
- Men's 67.5 kg: 18 competitors [Q7979974::c0] (Not > 24)
- Men's 90 kg: 23 competitors [Q7979978::c0] (Not > 24)
- Men's 56 kg: 22 competitors [Q7979972::c0] (Not > 24)
- Men's 82.5 kg: 31 competitors [Q7979977::c0] (> 24)
- Men's 60 kg: 31 competitors [Q7979973::c0] (> 24)

Therefore, exactly **2** events from the provided context had more than 24 competitors (the Men's 82.5 kg event and the Men's 60 kg event, both with 31 competitors).

**Sources:**
- [Q7979973::c0]
- [Q7979977::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.02 seconds
- Tokens Used: 5912 (Prompt: 5778, Completion: 134)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, there is **1** weightlifting event at the 1992 Summer Olympics that had more than 24 competitors:

* **Men's 100 kg** with **25 competitors** (as indicated by the structured graph evidence: `(1992 Summer)-[:INCLUDES_EVENT]->(Weightlifting at the 1992 Summer Olympics – Men's 100 kg [sport=Weightlifting, competitors=25])`).

(Note: The other listed events had 20, 24, 17, and 22 competitors respectively.)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.12 seconds
- Tokens Used: 216 (Prompt: 185, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Weightlifting at the 1992 Summer Olympics – Men's 82.5 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 60 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 75 kg (34 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 100 kg (25 competitors)"], "competition": "1992 Summer", "threshold": 24, "sport": "Weightlifting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Weightlifting at the 1992 Summer Olympics – Men's 82.5 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 60 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 75 kg (34 competitors)", "Weightlifting at the 1992 Summer Olympics – Men's 100 kg (25 competitors)"], "competition": "1992 Summer", "threshold": 24, "sport": "Weightlifting"}`
  - Supporting Document Chunks: `Q7979977::c0, Q7979973::c0, Q7979975::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 weightlifting events at the 1992 Summer Olympics that had more than 24 competitors."

### Question [12/50] — eval-012

- Query: "How many nations competed in Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.10 seconds
- Tokens Used: 5549 (Prompt: 5503, Completion: 46)
- Retrieved Context Chunks: `Q25991452::c0`
- Synthesized Prediction:
  > "Based on the provided context, 32 nations competed in the men's 100 metre butterfly event at the 2016 Summer Olympics [Q25991452::c0]."

#### Pipeline 2: GraphRAG
- Latency: 2.80 seconds
- Tokens Used: 5535 (Prompt: 5489, Completion: 46)
- Retrieved Subgraph Chunks: `Q25991452::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 32 nations competed in the Men's 100 metre butterfly event at the 2016 Summer Olympics [Q25991452::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.66 seconds
- Tokens Used: 2804 (Prompt: 2731, Completion: 73)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly", "attributes": {"name": "Men's 100 metre butterfly", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 43, "nations": 32}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly", "attributes": {"name": "Men's 100 metre butterfly", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 43, "nations": 32}}`
  - Supporting Document Chunks: `Q25991452::c0, Q25991452::c1`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **32** nations competed in the Men's 100 metre butterfly event at the 2016 Summer Olympics (Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly) [Q25991452::c0]."

### Question [13/50] — eval-013

- Query: "According to the provided corpus, how many cycling events at the 2016 Summer Olympics had more than 27 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.12 seconds
- Tokens Used: 6780 (Prompt: 6653, Completion: 127)
- Retrieved Context Chunks: `Q26260943::c0, Q26260960::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 cycling events at the 2016 Summer Olympics that had more than 27 competitors:
1. The **Men's team pursuit** had 40 competitors [Q26260943::c0].
2. The **Women's team pursuit** had 39 competitors [Q26260960::c0].

Sources cited:
- [Q26260943::c0]
- [Q26260960::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.03 seconds
- Tokens Used: 5786 (Prompt: 5625, Completion: 161)
- Retrieved Subgraph Chunks: `Q24760634::c0, Q25476845::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, there are **2** cycling events at the 2016 Summer Olympics listed with more than 27 competitors:

1. **Cycling at the 2016 Summer Olympics – Men's individual road race** with **144** competitors [Q24760634::c0].
2. **Cycling at the 2016 Summer Olympics – Men's cross-country** with **49** competitors [Q25476845::c0]. 

*(Note: The Men's keirin had 27 competitors and the Men's omnium had 18 competitors, neither of which is strictly greater than 27).*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.45 seconds
- Tokens Used: 211 (Prompt: 180, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Cycling at the 2016 Summer Olympics – Men's individual road race (144 competitors)", "Cycling at the 2016 Summer Olympics – Women's individual road race (68 competitors)", "Cycling at the 2016 Summer Olympics – Men's team pursuit (40 competitors)", "Cycling at the 2016 Summer Olympics – Men's cross-country (49 competitors)", "Cycling at the 2016 Summer Olympics – Women's cross-country (29 competitors)", "Cycling at the 2016 Summer Olympics – Women's team pursuit (39 competitors)"], "competition": "2016 Summer", "threshold": 27, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Cycling at the 2016 Summer Olympics – Men's individual road race (144 competitors)", "Cycling at the 2016 Summer Olympics – Women's individual road race (68 competitors)", "Cycling at the 2016 Summer Olympics – Men's team pursuit (40 competitors)", "Cycling at the 2016 Summer Olympics – Men's cross-country (49 competitors)", "Cycling at the 2016 Summer Olympics – Women's cross-country (29 competitors)", "Cycling at the 2016 Summer Olympics – Women's team pursuit (39 competitors)"], "competition": "2016 Summer", "threshold": 27, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q24760634::c0, Q24760634::c1, Q24761058::c0`
- Synthesized Prediction:
  > "According to the verified database results, there were 6 cycling events at the 2016 Summer Olympics that had more than 27 competitors."

### Question [14/50] — eval-014

- Query: "Who won the gold medal in the event held at San Sicario on February 15, 2006?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.10 seconds
- Tokens Used: 6554 (Prompt: 6499, Completion: 55)
- Retrieved Context Chunks: `Q771123::c0`
- Synthesized Prediction:
  > "Based on the provided context, Michaela Dorfmeister won the gold medal in the event held at San Sicario on February 15, 2006 (the women's downhill event).

Sources: [Q771123::c0]"

#### Pipeline 2: GraphRAG
- Latency: 2.44 seconds
- Tokens Used: 5529 (Prompt: 5474, Completion: 55)
- Retrieved Subgraph Chunks: `Q771123::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, **Michaela Dorfmeister** won the gold medal in the event held at San Sicario on February 15, 2006 (the Women's downhill) [Q771123::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 2.90 seconds
- Tokens Used: 1228 (Prompt: 1157, Completion: 71)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "San Sicario", "date_constraint": "february 15, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics – Women's downhill", "gold_winners": ["Michaela Dorfmeister"], "date_matched": true, "candidate_events_checked": 3}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "San Sicario", "date_constraint": "february 15, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics – Women's downhill", "gold_winners": ["Michaela Dorfmeister"], "date_matched": true, "candidate_events_checked": 3}`
  - Supporting Document Chunks: `Q771123::c0`
- Synthesized Prediction:
  > "**Michaela Dorfmeister** won the gold medal in the **Women's downhill** event (full event title: *Alpine skiing at the 2006 Winter Olympics – Women's downhill*) held at San Sicario on February 15, 2006 [Q771123::c0]."

### Question [15/50] — eval-015

- Query: "How many nations competed in Athletics at the 2016 Summer Olympics – Men's 400 metres?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.14 seconds
- Tokens Used: 7071 (Prompt: 7024, Completion: 47)
- Retrieved Context Chunks: `Q26219858::c0`
- Synthesized Prediction:
  > "Based on the provided context, 35 nations competed in the Men's 400 metres event at the 2016 Summer Olympics.

[Q26219858::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.34 seconds
- Tokens Used: 4920 (Prompt: 4875, Completion: 45)
- Retrieved Subgraph Chunks: `Q26219858::c0`
- Synthesized Prediction:
  > "Based on the provided context, 35 nations competed in the men's 400 metres event at the 2016 Summer Olympics [Q26219858::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.50 seconds
- Tokens Used: 3296 (Prompt: 3214, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Athletics at the 2016 Summer Olympics – Men's 400 metres", "attributes": {"name": "Men's 400 metres", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 53, "nations": 35}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Athletics at the 2016 Summer Olympics – Men's 400 metres", "attributes": {"name": "Men's 400 metres", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 53, "nations": 35}}`
  - Supporting Document Chunks: `Q26219858::c0, Q26219858::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **35** nations competed in the Men's 400 metres at the 2016 Summer Olympics (full event title: *Athletics at the 2016 Summer Olympics – Men's 400 metres*) [graph_lookup, Q26219858::c0]."

### Question [16/50] — eval-016

- Query: "How many nations competed in Athletics at the 2008 Summer Olympics – Women's shot put?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.07 seconds
- Tokens Used: 6818 (Prompt: 6778, Completion: 40)
- Retrieved Context Chunks: `Q848278::c0`
- Synthesized Prediction:
  > "Based on the provided context, 22 nations competed in the women's shot put event at the 2008 Summer Olympics [Q848278::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.19 seconds
- Tokens Used: 5835 (Prompt: 5795, Completion: 40)
- Retrieved Subgraph Chunks: `Q848278::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, 22 nations competed in the Women's shot put event at the 2008 Summer Olympics [Q848278::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.60 seconds
- Tokens Used: 2316 (Prompt: 2234, Completion: 82)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Athletics at the 2008 Summer Olympics – Women's shot put", "attributes": {"name": "Women's shot put", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 35, "nations": 22}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Athletics at the 2008 Summer Olympics – Women's shot put", "attributes": {"name": "Women's shot put", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 35, "nations": 22}}`
  - Supporting Document Chunks: `Q848278::c0, Q848278::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting passages, **22** nations competed in the Women's shot put event at the 2008 Summer Olympics [Q848278::c0]. 

* **Specific Event Name:** Women's shot put
* **Full Event Title:** Athletics at the 2008 Summer Olympics – Women's shot put"

### Question [17/50] — eval-017

- Query: "Who won the gold medal in the event held at Eton Dorney on 28 July – 4 August 2012?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.06 seconds
- Tokens Used: 7311 (Prompt: 7305, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 5.00 seconds
- Tokens Used: 5384 (Prompt: 5379, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 9.65 seconds
- Tokens Used: 3745 (Prompt: 3670, Completion: 75)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Eton Dorney", "date_constraint": "28 july", "year_filter": "2012", "event": "Rowing at the 2012 Summer Olympics – Women's single sculls", "gold_winners": ["Miroslava Knapková"], "date_matched": true, "candidate_events_checked": 24}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Eton Dorney", "date_constraint": "28 july", "year_filter": "2012", "event": "Rowing at the 2012 Summer Olympics – Women's single sculls", "gold_winners": ["Miroslava Knapková"], "date_matched": true, "candidate_events_checked": 24}`
  - Supporting Document Chunks: `Q1222270::c0, Q1222270::c1`
- Synthesized Prediction:
  > "The gold medal in the event held at Eton Dorney from 28 July – 4 August 2012 (Rowing at the 2012 Summer Olympics – Women's single sculls) was won by **Miroslava Knapková** (representing the Czech Republic) [Q1222270::c0]."

### Question [18/50] — eval-018

- Query: "Who won the gold medal in the event held at Olympic Stadium on 16–18 August 2016?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.68 seconds
- Tokens Used: 8849 (Prompt: 8697, Completion: 152)
- Retrieved Context Chunks: `Q26234119::c0, Q26215594::c0`
- Synthesized Prediction:
  > "Based on the provided context, the event held at the Olympic Stadium on 12–15 August 2016 was the women's hammer throw, in which Anita Włodarczyk won the gold medal [Q26234119::c0]. (Note: The men's hammer throw took place at the *Estádio Olímpico João Havelange* between 17–19 August 2016 [Q26215594::c0], and no event is listed in the text as being held at the Olympic Stadium on 16–18 August). 

Source chunk used: [Q26234119::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.40 seconds
- Tokens Used: 4942 (Prompt: 4758, Completion: 184)
- Retrieved Subgraph Chunks: `Q26203840::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the specific event held at the Olympic Stadium *strictly* on "16–18 August 2016" is not explicitly listed with that exact date range in the text (the 110m hurdles was 15–16 August, the 3000m steeplechase was 15–17 August, the 100m was 13–14 August, and the 10,000 metres does not specify full event dates). 

However, if looking at events concluding or taking place around August 16:
- **Omar McLeod** won the gold medal in the men's 110 metres hurdles (held 15–16 August 2016) [Q26203840::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 12.11 seconds
- Tokens Used: 2111 (Prompt: 1947, Completion: 164)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "16–18 august 2016", "year_filter": "2016", "event": "Athletics at the 2016 Summer Olympics – Women's javelin throw", "gold_winners": ["Sara Kolak"], "date_matched": true, "candidate_events_checked": 32}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "16–18 august 2016", "year_filter": "2016", "event": "Athletics at the 2016 Summer Olympics – Women's javelin throw", "gold_winners": ["Sara Kolak"], "date_matched": true, "candidate_events_checked": 32}`
  - Supporting Document Chunks: `Q26234144::c0, Q26234144::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context passages, the gold medal in the event held at the Olympic Stadium on 16–18 August 2016 was won by **Sara Kolak** [Q26234144::c0]. 

* **Event Name:** Women's javelin throw [Q26234144::c0]
* **Full Event Title:** Athletics at the 2016 Summer Olympics – Women's javelin throw [Q26234144::c0]
* **Gold Medalist:** Sara Kolak (representing Croatia, with a winning distance of 66.18 m) [Q26234144::c0]"

### Question [19/50] — eval-019

- Query: "According to the provided corpus, how many alpine skiing events at the 1998 Winter Olympics had more than 45 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.47 seconds
- Tokens Used: 8868 (Prompt: 8708, Completion: 160)
- Retrieved Context Chunks: `Q1005576::c0, Q1005749::c0, Q1222646::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, none of the alpine skiing events listed had more than 45 competitors (the men's downhill had 43 [Q1005576::c0], the men's super-G had 45 [Q1005749::c0], and the women's super-G had 43 [Q1222646::c0]). Therefore, the number of alpine skiing events with more than 45 competitors is 0.

Sources:
- [Q1005576::c0]
- [Q1005749::c0]
- [Q1222646::c0]"

#### Pipeline 2: GraphRAG
- Latency: 2.82 seconds
- Tokens Used: 6338 (Prompt: 6236, Completion: 102)
- Retrieved Subgraph Chunks: `Q1005810::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, there is only **1** alpine skiing event at the 1998 Winter Olympics that had more than 45 competitors:

* **Men's giant slalom** with **62 competitors** ([Q1005810::c0]).

The other mentioned events had 43 competitors (Men's downhill) and 38 competitors (Men's combined), which are not more than 45."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.37 seconds
- Tokens Used: 212 (Prompt: 180, Completion: 32)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Alpine skiing at the 1998 Winter Olympics – Women's slalom (57 competitors)", "Alpine skiing at the 1998 Winter Olympics – Men's slalom (65 competitors)", "Alpine skiing at the 1998 Winter Olympics – Women's giant slalom (56 competitors)", "Alpine skiing at the 1998 Winter Olympics – Men's giant slalom (62 competitors)"], "competition": "1998 Winter", "threshold": 45, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Alpine skiing at the 1998 Winter Olympics – Women's slalom (57 competitors)", "Alpine skiing at the 1998 Winter Olympics – Men's slalom (65 competitors)", "Alpine skiing at the 1998 Winter Olympics – Women's giant slalom (56 competitors)", "Alpine skiing at the 1998 Winter Olympics – Men's giant slalom (62 competitors)"], "competition": "1998 Winter", "threshold": 45, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1222533::c0, Q1005643::c0, Q1222717::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 4 alpine skiing events at the 1998 Winter Olympics that had more than 45 competitors."

### Question [20/50] — eval-020

- Query: "Who won the gold medal in the event held at Royal Artillery Barracks on 5 August 2012?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.33 seconds
- Tokens Used: 6088 (Prompt: 6083, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Latency: 4.35 seconds
- Tokens Used: 5389 (Prompt: 5328, Completion: 61)
- Retrieved Subgraph Chunks: `Q2353475::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the event held at the Royal Artillery Barracks on 5 August 2012 (the Men's 50 metre pistol) was won by **Jin Jong-oh** [Q2353475::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 5.42 seconds
- Tokens Used: 3398 (Prompt: 3261, Completion: 137)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Royal Artillery Barracks", "date_constraint": "5 august 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics – Men's 50 metre pistol", "gold_winners": ["Jin Jong-oh"], "date_matched": true, "candidate_events_checked": 12}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Royal Artillery Barracks", "date_constraint": "5 august 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics – Men's 50 metre pistol", "gold_winners": ["Jin Jong-oh"], "date_matched": true, "candidate_events_checked": 12}`
  - Supporting Document Chunks: `Q2353475::c0, Q2353475::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **Jin Jong-oh** won the gold medal in the Men's 50 metre pistol event at the Royal Artillery Barracks on 5 August 2012 [Q2353475::c0]. 

* **Event:** Men's 50 metre pistol (Shooting at the 2012 Summer Olympics – Men's 50 metre pistol) [Q2353475::c0]
* **Gold Medalist:** Jin Jong-oh (South Korea) [Q2353475::c0]"

### Question [21/50] — eval-021

- Query: "Who won the gold medal in the men's 200 metre backstroke swimming event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 1.97 seconds
- Tokens Used: 7907 (Prompt: 7888, Completion: 19)
- Retrieved Context Chunks: `Q25991449::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q25991449::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.60 seconds
- Tokens Used: 6071 (Prompt: 6005, Completion: 66)
- Retrieved Subgraph Chunks: `Q2071160::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's 200 metre backstroke swimming event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by **Tyler Clary** [Q2071160::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.55 seconds
- Tokens Used: 15758 (Prompt: 15548, Completion: 210)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Swimming at the 2012 Summer Olympics – Men's 200 metre backstroke", "gold_winner": "Tyler Clary", "date_held": ""}`
  - Supporting Document Chunks: `Q2071160::c0, Q916930::c0, Q905555::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting passages, the Summer Olympics held immediately before the 2016 Summer Games were the 2012 Summer Olympics [temporal_precedes]. 

The gold medal in the men's 200 metre backstroke swimming event at the 2012 Summer Olympics was won by **Tyler Clary** (representing the United States) [temporal_precedes, Q2071160::c0]. 

* **Specific Event Name:** Men's 200 metre backstroke
* **Full Event Title:** Swimming at the 2012 Summer Olympics – Men's 200 metre backstroke [temporal_precedes, Q2071160::c0]
* **Gold Medalist:** Tyler Clary [temporal_precedes, Q2071160::c0]
* **Chunk Citation:** [Q2071160::c0]"

### Question [22/50] — eval-022

- Query: "How many nations competed in Cross-country skiing at the 2014 Winter Olympics – Men's sprint?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.35 seconds
- Tokens Used: 8540 (Prompt: 8491, Completion: 49)
- Retrieved Context Chunks: `Q15055036::c0`
- Synthesized Prediction:
  > "Based on the provided context, 40 nations competed in the men's sprint cross-country skiing event at the 2014 Winter Olympics.

Source: [Q15055036::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.25 seconds
- Tokens Used: 6490 (Prompt: 6485, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.51 seconds
- Tokens Used: 2202 (Prompt: 2159, Completion: 43)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2014 Winter Olympics – Men's sprint", "attributes": {"name": "Men's sprint", "sport": "", "discipline": "", "gender": "", "competitors": 86, "nations": 40}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2014 Winter Olympics – Men's sprint", "attributes": {"name": "Men's sprint", "sport": "", "discipline": "", "gender": "", "competitors": 86, "nations": 40}}`
  - Supporting Document Chunks: `Q15055036::c0, Q15055036::c1`
- Synthesized Prediction:
  > "A total of **40 nations** competed in the Cross-country skiing at the 2014 Winter Olympics – Men's sprint [Q15055036::c0]."

### Question [23/50] — eval-023

- Query: "According to the provided corpus, how many shooting events at the 2000 Summer Olympics had more than 42 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.78 seconds
- Tokens Used: 7329 (Prompt: 7094, Completion: 235)
- Retrieved Context Chunks: `Q7500809::c0, Q7500810::c0, Q7500817::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there were 36 competitors in the men's 50 metre pistol [Q7500809::c0], 20 competitors in the men's 25 metre rapid fire pistol [Q7500810::c0], 42 competitors in the women's 25 metre pistol [Q7500817::c0], and 44 competitors in the men's 50 metre rifle three positions [Q7500813::c0]. 

Therefore, only **1** shooting event (the men's 50 metre rifle three positions with 44 competitors) had more than 42 competitors [Q7500813::c0].

**Citations:**
- [Q7500809::c0]
- [Q7500810::c0]
- [Q7500817::c0]
- [Q7500813::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.09 seconds
- Tokens Used: 4818 (Prompt: 4694, Completion: 124)
- Retrieved Subgraph Chunks: `Q4443765::c0, Q4443763::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, there are **2** shooting events at the 2000 Summer Olympics that had more than 42 competitors:

1. **Shooting at the 2000 Summer Olympics – Men's 10 metre air pistol** with 43 competitors [Q4443765::c0].
2. **Shooting at the 2000 Summer Olympics – Men's 10 metre air rifle** with 46 competitors [Q4443763::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.15 seconds
- Tokens Used: 212 (Prompt: 182, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 7, "matching_events": ["Shooting at the 2000 Summer Olympics – Women's 10 metre air rifle (49 competitors)", "Shooting at the 2000 Summer Olympics – Men's 50 metre rifle prone (53 competitors)", "Shooting at the 2000 Summer Olympics – Men's 10 metre air rifle (46 competitors)", "Shooting at the 2000 Summer Olympics – Men's skeet (49 competitors)", "Shooting at the 2000 Summer Olympics – Men's 50 metre rifle three positions (44 competitors)", "Shooting at the 2000 Summer Olympics – Men's 10 metre air pistol (43 competitors)", "Shooting at the 2000 Summer Olympics – Women's 10 metre air pistol (45 competitors)"], "competition": "2000 Summer", "threshold": 42, "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 7, "matching_events": ["Shooting at the 2000 Summer Olympics – Women's 10 metre air rifle (49 competitors)", "Shooting at the 2000 Summer Olympics – Men's 50 metre rifle prone (53 competitors)", "Shooting at the 2000 Summer Olympics – Men's 10 metre air rifle (46 competitors)", "Shooting at the 2000 Summer Olympics – Men's skeet (49 competitors)", "Shooting at the 2000 Summer Olympics – Men's 50 metre rifle three positions (44 competitors)", "Shooting at the 2000 Summer Olympics – Men's 10 metre air pistol (43 competitors)", "Shooting at the 2000 Summer Olympics – Women's 10 metre air pistol (45 competitors)"], "competition": "2000 Summer", "threshold": 42, "sport": "Shooting"}`
  - Supporting Document Chunks: `Q4354069::c0, Q7500812::c0, Q4443763::c0`
- Synthesized Prediction:
  > "According to the verified database, there were 7 shooting events at the 2000 Summer Olympics that had more than 42 competitors."

### Question [24/50] — eval-024

- Query: "According to the provided corpus, which cross-country skiing event at the 1998 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.38 seconds
- Tokens Used: 8769 (Prompt: 8708, Completion: 61)
- Retrieved Context Chunks: `Q1004937::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the cross-country skiing event at the 1998 Winter Olympics with the highest number of competitors was the **Men's 10 kilometre classical** event, which had 97 competitors [Q1004937::c0]."

#### Pipeline 2: GraphRAG
- Latency: 3.38 seconds
- Tokens Used: 7355 (Prompt: 7296, Completion: 59)
- Retrieved Subgraph Chunks: `Q1004937::c0`
- Synthesized Prediction:
  > "Based on the provided context, the cross-country skiing event at the 1998 Winter Olympics with the highest number of competitors was the **Men's 10 kilometre classical**, which had **97 competitors** [Q1004937::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.17 seconds
- Tokens Used: 2431 (Prompt: 2340, Completion: 91)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_heapaccum` -> Details: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 10 kilometre classical", "full_event_title": "Cross-country skiing at the 1998 Winter Olympics – Men's 10 kilometre classical", "competitors": 97, "competition": "1998 Winter", "sport": "Cross-country skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 10 kilometre classical", "full_event_title": "Cross-country skiing at the 1998 Winter Olympics – Men's 10 kilometre classical", "competitors": 97, "competition": "1998 Winter", "sport": "Cross-country skiing"}`
  - Supporting Document Chunks: `Q1004937::c0`
- Synthesized Prediction:
  > "Based on the provided corpus and database facts, the cross-country skiing event at the 1998 Winter Olympics with the highest number of competitors was the **Men's 10 kilometre classical** (full title: *Cross-country skiing at the 1998 Winter Olympics – Men's 10 kilometre classical*), which featured **97** competitors [Q1004937::c0]."

### Question [25/50] — eval-025

- Query: "According to the provided corpus, which rowing event at the 2016 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.26 seconds
- Tokens Used: 5926 (Prompt: 5875, Completion: 51)
- Retrieved Context Chunks: `Q22968979::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the rowing event at the 2016 Summer Olympics with the highest number of competitors was the Women's eight, with 56 competitors [Q22968979::c0]."

#### Pipeline 2: GraphRAG
- Latency: 7.10 seconds
- Tokens Used: 5984 (Prompt: 5911, Completion: 73)
- Retrieved Subgraph Chunks: `Q22968981::c0`
- Synthesized Prediction:
  > "Based on the structured graph evidence and supporting passages, the rowing events at the 2016 Summer Olympics with the highest number of competitors (52 competitors each) are:

1. **Men's coxless four**
2. **Men's lightweight coxless four** ([Q22968981::c0])"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 58.46 seconds
- Tokens Used: 1779 (Prompt: 1541, Completion: 238)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2016 Summer Olympics – Women's eight", "competitors": 56, "competition": "2016 Summer", "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2016 Summer Olympics – Women's eight", "competitors": 56, "competition": "2016 Summer", "sport": "Rowing"}`
  - Supporting Document Chunks: `Q22968979::c0`
- Synthesized Prediction:
  > "Women's eight (Rowing at the 2016 Summer Olympics – Women's eight) – 56 competitors【Q22968979::c0】"

### Question [26/50] — eval-026

- Query: "How many nations competed in Fencing at the 2000 Summer Olympics – Men's foil?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 9.07 seconds
- Tokens Used: 3447 (Prompt: 3408, Completion: 39)
- Retrieved Context Chunks: `Q632472::c0`
- Synthesized Prediction:
  > "Based on the provided context, 22 nations competed in the men's foil event at the 2000 Summer Olympics [Q632472::c0]."

#### Pipeline 2: GraphRAG
- Latency: 3.82 seconds
- Tokens Used: 2941 (Prompt: 2901, Completion: 40)
- Retrieved Subgraph Chunks: `Q632472::c0`
- Synthesized Prediction:
  > "Based on the provided context, **22** nations competed in the Men's foil event at the 2000 Summer Olympics [Q632472::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 9.80 seconds
- Tokens Used: 1528 (Prompt: 1469, Completion: 59)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_lookup` -> Details: `{"tool": "graph_lookup", "event": "Fencing at the 2000 Summer Olympics – Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 40, "nations": 22}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Fencing at the 2000 Summer Olympics – Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 40, "nations": 22}}`
  - Supporting Document Chunks: `Q632472::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **22** nations competed in the Men's foil event (full event title: *Fencing at the 2000 Summer Olympics – Men's foil*) [Q632472::c0]."

### Question [27/50] — eval-027

- Query: "According to the provided corpus, which cycling event at the 2012 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 4.08 seconds
- Tokens Used: 5753 (Prompt: 5678, Completion: 75)
- Retrieved Context Chunks: `Q2297621::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the cycling event at the 2012 Summer Olympics with the highest number of competitors is the **Men's team pursuit**, which had **44** competitors [Q2297621::c0]. 

Source chunks used:
- [Q2297621::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.55 seconds
- Tokens Used: 5313 (Prompt: 5256, Completion: 57)
- Retrieved Subgraph Chunks: `Q754412::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and text passages, the cycling event at the 2012 Summer Olympics with the highest number of competitors was the **Men's individual road race**, with 144 competitors [Q754412::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.47 seconds
- Tokens Used: 2651 (Prompt: 2563, Completion: 88)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2012 Summer Olympics – Men's individual road race", "competitors": 144, "competition": "2012 Summer", "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2012 Summer Olympics – Men's individual road race", "competitors": 144, "competition": "2012 Summer", "sport": "Cycling"}`
  - Supporting Document Chunks: `Q754412::c0, Q754412::c1`
- Synthesized Prediction:
  > "Based on the provided corpus and verified graph facts, the cycling event at the 2012 Summer Olympics with the highest number of competitors was the **Men's cycling road race** (full title: *Cycling at the 2012 Summer Olympics – Men's individual road race*), which featured **144** competitors [graph_cache_fallback, Q754412::c0]."

### Question [28/50] — eval-028

- Query: "According to the provided corpus, how many wrestling events at the 2012 Summer Olympics had more than 19 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.61 seconds
- Tokens Used: 2495 (Prompt: 2395, Completion: 100)
- Retrieved Context Chunks: `Q2521962::c0, Q2550697::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 wrestling events at the 2012 Summer Olympics that had more than 19 competitors (20 competitors):

1. **Women's freestyle 63 kg** with 20 competitors ([Q2521962::c0]).
2. **Men's Greco-Roman 120 kg** with 20 competitors ([Q2550697::c0])."

#### Pipeline 2: GraphRAG
- Latency: 4.78 seconds
- Tokens Used: 2595 (Prompt: 2486, Completion: 109)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the structured graph evidence and supporting passages, there are **2** wrestling events at the 2012 Summer Olympics that had more than 19 competitors (i.e., 20 competitors):

1. **Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 120 kg** (20 competitors)
2. **Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 84 kg** (20 competitors)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 15.76 seconds
- Tokens Used: 215 (Prompt: 184, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 120 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 84 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics – Women's freestyle 63 kg (20 competitors)"], "competition": "2012 Summer", "threshold": 19, "sport": "Wrestling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 120 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics – Men's Greco-Roman 84 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics – Women's freestyle 63 kg (20 competitors)"], "competition": "2012 Summer", "threshold": 19, "sport": "Wrestling"}`
  - Supporting Document Chunks: `Q2550697::c0, Q305439::c0, Q2521962::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 wrestling events at the 2012 Summer Olympics that had more than 19 competitors."

### Question [29/50] — eval-029

- Query: "According to the provided corpus, how many boxing events at the 2012 Summer Olympics had more than 26 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.40 seconds
- Tokens Used: 2908 (Prompt: 2756, Completion: 152)
- Retrieved Context Chunks: `Q31850::c0, Q326384::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there is **1** boxing event at the 2012 Summer Olympics that had more than 26 competitors: the men's light welterweight boxing competition, which had 28 competitors [Q31850::c0]. 

(The flyweight, light heavyweight, and light flyweight events each had 26 competitors [Q332673::c0, Q348720::c0, Q2000524::c0], and the heavyweight event had 15 competitors [Q326384::c0]).

Sources:
- [Q31850::c0]"

#### Pipeline 2: GraphRAG
- Latency: 4.17 seconds
- Tokens Used: 3036 (Prompt: 2874, Completion: 162)
- Retrieved Subgraph Chunks: `Q332673::c0, Q2000524::c0, Q348720::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and text passages, all listed boxing events at the 2012 Summer Olympics (Men's flyweight [Q332673::c0], Men's heavyweight, Men's light flyweight [Q2000524::c0], Men's light heavyweight [Q348720::c0], and Men's light welterweight) had either 26 or fewer competitors (specifically, 26, 15, 26, 26, and 28 competitors respectively). 

Therefore, the number of boxing events with *more* than 26 competitors is **1** (the Men's light welterweight event with 28 competitors)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.40 seconds
- Tokens Used: 210 (Prompt: 179, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 2012 Summer Olympics – Men's light welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics – Men's welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics – Men's lightweight (28 competitors)"], "competition": "2012 Summer", "threshold": 26, "sport": "Boxing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 2012 Summer Olympics – Men's light welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics – Men's welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics – Men's lightweight (28 competitors)"], "competition": "2012 Summer", "threshold": 26, "sport": "Boxing"}`
  - Supporting Document Chunks: `Q31850::c0, Q348714::c0, Q31844::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 boxing events at the 2012 Summer Olympics that had more than 26 competitors."

### Question [30/50] — eval-030

- Query: "According to the provided corpus, which alpine skiing event at the 1994 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.49 seconds
- Tokens Used: 6601 (Prompt: 6541, Completion: 60)
- Retrieved Context Chunks: `Q1005746::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the alpine skiing event at the 1994 Winter Olympics with the highest number of competitors was the **Men's Super G**, which had 69 competitors.

Sources:
- [Q1005746::c0]"

#### Pipeline 2: GraphRAG
- Latency: 4.81 seconds
- Tokens Used: 7261 (Prompt: 7137, Completion: 124)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and supporting passages, the alpine skiing event at the 1994 Winter Olympics with the highest number of competitors was the **Men's giant slalom**, which had **61 competitors** (compared to 57 for the slalom, 56 for the combined, and 55 for the downhill). 

*(Structured Graph Evidence: `(1994 Winter)-[:INCLUDES_EVENT]->(Alpine skiing at the 1994 Winter Olympics – Men's giant slalom [sport=Alpine skiing, competitors=61])`)*"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.34 seconds
- Tokens Used: 2306 (Prompt: 2219, Completion: 87)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Men's Super G", "full_event_title": "Alpine skiing at the 1994 Winter Olympics – Men's super-G", "competitors": 69, "competition": "1994 Winter", "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's Super G", "full_event_title": "Alpine skiing at the 1994 Winter Olympics – Men's super-G", "competitors": 69, "competition": "1994 Winter", "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1005746::c0`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the alpine skiing event at the 1994 Winter Olympics with the highest number of competitors was the **Men's Super G** (full title: *Alpine skiing at the 1994 Winter Olympics – Men's super-G*), which featured **69** competitors from 28 nations [Q1005746::c0]."

### Question [31/50] — eval-031

- Query: "Who won the gold medal in the men's 62 kg weightlifting event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.07 seconds
- Tokens Used: 8398 (Prompt: 8306, Completion: 92)
- Retrieved Context Chunks: `Q26212149::c0`
- Synthesized Prediction:
  > "Based on the provided context, the men's 62 kg weightlifting event at the 2016 Summer Olympics lists its previous edition as "2012" [Q26212149::c0], but the passages do not state who won the gold medal in that 2012 event. 

Unknown based on provided context [Q26212149::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.37 seconds
- Tokens Used: 5519 (Prompt: 5457, Completion: 62)
- Retrieved Subgraph Chunks: `Q1139399::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, Kim Un-guk won the gold medal in the men's 62 kg weightlifting event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) [Q1139399::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 13.37 seconds
- Tokens Used: 15045 (Prompt: 14872, Completion: 173)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics – Men's 62 kg", "gold_winner": "Kim Un-guk", "date_held": "30 July 2012"}`
  - Supporting Document Chunks: `Q1997551::c0, Q1139399::c0, Q1372090::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the men's 62 kg weightlifting event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics in London) was won by **Kim Un-guk** [temporal_precedes, Q1139399::c0]. 

* **Specific Event Name:** Men's 62 kg [temporal_precedes]
* **Full Event Title:** Weightlifting at the 2012 Summer Olympics – Men's 62 kg [temporal_precedes, Q1139399::c0]
* **Gold Medalist:** Kim Un-guk [temporal_precedes, Q1139399::c0]"

### Question [32/50] — eval-032

- Query: "Who won the gold medal in the event held at Pacific Coliseum on February 20, 2010?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.91 seconds
- Tokens Used: 8381 (Prompt: 8376, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Latency: 2.83 seconds
- Tokens Used: 4709 (Prompt: 4618, Completion: 91)
- Retrieved Subgraph Chunks: `Q938791::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the events held at the Pacific Coliseum on February 20, 2010, include the final of the men's 1000 metres in short-track speed skating, where **Lee Jung-su** won the gold medal [Q938791::c0], and the women's 1000 metres, where **Wang Meng** won the gold medal."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 3.78 seconds
- Tokens Used: 1715 (Prompt: 1639, Completion: 76)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Pacific Coliseum", "date_constraint": "february 20, 2010", "year_filter": "2010", "event": "Short-track speed skating at the 2010 Winter Olympics – Women's 1500 metres", "gold_winners": ["Zhou Yang"], "date_matched": true, "candidate_events_checked": 6}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Pacific Coliseum", "date_constraint": "february 20, 2010", "year_filter": "2010", "event": "Short-track speed skating at the 2010 Winter Olympics – Women's 1500 metres", "gold_winners": ["Zhou Yang"], "date_matched": true, "candidate_events_checked": 6}`
  - Supporting Document Chunks: `Q916747::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **Zhou Yang** won the gold medal in the **Short-track speed skating at the 2010 Winter Olympics – Women's 1500 metres**, which was held at the Pacific Coliseum on February 20, 2010 [Q916747::c0]."

### Question [33/50] — eval-033

- Query: "According to the provided corpus, how many alpine skiing events at the 1988 Winter Olympics had more than 57 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.82 seconds
- Tokens Used: 6872 (Prompt: 6707, Completion: 165)
- Retrieved Context Chunks: `Q1005571::c0, Q1005744::c0, Q1222641::c0`
- Synthesized Prediction:
  > "Based on the provided context, there is **1** alpine skiing event at the 1988 Winter Olympics that had more than 57 competitors (the Men's Super-G had 94 competitors, whereas the Men's Downhill had 51, the Men's Combined results list fewer in the provided snippet, and the Women's Super-G had 46 competitors) [Q1005571::c0, Q1005744::c0, Q1222641::c0]. 

Source chunks: [Q1005571::c0], [Q1005744::c0], [Q1222641::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.02 seconds
- Tokens Used: 7869 (Prompt: 7770, Completion: 99)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context, the alpine skiing events at the 1988 Winter Olympics with more than 57 competitors are:

1. **Men's giant slalom** with 117 competitors.
2. **Men's slalom** with 109 competitors.

Therefore, there are **2** alpine skiing events with more than 57 competitors (the Men's combined had 56 and Men's downhill had 51)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 2.81 seconds
- Tokens Used: 212 (Prompt: 181, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 1988 Winter Olympics – Women's giant slalom (64 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's giant slalom (117 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's super-G (94 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's slalom (109 competitors)"], "competition": "1988 Winter", "threshold": 57, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 1988 Winter Olympics – Women's giant slalom (64 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's giant slalom (117 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's super-G (94 competitors)", "Alpine skiing at the 1988 Winter Olympics – Men's slalom (109 competitors)"], "competition": "1988 Winter", "threshold": 57, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1222713::c0, Q1005804::c0, Q1005744::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 4 alpine skiing events at the 1988 Winter Olympics that had more than 57 competitors."

### Question [34/50] — eval-034

- Query: "Who won the gold medal in the men's freestyle 120 kg wrestling event at the Summer Olympics held immediately before 2012?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.31 seconds
- Tokens Used: 2669 (Prompt: 2652, Completion: 17)
- Retrieved Context Chunks: `Q677063::c0`
- Synthesized Prediction:
  > "Unknown based on provided context [Q677063::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.97 seconds
- Tokens Used: 2766 (Prompt: 2656, Completion: 110)
- Retrieved Subgraph Chunks: `Q581364::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the men's freestyle 120 kg wrestling event at the 2008 Summer Olympics (held immediately before 2012) was won by Bakhtiyar Akhmedov [Q581364::c0]. (Note: Artur Taymazov originally won the gold medal [Q581364::c0], but was later stripped of it due to a positive doping test [Q581364::c0].)"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 8.67 seconds
- Tokens Used: 5304 (Prompt: 5140, Completion: 164)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2008 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2008 Summer", "matched_event": "Wrestling at the 2008 Summer Olympics – Men's freestyle 120 kg", "gold_winner": "Bakhtiyar Akhmedov", "date_held": "21 August 2008"}`
  - Supporting Document Chunks: `Q581364::c0, Q1005230::c0, Q923513::c0`
- Synthesized Prediction:
  > "The Summer Olympics immediately preceding 2012 were the 2008 Summer Olympics. 

In the **Men's freestyle 120 kg** event (full title: **Wrestling at the 2008 Summer Olympics – Men's freestyle 120 kg**), held on August 21, 2008, the gold medal was won by **Bakhtiyar Akhmedov** [Q581364::c0]. 

*(Note: Artur Taymazov of Uzbekistan originally crossed the finish line/won first place, but was subsequently stripped of the gold medal due to a positive doping test, leaving Bakhtiyar Akhmedov as the gold medalist) [Q581364::c0].*"

### Question [35/50] — eval-035

- Query: "According to the provided corpus, which rowing event at the 2012 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.27 seconds
- Tokens Used: 4999 (Prompt: 4954, Completion: 45)
- Retrieved Context Chunks: `Q370500::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the Women's eight competition at the 2012 Summer Olympics had 56 competitors. 

Sources:
[Q370500::c0]"

#### Pipeline 2: GraphRAG
- Latency: 3.23 seconds
- Tokens Used: 6184 (Prompt: 6108, Completion: 76)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, both the **Men's coxless four** and the **Men's lightweight coxless four** rowing events at the 2012 Summer Olympics had the highest number of competitors, with **52 competitors** each [Q1005506::c0, Q536380::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.87 seconds
- Tokens Used: 1722 (Prompt: 1570, Completion: 152)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2012 Summer Olympics – Women's eight", "competitors": 56, "competition": "2012 Summer", "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2012 Summer Olympics – Women's eight", "competitors": 56, "competition": "2012 Summer", "sport": "Rowing"}`
  - Supporting Document Chunks: `Q370500::c0`
- Synthesized Prediction:
  > "According to the provided corpus and verified graph facts, the rowing event at the 2012 Summer Olympics with the highest number of competitors (56 competitors across 7 nations) is the **Women's eight** (Full title: *Rowing at the 2012 Summer Olympics – Women's eight*) [Q370500::c0]. 

The winning athletes representing the United States (USA) in this team event are:
* Erin Cafaro
* Susan Francia
* Esther Lofgren
* Taylor Ritzel
* Meghan Musnicki
* Elle Logan
* Caroline Lind
* Caryn Davies
* Mary Whipple

[Q370500::c0]"

### Question [36/50] — eval-036

- Query: "According to the provided corpus, how many short-track speed skating events at the 2018 Winter Olympics had more than 34 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.42 seconds
- Tokens Used: 4722 (Prompt: 4619, Completion: 103)
- Retrieved Context Chunks: `Q47309958::c0, Q47309900::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are **2** short-track speed skating events at the 2018 Winter Olympics that had more than 34 competitors:

1. **Women's 3000 metre relay** with 37 competitors [Q47309958::c0].
2. **Men's 1500 metres** with 37 competitors [Q47309900::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.55 seconds
- Tokens Used: 4232 (Prompt: 4070, Completion: 162)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the structured graph evidence and supporting passages, we can check the number of competitors for each of the listed short-track speed skating events at the 2018 Winter Olympics:

1. **Men's 1000 metres**: 32 competitors
2. **Men's 1500 metres**: 37 competitors (more than 34)
3. **Men's 500 metres**: 33 competitors
4. **Men's 5000 metre relay**: 34 competitors
5. **Women's 1000 metres**: 32 competitors

Therefore, **1** event (the Men's 1500 metres) had more than 34 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.81 seconds
- Tokens Used: 228 (Prompt: 194, Completion: 34)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `gsql_sumaccum` -> Details: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Short-track speed skating at the 2018 Winter Olympics – Men's 1500 metres (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics – Women's 3000 metre relay (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics – Women's 1500 metres (36 competitors)"], "competition": "2018 Winter", "threshold": 34, "sport": "Short-track speed skating"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Short-track speed skating at the 2018 Winter Olympics – Men's 1500 metres (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics – Women's 3000 metre relay (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics – Women's 1500 metres (36 competitors)"], "competition": "2018 Winter", "threshold": 34, "sport": "Short-track speed skating"}`
  - Supporting Document Chunks: `Q47309900::c0, Q47309958::c0, Q47309929::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 3 short-track speed skating events at the 2018 Winter Olympics that had more than 34 competitors."

### Question [37/50] — eval-037

- Query: "According to the provided corpus, which sailing event at the 1996 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.32 seconds
- Tokens Used: 5979 (Prompt: 5941, Completion: 38)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided context passages, the exact number of competitors for each sailing event is not explicitly listed, so it cannot be determined from the passages. 

Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 3.69 seconds
- Tokens Used: 6344 (Prompt: 6285, Completion: 59)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and context passages, the sailing event at the 1996 Summer Olympics with the highest number of competitors was the **Sailing at the 1996 Summer Olympics – Men's 470**, which had **72 competitors**."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 2.18 seconds
- Tokens Used: 2203 (Prompt: 2118, Completion: 85)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "470 Men's", "full_event_title": "Sailing at the 1996 Summer Olympics – Men's 470", "competitors": 72, "competition": "1996 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "470 Men's", "full_event_title": "Sailing at the 1996 Summer Olympics – Men's 470", "competitors": 72, "competition": "1996 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400319::c0, Q7400319::c1`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the sailing event at the 1996 Summer Olympics with the highest number of competitors was the **470 Men's** event, also known as **Sailing at the 1996 Summer Olympics – Men's 470**, with a total of **72** competitors [Q7400319::c0]."

### Question [38/50] — eval-038

- Query: "According to the provided corpus, how many athletics events at the 2008 Summer Olympics had more than 40 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 1.96 seconds
- Tokens Used: 6862 (Prompt: 6855, Completion: 7)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on the provided context."

#### Pipeline 2: GraphRAG
- Latency: 3.92 seconds
- Tokens Used: 5339 (Prompt: 5144, Completion: 195)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Based on the provided evidence, the 2008 Summer Olympics included the following athletics events with more than 40 competitors:

1. **Men's 10,000 metres** – 39 competitors (does not exceed 40)
2. **Men's 100 metres** – 80 competitors
3. **Men's 110 metres hurdles** – 43 competitors
4. **Men's 1500 metres** – 48 competitors
5. **Men's 20 kilometres walk** – 51 competitors

Out of the events listed in the structured graph evidence, **4** athletics events (Men's 100 metres, Men's 110 metres hurdles, Men's 1500 metres, and Men's 20 kilometres walk) had more than 40 competitors."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.67 seconds
- Tokens Used: 213 (Prompt: 182, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 21, "matching_events": ["Athletics at the 2008 Summer Olympics – Women's 100 metres (85 competitors)", "Athletics at the 2008 Summer Olympics – Women's 400 metres (50 competitors)", "Athletics at the 2008 Summer Olympics – Men's marathon (95 competitors)", "Athletics at the 2008 Summer Olympics – Women's hammer throw (50 competitors)", "Athletics at the 2008 Summer Olympics – Men's 400 metres (55 competitors)", "Athletics at the 2008 Summer Olympics – Women's long jump (42 competitors)", "Athletics at the 2008 Summer Olympics – Women's 200 metres (46 competitors)", "Athletics at the 2008 Summer Olympics – Women's 20 kilometres walk (48 competitors)", "Athletics at the 2008 Summer Olympics – Men's 200 metres (63 competitors)", "Athletics at the 2008 Summer Olympics – Women's 3000 metres steeplechase (50 competitors)", "Athletics at the 2008 Summer Olympics – Women's marathon (82 competitors)", "Athletics at the 2008 Summer Olympics – Men's 800 metres (58 competitors)", "Athletics at the 2008 Summer Olympics – Men's 50 kilometres walk (61 competitors)", "Athletics at the 2008 Summer Olympics – Women's heptathlon (43 competitors)", "Athletics at the 2008 Summer Olympics – Men's shot put (44 competitors)", "Athletics at the 2008 Summer Olympics – Men's 110 metres hurdles (43 competitors)", "Athletics at the 2008 Summer Olympics – Men's 1500 metres (48 competitors)", "Athletics at the 2008 Summer Olympics – Men's 5000 metres (43 competitors)", "Athletics at the 2008 Summer Olympics – Women's javelin throw (54 competitors)", "Athletics at the 2008 Summer Olympics – Men's 100 metres (80 competitors)", "Athletics at the 2008 Summer Olympics – Men's 20 kilometres walk (51 competitors)"], "competition": "2008 Summer", "threshold": 40, "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 21, "matching_events": ["Athletics at the 2008 Summer Olympics – Women's 100 metres (85 competitors)", "Athletics at the 2008 Summer Olympics – Women's 400 metres (50 competitors)", "Athletics at the 2008 Summer Olympics – Men's marathon (95 competitors)", "Athletics at the 2008 Summer Olympics – Women's hammer throw (50 competitors)", "Athletics at the 2008 Summer Olympics – Men's 400 metres (55 competitors)", "Athletics at the 2008 Summer Olympics – Women's long jump (42 competitors)", "Athletics at the 2008 Summer Olympics – Women's 200 metres (46 competitors)", "Athletics at the 2008 Summer Olympics – Women's 20 kilometres walk (48 competitors)", "Athletics at the 2008 Summer Olympics – Men's 200 metres (63 competitors)", "Athletics at the 2008 Summer Olympics – Women's 3000 metres steeplechase (50 competitors)", "Athletics at the 2008 Summer Olympics – Women's marathon (82 competitors)", "Athletics at the 2008 Summer Olympics – Men's 800 metres (58 competitors)", "Athletics at the 2008 Summer Olympics – Men's 50 kilometres walk (61 competitors)", "Athletics at the 2008 Summer Olympics – Women's heptathlon (43 competitors)", "Athletics at the 2008 Summer Olympics – Men's shot put (44 competitors)", "Athletics at the 2008 Summer Olympics – Men's 110 metres hurdles (43 competitors)", "Athletics at the 2008 Summer Olympics – Men's 1500 metres (48 competitors)", "Athletics at the 2008 Summer Olympics – Men's 5000 metres (43 competitors)", "Athletics at the 2008 Summer Olympics – Women's javelin throw (54 competitors)", "Athletics at the 2008 Summer Olympics – Men's 100 metres (80 competitors)", "Athletics at the 2008 Summer Olympics – Men's 20 kilometres walk (51 competitors)"], "competition": "2008 Summer", "threshold": 40, "sport": "Athletics"}`
  - Supporting Document Chunks: `Q853040::c0, Q853040::c1, Q932865::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 21 athletics events at the 2008 Summer Olympics that had more than 40 competitors."

### Question [39/50] — eval-039

- Query: "According to the provided corpus, how many boxing events at the 1992 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.11 seconds
- Tokens Used: 5998 (Prompt: 5758, Completion: 240)
- Retrieved Context Chunks: `Q10706347::c0, Q10572431::c0, Q10572463::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, none of the included boxing events at the 1992 Summer Olympics had more than 30 competitors. The competitors for the events detailed are:
- Heavyweight: 23 competitors ([Q10706347::c0])
- Light heavyweight: 26 competitors ([Q10572431::c0])
- Lightweight: 29 competitors ([Q10572463::c0])
- Featherweight: 31 competitors ([Q10495989::c0]) — wait, let's check: 31 competitors. Ah, "more than 30". Featherweight has 31 competitors ([Q10495989::c0]).
- Super heavyweight: 17 competitors ([Q10684073::c0])

Therefore, exactly **1** boxing event (Featherweight, with 31 competitors) had more than 30 competitors.

Sources: [Q10495989::c0]"

#### Pipeline 2: GraphRAG
- Latency: 4.66 seconds
- Tokens Used: 3791 (Prompt: 3628, Completion: 163)
- Retrieved Subgraph Chunks: `Q10426127::c0, Q10706347::c0, Q10572415::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and supporting passages, the 1992 Summer Olympics boxing events with their number of competitors are:
- Bantamweight: 31 competitors [Q10426127::c0]
- Featherweight: 31 competitors 
- Flyweight: 31 competitors 
- Heavyweight: 23 competitors [Q10706347::c0]
- Light flyweight: 30 competitors [Q10572415::c0]

There were **3** boxing events at the 1992 Summer Olympics that had more than 30 competitors (Bantamweight, Featherweight, and Flyweight, each having 31 competitors)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 3.25 seconds
- Tokens Used: 206 (Prompt: 175, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 1992 Summer Olympics – Flyweight (31 competitors)", "Boxing at the 1992 Summer Olympics – Bantamweight (31 competitors)", "Boxing at the 1992 Summer Olympics – Featherweight (31 competitors)"], "competition": "1992 Summer", "threshold": 30, "sport": "Boxing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 1992 Summer Olympics – Flyweight (31 competitors)", "Boxing at the 1992 Summer Olympics – Bantamweight (31 competitors)", "Boxing at the 1992 Summer Olympics – Featherweight (31 competitors)"], "competition": "1992 Summer", "threshold": 30, "sport": "Boxing"}`
  - Supporting Document Chunks: `Q10497008::c0, Q10426127::c0, Q10495989::c0`
- Synthesized Prediction:
  > "According to the provided database result, there were 3 boxing events at the 1992 Summer Olympics that had more than 30 competitors."

### Question [40/50] — eval-040

- Query: "Who won the gold medal in the event held at Stadium Australia on 27 September 2000 (heats)29 September 2000 (semi-finals)30 September 2000 (final)?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.31 seconds
- Tokens Used: 8174 (Prompt: 8154, Completion: 20)
- Retrieved Context Chunks: `Q3628760::c0`
- Synthesized Prediction:
  > "Nouria Mérah-Benida [Q3628760::c0]."

#### Pipeline 2: GraphRAG
- Latency: 3.95 seconds
- Tokens Used: 5570 (Prompt: 5524, Completion: 46)
- Retrieved Subgraph Chunks: `Q3628761::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal for the men's 1500 metres event held at Stadium Australia was won by **Noah Ngeny** [Q3628761::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 12.18 seconds
- Tokens Used: 3726 (Prompt: 3528, Completion: 198)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Stadium Australia", "date_constraint": "27 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics – Women's 1500 metres", "gold_winners": ["Nouria Mérah-Benida"], "date_matched": true, "candidate_events_checked": 31}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Stadium Australia", "date_constraint": "27 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics – Women's 1500 metres", "gold_winners": ["Nouria Mérah-Benida"], "date_matched": true, "candidate_events_checked": 31}`
  - Supporting Document Chunks: `Q3628760::c0, Q3628760::c1`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the **Women's 1500 metres** (full event title: *Athletics at the 2000 Summer Olympics – Women's 1500 metres*), held at Stadium Australia with heats on 27 September 2000, semi-finals on 29 September 2000, and the final on 30 September 2000, was won by **Nouria Mérah-Benida** representing Algeria [Q3628760::c0].

**Sources:**
- Graph Facts: `gold_winners` = ["Nouria Mérah-Benida"], `event` = "Athletics at the 2000 Summer Olympics – Women's 1500 metres"
- Supporting Context: [Q3628760::c0]"

### Question [41/50] — eval-041

- Query: "According to the provided corpus, how many alpine skiing events at the 2006 Winter Olympics had more than 63 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.57 seconds
- Tokens Used: 5793 (Prompt: 5646, Completion: 147)
- Retrieved Context Chunks: `Q917747::c1, Q917752::c0, Q585893::c0`
- Synthesized Prediction:
  > "Based on the provided context, the number of competitors for the listed events are:
- Men's combined: Not specified (list shows up to position 35, [Q917747::c1]).
- Men's downhill: 55 competitors ([Q917752::c0]).
- Men's super-G: 63 competitors ([Q585893::c0]).

Therefore, 0 alpine skiing events at the 2006 Winter Olympics had more than 63 competitors.

Sources: [Q917752::c0], [Q585893::c0]"

#### Pipeline 2: GraphRAG
- Latency: 5.62 seconds
- Tokens Used: 7582 (Prompt: 7389, Completion: 193)
- Retrieved Subgraph Chunks: `Q917747::c0, Q1005801::c0, Q917743::c0`
- Synthesized Prediction:
  > "Based on the provided structured graph evidence and text passages, there are **3** alpine skiing events at the 2006 Winter Olympics that had more than 63 competitors:

1. **Men's combined** – 60 competitors (Wait, 60 is not more than 63). Let's check all events:
   - Men's combined: 60 competitors [Q917747::c0]
   - Men's downhill: 55 competitors
   - Men's giant slalom: 82 competitors [Q1005801::c0]
   - Men's slalom: 97 competitors [Q917743::c0]

Therefore, exactly **2** events had more than 63 competitors (Men's giant slalom with 82 and Men's slalom with 97)."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.57 seconds
- Tokens Used: 211 (Prompt: 180, Completion: 31)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 2006 Winter Olympics – Women's slalom (64 competitors)", "Alpine skiing at the 2006 Winter Olympics – Men's giant slalom (82 competitors)", "Alpine skiing at the 2006 Winter Olympics – Women's giant slalom (65 competitors)", "Alpine skiing at the 2006 Winter Olympics – Men's slalom (97 competitors)"], "competition": "2006 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 2006 Winter Olympics – Women's slalom (64 competitors)", "Alpine skiing at the 2006 Winter Olympics – Men's giant slalom (82 competitors)", "Alpine skiing at the 2006 Winter Olympics – Women's giant slalom (65 competitors)", "Alpine skiing at the 2006 Winter Olympics – Men's slalom (97 competitors)"], "competition": "2006 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1042644::c0, Q1005801::c0, Q2574045::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 alpine skiing events at the 2006 Winter Olympics that had more than 63 competitors."

### Question [42/50] — eval-042

- Query: "Who won the gold medal in the mixed trap shooting event at the Summer Olympics held immediately before 1992?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.59 seconds
- Tokens Used: 6648 (Prompt: 6596, Completion: 52)
- Retrieved Context Chunks: `Q7500750::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the trap shooting event at the 1988 Summer Olympics (held immediately before 1992) was won by Dmitry Monakov [Q7500750::c0]."

#### Pipeline 2: GraphRAG
- Latency: 4.22 seconds
- Tokens Used: 4936 (Prompt: 4883, Completion: 53)
- Retrieved Subgraph Chunks: `Q7500750::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the mixed trap shooting event at the 1988 Summer Olympics (held immediately before 1992) was won by Dmitry Monakov [Q7500750::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.74 seconds
- Tokens Used: 13157 (Prompt: 12957, Completion: 200)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "1988 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "1988 Summer", "matched_event": "Shooting at the 1988 Summer Olympics – Mixed trap", "gold_winner": "Dmitry Monakov", "date_held": "20 September 1988"}`
  - Supporting Document Chunks: `Q7500750::c0, Q7500750::c1, Q7500739::c0`
- Synthesized Prediction:
  > "The gold medal in the mixed trap shooting event at the Summer Olympics held immediately before 1992 (the 1988 Summer Olympics) was won by **Dmitry Monakov** [temporal_precedes, Q7500750::c0].

* **Specific Event Name:** Mixed trap [temporal_precedes]
* **Full Event Title:** Shooting at the 1988 Summer Olympics – Mixed trap [temporal_precedes, Q7500750::c0]
* **Gold Winner:** Dmitry Monakov [temporal_precedes, Q7500750::c0]
* **Date Held:** 20 September 1988 [temporal_precedes, Q7500750::c0]

**Citations:**
- [temporal_precedes]
- [Q7500750::c0]"

### Question [43/50] — eval-043

- Query: "Who won the gold medal in the event held at Carioca Arena 3 on 11 August 2016?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.19 seconds
- Tokens Used: 4721 (Prompt: 4715, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 11.03 seconds
- Tokens Used: 5191 (Prompt: 5186, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 7.62 seconds
- Tokens Used: 1144 (Prompt: 996, Completion: 148)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Carioca Arena 3", "date_constraint": "11 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics – Women's team épée", "gold_winners": ["Loredana Dinu, Simona Gherman, Simona Pop, Ana Maria, Popescu"], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Carioca Arena 3", "date_constraint": "11 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics – Women's team épée", "gold_winners": ["Loredana Dinu, Simona Gherman, Simona Pop, Ana Maria, Popescu"], "date_matched": true, "candidate_events_checked": 17}`
  - Supporting Document Chunks: `Q25384917::c0`
- Synthesized Prediction:
  > "Based on the verified database facts and supporting context, the gold medal in the event held at Carioca Arena 3 on 11 August 2016 (Women's team épée in Fencing at the 2016 Summer Olympics) was won by the team representing Romania [Q25384917::c0]. 

The winning athletes (gold medalists) are:
* Loredana Dinu
* Simona Gherman
* Simona Pop
* Ana Maria Popescu

**Event Title:** Fencing at the 2016 Summer Olympics – Women's team épée [Q25384917::c0]"

### Question [44/50] — eval-044

- Query: "Who won the gold medal in the women's 75 kg weightlifting event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.22 seconds
- Tokens Used: 6817 (Prompt: 6725, Completion: 92)
- Retrieved Context Chunks: `Q26212188::c0`
- Synthesized Prediction:
  > "Based on the provided context, the winner of the gold medal for the women's 75 kg weightlifting event is not mentioned (the text only mentions the 2016 event and that there was a "prev: 2012" edition, but does not state who won the gold medal in 2012). 

Unknown based on provided context [Q26212188::c0]."

#### Pipeline 2: GraphRAG
- Latency: 3.79 seconds
- Tokens Used: 5521 (Prompt: 5435, Completion: 86)
- Retrieved Subgraph Chunks: `Q1997032::c0`
- Synthesized Prediction:
  > "Based on the provided structured knowledge graph evidence and context passages, the gold medal in the women's 75 kg weightlifting event at the 2012 Summer Olympics (held immediately before the 2016 Summer Olympics) was won by **Lydia Valentín** of Spain (after original medalists were disqualified due to doping retests) [Q1997032::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 10.50 seconds
- Tokens Used: 13433 (Prompt: 13302, Completion: 131)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics – Women's 75 kg", "gold_winner": "Lydia Valentín", "date_held": "3 August 2012"}`
  - Supporting Document Chunks: `Q1371783::c0, Q1997032::c0, Q2380135::c0`
- Synthesized Prediction:
  > "The Summer Olympics held immediately before 2016 were the **2012 Summer Olympics** [temporal_precedes]. 

The gold medal in the women's 75 kg weightlifting event, titled **Weightlifting at the 2012 Summer Olympics – Women's 75 kg**, was won by **Lydia Valentín** of Spain [temporal_precedes, Q1997032::c0]. (She was officially declared the champion following subsequent disqualifications of the original medalists due to doping retests) [Q1997032::c0]."

### Question [45/50] — eval-045

- Query: "Who won the gold medal in the women's moguls freestyle skiing event at the Winter Olympics held immediately before 2014?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.24 seconds
- Tokens Used: 9323 (Prompt: 9256, Completion: 67)
- Retrieved Context Chunks: `Q905561::c0`
- Synthesized Prediction:
  > "Based on the provided context, the gold medal in the women's moguls freestyle skiing event at the 2010 Winter Olympics (held immediately before the 2014 Winter Olympics) was won by Hannah Kearney of the United States.

Source chunk: [Q905561::c0]"

#### Pipeline 2: GraphRAG
- Latency: 7.52 seconds
- Tokens Used: 7369 (Prompt: 7314, Completion: 55)
- Retrieved Subgraph Chunks: `Q905561::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the women's moguls freestyle skiing event at the 2010 Winter Olympics (held immediately before 2014) was won by Hannah Kearney [Q905561::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 8.86 seconds
- Tokens Used: 11236 (Prompt: 11120, Completion: 116)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "Freestyle skiing at the 2010 Winter Olympics – Women's moguls", "gold_winner": "Hannah Kearney", "date_held": ""}`
  - Supporting Document Chunks: `Q905561::c0, Q905472::c0, Q905561::c1`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the women's moguls freestyle skiing event at the Winter Olympics held immediately before 2014 (the 2010 Winter Olympics) was won by **Hannah Kearney**.

* **Specific Event Name:** Women's moguls
* **Full Event Title:** Freestyle skiing at the 2010 Winter Olympics – Women's moguls
* **Gold Medalist:** Hannah Kearney
* **Source Citations:** [Q905561::c0]"

### Question [46/50] — eval-046

- Query: "Who won the gold medal in the light flyweight boxing event at the Summer Olympics held immediately before 2004?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.11 seconds
- Tokens Used: 4324 (Prompt: 4318, Completion: 6)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context."

#### Pipeline 2: GraphRAG
- Latency: 3.36 seconds
- Tokens Used: 3426 (Prompt: 3364, Completion: 62)
- Retrieved Subgraph Chunks: `Q4951841::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the gold medal in the light flyweight boxing event at the 2000 Summer Olympics (held immediately before the 2004 Summer Olympics) was won by **Brahim Asloum** [Q4951841::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 9.09 seconds
- Tokens Used: 7107 (Prompt: 6954, Completion: 153)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Tool Executed: `temporal_precedes` -> Details: `{"tool": "temporal_precedes", "preceding_competition": "2000 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2000 Summer", "matched_event": "Boxing at the 2000 Summer Olympics – Light flyweight", "gold_winner": "Brahim Asloum", "date_held": "17 September to 30 September 2000"}`
  - Supporting Document Chunks: `Q4951841::c0, Q4951844::c0, Q4951837::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the light flyweight boxing event at the Summer Olympics held immediately before 2004 (the 2000 Summer Olympics in Sydney) was won by **Brahim Asloum** (representing France).

* **Specific Event Name:** Light flyweight
* **Full Event Title:** Boxing at the 2000 Summer Olympics – Light flyweight

**Citations:**
- Graph Fact: `temporal_precedes`, `2000 Summer`, `Boxing at the 2000 Summer Olympics – Light flyweight`, `Brahim Asloum`
- [Q4951841::c0]"

### Question [47/50] — eval-047

- Query: "According to the provided corpus, which cycling event at the 2004 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.48 seconds
- Tokens Used: 5721 (Prompt: 5647, Completion: 74)
- Retrieved Context Chunks: `Q2445057::c0`
- Synthesized Prediction:
  > "Based on the provided context, the men's individual road race at the 2004 Summer Olympics had 144 competitors [Q2445057::c0]. The text does not provide the total number of competitors for the other cycling events mentioned, so it is unknown based on the provided context which event had the highest overall."

#### Pipeline 2: GraphRAG
- Latency: 3.86 seconds
- Tokens Used: 5381 (Prompt: 5328, Completion: 53)
- Retrieved Subgraph Chunks: `2445057::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the cycling event at the 2004 Summer Olympics with the highest number of competitors was the **Men's individual road race**, which had 144 competitors [2445057::c0]."

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 2.31 seconds
- Tokens Used: 1931 (Prompt: 1844, Completion: 87)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2004 Summer Olympics – Men's individual road race", "competitors": 144, "competition": "2004 Summer", "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2004 Summer Olympics – Men's individual road race", "competitors": 144, "competition": "2004 Summer", "sport": "Cycling"}`
  - Supporting Document Chunks: `Q2445057::c0, Q2445057::c1`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the cycling event at the 2004 Summer Olympics with the highest number of competitors was the **Men's cycling road race** (full event title: **Cycling at the 2004 Summer Olympics – Men's individual road race**), featuring **144** competitors from 43 nations [Q2445057::c0]."

### Question [48/50] — eval-048

- Query: "According to the provided corpus, how many cycling events at the 2012 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 3.02 seconds
- Tokens Used: 5800 (Prompt: 5680, Completion: 120)
- Retrieved Context Chunks: `Q2297621::c0, Q2297633::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, there are 2 cycling events at the 2012 Summer Olympics that had more than 30 competitors:
1. The **men's team pursuit**, which had 44 competitors [Q2297621::c0].
2. The **women's team pursuit**, which had 32 competitors [Q2297633::c0].

Sources: [Q2297621::c0], [Q2297633::c0]."

#### Pipeline 2: GraphRAG
- Latency: 6.31 seconds
- Tokens Used: 5194 (Prompt: 5086, Completion: 108)
- Retrieved Subgraph Chunks: `Q754412::c0, Q1005298::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, there are **3** cycling events at the 2012 Summer Olympics that had more than 30 competitors:

1. **Men's individual road race** – 144 competitors ([Q754412::c0])
2. **Men's cross-country** – 47 competitors (Structured Graph Evidence)
3. **Men's BMX** – 32 competitors ([Q1005298::c0])"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 2.54 seconds
- Tokens Used: 209 (Prompt: 179, Completion: 30)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "result_count": 7, "matching_events": ["Cycling at the 2012 Summer Olympics – Men's cross-country (47 competitors)", "Cycling at the 2012 Summer Olympics – Men's team pursuit (44 competitors)", "Cycling at the 2012 Summer Olympics – Men's individual road race (144 competitors)", "Cycling at the 2012 Summer Olympics – Men's road time trial (37 competitors)", "Cycling at the 2012 Summer Olympics – Women's team pursuit (32 competitors)", "Cycling at the 2012 Summer Olympics – Women's individual road race (66 competitors)", "Cycling at the 2012 Summer Olympics – Men's BMX (32 competitors)"], "competition": "2012 Summer", "threshold": 30, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 7, "matching_events": ["Cycling at the 2012 Summer Olympics – Men's cross-country (47 competitors)", "Cycling at the 2012 Summer Olympics – Men's team pursuit (44 competitors)", "Cycling at the 2012 Summer Olympics – Men's individual road race (144 competitors)", "Cycling at the 2012 Summer Olympics – Men's road time trial (37 competitors)", "Cycling at the 2012 Summer Olympics – Women's team pursuit (32 competitors)", "Cycling at the 2012 Summer Olympics – Women's individual road race (66 competitors)", "Cycling at the 2012 Summer Olympics – Men's BMX (32 competitors)"], "competition": "2012 Summer", "threshold": 30, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q2036655::c0, Q2297621::c0, Q754412::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 7 cycling events at the 2012 Summer Olympics that had more than 30 competitors."

### Question [49/50] — eval-049

- Query: "According to the provided corpus, which shooting event at the 1988 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.54 seconds
- Tokens Used: 5626 (Prompt: 5408, Completion: 218)
- Retrieved Context Chunks: `Q7500739::c0, Q7500753::c0, Q7500737::c0`
- Synthesized Prediction:
  > "Based on the provided context passages, the shooting events mentioned and their competitor counts are:
- Men's 25 metre rapid fire pistol: 32 competitors ([Q7500739::c0])
- Women's 10 metre air rifle: 45 competitors ([Q7500753::c0])
- Men's 10 metre air rifle: 46 competitors ([Q7500737::c0])
- Women's 25 metre pistol: 35 competitors ([Q11883936::c0])

Therefore, the event with the highest number of competitors was the Men's 10 metre air rifle with 46 competitors.

Sources: [Q7500737::c0], [Q7500739::c0], [Q7500753::c0], [Q11883936::c0]"

#### Pipeline 2: GraphRAG
- Latency: 4.36 seconds
- Tokens Used: 5093 (Prompt: 4947, Completion: 146)
- Retrieved Subgraph Chunks: `Q7500743::c0, Q7500739::c0`
- Synthesized Prediction:
  > "Based on the provided evidence, the shooting event at the 1988 Summer Olympics with the highest number of competitors was the **Men's 10 metre air rifle**, which had **46 competitors** [Shooting at the 1988 Summer Olympics – Men's 10 metre air rifle]. 

For comparison:
* Men's 10 metre air pistol: 44 competitors
* Men's 50 metre pistol: 43 competitors [Q7500743::c0]
* Men's 25 metre rapid fire pistol: 32 competitors [Q7500739::c0]"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 1.40 seconds
- Tokens Used: 1558 (Prompt: 1475, Completion: 83)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Tool Executed: `graph_cache_fallback` -> Details: `{"tool": "graph_cache_fallback", "superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 1988 Summer Olympics – Men's 50 metre rifle prone", "competitors": 55, "competition": "1988 Summer", "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 1988 Summer Olympics – Men's 50 metre rifle prone", "competitors": 55, "competition": "1988 Summer", "sport": "Shooting"}`
  - Supporting Document Chunks: `Q7500747::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the shooting event at the 1988 Summer Olympics with the highest number of competitors (55 competitors) was the **Men's 50 metre rifle prone** (full event title: *Shooting at the 1988 Summer Olympics – Men's 50 metre rifle prone*) [Q7500747::c0]."

### Question [50/50] — eval-050

- Query: "Who won the gold medal in the event held at Olympic Stadium on 6–9 August at the 2012 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Pipeline 1: Standard RAG
- Latency: 2.11 seconds
- Tokens Used: 6257 (Prompt: 6252, Completion: 5)
- Retrieved Context Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 2: GraphRAG
- Latency: 8.29 seconds
- Tokens Used: 4935 (Prompt: 4930, Completion: 5)
- Retrieved Subgraph Chunks: `None`
- Synthesized Prediction:
  > "Unknown based on provided context"

#### Pipeline 3: Autonomous Agentic GraphRAG
- Latency: 17.77 seconds
- Tokens Used: 3402 (Prompt: 0, Completion: 0)
- Approach & Action Trace:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Tool Executed: `multi_hop_chain` -> Details: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "6–9 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 37}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "6–9 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
  - Supporting Document Chunks: `Q1827915::c0, Q1827915::c1, Q326112::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, the gold medal in the men's 800 metres event (Athletics at the 2012 Summer Olympics – Men's 800 metres) held at the Olympic Stadium on 6–9 August 2012 was won by **David Rudisha** of Kenya [Q1049551::c0]."

