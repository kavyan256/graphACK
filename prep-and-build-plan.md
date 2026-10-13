# Prep (Oct 6-14) and build plan (Oct 15-18) for TieTrace

Rules reminder: before Oct 15 12:01 AM IST only notes, sketches, diagrams, reading docs and setting up tools. **No project code.** Everything in the repo must be written during the event, and AI use disclosed.

---

## Prep, Oct 6-14 (non-code)

### Accounts and setup (your actions)
- [ ] Confirm registration on the WeMakeDevs panel (solo or team) before submissions close.
- [ ] Create a free OpenAlex account to get an API key ($1/day free usage instead of ~$0.10). Your choice: it needs your email.
- [ ] Decide the LLM for the agent (needed for "tool selection through MCP"). Options: Claude API (needs credits), a free tier elsewhere, or demoing tool selection through Claude Desktop as the MCP client. Note the cost.
- [ ] Install Docker; pull `falkordb/falkordb:latest` (6.0) and run it once; open FalkorDB Browser. (Tool setup, not project code.)
- [ ] Install Python 3.12 + the official FalkorDB Python client + the MCP Python SDK (just install, no code).

### Design artefacts (allowed: notes, sketches, diagrams)
- [ ] Graph model diagram (from `design-r1.md` section 2 + 5b): research graph + newsroom memory graph.
- [ ] Architecture diagram: loader -> FalkorDB (research graph, newsroom graphs) -> MCP server (read-only tools + fixed write tools) -> agents (Scout, Tie-Checker, Verifier, Review Desk, Writer, Memory) -> UI.
- [ ] Query sketch list (one line per tool: which procedure, which edge types, which parameters).
- [ ] Demo script (90 s) from `design-r1.md` section 7, with exact on-screen steps.
- [ ] README outline: problem, demo GIF, how it works, graph data model, list of Cypher queries/algorithms, evaluation, human verifier layer, ethics, data and licences, setup, AI disclosure, tracks.
- [ ] Ethics section draft: what a "tie" means and doesn't mean; wording rules; human gates; right of reply; named people only from documented public cases.
- [ ] Evaluation protocol: GEBN validation steps, baseline comparison, hold-out test, profile-guard stats.
- [ ] Blog post outline (Best Blog Post award): "How a graph found what the NYT found in 2015".

### Reading (docs pages to read once)
- [ ] Algorithms: maxFlow, SPpaths, BFS, betweenness, labelPropagation; full-text index; GRAPH.COPY; GRAPH.RO_QUERY; Cypher known limitations; MCP server (read-only mode); Python client.
- [ ] OpenAlex: works filters (topics.id, authorships.institutions.id, funders.id, from_publication_date), group_by, institutions (associated_institutions, lineage), authors (ORCID), paging, API key usage.

### Decisions to write down before Oct 15
- [ ] Topics + companies: (1) obesity / physical activity + Coca-Cola (validation), (2) mRNA vaccines + Pfizer (live), reserve: glyphosate + Bayer. Look up the OpenAlex topic IDs (data exploration, no project code).
- [ ] Graph size target: compact demo graph that fits FalkorDB Cloud's free 100 MB if we want a live deployment; otherwise local Docker.
- [ ] UI choice (simplest that shows a path graph and a review card).

---

## Build plan, Oct 15-18 (IST; solo pace; checkpoints are go/no-go)

### Day 1 — Oct 15: data and graph
| Time | Task |
|---|---|
| Hours 1-2 | FalkorDB 6.0 up; 10-node toy graph to test direction behaviour of maxFlow, SPpaths (relDirection), BFS, betweenness; test GRAPH.RO_QUERY and GRAPH.COPY |
| Hours 3-8 | Loader: OpenAlex -> FalkorDB for topic 1 (obesity + Coca-Cola): works, authors, affiliations, corporate families, funders; derive CO_AUTHORED with counts/years/recency_cost; full-text index |
| Hours 8-10 | Load topic 2 (mRNA + Pfizer); node/edge counts; memory size check |
| **Checkpoint** | One Cypher query returns a dated path from a GEBN scientist to Coca-Cola funding. **If the pipeline is broken by hour 6, switch to backup C01.** |

### Day 2 — Oct 16: core tools and validation
| Time | Task |
|---|---|
| Morning | find_experts, tie_paths (SPpaths), tie_strength (maxFlow), prove_independence (BFS), profile_quality, verify_tie |
| Afternoon | GEBN validation run + baseline numbers (direct vs graph) + profile-guard stats; fix data issues |
| Evening | MCP server exposing the tools (read-only via GRAPH.RO_QUERY; fixed write tools separate) |
| **Checkpoint** | From an MCP client: "How tied is expert X to Coca-Cola?" returns a score + paths with DOIs |

### Day 3 — Oct 17: human verifier, memory, agent, UI
| Time | Task |
|---|---|
| Morning | Newsroom memory graph: save_check, Decision, re-check diff |
| Midday | Human verifier layer: review_queue ranked by impact, record_verdict (paper ruled out; SAME_AS / DIFFERENT_FROM), impact_of_verdict ("changed N scores") |
| Afternoon | Agent orchestration (LLM picks tools), Writer draft note + editor approval |
| Evening | Minimal UI: expert list, path view, review card, approval buttons |
| **Checkpoint** | Full demo flow works end to end. **If not: drop all stretch items.** |

### Day 4 — Oct 18: evaluation, docs, video, submit
| Time | Task |
|---|---|
| Morning | Final evaluation numbers; README (data model, queries, evaluation, ethics, licences, AI disclosure); architecture diagram |
| Midday | Record the 90-second demo video; optional live deployment (only if stable) |
| Afternoon | Submit (repo, README, video, deployment or local setup, tracks 1 + 2) **by ~6 PM IST**, leaving a buffer before 11:59 PM |
| Evening | Optional blog post |

### Stretch order (only after the day-3 checkpoint passes)
1. GRAPH.COPY verdict preview ("if you rule this paper out, 16 scores change")
2. Editor panel builder
3. Independent alternatives via labelPropagation communities
4. Bridges via betweenness
5. Live deployment
6. Blog post

### Backup plan (C01 LayoverGuard)
Trigger: TieTrace data pipeline not working by Oct 15 hour 6. Data: OpenFlights (ODbL) + hand-curated transit rules (`design-c01.md`). Small graph, lower risk, weaker graph story.
