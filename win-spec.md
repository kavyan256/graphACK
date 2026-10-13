# Win spec: what a winning Graph Hacks Track 1 entry looks like (Stage 0 output, Oct 5 2026)

Internet-only research. Every claim below has a source; anything inferred is marked **(inferred)**.

---

## 1. What the organisers have actually published

| Source | What it says | What it does NOT say |
|---|---|---|
| [Event page](https://www.wemakedevs.org/hackathons/falkordb) | Brief: "Build an agent that acts on connected data, remembers what it learns, and can show how it got to each answer." "The graph has to shape what the agent does, not sit on the side." Track 1 focus: multi-hop reasoning, graph queries and algorithms as agent tools, tool selection through MCP, actions based on what the graph shows, explainable results. | No judges, no judging criteria, no workshops listed |
| [Rules](https://www.wemakedevs.org/hackathons/falkordb/rules) | "If the product still works once FalkorDB is taken out, the graph is decoration rather than the thing the product runs on." Must explain "the graph model, the queries, the project architecture, and the technical decisions behind them." Fully AI-generated work without "meaningful participant contribution, verification, or technical understanding may be rejected." | No criteria or weights, no video length |
| [Schedule](https://www.wemakedevs.org/hackathons/falkordb/schedule) | Only: registration open, hacking starts Oct 15 12:01 AM IST, submissions close Oct 18 11:59 PM IST | No results date, no live judging |
| [Resources](https://www.wemakedevs.org/hackathons/falkordb/resources) | Links: getting started, Docker, FalkorDB Cloud, Browser, Cypher, clients, algorithms, integrations, community projects, GraphRAG-SDK, videos ("Write effective Cypher queries", "Advanced graph algorithms in FalkorDB") | No starter template |

**Judging is online, from the README + demo video + repo (+ live deployment if any) (inferred from the submission list).** Judges cannot ask us questions, so the README and video carry everything.

---

## 2. How WeMakeDevs judges (best available proxy)

WeMakeDevs publishes criteria for its other hackathons, and they are consistent:

| Hackathon | Criteria |
|---|---|
| [Agent Harness (Aug 2026, TrueFoundry)](https://www.wemakedevs.org/hackathons/trueforge) | 6 criteria, **weighted equally**: Potential impact ("Does the agent do a clear, useful job someone would actually hand over?"), Creativity and originality ("an inventive job to give an agent, or an inventive way of doing it?"), Technical excellence ("complete, reliable, and well structured?"), Use of sponsor tools ("central to the project rather than a thin wrapper"), Control and safety ("stop for a human before anything irreversible?"), Presentation ("Does the demo clearly explain the problem, the agent working, and where [the sponsor tool] fits?") |
| [FutureStack GenAI (2025)](https://archive.wemakedevs.org/hackathons/futurestack25) | Potential impact, Creativity & originality, Technical implementation (incl. "quality of integration with required sponsor technologies"), Learning & growth, Aesthetics & UX, Presentation & communication ("clarity of the README, the quality of the demo video") |
| [AgentHack (2025, Portia)](https://archive.wemakedevs.org/hackathons/agenthack25) | Potential impact, Creativity & originality, Learning & growth, Implementation (incl. sponsor features), Aesthetics & UX |

The Agent Harness kick-off guide also warned: "LLMs are already very good at explaining what someone should do. The harder problem is building an AI system that can reliably do the work." ([source](https://www.wemakedevs.org/blogs/agent-harness-hackathon-kick-off))

**Inference:** Graph Hacks will most likely be judged on about six equal criteria: impact, originality, technical excellence, use of FalkorDB, one event-specific criterion (here probably explainability / "show how it got to each answer"), and presentation.

---

## 3. What FalkorDB's own judges praised before

**Memory Meets Motion** (Aug 2026, SF, 8 hours; [write-up](https://www.falkordb.com/blog/memory-meets-motion-the-falkordb-standouts/)). 1st: Atrium.
- Atrium: "cleverest move is graph-native"; grouping students by misconception is "the kind of relationship that... a flat table or vector search simply cannot express."
- Hopper: 7-hop path "in under 100 milliseconds"; avoids vector search because "a negative result needs an actual traversal, not a similarity score."
- Smart Home: fairness is "explicitly a multi-hop graph query... awkward to model outside a graph database."
- AgentCourt: a deterministic, non-LLM "Bailiff" has final authority. DealBench: "fails loudly rather than quietly falling back."

**Hack for Humanity** (Sep 19 2026, SF, 4 hours; [write-up](https://www.falkordb.com/blog/how-builders-at-hack-for-humanity-used-falkordb-to-solve-real-community-problems/)). 1st Board of SuperVision, 2nd Can I Park Here?, 3rd LOCAL GACHA.
- Board of SuperVision: real public data (66 meetings, 7,553 nodes), votes as edges, "traversals over the record, not guesses from similar-looking text", read-only Cypher with a 3-second timeout, write-blocking, 100-row limit, UI shows the executed query, **passed 30/30 evaluation tests**.
- Can I Park Here?: everyday pain (street-sweeping tickets), graph versioning, idempotent MERGE imports.
- LOCAL GACHA: model gets no database credentials; every recommendation returns a "via" column.
- Author's summary line: **"The model got to suggest and a read-only query got to decide."**

**What FalkorDB is marketing right now** ([blog](https://www.falkordb.com/blog/)): FalkorDB **6.0 on the new Rust engine (Sep 29)**: 39% fewer CPU instructions, columnar batch execution, **MVCC so reads never block writes**. Other recent themes: agent memory as a retrieval problem, GraphRAG grounding, fraud, supply chain, master data, data-pipeline lineage ("X-ray vision into data pipelines"), shipping enterprise AI as a Claude Skill, n8n agents with a knowledge graph.

---

## 4. The new rubric (replaces the old C1-C9 weights)

Six criteria, mirroring WeMakeDevs, **equal weight, 1-5 each, max 30**. FalkorDB's past-judge taste is built into the descriptions.

| # | Criterion | 5 looks like | 1 looks like |
|---|---|---|---|
| J1 | **Potential impact** | A clear job someone would hand over; a user a judge recognises in 10 seconds; public evidence that the pain is real and common | Vague user, invented pain |
| J2 | **Creativity & originality** | A "that's clever" insight (a hidden reasoning unit as a node, a negative proof, an unexpected use of an algorithm); no close prior art, or a clear difference | Organiser example (fraud, blast radius, generic GraphRAG) with no twist |
| J3 | **Technical excellence** | Works end to end on real data; idempotent import; read-only guards + timeouts; an **evaluation with a number** (e.g. 30/30 tests, precision/recall); clean repo | Demo-only, canned data, no checks |
| J4 | **Use of FalkorDB** | Passes the removal test hard: the core answer *is* a traversal / algorithm / multigraph operation; questions a table or vector search can't express; several Track 1 focus areas visible; memory written back to the graph | Graph is storage; a table would do |
| J5 | **Control, safety & explainability** | Every answer shows its path/evidence; model only suggests, read-only query decides; deterministic check overrides the LLM; human approval before anything irreversible; honest "no data" answers | Black-box answers, model writes to the DB |
| J6 | **Presentation & UX** | 90-second video that tells problem -> agent working -> graph lighting up -> action -> evidence; README with data model + queries; understandable without domain knowledge | Hard to follow, needs domain knowledge |

Plus two numbers **we** track that judges don't score directly:
- **Build risk (solo, 4 days)**: 1 = safe, 5 = likely to fail. Assumes a solo build.
- **Evidence strength**: how much of the scoring rests on verified facts vs. guesses.

### Calibration check (does the rubric rank past winners on top?)
Scored with hindsight, so this is a sanity check, not proof. The rubric's *structure* comes from WeMakeDevs' published criteria, which is independent evidence.

| Hack for Humanity | J1 | J2 | J3 | J4 | J5 | J6 | Total | Actual |
|---|---|---|---|---|---|---|---|---|
| Board of SuperVision | 4 | 4 | 5 | 4 | 5 | 4 | **26** | 1st |
| Can I Park Here? | 5 | 3 | 4 | 3 | 3 | 5 | **23** | 2nd |
| LOCAL GACHA | 3 | 4 | 3 | 3 | 4 | 4 | **21** | 3rd |
| SF Civic Lens / WildSignal / Rimai / Postscript | 3-4 | 2-4 | 3 | 2 | 3-4 | 3-4 | 17-19 | unplaced |

| Memory Meets Motion | J1 | J2 | J3 | J4 | J5 | J6 | Total | Actual |
|---|---|---|---|---|---|---|---|---|
| Atrium | 5 | 5 | 4 | 4 | 4 | 5 | **27** | 1st |
| Hopper (security) | 4 | 3 | 4 | 5 | 5 | 4 | 25 | standout |
| AgentCourt | 3 | 4 | 4 | 3 | 5 | 4 | 23 | standout |
| Drift / Nous | 4 | 4 | 3 | 3 | 4-5 | 3-4 | 22 | standout |
| Other 8 standouts | 2-4 | 3-4 | 3-4 | 2-4 | 2-4 | 3-4 | 17-20 | standout |

Both events' winners come out on top (the old rubric put Atrium at 57/80, below ideas we later dropped).

**What the calibration teaches:**
1. Winners pair a **graph-native concept a judge grasps instantly** with **visible engineering discipline** (guards, evaluations, evidence shown).
2. Algorithmic depth alone does not win (Atrium's core query was two hops). But for **Track 1** the focus list explicitly asks for algorithms and multi-hop, so J4 should show at least one named algorithm doing real work.
3. Everyday pain beats niche pain for J1 (parking tickets came 2nd in a 4-hour hack on impact and UX alone).

### Thresholds
- **25+ / 30**: winner-level (Atrium 27, Board of SuperVision 26). Target.
- **22-24**: competitive; fix the weakest criterion.
- **Under 22**: drop.
- Build risk 4-5: drop or cut scope, whatever the score.

---

## 5. Gates (pass/fail, from the rules)

- [ ] FalkorDB is the primary graph database and **the removal test fails hard** (without FalkorDB the product cannot produce its core answer).
- [ ] Data is public, synthetic, or our own; licence allows a public repo; nothing login-protected, paywalled, or someone else's personal data.
- [ ] Main coding and design work happen Oct 15-18 (notes, sketches, diagrams before are fine).
- [ ] We can explain every part (graph model, queries, architecture, decisions); AI use disclosed.
- [ ] Deliverables possible: public repo, README with setup + graph data model, list of Cypher queries / algorithms, demo video, live deployment or full local setup, track(s) named.

## 6. Kill rules (fixed now, before any idea exists)

1. The core answer is a lookup, or a plain SQL join does ~80% of it -> **kill**.
2. The core needs links extracted by an LLM/ML model -> **kill**.
3. The problem occurs in under ~10% of the data we can use (measured, not assumed) -> **kill**.
4. A free existing tool already gives the core answer and we can't name what we add -> **kill**.
5. Data licence or access breaks a gate -> **kill**.
6. A named algorithm's output is the same as a naive count/sort on our data -> that algorithm is decoration; **kill the claim** (and the idea if it was the core).
7. No public evidence (posts, issues, reviews, statistics) that real people hit the problem -> **warning**; two warnings -> kill.

---

## 7. Must-haves the demo has to show (checklist for any finalist)

**The brief (all three):** acts on connected data / remembers what it learns (written back to the graph, reused next session) / shows how it got to each answer.

**Track 1 focus (aim for all five):**
- [ ] Multi-hop reasoning (3+ typed hops in a real question)
- [ ] Graph queries and algorithms as agent tools (at least one native algorithm doing real work: shortest paths, BFS, PageRank, betweenness, harmonic, WCC, label propagation, max flow, MSF)
- [ ] Tool selection through MCP
- [ ] Actions based on what the graph shows (plan, report, ticket, draft, flag), with human approval
- [ ] Explainable results (path / subgraph shown with every answer)

**FalkorDB strengths worth putting on screen (pick what the idea genuinely needs):**
- An agent loop that fires **many multi-hop queries per question**, fast (the Securin pattern: 5-10 queries, up to 7 hops)
- **"No path" as proof** (Hopper)
- In-database algorithms as named MCP tools
- **One graph per user / case / scenario**, and `GRAPH.COPY` for what-ifs
- `GRAPH.RO_QUERY` for every model-chosen query ("the model suggests, a read-only query decides")
- Vector / full-text index next to traversal, if search is needed
- **Built on FalkorDB 6.0**; with several agents writing while others read, MVCC is a real (not cosmetic) reason to mention it

**Engineering habits past judges noticed (cheap to copy):**
- Read-only Cypher with timeouts and row limits; model never holds DB credentials
- Idempotent MERGE imports, graph version stamped by data hash
- An evaluation suite with a pass count (30/30) or precision/recall on labelled cases
- UI shows the executed query and the evidence
- Says clearly when it has hit the limits of its data; fails loudly, never silently

---

## 8. Competition seen so far (public repos, Oct 5)

| Repo | Theme | Track |
|---|---|---|
| [aegis-graph](https://github.com/Mugunth007/aegis-graph) | Cloud blast radius + self-healing incidents | 1 |
| [renigat7-cpu/graph-hacks-2026](https://github.com/renigat7-cpu/graph-hacks-2026) | Episodic/semantic/procedural memory layer for an agent | 2 |
| [Hydra-Of-Malice/FalkorDB](https://github.com/Hydra-Of-Malice/FalkorDB) ("Minutes") | Shared time-aware memory for agent teams | 2, 3 |
| [howdycarter/graph-hacks-falkordb-2026](https://github.com/howdycarter/graph-hacks-falkordb-2026) | Planning docs, aiming at Track 2 | 2 |
| [SnapGraph-AI-FalkorDB](https://github.com/Rafiaminhaj/SnapGraph-AI-FalkorDB) | Generic multi-agent GraphRAG | ? |
| ClashBuddy (Discord) | Game deck coach, practice project | 1 |

**Reading:** visible peers cluster around **agent memory (Track 2)** and **generic GraphRAG**. Track 1 looks less crowded, but blast radius is taken. "LLM picks a tool -> read-only Cypher -> show the query" is the baseline everyone will have, not a difference.

---

## 9. Presentation plan (applies to any idea)

- 90-second demo video structure: problem in one sentence -> the agent working on a real case -> graph lights up (path / cut / cluster) -> action with human approval -> evidence -> session 2 is better because of memory.
- README: one-paragraph problem, graph data model diagram, the list of Cypher queries / algorithms, evaluation numbers, AI-use disclosure, data sources + licences, FalkorDB SSPLv1 note.
- Separate Best Blog Post award (AirPods 5): the README sections double as the blog post.
