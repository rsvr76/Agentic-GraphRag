# Comparative Benchmark Traces and Agent Execution Analysis

## Overview

This report documents the detailed execution traces, reasoning paths, tool interactions, and synthesized outputs for all 50 held-out evaluation questions (eval_hidden.jsonl) using Pipeline 3: Autonomous Agentic GraphRAG (LangGraph StateGraph + GSQL Accumulators).

All questions were evaluated using the primary model configured in .env: Google Gemini (gemini-3.5-flash-lite).

## Held-Out Benchmark Summary

| Pipeline | Question Count | Model | Avg Tokens / Query | Avg Latency (s) | Evaluation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Agentic GraphRAG | 50 | gemini-3.5-flash-lite | 3430.1 | 7.50 | Raw Outputs Logged (Held-Out Test Set) |

## Per-Archetype Question Distribution

| Archetype | Question Count | Evaluation Status |
| :--- | :--- | :--- |
| aggregation | 15 | Official Held-Out Evaluation |
| lookup | 7 | Official Held-Out Evaluation |
| multi_hop | 10 | Official Held-Out Evaluation |
| superlative | 10 | Official Held-Out Evaluation |
| temporal | 8 | Official Held-Out Evaluation |

## Question-by-Question Agent Traces and Approach Analysis

### Question [1/50] — eval-001

- Query: "Who won the gold medal in the event held at Olympic Tennis Centre on 15 to 22 August 2004?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.29 seconds
- Tokens Used: 910 (Prompt: 758, Completion: 152)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Tennis Centre", "date_constraint": "15 to 22 august 2004", "year_filter": "2004", "event": "Tennis at the 2004 Summer Olympics \u2013 Women's doubles", "gold_winners": ["Li Ting, Sun Tiantian"], "date_matched": true, "candidate_events_checked": 1}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Tennis Centre", "date_constraint": "15 to 22 august 2004", "year_filter": "2004", "event": "Tennis at the 2004 Summer Olympics \u2013 Women's doubles", "gold_winners": ["Li Ting, Sun Tiantian"], "date_matched": true, "candidate_events_checked": 1}`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.39 seconds
- Tokens Used: 2431 (Prompt: 2384, Completion: 47)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Fencing at the 1988 Summer Olympics \u2013 Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 68, "nations": 29}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Fencing at the 1988 Summer Olympics \u2013 Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 68, "nations": 29}}`
  - Supporting Document Chunks: `Q5443136::c0, Q5443136::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **29** nations competed in Fencing at the 1988 Summer Olympics – Men's foil [Q5443136::c0]."

### Question [3/50] — eval-003

- Query: "According to the provided corpus, how many cycling events at the 2008 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 3.83 seconds
- Tokens Used: 208 (Prompt: 178, Completion: 30)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 8, "matching_events": ["Cycling at the 2008 Summer Olympics \u2013 Men's team sprint (39 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's Madison (32 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's team pursuit (44 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Women's individual road race (66 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's individual road race (143 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's cross-country (50 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's BMX (32 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's road time trial (39 competitors)"], "competition": "2008 Summer", "threshold": 30, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 8, "matching_events": ["Cycling at the 2008 Summer Olympics \u2013 Men's team sprint (39 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's Madison (32 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's team pursuit (44 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Women's individual road race (66 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's individual road race (143 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's cross-country (50 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's BMX (32 competitors)", "Cycling at the 2008 Summer Olympics \u2013 Men's road time trial (39 competitors)"], "competition": "2008 Summer", "threshold": 30, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q1005322::c0, Q1005614::c0, Q635304::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 8 cycling events at the 2008 Summer Olympics that had more than 30 competitors."

### Question [4/50] — eval-004

- Query: "Who won the gold medal in the event held at Sydney International Shooting Centre on 22 September 2000?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.67 seconds
- Tokens Used: 1891 (Prompt: 1809, Completion: 82)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Sydney International Shooting Centre", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics \u2013 Women's 25 metre pistol", "gold_winners": ["Mariya Grozdeva"], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Sydney International Shooting Centre", "date_constraint": "22 september 2000", "year_filter": "2000", "event": "Shooting at the 2000 Summer Olympics \u2013 Women's 25 metre pistol", "gold_winners": ["Mariya Grozdeva"], "date_matched": true, "candidate_events_checked": 17}`
  - Supporting Document Chunks: `Q7500817::c0`
- Synthesized Prediction:
  > "**Mariya Grozdeva** won the gold medal in the **Women's 25 metre pistol** event (full event title: *Shooting at the 2000 Summer Olympics – Women's 25 metre pistol*) held at the Sydney International Shooting Centre on 22 September 2000 [Q7500817::c0]."

### Question [5/50] — eval-005

- Query: "According to the provided corpus, which sailing event at the 2016 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.46 seconds
- Tokens Used: 741 (Prompt: 650, Completion: 91)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_heapaccum` -> Details: `{"superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics \u2013 Men's 470", "competitors": 52, "competition": "2016 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics \u2013 Men's 470", "competitors": 52, "competition": "2016 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "Based on the provided graph facts and supporting context, the sailing event at the 2016 Summer Olympics with the highest number of competitors was the **Men's 470** (full event title: *Sailing at the 2004 Summer Olympics – Men's 470*), featuring **52** competitors [gsql_heapaccum, Q7400344::c0]."

### Question [6/50] — eval-006

- Query: "According to the provided corpus, how many cross-country skiing events at the 2010 Winter Olympics had more than 62 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.19 seconds
- Tokens Used: 200 (Prompt: 166, Completion: 34)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 0, "matching_events": [], "competition": "2010 Winter", "threshold": 62, "sport": "Cross-country skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 0, "matching_events": [], "competition": "2010 Winter", "threshold": 62, "sport": "Cross-country skiing"}`
- Synthesized Prediction:
  > "According to the verified database result, there were 0 cross-country skiing events at the 2010 Winter Olympics that had more than 62 competitors."

### Question [7/50] — eval-007

- Query: "Who won the gold medal in the men's heavyweight boxing event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 10.63 seconds
- Tokens Used: 5709 (Prompt: 5607, Completion: 102)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2012 Summer.", "formulated_query": "Who won the gold medal in the men's heavyweight boxing event at the 2012 Summer Olympics?", "extracted_entities": {"event": "Boxing at the 2012 Summer Olympics \u2013 Men's heavyweight"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "Boxing at the 2012 Summer Olympics \u2013 Men's heavyweight", "gold_winner": "Oleksandr Usyk", "date_held": "1\u201311 August 2012"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Boxing at the 2012 Summer Olympics \u2013 Men's heavyweight", "gold_winner": "Oleksandr Usyk", "date_held": "1\u201311 August 2012"}`
  - Supporting Document Chunks: `Q348720::c0, Q326382::c0, Q326384::c0, Q31850::c0, Q332673::c0, Q31844::c0, Q2000524::c0, Q348714::c0, Q2070048::c0, Q2070058::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting documentation, the gold medal in the men's heavyweight boxing event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics in London) was won by **Oleksandr Usyk** [Q326384::c0]. 

* **Specific Event Name:** Men's heavyweight boxing
* **Full Event Title:** Boxing at the 2012 Summer Olympics – Men's heavyweight"

### Question [8/50] — eval-008

- Query: "According to the provided corpus, how many sailing events at the 1996 Summer Olympics had more than 46 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.54 seconds
- Tokens Used: 205 (Prompt: 175, Completion: 30)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 4, "matching_events": ["Sailing at the 1996 Summer Olympics \u2013 Soling (66 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Men's 470 (72 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Laser (56 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Star (50 competitors)"], "competition": "1996 Summer", "threshold": 46, "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Sailing at the 1996 Summer Olympics \u2013 Soling (66 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Men's 470 (72 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Laser (56 competitors)", "Sailing at the 1996 Summer Olympics \u2013 Star (50 competitors)"], "competition": "1996 Summer", "threshold": 46, "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400322::c0, Q7400319::c0, Q7400319::c1`
- Synthesized Prediction:
  > "According to the provided database, there were 4 sailing events at the 1996 Summer Olympics that had more than 46 competitors."

### Question [9/50] — eval-009

- Query: "According to the provided corpus, which sailing event at the 2004 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.28 seconds
- Tokens Used: 734 (Prompt: 650, Completion: 84)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_heapaccum` -> Details: `{"superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics \u2013 Men's 470", "competitors": 54, "competition": "2004 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 470", "full_event_title": "Sailing at the 2004 Summer Olympics \u2013 Men's 470", "competitors": 54, "competition": "2004 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400344::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the sailing event at the 2004 Summer Olympics with the highest number of competitors was the **Men's 470** (full event title: *Sailing at the 2004 Summer Olympics – Men's 470*), with a total of **54** competitors [Q7400344::c0]."

### Question [10/50] — eval-010

- Query: "How many nations competed in Boxing at the 1996 Summer Olympics – Flyweight?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.08 seconds
- Tokens Used: 643 (Prompt: 572, Completion: 71)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Boxing at the 1996 Summer Olympics \u2013 Flyweight", "attributes": {"name": "Flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 32, "nations": 32}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Boxing at the 1996 Summer Olympics \u2013 Flyweight", "attributes": {"name": "Flyweight boxing", "sport": "Boxing", "discipline": "", "gender": "", "competitors": 32, "nations": 32}}`
  - Supporting Document Chunks: `Q10497009::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, 32 nations competed in the Flyweight boxing event at the 1996 Summer Olympics (Event name: *Flyweight boxing*, Full title: *Boxing at the 1996 Summer Olympics – Flyweight*) [Q10497009::c0]."

### Question [11/50] — eval-011

- Query: "According to the provided corpus, how many weightlifting events at the 1992 Summer Olympics had more than 24 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.12 seconds
- Tokens Used: 216 (Prompt: 185, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 4, "matching_events": ["Weightlifting at the 1992 Summer Olympics \u2013 Men's 82.5 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 60 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 75 kg (34 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 100 kg (25 competitors)"], "competition": "1992 Summer", "threshold": 24, "sport": "Weightlifting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Weightlifting at the 1992 Summer Olympics \u2013 Men's 82.5 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 60 kg (31 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 75 kg (34 competitors)", "Weightlifting at the 1992 Summer Olympics \u2013 Men's 100 kg (25 competitors)"], "competition": "1992 Summer", "threshold": 24, "sport": "Weightlifting"}`
  - Supporting Document Chunks: `Q7979977::c0, Q7979973::c0, Q7979975::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 weightlifting events at the 1992 Summer Olympics that had more than 24 competitors."

### Question [12/50] — eval-012

- Query: "How many nations competed in Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.66 seconds
- Tokens Used: 2804 (Prompt: 2731, Completion: 73)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Swimming at the 2016 Summer Olympics \u2013 Men's 100 metre butterfly", "attributes": {"name": "Men's 100 metre butterfly", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 43, "nations": 32}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Swimming at the 2016 Summer Olympics \u2013 Men's 100 metre butterfly", "attributes": {"name": "Men's 100 metre butterfly", "sport": "Swimming", "discipline": "", "gender": "", "competitors": 43, "nations": 32}}`
  - Supporting Document Chunks: `Q25991452::c0, Q25991452::c1`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **32** nations competed in the Men's 100 metre butterfly event at the 2016 Summer Olympics (Swimming at the 2016 Summer Olympics – Men's 100 metre butterfly) [Q25991452::c0]."

### Question [13/50] — eval-013

- Query: "According to the provided corpus, how many cycling events at the 2016 Summer Olympics had more than 27 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.45 seconds
- Tokens Used: 211 (Prompt: 180, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 6, "matching_events": ["Cycling at the 2016 Summer Olympics \u2013 Men's individual road race (144 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's individual road race (68 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Men's team pursuit (40 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Men's cross-country (49 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's cross-country (29 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's team pursuit (39 competitors)"], "competition": "2016 Summer", "threshold": 27, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 6, "matching_events": ["Cycling at the 2016 Summer Olympics \u2013 Men's individual road race (144 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's individual road race (68 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Men's team pursuit (40 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Men's cross-country (49 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's cross-country (29 competitors)", "Cycling at the 2016 Summer Olympics \u2013 Women's team pursuit (39 competitors)"], "competition": "2016 Summer", "threshold": 27, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q24760634::c0, Q24760634::c1, Q24761058::c0`
- Synthesized Prediction:
  > "According to the verified database results, there were 6 cycling events at the 2016 Summer Olympics that had more than 27 competitors."

### Question [14/50] — eval-014

- Query: "Who won the gold medal in the event held at San Sicario on February 15, 2006?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 2.90 seconds
- Tokens Used: 1228 (Prompt: 1157, Completion: 71)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "San Sicario", "date_constraint": "february 15, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics \u2013 Women's downhill", "gold_winners": ["Michaela Dorfmeister"], "date_matched": true, "candidate_events_checked": 3}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "San Sicario", "date_constraint": "february 15, 2006", "year_filter": "2006", "event": "Alpine skiing at the 2006 Winter Olympics \u2013 Women's downhill", "gold_winners": ["Michaela Dorfmeister"], "date_matched": true, "candidate_events_checked": 3}`
  - Supporting Document Chunks: `Q771123::c0`
- Synthesized Prediction:
  > "**Michaela Dorfmeister** won the gold medal in the **Women's downhill** event (full event title: *Alpine skiing at the 2006 Winter Olympics – Women's downhill*) held at San Sicario on February 15, 2006 [Q771123::c0]."

### Question [15/50] — eval-015

- Query: "How many nations competed in Athletics at the 2016 Summer Olympics – Men's 400 metres?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.50 seconds
- Tokens Used: 3296 (Prompt: 3214, Completion: 82)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Athletics at the 2016 Summer Olympics \u2013 Men's 400 metres", "attributes": {"name": "Men's 400 metres", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 53, "nations": 35}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Athletics at the 2016 Summer Olympics \u2013 Men's 400 metres", "attributes": {"name": "Men's 400 metres", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 53, "nations": 35}}`
  - Supporting Document Chunks: `Q26219858::c0, Q26219858::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **35** nations competed in the Men's 400 metres at the 2016 Summer Olympics (full event title: *Athletics at the 2016 Summer Olympics – Men's 400 metres*) [graph_lookup, Q26219858::c0]."

### Question [16/50] — eval-016

- Query: "How many nations competed in Athletics at the 2008 Summer Olympics – Women's shot put?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.60 seconds
- Tokens Used: 2316 (Prompt: 2234, Completion: 82)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Athletics at the 2008 Summer Olympics \u2013 Women's shot put", "attributes": {"name": "Women's shot put", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 35, "nations": 22}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Athletics at the 2008 Summer Olympics \u2013 Women's shot put", "attributes": {"name": "Women's shot put", "sport": "Athletics", "discipline": "", "gender": "", "competitors": 35, "nations": 22}}`
  - Supporting Document Chunks: `Q848278::c0, Q848278::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting passages, **22** nations competed in the Women's shot put event at the 2008 Summer Olympics [Q848278::c0]. 

* **Specific Event Name:** Women's shot put
* **Full Event Title:** Athletics at the 2008 Summer Olympics – Women's shot put"

### Question [17/50] — eval-017

- Query: "Who won the gold medal in the event held at Eton Dorney on 28 July – 4 August 2012?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 9.65 seconds
- Tokens Used: 3745 (Prompt: 3670, Completion: 75)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Eton Dorney", "date_constraint": "28 july", "year_filter": "2012", "event": "Rowing at the 2012 Summer Olympics \u2013 Women's single sculls", "gold_winners": ["Miroslava Knapkov\u00e1"], "date_matched": true, "candidate_events_checked": 24}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Eton Dorney", "date_constraint": "28 july", "year_filter": "2012", "event": "Rowing at the 2012 Summer Olympics \u2013 Women's single sculls", "gold_winners": ["Miroslava Knapkov\u00e1"], "date_matched": true, "candidate_events_checked": 24}`
  - Supporting Document Chunks: `Q1222270::c0, Q1222270::c1`
- Synthesized Prediction:
  > "The gold medal in the event held at Eton Dorney from 28 July – 4 August 2012 (Rowing at the 2012 Summer Olympics – Women's single sculls) was won by **Miroslava Knapková** (representing the Czech Republic) [Q1222270::c0]."

### Question [18/50] — eval-018

- Query: "Who won the gold medal in the event held at Olympic Stadium on 16–18 August 2016?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 12.11 seconds
- Tokens Used: 2111 (Prompt: 1947, Completion: 164)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "16\u201318 august 2016", "year_filter": "2016", "event": "Athletics at the 2016 Summer Olympics \u2013 Women's javelin throw", "gold_winners": ["Sara Kolak"], "date_matched": true, "candidate_events_checked": 32}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "16\u201318 august 2016", "year_filter": "2016", "event": "Athletics at the 2016 Summer Olympics \u2013 Women's javelin throw", "gold_winners": ["Sara Kolak"], "date_matched": true, "candidate_events_checked": 32}`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.37 seconds
- Tokens Used: 212 (Prompt: 180, Completion: 32)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 4, "matching_events": ["Alpine skiing at the 1998 Winter Olympics \u2013 Women's slalom (57 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Men's slalom (65 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Women's giant slalom (56 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Men's giant slalom (62 competitors)"], "competition": "1998 Winter", "threshold": 45, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 4, "matching_events": ["Alpine skiing at the 1998 Winter Olympics \u2013 Women's slalom (57 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Men's slalom (65 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Women's giant slalom (56 competitors)", "Alpine skiing at the 1998 Winter Olympics \u2013 Men's giant slalom (62 competitors)"], "competition": "1998 Winter", "threshold": 45, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1222533::c0, Q1005643::c0, Q1222717::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 4 alpine skiing events at the 1998 Winter Olympics that had more than 45 competitors."

### Question [20/50] — eval-020

- Query: "Who won the gold medal in the event held at Royal Artillery Barracks on 5 August 2012?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 5.42 seconds
- Tokens Used: 3398 (Prompt: 3261, Completion: 137)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Royal Artillery Barracks", "date_constraint": "5 august 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics \u2013 Men's 50 metre pistol", "gold_winners": ["Jin Jong-oh"], "date_matched": true, "candidate_events_checked": 12}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Royal Artillery Barracks", "date_constraint": "5 august 2012", "year_filter": "2012", "event": "Shooting at the 2012 Summer Olympics \u2013 Men's 50 metre pistol", "gold_winners": ["Jin Jong-oh"], "date_matched": true, "candidate_events_checked": 12}`
  - Supporting Document Chunks: `Q2353475::c0, Q2353475::c1`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **Jin Jong-oh** won the gold medal in the Men's 50 metre pistol event at the Royal Artillery Barracks on 5 August 2012 [Q2353475::c0]. 

* **Event:** Men's 50 metre pistol (Shooting at the 2012 Summer Olympics – Men's 50 metre pistol) [Q2353475::c0]
* **Gold Medalist:** Jin Jong-oh (South Korea) [Q2353475::c0]"

### Question [21/50] — eval-021

- Query: "Who won the gold medal in the men's 200 metre backstroke swimming event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.55 seconds
- Tokens Used: 15758 (Prompt: 15548, Completion: 210)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2012 Summer.", "formulated_query": "Who won the gold medal in the men's 200 metre backstroke swimming event at the 2012 Summer Olympics?", "extracted_entities": {"event": "Swimming at the 2012 Summer Olympics \u2013 Men's 200 metre backstroke"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "Swimming at the 2012 Summer Olympics \u2013 Men's 200 metre backstroke", "gold_winner": "Tyler Clary", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Swimming at the 2012 Summer Olympics \u2013 Men's 200 metre backstroke", "gold_winner": "Tyler Clary", "date_held": ""}`
  - Supporting Document Chunks: `Q2071160::c0, Q916930::c0, Q905555::c0, Q2051400::c0, Q2071160::c2, Q2051400::c1, Q1067796::c0, Q2001050::c0, Q2269716::c0, Q1798905::c0, Q2071160::c1`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.51 seconds
- Tokens Used: 2202 (Prompt: 2159, Completion: 43)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Cross-country skiing at the 2014 Winter Olympics \u2013 Men's sprint", "attributes": {"name": "Men's sprint", "sport": "", "discipline": "", "gender": "", "competitors": 86, "nations": 40}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Cross-country skiing at the 2014 Winter Olympics \u2013 Men's sprint", "attributes": {"name": "Men's sprint", "sport": "", "discipline": "", "gender": "", "competitors": 86, "nations": 40}}`
  - Supporting Document Chunks: `Q15055036::c0, Q15055036::c1`
- Synthesized Prediction:
  > "A total of **40 nations** competed in the Cross-country skiing at the 2014 Winter Olympics – Men's sprint [Q15055036::c0]."

### Question [23/50] — eval-023

- Query: "According to the provided corpus, how many shooting events at the 2000 Summer Olympics had more than 42 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.15 seconds
- Tokens Used: 212 (Prompt: 182, Completion: 30)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 7, "matching_events": ["Shooting at the 2000 Summer Olympics \u2013 Women's 10 metre air rifle (49 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 50 metre rifle prone (53 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 10 metre air rifle (46 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's skeet (49 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 50 metre rifle three positions (44 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 10 metre air pistol (43 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Women's 10 metre air pistol (45 competitors)"], "competition": "2000 Summer", "threshold": 42, "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 7, "matching_events": ["Shooting at the 2000 Summer Olympics \u2013 Women's 10 metre air rifle (49 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 50 metre rifle prone (53 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 10 metre air rifle (46 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's skeet (49 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 50 metre rifle three positions (44 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Men's 10 metre air pistol (43 competitors)", "Shooting at the 2000 Summer Olympics \u2013 Women's 10 metre air pistol (45 competitors)"], "competition": "2000 Summer", "threshold": 42, "sport": "Shooting"}`
  - Supporting Document Chunks: `Q4354069::c0, Q7500812::c0, Q4443763::c0`
- Synthesized Prediction:
  > "According to the verified database, there were 7 shooting events at the 2000 Summer Olympics that had more than 42 competitors."

### Question [24/50] — eval-024

- Query: "According to the provided corpus, which cross-country skiing event at the 1998 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.17 seconds
- Tokens Used: 2431 (Prompt: 2340, Completion: 91)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_heapaccum` -> Details: `{"superlative_event": "Men's 10 kilometre classical", "full_event_title": "Cross-country skiing at the 1998 Winter Olympics \u2013 Men's 10 kilometre classical", "competitors": 97, "competition": "1998 Winter", "sport": "Cross-country skiing"}`
  - In-Database Graph Facts: `{"tool": "gsql_heapaccum", "superlative_event": "Men's 10 kilometre classical", "full_event_title": "Cross-country skiing at the 1998 Winter Olympics \u2013 Men's 10 kilometre classical", "competitors": 97, "competition": "1998 Winter", "sport": "Cross-country skiing"}`
  - Supporting Document Chunks: `Q1004937::c0`
- Synthesized Prediction:
  > "Based on the provided corpus and database facts, the cross-country skiing event at the 1998 Winter Olympics with the highest number of competitors was the **Men's 10 kilometre classical** (full title: *Cross-country skiing at the 1998 Winter Olympics – Men's 10 kilometre classical*), which featured **97** competitors [Q1004937::c0]."

### Question [25/50] — eval-025

- Query: "According to the provided corpus, which rowing event at the 2016 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 58.46 seconds
- Tokens Used: 1779 (Prompt: 1541, Completion: 238)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Women's eight", "full_event_title": "Rowing at the 2016 Summer Olympics \u2013 Women's eight", "competitors": 56, "competition": "2016 Summer", "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2016 Summer Olympics \u2013 Women's eight", "competitors": 56, "competition": "2016 Summer", "sport": "Rowing"}`
  - Supporting Document Chunks: `Q22968979::c0`
- Synthesized Prediction:
  > "Women's eight (Rowing at the 2016 Summer Olympics – Women's eight) – 56 competitors【Q22968979::c0】"

### Question [26/50] — eval-026

- Query: "How many nations competed in Fencing at the 2000 Summer Olympics – Men's foil?"
- Archetype: `lookup`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 9.80 seconds
- Tokens Used: 1528 (Prompt: 1469, Completion: 59)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `lookup`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_lookup` -> Details: `{"event": "Fencing at the 2000 Summer Olympics \u2013 Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 40, "nations": 22}}`
  - In-Database Graph Facts: `{"tool": "graph_lookup", "event": "Fencing at the 2000 Summer Olympics \u2013 Men's foil", "attributes": {"name": "Men's foil", "sport": "Fencing", "discipline": "", "gender": "", "competitors": 40, "nations": 22}}`
  - Supporting Document Chunks: `Q632472::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, **22** nations competed in the Men's foil event (full event title: *Fencing at the 2000 Summer Olympics – Men's foil*) [Q632472::c0]."

### Question [27/50] — eval-027

- Query: "According to the provided corpus, which cycling event at the 2012 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.47 seconds
- Tokens Used: 2651 (Prompt: 2563, Completion: 88)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2012 Summer Olympics \u2013 Men's individual road race", "competitors": 144, "competition": "2012 Summer", "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2012 Summer Olympics \u2013 Men's individual road race", "competitors": 144, "competition": "2012 Summer", "sport": "Cycling"}`
  - Supporting Document Chunks: `Q754412::c0, Q754412::c1`
- Synthesized Prediction:
  > "Based on the provided corpus and verified graph facts, the cycling event at the 2012 Summer Olympics with the highest number of competitors was the **Men's cycling road race** (full title: *Cycling at the 2012 Summer Olympics – Men's individual road race*), which featured **144** competitors [graph_cache_fallback, Q754412::c0]."

### Question [28/50] — eval-028

- Query: "According to the provided corpus, how many wrestling events at the 2012 Summer Olympics had more than 19 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 15.76 seconds
- Tokens Used: 215 (Prompt: 184, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 3, "matching_events": ["Wrestling at the 2012 Summer Olympics \u2013 Men's Greco-Roman 120 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics \u2013 Men's Greco-Roman 84 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics \u2013 Women's freestyle 63 kg (20 competitors)"], "competition": "2012 Summer", "threshold": 19, "sport": "Wrestling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Wrestling at the 2012 Summer Olympics \u2013 Men's Greco-Roman 120 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics \u2013 Men's Greco-Roman 84 kg (20 competitors)", "Wrestling at the 2012 Summer Olympics \u2013 Women's freestyle 63 kg (20 competitors)"], "competition": "2012 Summer", "threshold": 19, "sport": "Wrestling"}`
  - Supporting Document Chunks: `Q2550697::c0, Q305439::c0, Q2521962::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 wrestling events at the 2012 Summer Olympics that had more than 19 competitors."

### Question [29/50] — eval-029

- Query: "According to the provided corpus, how many boxing events at the 2012 Summer Olympics had more than 26 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.40 seconds
- Tokens Used: 210 (Prompt: 179, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 3, "matching_events": ["Boxing at the 2012 Summer Olympics \u2013 Men's light welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics \u2013 Men's welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics \u2013 Men's lightweight (28 competitors)"], "competition": "2012 Summer", "threshold": 26, "sport": "Boxing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 2012 Summer Olympics \u2013 Men's light welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics \u2013 Men's welterweight (28 competitors)", "Boxing at the 2012 Summer Olympics \u2013 Men's lightweight (28 competitors)"], "competition": "2012 Summer", "threshold": 26, "sport": "Boxing"}`
  - Supporting Document Chunks: `Q31850::c0, Q348714::c0, Q31844::c0`
- Synthesized Prediction:
  > "According to the verified database result, there were 3 boxing events at the 2012 Summer Olympics that had more than 26 competitors."

### Question [30/50] — eval-030

- Query: "According to the provided corpus, which alpine skiing event at the 1994 Winter Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.34 seconds
- Tokens Used: 2306 (Prompt: 2219, Completion: 87)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Men's Super G", "full_event_title": "Alpine skiing at the 1994 Winter Olympics \u2013 Men's super-G", "competitors": 69, "competition": "1994 Winter", "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's Super G", "full_event_title": "Alpine skiing at the 1994 Winter Olympics \u2013 Men's super-G", "competitors": 69, "competition": "1994 Winter", "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1005746::c0`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the alpine skiing event at the 1994 Winter Olympics with the highest number of competitors was the **Men's Super G** (full title: *Alpine skiing at the 1994 Winter Olympics – Men's super-G*), which featured **69** competitors from 28 nations [Q1005746::c0]."

### Question [31/50] — eval-031

- Query: "Who won the gold medal in the men's 62 kg weightlifting event at the Summer Olympics held immediately before 2016?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 13.37 seconds
- Tokens Used: 15045 (Prompt: 14872, Completion: 173)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2012 Summer.", "formulated_query": "Who won the gold medal in the men's 62 kg weightlifting event at the 2012 Summer Olympics?", "extracted_entities": {"event": "Weightlifting at the 2012 Summer Olympics \u2013 Men's 62 kg"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics \u2013 Men's 62 kg", "gold_winner": "Kim Un-guk", "date_held": "30 July 2012"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics \u2013 Men's 62 kg", "gold_winner": "Kim Un-guk", "date_held": "30 July 2012"}`
  - Supporting Document Chunks: `Q1997551::c0, Q1139399::c0, Q1372090::c0, Q2196657::c0, Q2715839::c0, Q2740554::c0, Q2557145::c0, Q2364389::c0, Q2380135::c0, Q1371783::c0`
- Synthesized Prediction:
  > "Based on the verified database graph facts and supporting context, the gold medal in the men's 62 kg weightlifting event at the Summer Olympics held immediately before 2016 (the 2012 Summer Olympics in London) was won by **Kim Un-guk** [temporal_precedes, Q1139399::c0]. 

* **Specific Event Name:** Men's 62 kg [temporal_precedes]
* **Full Event Title:** Weightlifting at the 2012 Summer Olympics – Men's 62 kg [temporal_precedes, Q1139399::c0]
* **Gold Medalist:** Kim Un-guk [temporal_precedes, Q1139399::c0]"

### Question [32/50] — eval-032

- Query: "Who won the gold medal in the event held at Pacific Coliseum on February 20, 2010?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 3.78 seconds
- Tokens Used: 1715 (Prompt: 1639, Completion: 76)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Pacific Coliseum", "date_constraint": "february 20, 2010", "year_filter": "2010", "event": "Short-track speed skating at the 2010 Winter Olympics \u2013 Women's 1500 metres", "gold_winners": ["Zhou Yang"], "date_matched": true, "candidate_events_checked": 6}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Pacific Coliseum", "date_constraint": "february 20, 2010", "year_filter": "2010", "event": "Short-track speed skating at the 2010 Winter Olympics \u2013 Women's 1500 metres", "gold_winners": ["Zhou Yang"], "date_matched": true, "candidate_events_checked": 6}`
  - Supporting Document Chunks: `Q916747::c0`
- Synthesized Prediction:
  > "Based on the verified graph facts and supporting context, **Zhou Yang** won the gold medal in the **Short-track speed skating at the 2010 Winter Olympics – Women's 1500 metres**, which was held at the Pacific Coliseum on February 20, 2010 [Q916747::c0]."

### Question [33/50] — eval-033

- Query: "According to the provided corpus, how many alpine skiing events at the 1988 Winter Olympics had more than 57 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 2.81 seconds
- Tokens Used: 212 (Prompt: 181, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 4, "matching_events": ["Alpine skiing at the 1988 Winter Olympics \u2013 Women's giant slalom (64 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's giant slalom (117 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's super-G (94 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's slalom (109 competitors)"], "competition": "1988 Winter", "threshold": 57, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 1988 Winter Olympics \u2013 Women's giant slalom (64 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's giant slalom (117 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's super-G (94 competitors)", "Alpine skiing at the 1988 Winter Olympics \u2013 Men's slalom (109 competitors)"], "competition": "1988 Winter", "threshold": 57, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1222713::c0, Q1005804::c0, Q1005744::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 4 alpine skiing events at the 1988 Winter Olympics that had more than 57 competitors."

### Question [34/50] — eval-034

- Query: "Who won the gold medal in the men's freestyle 120 kg wrestling event at the Summer Olympics held immediately before 2012?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 8.67 seconds
- Tokens Used: 5304 (Prompt: 5140, Completion: 164)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2008 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2008 Summer.", "formulated_query": "men's freestyle 120 kg wrestling gold medalists 2008 Summer Olympics", "extracted_entities": {"event": "Wrestling at the 2008 Summer Olympics \u2013 Men's freestyle 120 kg"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2008 Summer", "matched_event": "Wrestling at the 2008 Summer Olympics \u2013 Men's freestyle 120 kg", "gold_winner": "Bakhtiyar Akhmedov", "date_held": "21 August 2008"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2008 Summer", "matched_event": "Wrestling at the 2008 Summer Olympics \u2013 Men's freestyle 120 kg", "gold_winner": "Bakhtiyar Akhmedov", "date_held": "21 August 2008"}`
  - Supporting Document Chunks: `Q581364::c0, Q1005230::c0, Q923513::c0, Q1005262::c0, Q61539::c0, Q679802::c0, Q140244::c0, Q600157::c0, Q3499032::c1, Q1005272::c0`
- Synthesized Prediction:
  > "The Summer Olympics immediately preceding 2012 were the 2008 Summer Olympics. 

In the **Men's freestyle 120 kg** event (full title: **Wrestling at the 2008 Summer Olympics – Men's freestyle 120 kg**), held on August 21, 2008, the gold medal was won by **Bakhtiyar Akhmedov** [Q581364::c0]. 

*(Note: Artur Taymazov of Uzbekistan originally crossed the finish line/won first place, but was subsequently stripped of the gold medal due to a positive doping test, leaving Bakhtiyar Akhmedov as the gold medalist) [Q581364::c0].*"

### Question [35/50] — eval-035

- Query: "According to the provided corpus, which rowing event at the 2012 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.87 seconds
- Tokens Used: 1722 (Prompt: 1570, Completion: 152)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Women's eight", "full_event_title": "Rowing at the 2012 Summer Olympics \u2013 Women's eight", "competitors": 56, "competition": "2012 Summer", "sport": "Rowing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Women's eight", "full_event_title": "Rowing at the 2012 Summer Olympics \u2013 Women's eight", "competitors": 56, "competition": "2012 Summer", "sport": "Rowing"}`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.81 seconds
- Tokens Used: 228 (Prompt: 194, Completion: 34)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `gsql_sumaccum` -> Details: `{"result_count": 3, "matching_events": ["Short-track speed skating at the 2018 Winter Olympics \u2013 Men's 1500 metres (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics \u2013 Women's 3000 metre relay (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics \u2013 Women's 1500 metres (36 competitors)"], "competition": "2018 Winter", "threshold": 34, "sport": "Short-track speed skating"}`
  - In-Database Graph Facts: `{"tool": "gsql_sumaccum", "result_count": 3, "matching_events": ["Short-track speed skating at the 2018 Winter Olympics \u2013 Men's 1500 metres (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics \u2013 Women's 3000 metre relay (37 competitors)", "Short-track speed skating at the 2018 Winter Olympics \u2013 Women's 1500 metres (36 competitors)"], "competition": "2018 Winter", "threshold": 34, "sport": "Short-track speed skating"}`
  - Supporting Document Chunks: `Q47309900::c0, Q47309958::c0, Q47309929::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 3 short-track speed skating events at the 2018 Winter Olympics that had more than 34 competitors."

### Question [37/50] — eval-037

- Query: "According to the provided corpus, which sailing event at the 1996 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 2.18 seconds
- Tokens Used: 2203 (Prompt: 2118, Completion: 85)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "470 Men's", "full_event_title": "Sailing at the 1996 Summer Olympics \u2013 Men's 470", "competitors": 72, "competition": "1996 Summer", "sport": "Sailing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "470 Men's", "full_event_title": "Sailing at the 1996 Summer Olympics \u2013 Men's 470", "competitors": 72, "competition": "1996 Summer", "sport": "Sailing"}`
  - Supporting Document Chunks: `Q7400319::c0, Q7400319::c1`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the sailing event at the 1996 Summer Olympics with the highest number of competitors was the **470 Men's** event, also known as **Sailing at the 1996 Summer Olympics – Men's 470**, with a total of **72** competitors [Q7400319::c0]."

### Question [38/50] — eval-038

- Query: "According to the provided corpus, how many athletics events at the 2008 Summer Olympics had more than 40 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.67 seconds
- Tokens Used: 213 (Prompt: 182, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 21, "matching_events": ["Athletics at the 2008 Summer Olympics \u2013 Women's 100 metres (85 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 400 metres (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's marathon (95 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's hammer throw (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 400 metres (55 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's long jump (42 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 200 metres (46 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 20 kilometres walk (48 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 200 metres (63 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 3000 metres steeplechase (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's marathon (82 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 800 metres (58 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 50 kilometres walk (61 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's heptathlon (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's shot put (44 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 110 metres hurdles (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 1500 metres (48 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 5000 metres (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's javelin throw (54 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 100 metres (80 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 20 kilometres walk (51 competitors)"], "competition": "2008 Summer", "threshold": 40, "sport": "Athletics"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 21, "matching_events": ["Athletics at the 2008 Summer Olympics \u2013 Women's 100 metres (85 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 400 metres (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's marathon (95 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's hammer throw (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 400 metres (55 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's long jump (42 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 200 metres (46 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 20 kilometres walk (48 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 200 metres (63 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's 3000 metres steeplechase (50 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's marathon (82 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 800 metres (58 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 50 kilometres walk (61 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's heptathlon (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's shot put (44 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 110 metres hurdles (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 1500 metres (48 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 5000 metres (43 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Women's javelin throw (54 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 100 metres (80 competitors)", "Athletics at the 2008 Summer Olympics \u2013 Men's 20 kilometres walk (51 competitors)"], "competition": "2008 Summer", "threshold": 40, "sport": "Athletics"}`
  - Supporting Document Chunks: `Q853040::c0, Q853040::c1, Q932865::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 21 athletics events at the 2008 Summer Olympics that had more than 40 competitors."

### Question [39/50] — eval-039

- Query: "According to the provided corpus, how many boxing events at the 1992 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 3.25 seconds
- Tokens Used: 206 (Prompt: 175, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 3, "matching_events": ["Boxing at the 1992 Summer Olympics \u2013 Flyweight (31 competitors)", "Boxing at the 1992 Summer Olympics \u2013 Bantamweight (31 competitors)", "Boxing at the 1992 Summer Olympics \u2013 Featherweight (31 competitors)"], "competition": "1992 Summer", "threshold": 30, "sport": "Boxing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 3, "matching_events": ["Boxing at the 1992 Summer Olympics \u2013 Flyweight (31 competitors)", "Boxing at the 1992 Summer Olympics \u2013 Bantamweight (31 competitors)", "Boxing at the 1992 Summer Olympics \u2013 Featherweight (31 competitors)"], "competition": "1992 Summer", "threshold": 30, "sport": "Boxing"}`
  - Supporting Document Chunks: `Q10497008::c0, Q10426127::c0, Q10495989::c0`
- Synthesized Prediction:
  > "According to the provided database result, there were 3 boxing events at the 1992 Summer Olympics that had more than 30 competitors."

### Question [40/50] — eval-040

- Query: "Who won the gold medal in the event held at Stadium Australia on 27 September 2000 (heats)29 September 2000 (semi-finals)30 September 2000 (final)?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 12.18 seconds
- Tokens Used: 3726 (Prompt: 3528, Completion: 198)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Stadium Australia", "date_constraint": "27 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics \u2013 Women's 1500 metres", "gold_winners": ["Nouria M\u00e9rah-Benida"], "date_matched": true, "candidate_events_checked": 31}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Stadium Australia", "date_constraint": "27 september 2000", "year_filter": "2000", "event": "Athletics at the 2000 Summer Olympics \u2013 Women's 1500 metres", "gold_winners": ["Nouria M\u00e9rah-Benida"], "date_matched": true, "candidate_events_checked": 31}`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.57 seconds
- Tokens Used: 211 (Prompt: 180, Completion: 31)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 4, "matching_events": ["Alpine skiing at the 2006 Winter Olympics \u2013 Women's slalom (64 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Men's giant slalom (82 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Women's giant slalom (65 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Men's slalom (97 competitors)"], "competition": "2006 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 4, "matching_events": ["Alpine skiing at the 2006 Winter Olympics \u2013 Women's slalom (64 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Men's giant slalom (82 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Women's giant slalom (65 competitors)", "Alpine skiing at the 2006 Winter Olympics \u2013 Men's slalom (97 competitors)"], "competition": "2006 Winter", "threshold": 63, "sport": "Alpine skiing"}`
  - Supporting Document Chunks: `Q1042644::c0, Q1005801::c0, Q2574045::c0`
- Synthesized Prediction:
  > "According to the provided corpus, there were 4 alpine skiing events at the 2006 Winter Olympics that had more than 63 competitors."

### Question [42/50] — eval-042

- Query: "Who won the gold medal in the mixed trap shooting event at the Summer Olympics held immediately before 1992?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.74 seconds
- Tokens Used: 13157 (Prompt: 12957, Completion: 200)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "1988 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 1988 Summer.", "formulated_query": "mixed trap shooting event winner 1988 Summer Olympics", "extracted_entities": {"event": "Shooting at the 1988 Summer Olympics \u2013 Mixed trap"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "1988 Summer", "matched_event": "Shooting at the 1988 Summer Olympics \u2013 Mixed trap", "gold_winner": "Dmitry Monakov", "date_held": "20 September 1988"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "1988 Summer", "matched_event": "Shooting at the 1988 Summer Olympics \u2013 Mixed trap", "gold_winner": "Dmitry Monakov", "date_held": "20 September 1988"}`
  - Supporting Document Chunks: `Q7500750::c0, Q7500750::c1, Q7500739::c0, Q7500737::c0, Q7500772::c0, Q7500743::c0, Q7500748::c0, Q775967::c0, Q7500753::c0, Q7500743::c1`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 7.62 seconds
- Tokens Used: 1144 (Prompt: 996, Completion: 148)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Carioca Arena 3", "date_constraint": "11 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics \u2013 Women's team \u00e9p\u00e9e", "gold_winners": ["Loredana Dinu, Simona Gherman, Simona Pop, Ana Maria, Popescu"], "date_matched": true, "candidate_events_checked": 17}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Carioca Arena 3", "date_constraint": "11 august 2016", "year_filter": "2016", "event": "Fencing at the 2016 Summer Olympics \u2013 Women's team \u00e9p\u00e9e", "gold_winners": ["Loredana Dinu, Simona Gherman, Simona Pop, Ana Maria, Popescu"], "date_matched": true, "candidate_events_checked": 17}`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 10.50 seconds
- Tokens Used: 13433 (Prompt: 13302, Completion: 131)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2012 Summer.", "formulated_query": "Who won the gold medal in the women's 75 kg weightlifting event at the 2012 Summer Olympics?", "extracted_entities": {"event": "Weightlifting at the 2012 Summer Olympics \u2013 Women's 75 kg"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics \u2013 Women's 75 kg", "gold_winner": "Lydia Valent\u00edn", "date_held": "3 August 2012"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2012 Summer", "matched_event": "Weightlifting at the 2012 Summer Olympics \u2013 Women's 75 kg", "gold_winner": "Lydia Valent\u00edn", "date_held": "3 August 2012"}`
  - Supporting Document Chunks: `Q1371783::c0, Q1997032::c0, Q2380135::c0, Q905493::c0, Q241789::c0, Q955487::c0, Q1997551::c0, Q1092809::c0, Q1065640::c0, Q2196657::c0`
- Synthesized Prediction:
  > "The Summer Olympics held immediately before 2016 were the **2012 Summer Olympics** [temporal_precedes]. 

The gold medal in the women's 75 kg weightlifting event, titled **Weightlifting at the 2012 Summer Olympics – Women's 75 kg**, was won by **Lydia Valentín** of Spain [temporal_precedes, Q1997032::c0]. (She was officially declared the champion following subsequent disqualifications of the original medalists due to doping retests) [Q1997032::c0]."

### Question [45/50] — eval-045

- Query: "Who won the gold medal in the women's moguls freestyle skiing event at the Winter Olympics held immediately before 2014?"
- Archetype: `temporal`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 8.86 seconds
- Tokens Used: 11236 (Prompt: 11120, Completion: 116)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2010 Winter", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2010 Winter.", "formulated_query": "Women's moguls freestyle skiing event 2010 Winter Olympics gold medal winner", "extracted_entities": {"event": "Freestyle skiing at the 2010 Winter Olympics \u2013 Women's moguls"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2010 Winter", "matched_event": "Freestyle skiing at the 2010 Winter Olympics \u2013 Women's moguls", "gold_winner": "Hannah Kearney", "date_held": ""}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2010 Winter", "matched_event": "Freestyle skiing at the 2010 Winter Olympics \u2013 Women's moguls", "gold_winner": "Hannah Kearney", "date_held": ""}`
  - Supporting Document Chunks: `Q905561::c0, Q905472::c0, Q905561::c1, Q938164::c0, Q850196::c0, Q1067177::c0, Q1222488::c0, Q15056095::c0, Q905472::c1, Q1067177::c1`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 9.09 seconds
- Tokens Used: 7107 (Prompt: 6954, Completion: 153)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `temporal`
  - Termination Reason: `sufficient_evidence` (Iteration 2)
  - Action Trace:
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2000 Summer", "matched_event": "", "gold_winner": "", "date_held": ""}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event for the competition 2000 Summer.", "formulated_query": "Who won the gold medal in the light flyweight boxing event at the 2000 Summer Olympics?", "extracted_entities": {"event": "Boxing at the 2000 Summer Olympics \u2013 Light flyweight"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `temporal_precedes` -> Details: `{"preceding_competition": "2000 Summer", "matched_event": "Boxing at the 2000 Summer Olympics \u2013 Light flyweight", "gold_winner": "Brahim Asloum", "date_held": "17 September to 30 September 2000"}`
  - In-Database Graph Facts: `{"tool": "temporal_precedes", "preceding_competition": "2000 Summer", "matched_event": "Boxing at the 2000 Summer Olympics \u2013 Light flyweight", "gold_winner": "Brahim Asloum", "date_held": "17 September to 30 September 2000"}`
  - Supporting Document Chunks: `Q4951841::c0, Q4951844::c0, Q4951837::c0, Q4951839::c0, Q3925468::c0, Q10497009::c0, Q4951834::c0, Q4951842::c0, Q15056263::c0, Q4951845::c0`
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

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 2.31 seconds
- Tokens Used: 1931 (Prompt: 1844, Completion: 87)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2004 Summer Olympics \u2013 Men's individual road race", "competitors": 144, "competition": "2004 Summer", "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's cycling road race", "full_event_title": "Cycling at the 2004 Summer Olympics \u2013 Men's individual road race", "competitors": 144, "competition": "2004 Summer", "sport": "Cycling"}`
  - Supporting Document Chunks: `Q2445057::c0, Q2445057::c1`
- Synthesized Prediction:
  > "According to the provided corpus and graph facts, the cycling event at the 2004 Summer Olympics with the highest number of competitors was the **Men's cycling road race** (full event title: **Cycling at the 2004 Summer Olympics – Men's individual road race**), featuring **144** competitors from 43 nations [Q2445057::c0]."

### Question [48/50] — eval-048

- Query: "According to the provided corpus, how many cycling events at the 2012 Summer Olympics had more than 30 competitors?"
- Archetype: `aggregation`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 2.54 seconds
- Tokens Used: 209 (Prompt: 179, Completion: 30)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `aggregation`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"result_count": 7, "matching_events": ["Cycling at the 2012 Summer Olympics \u2013 Men's cross-country (47 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's team pursuit (44 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's individual road race (144 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's road time trial (37 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Women's team pursuit (32 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Women's individual road race (66 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's BMX (32 competitors)"], "competition": "2012 Summer", "threshold": 30, "sport": "Cycling"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "result_count": 7, "matching_events": ["Cycling at the 2012 Summer Olympics \u2013 Men's cross-country (47 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's team pursuit (44 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's individual road race (144 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's road time trial (37 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Women's team pursuit (32 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Women's individual road race (66 competitors)", "Cycling at the 2012 Summer Olympics \u2013 Men's BMX (32 competitors)"], "competition": "2012 Summer", "threshold": 30, "sport": "Cycling"}`
  - Supporting Document Chunks: `Q2036655::c0, Q2297621::c0, Q754412::c0`
- Synthesized Prediction:
  > "According to the provided database, there were 7 cycling events at the 2012 Summer Olympics that had more than 30 competitors."

### Question [49/50] — eval-049

- Query: "According to the provided corpus, which shooting event at the 1988 Summer Olympics had the highest number of competitors?"
- Archetype: `superlative`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 1.40 seconds
- Tokens Used: 1558 (Prompt: 1475, Completion: 83)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `superlative`
  - Termination Reason: `sufficient_evidence` (Iteration 1)
  - Action Trace:
    - Tool Executed: `graph_cache_fallback` -> Details: `{"superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 1988 Summer Olympics \u2013 Men's 50 metre rifle prone", "competitors": 55, "competition": "1988 Summer", "sport": "Shooting"}`
  - In-Database Graph Facts: `{"tool": "graph_cache_fallback", "superlative_event": "Men's 50 metre rifle prone", "full_event_title": "Shooting at the 1988 Summer Olympics \u2013 Men's 50 metre rifle prone", "competitors": 55, "competition": "1988 Summer", "sport": "Shooting"}`
  - Supporting Document Chunks: `Q7500747::c0`
- Synthesized Prediction:
  > "According to the provided corpus, the shooting event at the 1988 Summer Olympics with the highest number of competitors (55 competitors) was the **Men's 50 metre rifle prone** (full event title: *Shooting at the 1988 Summer Olympics – Men's 50 metre rifle prone*) [Q7500747::c0]."

### Question [50/50] — eval-050

- Query: "Who won the gold medal in the event held at Olympic Stadium on 6–9 August at the 2012 Summer Olympics?"
- Archetype: `multi_hop`
- Ground Truth: Held-Out Ground Truth (Official Judging)

#### Agentic GraphRAG

- Evaluation Status: Raw Output Logged (Held-Out Benchmark Set)
- Latency: 89.98 seconds
- Tokens Used: 28442 (Prompt: 28107, Completion: 335)
- Approach Taken:
  - Orchestration Architecture: LangGraph StateGraph Dynamic Router
  - Routed Archetype: `multi_hop`
  - Termination Reason: `max_iterations` (Iteration 6)
  - Action Trace:
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 37}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Could not bind the specific event held at venue Olympic Stadium on date 6\u20139 august.", "formulated_query": "Olympic Stadium\" 2012 Summer Olympics event 6\u20139 August gold medal winner", "extracted_entities": {"event": "Men's javelin throw"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Already resolved: event=Men's javelin throw. Still missing: Could not bind the specific event held at venue Olympic Stadium on date 6\u20139 august.", "formulated_query": "2012 Summer Olympics athletics Men's javelin throw Olympic Stadium 6-9 August gold medal winner", "extracted_entities": {"event": "Men's javelin throw"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Already resolved: event=Men's javelin throw. Still missing: Could not bind the specific event held at venue Olympic Stadium on date 6\u20139 august.", "formulated_query": "Men's javelin throw Olympic Stadium 6-9 August 2012 Summer Olympics gold medal winner", "extracted_entities": {"event": "Women's javelin throw"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Already resolved: event=Women's javelin throw. Still missing: Could not bind the specific event held at venue Olympic Stadium on date 6\u20139 august.", "formulated_query": "Who won the gold medal in the Women's javelin throw held at Olympic Stadium on 6-9 August at the 2012 Summer Olympics?", "extracted_entities": {"event": "Women's javelin throw"}, "chunks_searched": 10, "resolution_status": "resolved"}`
    - Tool Executed: `multi_hop_chain` -> Details: `{"venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
    - Tool Executed: `agentic_gap_resolution` -> Details: `{"gap_addressed": "Already resolved: event=Women's javelin throw. Still missing: Could not bind the specific event held at venue Olympic Stadium on date 6\u20139 august.", "formulated_query": "2012 Summer Olympics Women's javelin throw Olympic Stadium 6-9 August gold medal winner", "extracted_entities": {"event": "Women's javelin throw"}, "chunks_searched": 10, "resolution_status": "resolved"}`
  - In-Database Graph Facts: `{"tool": "multi_hop_chain", "venue": "Olympic Stadium", "date_constraint": "6\u20139 august", "year_filter": "2012", "event": "", "gold_winners": [], "date_matched": false, "candidate_events_checked": 38}`
  - Supporting Document Chunks: `Q1827915::c0, Q1827915::c1, Q326112::c0, Q1798882::c0, Q1798873::c0, Q588440::c0, Q1771958::c0, Q1986718::c0, Q841530::c0, Q348720::c0, Q1799275::c0, Q2618235::c0, Q765839::c0, Q1986718::c1, Q2000939::c1, Q2000939::c0, Q2000968::c0, Q1772012::c0, Q593761::c0, Q284423::c0, Q1649415::c0, Q1771958::c1, Q1409616::c0, Q2069991::c0, Q2069991::c1`
- Synthesized Prediction:
  > "Based on the events held at the Olympic Stadium between 6–9 August at the 2012 Summer Olympics, the following gold medals were won:

- **Women's 100 metres hurdles** (held 6–7 August): **Sally Pearson** (Australia) [Q1827915::c0]
- **Men's discus throw** (held 6–7 August): **Robert Harting** (Germany) [Q765839::c0]
- **Women's javelin throw** (held 7–9 August): **Barbora Špotáková** (Czech Republic) [Q2000939::c0]
- **Men's 200 metres** (held 7–9 August): **Usain Bolt** (Jamaica) [Q1649415::c0]
- **Men's pole vault** (held 8–10 August): **Renaud Lavillenie** (France) [Q2000968::c0]
- **Women's hammer throw** (held 8–10 August): **Anita Włodarczyk** (Poland) — *promoted following the disqualification of Tatyana Lysenko* [Q2069991::c0]
- **Men's javelin throw** (held 8–11 August): **Keshorn Walcott** (Trinidad and Tobago) [Q1986718::c0]"
