# How FalkorDB is used: case studies, past hackathons, ecosystem (researched Oct 5 2026)

Everything below comes from FalkorDB's own pages/blogs and public repos found by web search. Vendor material, so treat claims (latency etc.) as unverified by us.

## 1. Production case studies (falkordb.com/category/case-studies)

| Who | Field | How FalkorDB is used | Reported result |
|---|---|---|---|
| Securin | Threat intelligence | Knowledge graph of CVEs, threat actors, ransomware families, techniques, assets; AI agents query it 5-10x per interaction, up to 7 hops | 0.3 s on 7-hop queries; removed a 25% query failure rate after migrating |
| SERGAS Group | Legal services | Knowledge graph shipped as a Claude Skill with cited answers | ~50% fewer legal escalations, answers under a minute |
| AdaptX | Healthcare | Clinical (EMR) data relationships | "ease of use", good on non-traversal queries |
| Virtuous AI | Ethical AI | Central store for public + private data feeding PyTorch/TensorFlow pipelines | low latency / accuracy (no numbers) |
| XR.Voyage | Immersive media | Data workstations + knowledge graphs | no numbers |

Use-case pages group these into: corporate documents (legal/compliance), code analysis (dependencies, impact of changes), security (attack paths, incident timelines).

## 2. Hackathons

### Hack for Humanity (civic / community problems, public city data)
Source: falkordb.com/blog/how-builders-at-hack-for-humanity-used-falkordb-to-solve-real-community-problems

| Project | Problem | Data and graph model | Why graph mattered |
|---|---|---|---|
| Board of SuperVision | Make city council decisions discoverable | 66 SF Board of Supervisors meetings -> 7,553 nodes, 6,961 votes. **Votes are edges** between supervisors and items. Query: supervisors who dissent together across meetings | Answers are traversals over the record with video-timestamp citations, not guesses from similar text |
| Can I Park Here? (Best Use of Photon) | Parking legality via iMessage | ~22,500 curb segments + 37,700 street-sweeping entries, curb -> schedule edges | Radius search and join in one query; finds nearby legal alternatives |
| LOCAL GACHA | Send tourists to overlooked local venues | Few Tokyo venues; two-hop traversal via shared neighbourhood or experience | "via" column explains each recommendation; model gets no DB credentials |
| SF Civic Lens | Street photos -> structured 311 tickets | Incidents linked to districts | Audit trail of incident lifecycle |
| Postscript | Patient after-visit summaries | FHIR-style records; separate graph for chat audit logs | Patient context + audit |
| WildSignal | Urban wildlife reports routed to agencies | Species, Area, Agency, Encounter nodes; locations blurred for privacy | Routing + privacy enforcement |
| Rimai | Inga-Spanish translator learning from community corrections | Word relationships, etymology, feedback | Community corrections accumulate |

Common pipeline: messy input -> LLM-structured facts -> `MERGE` into graph -> read-only Cypher -> answer with evidence. Teams also used schema validation, idempotent imports, timeouts, and kept the model away from direct DB access.

### Memory Meets Motion (Aug 3 2026, SF, 8 hours)
Source: falkordb.com/blog/memory-meets-motion-the-falkordb-standouts

| Project | Field | Graph idea |
|---|---|---|
| **Atrium (1st place)** | Education | Each wrong mental model is a node; two-hop traversal groups students by misconception, not score |
| MuscleMemory | Robotics | Links failures and lessons across runs |
| AgentCourt Precedent | AI governance | Prior rulings as precedent nodes; deterministic "Bailiff" overrides the LLM judge |
| Continuum | Enterprise ops | Tracks open-loop debt (unresolved decisions) |
| Facet | Media | Reader-persona-topic graph personalises feed |
| Drift | Dev tools | Decisions as nodes; flags contradictions between meetings and comments on the affected issue, with human approval gate |
| Smart Home Orchestrator | IoT | Room -> occupants -> history for fair conflict resolution |
| Hopper (Security) | Security | Advisory -> package -> dependency -> repo -> service -> customer -> contract clause in under 100 ms; **"no path found" treated as proof of safety** |
| Hopper (Distribution) | Logistics | Agents negotiate cost vs urgency and write outcomes back as precedent |
| Onari | Productivity | Accumulating context graph of ambient notes |
| Nous | Personal assistant | Life graph of people, commitments, protocols; Critic agent validates before arming |
| DealBench | Legal tech | M&A courtroom simulator with memory service |
| Oto.ai | Dev tools | Live task graph, resumes interrupted sessions |

Judge pattern: graph traversal where flat tables or vectors fail; absence of a path as meaningful proof; decisions/commitments/misconceptions as nodes; fail loudly, deterministic check over the LLM.

### Graph Hacks 2026 (Oct 15-18, this event), public peer entries seen so far
- aegis-graph (github.com/Mugunth007/aegis-graph): cloud blast radius + self-healing incident mesh; traces alert to breaking commit 4 hops away, betweenness for choke points, rehearses fix in an ephemeral multigraph, opens a hotfix PR. Synthetic "corporate digital twin" data.
- Minutes (github.com/Hydra-Of-Malice/FalkorDB): shared time-aware memory for agent teams (Tracks 2 and 3).
- ClashBuddy (Discord post, Oct 2026, practice project before the event): Clash Royale deck coach. Claude picks a tool, code runs read-only Cypher, answer shows the query. COUNTERS edges, missing deck roles via `WHERE NOT` ("missing path is the answer"), shortest path between cards, WCC found 4 deck archetypes from synergies, betweenness was all zeros until synergies were stored in both directions. Our score ~46/80 as an entry (tiny hand-made graph, no ground truth, no memory). Signal: "LLM picks tool + read-only Cypher + show the query" is becoming the baseline peers will all have.
- Tracks: Agents That Act on Connected Data (iPhone 18 Pro), Agent Memory and Coordination (PS5), Company Brain (M6 Mac mini).

## 3. Ecosystem and community

| What | Use |
|---|---|
| Graphiti (Zep) | Temporal knowledge graph for agent memory; FalkorDB is a supported backend (sub-10 ms, tenant isolation) |
| Mem0 (mem0-falkordb plugin) | Graph memory backend; ~2% higher score on multi-hop/temporal questions vs vector-only (vendor-reported) |
| Cognee | Agent memory combining graph + vector |
| LangChain / LlamaIndex | GraphRAG and agent-with-memory integrations |
| GraphRAG-SDK | Build GraphRAG apps on FalkorDB |
| QueryWeaver | Graph-powered text-to-SQL: schema as a graph, shortest join paths across tables |
| code-graph | Codebase as graph; MCP tools index_repo, search_code, find_symbol, get_neighbors, impact_analysis, find_path; security scans |
| Community projects | BFSI GraphRAG assistant, mental-health QA chatbot, trip-planning swarm agent, code-graph visualisation of AI repos |

## 4. Patterns worth copying
1. Edges that carry the evidence (votes, via-column, video timestamp, citation).
2. Negative proof: "no path found" = safe.
3. Human decisions/commitments/precedents/misconceptions as nodes.
4. Deterministic check overrides the LLM; model never gets DB credentials; read-only Cypher.
5. Small, relatable problem with public data and a one-sentence story.
6. Ephemeral graph per scenario for what-if rehearsal (multi-graph).

## 5. Gaps (from what we found)
- Most uses are GraphRAG, memory, or traversal. Few lean on native algorithms (max flow, SPpaths, MSF, WCC, PageRank) even though Track 1 names "graph algorithms as tools". Only aegis-graph (betweenness) and Securin (deep hops) clearly do.
- Crowded: security/blast radius, code impact, text-to-SQL, GraphRAG over documents, agent memory.

## Frameworks checked (Oct 5 2026)
- Flexible GraphRAG (github.com/stevereiner/flexible-graphrag, Apache 2.0, now v0.8.x; FalkorDB support since Sep 2025): document -> LLM-built KG -> GraphRAG/RAG/hybrid search platform with LlamaIndex/LangChain, 15 property-graph DBs, 10 vector DBs, MCP server, 14 data sources. Verdict: not for our Track 1 ideas (auto KG building = LLM extraction red flag; FalkorDB is just one swappable backend, so it hides the graph work; heavy setup). Possible fit only for a Track 3 "company brain" over documents.
