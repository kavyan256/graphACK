# Idea rating criteria: Graph Hacks (FalkorDB), Track 1

Track 1: **Agents That Act on Connected Data**
Event: Oct 15 12:01 AM IST to Oct 18 11:59 PM IST 2026, online, solo or up to 4.
Rule of thumb: rate the *problem* first, then the *solution*. Do not fall for a topic before it passes the gates.

---

## How to use this sheet

1. Write the idea in one sentence (see "Idea card" at the bottom).
2. Run the **quick screen** in Part H (official brief filter), then check the **gates** (Part A). Any failed gate means drop the idea.
3. Check the **Track 1 focus areas** (Part B).
4. Score the **quality criteria** (Part C), 1 to 5 each, and mark the evidence as Verified or Unverified.
5. Answer the **make-or-break questions** (Part D) in writing.
6. Add up the weighted score (Part E) and compare against the thresholds.

---

## Part A: Gates (pass or fail, from the hackathon rules)

- [ ] **Graph does real work.** Rule: "A visualisation drawn on top of ordinary storage does not qualify." FalkorDB must be the primary graph database and central to the product.
- [ ] **Data is allowed and legal to use.** Official rules (wemakedevs.org/hackathons/falkordb/rules, checked Oct 5 2026) permit **public information, synthetic datasets, or personal data you own**. Prohibited: private, login-protected, paywalled, personal (someone else's), or otherwise restricted data. Licence checked (watch for NonCommercial / NoDerivatives / ShareAlike when the repo must be public). Synthetic data is allowed, but then there is no ground truth beyond our own rules: say so honestly.
- [ ] **Data is reachable in 4 days** without heavy cleaning (we can name the dataset and where to download it).
- [ ] **Main coding starts after Oct 15.** Before that: ideas, notes, graph sketches, diagrams only. (Rules page: frameworks, open-source libraries, templates, public APIs and datasets are allowed; only original work done during the event is judged.)
- [ ] **We can explain the code and the graph model** (AI assistance is allowed but must be disclosed).
- [ ] **Deliverables are possible:** public repo, README with graph data model, the Cypher queries / graph algorithms used, demo video, live deployment or full local setup, declared track.
- [ ] **FalkorDB-fit (see Part F):** the core answer is produced by a FalkorDB native algorithm or a bounded Cypher traversal, and the data fits in RAM. Fail = the idea would run just as well on a table.

## Part B: Track 1 focus areas (we must be able to show all five)

- [ ] **Multi-hop reasoning:** a real question that needs 3+ links to answer.
- [ ] **Graph queries and algorithms as agent tools:** named tools (e.g. shortest path, reachability, centrality, max flow, components) that the agent calls.
- [ ] **Tool selection through MCP:** the tools are exposed via an MCP server.
- [ ] **Actions based on what the graph shows:** the agent decides and produces something (a plan, report, ticket, ranked list, draft), ideally with a human approval step.
- [ ] **Explainable results:** every answer shows the path / subgraph it used.

FalkorDB native algorithms (so heavy work can run inside the database): BFS, shortest path (SPpath), A* (geographic), all paths with constraints (SSpaths), minimum spanning forest, PageRank, betweenness centrality, harmonic centrality, weakly connected components, label-propagation communities, max flow. Plus Cypher variable-length paths.

---

## Part H: Official brief filter (from the event page, checked Oct 5 2026)

Source: wemakedevs.org/hackathons/falkordb (challenge, tracks, "why graphs", ecosystem sections). Use this as a **first-pass filter** before scoring: an idea that cannot tick H1 and most of H2 is not what the organisers asked for, however clever it is.

**H1. The brief in one line (all three verbs must be visible in the demo):**
> "Build an agent that **acts on connected data**, **remembers what it learns**, and can **show how it got to each answer**."
- [ ] **Acts:** the agent does something based on the graph (plan, ranked list, ticket, draft, flag), not only answers.
- [ ] **Remembers:** what the agent learns is written back into the graph (`MERGE` new nodes/edges: verdicts, precedents, user corrections) and is used again in a later session. Our current criteria do not score this, so check it here. Show it in the demo: session 2 is better or faster because of session 1.
- [ ] **Shows the path:** every answer comes with the path or subgraph it used.
- [ ] "The graph has to shape what the agent does, not sit on the side." If the agent would reach the same decision without the graph, fail.

**H2. "Work the graph has to do" (the page lists five; aim for at least four, Track 1 must have 1 and 5):**
- [ ] 1. Follow connections across data (multi-hop).
- [ ] 2. Remember across sessions (persistent graph memory, not a chat log).
- [ ] 3. Share state between agents (e.g. investigator agent + checker agent read and write the same graph).
- [ ] 4. Connect people, projects, and decisions (human-scale nodes, fits Part G move M1).
- [ ] 5. Show the path behind an answer.

**H3. The problem statement we are solving (the idea must cure at least two):**
- [ ] Agents "see pieces, not the whole picture".
- [ ] They "lose track of what happened in earlier sessions".
- [ ] They "miss how people, systems, and records relate".
- [ ] They "can't explain why they made a choice".

**H4. "One agent problem" test:** "Pick a task where the answer depends on how things connect." The core question must be like the page's examples, i.e. it does not live in one record:
- Which accounts are linked to this flagged transaction? (fraud: organiser example, crowded)
- What did this customer ask for last month, and was it resolved? (memory + history)
- Who on the team has worked on this system before? (people/expertise, closer to Track 3)
- What breaks if this service goes down? (blast radius: crowded, see Hopper and aegis-graph)
- [ ] Write our idea's question in the same style, one line. If it can be answered from one row, fail.
- [ ] Avoid copying an example question directly (C8 penalty), but the *shape* should match.

**H5. FalkorDB features the page promotes (using them signals fit; pick the ones that are genuinely needed):**
- [ ] **Graph algorithms as agent tools:** the page names shortest path, PageRank, centrality, connected components, community detection. At least one is a named MCP tool the agent chooses (Part G, M7).
- [ ] **Cypher:** match patterns, follow paths, return exactly what the agent needs (bounded variable-length paths).
- [ ] **MCP:** tools exposed through an MCP server (Track 1 focus "tool selection through MCP").
- [ ] **Multigraph / one graph per user or tenant:** "thousands of isolated graphs" in one instance. Good uses: one graph per case/investigation, a what-if copy, per-user memory graph.
- [ ] **Ecosystem integration** (optional, only if it saves time): GraphRAG-SDK, QueryWeaver (text-to-Cypher), Graphiti (temporal memory), Cognee, LangChain, LlamaIndex. Using one is fine; letting it hide the graph work is not.
- [ ] **FalkorDB Browser** for inspecting the model and for demo screenshots (saves building our own viz on day 1).
- [ ] "Context for AI agents" tags: agent memory, multi-agent state, connected company knowledge.

**H6. Rules and logistics from the page (adds to Part A):**
- [ ] FalkorDB is the **primary** graph database behind core functionality.
- [ ] Live deployment preferred; local setup + demo video accepted.
- [ ] New work during Oct 15-18. Frameworks, open-source libraries, public APIs, templates and public datasets are allowed; only original work done during the event is judged. Do **not** pre-write our own core code: the rules page says main coding *and design work* start after Oct 15 (notes and graph sketches are fine).
- [ ] Any language. Official clients: Python, Node.js, Java, Rust, Go, PHP, C#.
- [ ] Coding assistants allowed; we stay accountable for code and architecture.
- [ ] A team **may enter more than one track** with one project. Track 1 stays primary; note if the idea also fits Track 2 (memory: episodic/semantic/procedural, shared state, per-tenant memory) as a free second chance.

**H7. Prizes and extra chances:**
- One prize per track: Track 1 iPhone 18 Pro, Track 2 PS5 + GTA VI, Track 3 M6 Mac mini ($20,000 pool).
- **Best blog post: AirPods 5** (separate award; plan a write-up of the graph model and queries, cheap to do from the README).
- Top 50 teams get T-shirts.
- No published judging criteria, so the brief (H1) and Track 1 focus list (Part B) are the best proxy.

**H8. Extra points from the rules page (wemakedevs.org/hackathons/falkordb/rules, checked Oct 5 2026):**
- [ ] FalkorDB can run as **Docker, self-hosted, or FalkorDB Cloud** (all accepted). Plan: Docker locally, Cloud for the live demo if setup is quick.
- [ ] **Name every track we enter** at submission (one project can enter several).
- [ ] **AI use must be disclosed** in the README. A project "entirely generated using AI without meaningful participant contribution" may be rejected, so keep a short log of what we designed and decided ourselves.
- [ ] **We must be able to explain the code, the graph model, the queries and the architecture.** This is the only judging rule written down, so the README needs a clear data model diagram and a list of the queries, and every team member should be able to walk through them.
- [ ] Each person can be on **one team only**. Every member of a winning team gets the prize.
- [ ] IP stays with the team. Plagiarism or trying to game the judging means disqualification, so credit borrowed ideas (e.g. "move inspired by Atrium/Hopper") and every dataset/licence in the README.
- [ ] Submission checklist (all required): public repo; README with setup + graph data model; Cypher queries / algorithms the product depends on; demo video; live deployment or full local setup; track(s) entered.

**Quick screen (use before Parts C-E; 30 seconds per idea):**
1. Can I say the agent's question in one line, like the H4 examples, and is the answer a path or set, not a row?
2. What does the agent **write back** to the graph, and how does that help next session?
3. Which named algorithm or bounded traversal is the agent's main tool?
4. What action does it take, and what path does it show as proof?
If any answer is "nothing" or "not sure", the idea fails the brief: fix or drop.

---

> **Oct 5 2026: the C1-C9 weights and Part E thresholds are superseded by the J1-J6 rubric in `win-spec.md`** (mirrors WeMakeDevs' published criteria; ranks past winners on top). Parts A, B, F and H remain useful as checklists.

## Part C: Quality criteria (score 1 to 5, weight in brackets)

### C1. Graph does the heavy work (x3)
- [ ] The core answer is a **path, reachability set, cut/flow, component, centrality, or pattern**, not a lookup or one-hop join.
- [ ] **The "could SQL do this?" test:** name at least one query that is awkward in SQL (variable-depth, typed edges, path returned as the answer, what-if removal).
- [ ] The heavy computation runs **inside FalkorDB**, not in Python with the DB used as storage. Name the exact procedure (`algo.BFS`, `algo.SPpaths`, `algo.SSpaths`, `algo.pageRank`, `algo.betweenness`, `algo.WCC`, `algo.MSF`, max flow) or the bounded Cypher pattern. Score 3 or lower if none is named.
- [ ] **The "does a built-in already do it?" test:** if a standard tool (e.g. `apt rdepends --recurse`, `dependsOnPkgs()`, grep) already returns the core answer, the graph value must come from what sits on top (a cut, a plan, typed what-if, explanation). Say what that is.
- [ ] The graph is big or deep enough that a judge will not say "a table would do".
- [ ] Relationships are **given in the data**, not predicted by an ML model first (if a matcher does the real work, the graph is a small final step).

### C2. Real user and real pain (x2)
- [ ] We can name **who** uses it (a specific role), **what task** they do, and **what they do today** (the painful way).
- [ ] The user story fits in one sentence: "A [role] has to [task]. Today that means [pain]. Our agent does it by [graph step] and shows [evidence]."
- [ ] Honest about who realistically uses it (learners, researchers, small teams) vs. professionals who already have paid tools.

### C3. Objective way to check it works (x2)
- [ ] There is **ground truth** or a built-in correctness test (e.g. totals must match, recalculation, known cases, labelled data, hold-out set).
- [ ] We can compare against a **baseline** (keyword search, plain RAG, plain table) and show where we win.
- [ ] We can report accuracy / coverage honestly, including where we lose.

### C4. Action and explainability (x2)
- [ ] The agent **acts**, not only answers (plan, ranked list, report, draft, flagged cases).
- [ ] **Human approval** before anything final (Atrium-style gate).
- [ ] A **verification step** before output (check against source, simulation, or rule).
- [ ] Every result carries its **evidence path**.

### C5. Data ready and legal (x2)  (gate already passed, this scores how good the data is)
- [ ] Data is clean enough to load in a day.
- [ ] Size fits (not so small that a table does it, not so big we cannot load it).
- [ ] Licence allows a public repo and demo.

### C6. Feasibility in 4 days (x2)
- [ ] Core can be built as layers: Layer 1 (data + queries), Layer 2 (tools + MCP + agent), Layer 3 (action + checks), Layer 4 (demo + README).
- [ ] No single step is a research project (e.g. building an accurate matcher or extractor from scratch).
- [ ] A fallback demo exists if the hardest part fails.

### C7. Atrium-style insight (x1)  (Atrium won by modelling a hidden human reasoning unit as a node)
- [ ] One sentence with a "same X, different Y" contrast.
- [ ] The node is a **unit of human reasoning** (a misconception, a precedent, a decision, a commitment, a gap, a criterion), not just a technical object.
- [ ] A short traversal answers something a table or vector search cannot.

### C8. Originality (x1)
- [ ] We searched for prior art: commercial tools, open-source tools, research, earlier FalkorDB projects and hackathon entries.
- [ ] Our difference is stated (usually: the agent + explanation + action, or a fresh domain).
- [ ] Not just one of the organizers' own examples (fraud, security triage, codebase) without a twist.

### C9. Demo clarity (x1)
- [ ] A 90-second story: setup, question, graph lights up, action, evidence.
- [ ] A memorable visual (path, ripple, map) that is more than a chart.
- [ ] The problem is explainable to a judge who does not know the domain, in 10 seconds.

---

## Part D: Make-or-break questions (answer each in writing)

1. Is the problem real, and who feels it?
2. Does the graph do heavy work, or is it a lookup with a picture?
3. Does the dataset give us the links, or must a model guess them?
4. How will we prove it works, and what if the result is weak or null?
5. What already exists (tools, papers, projects), and what do we add?
6. What is the hardest technical step, and can we test it in the first hours?
7. What could embarrass us in the demo (wrong link, stale data, scale blow-up)?
8. What are the ethical / legal risks, and what is the disclaimer?
9. Which parts are verified by evidence and which are only my assumptions?

## Red flags (any one needs a clear answer or the idea is dropped)

- The core value is a **lookup table or converter**.
- A **matching or extraction model** does the real work; the graph is only cleanup.
- Data licence blocks a public repo (NoDerivatives, restricted, login-only).
- Data needs **personal information**.
- A **dense graph** where path counts explode and pruning cannot run inside the DB.
- The idea depends on a number we cannot see yet (for example, "how many stale references exist?"); mark it as the first thing to test.
- Heavy **prior art** with no clear difference.
- Only works if a **city, country, or private dataset** we cannot access is available.

---

## Part F: FalkorDB-fit test (use it to qualify the idea)

Why FalkorDB: it stores the graph as sparse adjacency matrices (one global matrix plus one per relationship type) and runs queries through GraphBLAS, so multi-hop traversal and whole-graph algorithms are its strong point. Vendor benchmark claims (e.g. PageRank 18.5 ms vs 417 ms on 820K nodes / 9.8M edges) are **unverified** until we run them ourselves.

**Strong fit (design the idea around these):**
- [ ] The answer is a **path, reachability set, component, centrality ranking, spanning forest, or flow/cut**, one of FalkorDB's native algorithms.
- [ ] Edges are **typed** and given in the data, so Cypher can filter by relationship type per hop.
- [ ] Graph is **thousands to a few million edges**: big enough that a table is awkward, small enough for RAM.
- [ ] **Multi-tenant / what-if graphs:** one graph key per scenario is natural (e.g. a copy with a node removed).
- [ ] The agent needs **MCP tools** and optionally **vector or full-text index** next to the graph (FalkorDB has an MCP server and a GraphRAG SDK).

**"Table + library" test (added Oct 5 2026):** if the whole idea is one fixed computation (a scheduling or colouring solve, one max-flow run) that networkx / OR-tools could do on a table in memory, FalkorDB is not needed and judges will notice. FalkorDB is justified when the graph is a long-lived, typed source of truth that the agent queries in **many different ways at question time** (multi-hop lookups, what-if copies, "no path" proofs, explanations), with algorithms as some of those tools. Example fail: exam-clash scheduling (graph colouring is not a native FalkorDB algorithm; a CSP solver does it better).

**Weak fit (avoid or mitigate):**
- [ ] Edges must be extracted from text with regex or an LLM (the graph becomes cleanup, red flag).
- [ ] Data is too big for RAM (e.g. full Lichess) unless we can sample it.
- [ ] Needs Neo4j-only features (APOC etc.). FalkorDB covers an openCypher **subset**: test every planned query in the first hours.
- [ ] Unbounded variable-length "all paths" on a dense graph. Use constrained procedures (SPpaths with limits, BFS with depth) so pruning runs inside the DB.
- [ ] The demo needs rich graph visualisation (we must build it ourselves).

**Before committing, check (unverified items as of Oct 2026):**
- [ ] Doc page for each planned algorithm: directed vs undirected, weights, limits. (Peer lesson, ClashBuddy: betweenness returned all zeros until edges were stored in both directions. Test direction behaviour of every algorithm on a 10-node toy graph in hour 1; e.g. cognate paths go child -> ancestor <- child, so a directed-only shortest path finds nothing.)
- [x] Licence wording: FalkorDB is SSPLv1 (verified Oct 5 2026, FalkorDB GitHub); README should say "SSPLv1", not "open source (OSI)".
- [ ] Every planned Cypher query runs on FalkorDB, not just in the openCypher spec.
- [ ] Persistence is not relied on for the demo (keep a reload script).

---

## What judges liked at the previous FalkorDB hackathon (Memory Meets Motion, Aug 2026)

Source: FalkorDB blog "Memory Meets Motion: The FalkorDB Standouts". Winner was Atrium (each wrong mental model is a node).
- Graph traversal where a flat table or vector search cannot express the question ("two-hop Cypher traversal").
- **Absence of a path treated as proof** (Hopper security: "no path found" = safe, not a similarity gap). Design for negative proofs where possible.
- Decisions, commitments, precedents and misconceptions modelled as nodes (Drift, Nous, AgentCourt, Atrium).
- Fail loudly, a deterministic check that overrides the LLM (AgentCourt "Bailiff", Nous "Critic").
- Crowded already: security "advisory -> package -> customer" blast radius (Hopper); a Graph Hacks 2026 entry "aegis-graph" does cloud blast radius + self-healing. Blast-radius ideas need a strong twist.

---

## Part G: Innovation moves (borrow the move, not the problem)

Source: past FalkorDB winners and standouts (see `falkordb-usage-landscape.md`). Rule from the user: do **not** pick a problem similar to theirs; reuse their kind of solution on a new, relatable, human-scale problem (not internet-scale infrastructure, not spreadsheets, not contrived toys).

- [ ] **M1 Hidden reasoning unit as a node** (Atrium: misconception). "Same X, different Y" contrast.
- [ ] **M2 The edge carries the evidence** (Board of SuperVision: votes as edges with video timestamps).
- [ ] **M3 Precedent nodes** (AgentCourt, Hopper Distribution): past decisions are written back and reused.
- [ ] **M4 "No path found" as proof** (Hopper Security).
- [ ] **M5 Explain with a "via"** (LOCAL GACHA): every answer says which link it came through.
- [ ] **M6 Deterministic check over the LLM** (AgentCourt Bailiff, Nous Critic; model gets read-only Cypher, no DB credentials).
- [ ] **M7 Native algorithm as a tool** (underused by past entries: max flow, SPpaths, WCC, PageRank, MSF). A Track 1 entry built on one stands out.

An idea should use at least two moves, and M1 or M2 should be the core.

---

## Lessons from stress tests so far

- **Extraction red flag is real.** The statute-to-regulation impact idea scored about 47/80: eCFR cross-references are text-only (not tagged links), authority citations are free text at part level, and prior art is heavy (arXiv "Measuring Law Over Time", UK Lex Graph, Regintelgraph, policy-change-impact-agent-v2). Dropped unless a 10-minute sample of one CFR title shows cleanly parseable edges.
- **Check the built-in baseline.** For package graphs (Debian, CRAN) the plain closure is already a one-liner. The graph value has to be the cut / removal plan / capability nodes / explanation.
- **Exact ground truth is rare and valuable** (e.g. `apt-get remove --simulate`, FEN equality in chess). Prefer ideas with it.
- **Tiny graphs fail the FalkorDB-fit gate.** Microservice root cause on RCAEval (Oct 5): labels are great but each system has only tens of services, the strongest baseline (BARO) is metric-based, and aegis-graph already does RCA. Grievance escalation: 3-4 levels per sector, a table does it.
- **LLM extraction as the core step keeps failing C1/C6** (unwritten-rules norms, outage contributing factors, PEP rejection reasons). Prefer ideas where the links are given by the data (e.g. "Fixes #123" issue-to-commit links).
- **Ideas that copy a past winner's domain get a lower C8.** Borrow the move (Part G), not the domain.
- Verified data licences so far: deps.dev CC-BY 4.0, Reactome CC0, Lichess CC0 (huge, sample), GloBI CC BY 4.0, OpenFlights ODbL (share-alike, 2014 data). Unverified: US Code XML status, Stacks Project licence, CourtListener bulk licence, Debian metadata licence.

---

## Part E: Scoring sheet

| Criterion | Weight | Score (1-5) | Weighted | Evidence (Verified / Unverified) |
|---|---|---|---|---|
| C1 Graph does the heavy work | x3 | | | |
| C2 Real user and pain | x2 | | | |
| C3 Objective check | x2 | | | |
| C4 Action and explainability | x2 | | | |
| C5 Data ready and legal | x2 | | | |
| C6 Feasibility in 4 days | x2 | | | |
| C7 Atrium-style insight | x1 | | | |
| C8 Originality | x1 | | | |
| C9 Demo clarity | x1 | | | |
| **Total (max 80)** | | | | |

Thresholds:
- **64 or more:** strong, worth a full stress test.
- **48 to 63:** consider, fix the weak criteria first.
- **Below 48:** drop.
- Any failed gate (Part A) or unanswered red flag: drop, whatever the score.

Scoring notes:
- Score only from evidence we have. Mark unverified claims as such and score them conservatively.
- Tier ideas instead of ranking them when scores are within a few points; the scoring has noise.
- If an idea relies on one unknown, name it and plan to test it first.

---

## Idea card (copy for each idea)

```
Idea name:
One sentence:
User story:  A [role] has to [task]. Today that means [pain].
Graph model: nodes: ...  edges: ...
The hidden thing made a node (Atrium move):
Heavy graph work (FalkorDB feature, exact procedure name):
FalkorDB-fit (Part F): strong / weak, and why:
SQL-awkward query:
Data source + licence + size:
Objective check:
Baseline to beat:
Action the agent takes:
MCP tools:
Prior art found:
Biggest risk + first test:
Gate check (A):  pass / fail
Score (E):       /80
```

---

## Saved candidates

> **ARCHIVED Oct 5 2026: the user scrapped every candidate below.** Kept only as a record of what was tried and why it failed. The new process is in `idea-discovery-plan.md`; lessons are carried over there.

### Candidate 1: Spreadsheet assumption auditor (saved Oct 5 2026, not yet scored)

```
Idea name: Spreadsheet assumption auditor
One sentence: Parse a workbook's formulas into a graph, then trace which input cells and hardcoded constants drive each output, with a recalculation proof.
User story:  A finance analyst or auditor has to trust a model's output. Today that means Excel trace-precedents arrows, one cell at a time.
Graph model: nodes: cell, range, sheet, constant, named input.  edges: REFERENCES (formula -> precedent), CONTAINS (range -> cell), HARDCODES (formula -> constant).
The hidden thing made a node (Atrium move): the assumption (input cell or constant buried in a formula). "Same output, different hidden inputs."
Heavy graph work (FalkorDB feature, exact procedure name): algo.BFS (descendants), algo.WCC (disconnected blocks), algo.pageRank / algo.betweenness (driver ranking), Cypher cycle pattern for circular refs.
FalkorDB-fit (Part F): strong. One graph per workbook (multi-graph), 1k-100k edges, edges from a deterministic parse (no ML).
SQL-awkward query: all descendants of an input cell through typed edges at unbounded depth; what-if removal of an input.
Data source + licence + size: Enron spreadsheet corpus (figshare, CC BY 4.0; 15,770 workbooks, ~20M formulas; SheetJS/enron_xls mirror, 74 GB total, cherry-pick files). FUSE corpus is an alternative (copyright of individual files unchecked).
Objective check: change an input, recalculate with headless LibreOffice; changed cells must equal the graph's descendant set (precision/recall, report losses).
Baseline to beat: Excel trace precedents/dependents (one cell, one level), pattern-based auditors (Spreadsheet Detective, SheetWhiz, ExcelErrorFinder).
Action the agent takes: ranked list of driving assumptions + audit report (hardcodes, dead cells, cycles, disconnected blocks), human approval before final.
MCP tools: descendants(cell), precedents(cell), top_drivers(output), find_hardcodes(sheet), find_cycles(), dead_cells(), recalc_check(cell).
Prior art found: commercial auditors exist (cell-by-cell or pattern-based). Our difference: agent + evidence path + recalculation proof.
Biggest risk + first test: range refs (A1:A100) explode into dense edges (model ranges as nodes); INDIRECT/OFFSET cannot be resolved statically (flag them); LibreOffice vs Excel function differences; Enron files are real corporate data (screen for personal info before choosing a demo workbook). First test: parse ~20 workbooks, count edges and range density.
Gate check (A):  pending (data reachability and personal-data screen)
Score (E):       /80 (not yet scored)
```

---

### Candidates 2-6: "move-borrowing" ideas (saved and stress-tested Oct 5 2026)

Scores are conservative and from desk research only (no data loaded). V = verified by web source, U = unverified.

#### Candidate 2: Bug deja vu ("same error, different root cause") — re-scored ~48/80 (Oct 5), weak
Re-score notes (V): >70% of bug reports lack stack traces (study of 835,381 issues, 250 projects); LLM localisation agents already get 63-79% top-1 file on SWE-bench Lite; GitHub has native duplicate detection (public preview June 2026); Sentry Seer claims 94.5% root-cause accuracy; Sentry already marks resolved issues as "regressed" and surfaces the commit that closed them. The regression-detector pivot only survives for library users reading public issue history, which is a thin niche.
```
One sentence: Match a new stack trace to past issues, follow each to the commit that fixed it, and when past fixes disagree, ask one question that splits them.
User story: A developer hits an error and finds 12 old issues; half had a different cause. Today they read them all.
Graph model: nodes: ErrorSignature, StackFrame, Function, File, Issue, FixCommit/PR.  edges: RAISED_IN (issue->signature), HAS_FRAME, IN_FUNCTION, FIXED_BY (issue->PR, from "Fixes #123", given by data), CHANGED (PR->function/file).
Moves: M1 (root cause as node), M3 (past fixes are precedents), M5 (answer says "via issue #X fixed by PR #Y").
Heavy graph work: frames -> functions -> PRs that changed them -> issues they fixed (3-4 typed hops); algo.BFS; PageRank over function-fix graph for "usual suspects".
Data: SWE-bench (V: 2,294 issue->PR pairs, 12 Python repos; licence U) or our own crawl of a few big repos' issues + linked PRs (GitHub API, token).
Objective check: hold out issues with known fixing PRs; does the graph rank the files actually changed in the top-k? Labels come free.
Baseline: IR bug localisation (BugLocator reported ~40% MAP, V), plain vector search over issue text.
Prior art: bug-localisation research (large), Sentry AI grouping (V: separates "different root cause" errors at event level), Copilot-style assistants.
Biggest risk / first test: the key number is unknown: how many issues contain stack traces, and how often one signature maps to different fixes. Count this on 2-3 repos first; if rare, the "same error, different cause" story collapses.
Score: C1 3, C2 4, C3 4, C4 4, C5 3, C6 3, C7 4, C8 2, C9 4 = 55
```

#### Candidate 3: Unwritten-rules reviewer — 51/80, consider (red flag)
```
One sentence: Mine past review comments into project norms, attach them to the folders where reviewers enforce them, and pre-review a PR against them with citations.
Evidence of pain (V): a mastra issue says projects enforce ~120 recurring review conventions by hand, ~10 written down.
Data (V): GitHub Public Pull Request Comments, Zenodo 10138317, CC BY 4.0, 13M+ comments; CodeReviewer dataset CC BY 4.0.
Moves: M1 (norm as node), M2 (review comment is the evidence edge).
Objective check: hold out recent PRs; did reviewers raise the predicted norms? Matching is fuzzy (needs an LLM judge).
Prior art (V): CodeRabbit Learnings and path_instructions do this commercially.
Red flag: an LLM clusters comments into norms, so a model does the real work; the graph (norm -> folder) is shallow.
Score: C1 2, C2 4, C3 3, C4 4, C5 4, C6 3, C7 4, C8 2, C9 3 = 51
```

#### Candidate 4: Precedent court for open-source proposals — 46/80, drop
```
Data (V): PEPs are public domain / CC0 and have a standard "Rejected Ideas" section; Rust RFCs Apache/MIT, closed RFC PRs labelled "postponed".
Problems: users are niche (people writing language proposals); matching "same idea" across proposals needs an LLM; graph shallow; prior art: OpenSpec rejected-proposal convention, Selvedge decision history, academic PEP decision studies.
Score: C1 2, C2 2, C3 2, C4 3, C5 4, C6 4, C7 4, C8 3, C9 3 = 46
```

#### Candidate 5: Outage precedent check for design docs — 41/80, drop
```
Data: VOID has ~10,000 incidents from ~600 companies (V) but licence U; danluu/post-mortems is CC BY-SA 4.0 data (V), links to external reports.
Problems: contributing factors must be extracted by an LLM (red flag); no ground truth; incident.io and AI-SRE tools already link past incidents.
Score: C1 2, C2 3, C3 2, C4 3, C5 2, C6 3, C7 4, C8 2, C9 3 = 41
```

#### Candidate 6: Grievance escalation navigator (India) — 46/80, drop (FalkorDB-fit gate fails)
```
Facts (V): RBI Ombudsman after 30 days of no reply, appeal within 30 days; telecom appeal within 3 months of disposal; IRDAI Bima Bharosa ~15 days then Insurance Ombudsman.
Problems: 3-4 levels per sector, a table does it; getnyay.in already publishes a full escalation matrix and per-company guides.
Score: C1 1, C2 5, C3 2, C4 4, C5 3, C6 4, C7 2, C8 1, C9 4 = 46
```

---

### New ideas, round 2 (Oct 5 2026, preliminary, not fully scored)

#### Candidate 7: Etymology bridge vocabulary planner
```
One sentence: To learn a new language, start from words you already know through a shared ancestor or loan, ordered by shortest etymology path, each with a "via" explanation.
User story: Someone moving to another Indian state (or learning any language) has to build vocabulary. Today that means flat word lists with no link to what they already know.
Moves: M1 (the ancestor word is the hidden node: "same root, different languages"), M5 (via explanation), M7 (shortest paths through a large DAG).
Data (V): EtymDB 2.0, CC BY-SA 4.0, 1.8M lexemes, 700k+ relations, 2,536 languages; etymology-db, CC BY-SA 3.0, 3.8M entries, 31 relation types (both from Wiktionary, links given by structured templates).
Coverage (V, uneven): Wiktionary lists 2,673 Hindi terms borrowed from Classical Persian, 1,082 Bengali, but only 33 Tamil from Classical Persian and 31 Tamil from Portuguese. Indian-language coverage is the first thing to test.
Objective check: hide explicit cognate links and test whether shared-ancestor paths recover them (precision/recall). Learning benefit itself is not measurable in 4 days.
Prior art: cognate tips (Rosetta Stone blog), apps like Cognate and Indilingo; no etymology-graph planner found.
Risks: coverage gaps outside Hindi/Urdu/Persian/English; "action" is a study plan, which is soft.
```

#### Candidate 8: Cricket matchup weakness planner
```
One sentence: From ball-by-ball data, find each batter's weakness pattern (bowler type, phase, venue) and plan which available bowler to use, with the deliveries as evidence.
Moves: M2 (each delivery is an evidence edge), M1 (weakness pattern as node: "same batter, different weakness"), M7 (PageRank-style opponent-adjusted ratings).
Data (V): Cricsheet, ODC-BY 1.0, 22,905 matches ball-by-ball, JSON/CSV.
Objective check: hold out recent matches; do predicted weak matchups produce more dismissals / lower strike rate than the batter's baseline?
Prior art (V): network/PageRank analysis of batsmen and bowlers (2012-2014 papers), Markov-chain rankings (cricmetric 2026), commercial matchup analytics.
Risks: much of it is aggregation a table can do; avoid anything that looks like fantasy-sports betting.
```

#### Rejected in round 2
- Kialo "crux finder" (max flow over argument trees): Kialo terms forbid research/commercial use of scraped data; only synthetic substitutes (syncIALO, ODC) exist.
- Election turncoat tracker: TCPD Political Career Tracker already shows party switchers; licence unclear; civic domain too close to Board of SuperVision.

---

### New ideas, round 3 (Oct 5 2026, preliminary, not scored)

- **Candidate 9: Football "cut the build-up" planner.** Passes are evidence edges (M2); max flow / min cut (M7) finds the fewest opposing players to press to cut the route from defence to striker. Data (V): StatsBomb open data, free under a user agreement with attribution + logo. Prior art: passing-network research is large; min-cut pressing plan not found yet (U). Check: held-out matches, does pressing the cut players line up with lower opponent xG (weak, partial).
- **Candidate 10: Human-like explanation paths (Wikispeedia).** Explain a new concept starting from one you know, along the route humans actually take, not the shortest one. Hidden node: the "landmark" concepts people route through (M1). Data (V): SNAP Wikispeedia, 4,604 articles, 119,882 links, 51,318 finished human paths; licence U. Check: do our paths match held-out human paths better than shortest paths? Labels exist. Risk: 2007 schools-Wikipedia, small and old.
- **Candidate 11: Pantry substitution via shared flavour compounds.** "Same compounds, different ingredient" (M1), answer says which compounds it went via (M5). Data (V): Ahn et al. 2011 flavour network dataset on Zenodo, CC BY 4.0 (FlavorDB is NC/ND, avoid). Check: needs a public substitution list as ground truth (U). Prior art: Foodpairing, KitcheNette research.
- **Candidate 12: Chess transposition-aware repertoire.** Position as hidden node ("same position, different move order"); exact ground truth (FEN equality); coverage on held-out Lichess games (CC0). Prior art (V): Chessbook, ChessFlare, Chessreps repertoire builders already use game data; crowded.
- **Candidate 13: Guitar "one chord unlocks the most songs".** Data (V): Chordonomicon, 666k+ songs, CC BY-NC 4.0, scraped from Ultimate Guitar. Mostly a bipartite coverage count, a table can do it.
- **Candidate 14: Swap chains (room / book / shift swaps) via cycles.** Synthetic data only, cycle packing is not a native FalkorDB algorithm. Weak.
- Rejected quickly: EV charging routes (ABRP, PlugShare, Google Maps), Codeforces practice paths (many recommenders, handles are other people's data), movie remake chains (no real action).

---

### Candidate 15: Claim Origin Tracer (saved Oct 5 2026 at user's request, not yet researched or scored)
```
One sentence: For a viral claim, trace where it first appeared and how it spread (who copied whom), and show the path back to the original source.
Possible moves: M1 (the claim itself is the hidden node: "same claim, different wording/outlets"), M2 (each copy/citation/repost is an evidence edge with timestamp), M4 ("no path to a primary source" = unsupported), M5 ("via" chain back to origin).
To research next: public data with given links (citations, quote/retweet/reshare links, hyperlinks between articles), licence, prior art (fact-checking tools, provenance research), ground truth (known fact-checked cases with documented origins), and whether matching "same claim" needs an LLM (red flag).
```

---

### Round 4 picks (saved Oct 5 2026 at user's request, desk research only, not scored)

#### Candidate 16: Benchmark Leak Tracer
```
One sentence: Trace how an AI benchmark's test questions travel into training datasets and from there into models, so a reported score can be flagged as possibly contaminated with the path as evidence.
Graph: Benchmark -> (copied into / derived from) Dataset -> (merged into) Dataset -> (trained on) Model. Lineage links come from dataset/model card metadata (e.g. Hugging Face `datasets:` / `base_model:` fields, U for dataset-to-dataset fields); overlap edges from deterministic n-gram matching (not an LLM).
Moves: M2 (overlap evidence on the edge), M4 ("no path from benchmark to model" = clean as far as metadata shows), M5 (via chain).
Why it matters (V): ~40% of HumanEval examples reported contaminated; removing contaminated GSM8K items drops accuracy ~13 points (per 2026 write-up).
Prior art (V): detection research (n-gram overlap, DyePack backdoor dye, PaCoST confidence tests). A lineage graph across datasets and models not found yet (U).
Risks: metadata is incomplete, so "clean" can only mean "no recorded path"; n-gram overlap at scale is compute-heavy, so sample.
```

#### Candidate 17: Rumour Firebreak
```
One sentence: For a spreading false claim, find the fewest accounts or groups whose correction would cut most of the spread (vertex/edge blocking), and draft the corrections.
Moves: M7 (cut/flow style blocking), M2 (reshare edges with timestamps), M4.
Prior art (V): a large research area: influence minimisation by vertex blocking, edge blocking, community cuts (several arXiv papers 2017-2025).
Data: PHEME and Twitter15/16 cascade datasets are used in research (licence U; Twitter data usually shared as IDs only). Live platform data is login/API restricted.
Risks: heavy academic prior art; blocking algorithms are not native FalkorDB procedures (max flow is, so frame it as a cut).
```

#### Candidate 18: Old Photo, New Story
```
One sentence: Trace a news image back to its first appearance and show the chain of reuse, flagging when an old image is passed off as new.
Moves: M1 ("same image, different story"), M2 (reuse edges with dates), M4 (no earlier appearance found = possibly original).
Risks: finding earlier appearances needs reverse image search (Google/TinEye APIs are keyed or paid, U); perceptual-hash matching is deterministic but needs an image corpus.
```

#### Candidate 19: AI or not, via provenance (not detection)
```
Finding (V): AI-text detectors are unreliable; OpenAI withdrew its classifier after it caught only 26% of AI text with a 9% false-positive rate. Classifying "is this AI?" is a model problem, not a graph problem.
Graph angle: C2PA Content Credentials embed signed manifests whose "ingredients" link each asset to the assets it was made from, forming a provenance graph (V); AI-generation disclosure is an assertion (C2PA v2.1); DALL-E 3 images carry C2PA metadata (V).
Idea: follow the ingredient chain; "AI-generated" propagates through edits; "no path back to a signed capture" = unverified origin (M4).
Risks: how many C2PA-signed files are publicly available (U); metadata is often stripped when images are re-uploaded.
```

#### Candidate 18 (revised Oct 5 2026): "Is this photo/video real?" Origin Tracer
User's framing: decide whether a photo or video is real by **finding its origin with a graph**, not by detecting AI generation.
```
Graph model: nodes: MediaItem (one per near-duplicate cluster), Appearance (a post/article where it was used, with date), Caption/Claim, Source (outlet/account), Keyframe (for video), Fact-check.
  edges: NEAR_DUPLICATE (perceptual-hash distance, deterministic), CROP_OF / FRAME_OF, APPEARS_IN (with date), CLAIMS (appearance -> caption), DEBUNKED_BY.
How the graph finds origin: cluster all copies (algo.WCC over NEAR_DUPLICATE), earliest dated Appearance in the cluster = origin candidate; path from the viral post back to it (time-respecting); compare first caption with viral caption ("same image, different story" = out of context, M1); no earlier appearance in the corpus = possibly original (M4, only within our corpus).
Verdicts: original / recycled (old media, new claim) / edited (crop or composite of earlier media) / unknown.
Ground truth (V): 5Pils dataset, 1,676 fact-checked images annotated with original provenance, source, date, location (licence U); AMMeBa large in-the-wild media misinformation dataset (licence U); fact-checked WhatsApp image sets from India 2019 (897 images) and Brazil 2018 (licence U); Snopes fauxtography 838 image-claim pairs. Check: does the graph's earliest node match the labelled original date/source?
Corpus for appearances: NewsCLIPpings ~988K news image-caption pairs built on VisualNews (licence U); COSMOS 200K images / 450K captions (arXiv licence, access by form).
Prior art (V): Google "About this image" shows when an image was first indexed and its early uses; InVID-WeVerify plugin extracts video keyframes and runs reverse search across Google, Bing, Yandex, Baidu, TinEye. Our add: the reuse/claim graph across many posts, caption drift, verdict with evidence path, agent-drafted verification note with human approval.
Biggest risk: coverage. We can only find origins inside the corpus we index; live reverse-search APIs are keyed or paid (U). First test: take 50 labelled 5Pils images and see how many have an earlier appearance in an open news corpus.
```

---

### Revived with synthetic data allowed (Oct 5 2026)

Re-checked earlier ideas that died mainly on data. Each must still pass the "table + library" test.

1. **Debate / Design-Decision Crux Finder** (revives the Kialo idea). Claims are nodes (M1), support/attack edges carry the reasoning (M2), "no supporting path from evidence" = unsupported claim (M4), the crux = the smallest set of claims whose rejection cuts the thesis off from its support (min cut via max flow, M7). Many query types over one lasting graph (what falls if I reject X, where do two people actually disagree, which claim decides it), so it passes the table test. Data (V): syncIALO, synthetic Kialo-style debates, ~560K claims, 1,000 training debates, "permissive ODC licence", NetworkX graphs on Hugging Face. IT-dev angle: technical design debates (e.g. "Postgres vs MongoDB" RFC threads). Risks: synthetic debates are LLM-generated; no human-labelled "true crux"; building a graph from a real discussion would need LLM extraction.
2. **Org / Club Access Continuity.** People, accounts, recovery emails/phones, roles; what-if "this person graduates/leaves", "no recovery path" proof, one backup that fixes the most. Synthetic university of hundreds of clubs. Passes table test (many what-if questions). Risks: toy feel; access topics sit near the crowded security lane.
3. **WhatsApp-style Forward Chain: origin + firebreak.** Synthetic forwarding network with simulated rumours; find the likely origin and the fewest groups to correct. Simulation gives exact ground truth (we know the true source). Risks: academic prior art on source detection and influence blocking; synthetic realism.
4. **Blood Match Network / Flood Relief Router** (medium): only valid as a lasting network the agent explores in many ways, not one max-flow run.

Still dead even with synthetic data: exam-clash scheduling (table test), microservice RCA (aegis-graph overlap), credential cascade (security crowded), origin tracer for images (needs real images).

---

### Candidate 20: Independence Counter / Citogenesis Detector (Oct 5 2026, after user preference check)
User preferences (asked Oct 5): users = developers, students, everyday people; demo should make judges think **"that's clever"**; liked areas = ripple events, origin/misinformation, dev workflow, learning; data = **mix of real and synthetic is fine**.
```
Clever insight: "12 sources" is often 1 source. True corroboration = the number of node-disjoint paths from a claim back to distinct original sources (Menger: max flow = disjoint paths). Circular loops (Wikipedia -> news -> back into Wikipedia) are citogenesis.
Moves: M1 (the original source is the hidden node: "many citations, one origin"), M2 (citation/link edges with dates), M4 ("no path to a primary source" = unsupported; a cycle back to itself = circular), M7 (max flow for independence count).
Real data (V): Wikipedia Citations dataset, 44.8M citations from the Feb 2024 English dump (Zenodo/Figshare; licence U); 29.3M in the 2020 version with URLs in 85% of citations. Links are given by citation templates, not an LLM.
Ground truth (V): Wikipedia's "List of citogenesis incidents" (documented real cases, e.g. Sacha Baron Cohen/Goldman Sachs, Maurice Jarre fake quotes, Casio F-91W year repeated by BBC). Check: does the graph flag these and their loops?
Missing link to fill: what each cited article itself cites/links to (crawl or Common Crawl link data, U) and edit dates (Wikipedia revision history API) to order events in time.
Synthetic layer: scenario generator for demo stories (a rumour copied across outlets) on top of the real structure.
Prior art (V): circular reporting is a known concept; fact-checking guides advise counting distinct domains; no tool found that computes disjoint-path independence or detects citogenesis loops automatically (U).
Risks: crawling cited pages' outbound links at scale; many news articles don't link their sources (so "no path" may mean "unlinked", not "unsupported"); citogenesis list is small (tens of cases).
```

#### Candidate 20 stress test (Oct 5 2026): 55/80, consider (best insight + demo so far)
```
Verified facts:
- Wikipedia Citations 2024 (Zenodo 10782978): CC BY 4.0, 44.8M citations, 10.96M news citations, 8.5 GB zip; fields include page title, source title, URL, domain, identifiers, citation text, type. It does NOT include the sentence/claim each citation supports (must map from wikitext around the <ref>, deterministic).
- Wikipedia "List of citogenesis incidents": ~50+ documented cases with diff links and archived sources (e.g. Bazalgette sewer anecdote, Maurice Jarre quotes, Alan MacMasters toaster hoax cited back via a museum page, fidget spinner inventor).
- FalkorDB algo.maxFlow: directed, weighted (capacity property), yields maxFlow, flow edges, edgeFlows; no min-cut output (derive it). Node-disjoint paths need node splitting (in/out node pair, capacity 1).
- Prior art: Ground News counts outlets per story with bias breakdown (not independence); Churnalism (2013) detected press-release copying with text matching; AllSides, MBFC rate outlets. No tool found computing disjoint-path independence or citogenesis loops (U).
- Studies: hyperlinking to sources in news is sporadic and most links do not point to primary sources -> hop-2 graph is sparse.
- Common Crawl host/domain web graphs are public (millions of nodes, billions of edges) but host-level loses per-article links; page-level needs WAT files or fetching.

Make-or-break answers:
1 Real problem: yes, documented; users = Wikipedia editors, fact-checkers, students/researchers; everyday readers indirectly.
2 Graph heavy? Only if hop-2 links exist. With only Wikipedia -> source edges the graph is a star and "independence" collapses to counting distinct domains (a table). Needs crawled outbound links + text-reuse edges.
3 Links given? Citations yes (templates). Hop-2: HTML links (deterministic parse) + n-gram text-reuse edges (deterministic, Churnalism-style), + dates. No LLM needed for core.
4 Proof: recall on the ~50 known citogenesis cases; synthetic scenarios with known truth; precision needs manual review. Small labels.
5 Hardest step: fetching cited articles (link rot -> Wayback), extracting dates and links. Test in first hours.
6 Embarrassment risk: calling a real claim "unsupported" when the article simply didn't link its source. Wording must be "no linked path found", never "false".
7 Ethics: never label a claim false; output is "independence count + paths for a human to review".

Scores: C1 3, C2 3, C3 3, C4 4, C5 3, C6 3, C7 5, C8 4, C9 5 = 55
Fixes that raise it: add text-reuse edges (covers unlinked copying), temporal rule (news published after an unsourced Wikipedia edit = candidate loop), what-if "if this source is discredited, which claims lose all independent support" (passes table test).
First test: (a) 10 citogenesis cases: are cited articles archived, and do dates show the loop? (b) 50 random news citations: what share of cited articles link onward to another source or share text with an earlier article?
```

---

### Candidate 21: Fix-Path Finder (Oct 5 2026) — stress test: ~47/80, drop as pitched; pivot noted
```
One sentence: "I hit upstream bug #123. Which upgrade gets me the fix without breaking my other dependencies?" Path: bug -> fixing PR/commit -> first release containing it -> constraints in my dependency tree -> upgrade plan. "No path" = fix not released / not reachable, so suggest pin or patch.

Verified facts:
- deps.dev API v3: no API key, no stated rate limits; GetRequirements (unresolved constraints, all 7 systems), GetDependencies (resolved graph for npm, Cargo, Maven, PyPI), advisories from OSV. Generated data CC BY 4.0; underlying registry data follows each registry's terms.
- Only 42.2% of closed issues are linked to commits (1,078 starred Java projects, 583,795 issues; cited across issue-commit link-recovery papers DeepLink, FRLink, LinkAnchor). So "bug -> fix commit" is missing more often than present; recovering it is an ML/LLM research problem (red flag).
- "Which release contains this commit" is `git tag --contains <sha>` (GitHub/GitLab feature requests point to this workaround). Built-in baseline covers that hop.
- Snyk already computes "minimum upgrade of the direct dependency that pulls in a fixed transitive version" (for vulnerabilities); Dependabot does security updates too.
- uv (PubGrub resolver) already explains unsatisfiable constraints with a derivation chain, i.e. a "no path" proof with explanation already exists in the resolver.

Make-or-break answers:
1 Real problem: yes but occasional; most devs just upgrade to latest and see if tests pass.
2 Graph heavy? No. Choosing compatible versions is constraint solving (SAT-like), which a resolver does better. Version ranges would have to be expanded into version-to-version edges (dense, red flag). Fails the "table + library" test (Part F): same failure as exam-clash scheduling.
3 Links given? Partly. Constraints yes (deps.dev). Bug -> fix only ~42% of the time; "introduced in" version almost never recorded for non-security bugs (OSV gives affected ranges only for advisories).
4 Proof: strong. Upgraded lockfile resolves (exact); BugsInPy-style datasets with fix commits + reproduction tests could check "bug actually gone" (licence U).
5 Prior art: Snyk/Dependabot (security), uv/pip resolvers (compatibility + explanation), git tag --contains (release). Our only gap: non-security bugs, where the data link is weakest.
6 Hardest step: bug -> fix commit when not linked. Test first: sample 50 issues from 3 repos, count closing-PR links.
7 Embarrassment: recommending a version the real resolver rejects; judge says "uv already does this".

Part H quick screen: question in one line yes; write-back yes (solved cases as precedents); named algorithm weak (BFS at best; core is the resolver); action yes (upgrade PR / pin).

Scores: C1 2, C2 3, C3 4, C4 4, C5 3, C6 3, C7 2, C8 2, C9 3 = 47 (drop)

Pivot worth a look (not scored): "Why is this pinned?" Pin Expiry Agent.
  The pin is the hidden decision node (M1: "same pin, different reason"). Graph: Pin -> REASON (issue) -> FIXED_BY (PR) -> MERGED_AS (commit) -> FIRST_IN (release) -> REQUIRES (constraints). The agent remembers why each pin exists, re-checks the chain each session, and opens a PR removing the pin once the fix is released and the resolver accepts it (resolver used as the deterministic checker, M6).
  "No path" = the pin is still needed, with the open link shown. Risk: pins with no recorded reason (comment or commit message) can't be traced; the graph may still be shallow (5 hops, one chain per pin). First test: grep 100 public requirements/package.json files for pin comments that cite an issue URL.
```

#### Candidate 20 re-score with Part H upgrades (Oct 5 2026): ~59/80, consider (top candidate)
```
New prior art (V):
- github.com/andrewdingcanada8/citogenesis: 0 stars, 260 commits, early stage, no licence shown. Proxy page that rates each Wikipedia statement by the number of unique supporting sources found by graph search over citations-of-citations, and checks sources were published before the Wikipedia edit (revision API). No max flow / disjoint paths, no text reuse.
- NewsDeps (arXiv 1909.10266): finds where a news article's information came from by text-reuse / plagiarism detection, shown as a temporal graph. Code availability not stated.
- Text reuse is common but its size is disputed: 39% non-original text in French news, 56% of Greek articles with >=40% non-original content; a 2019 large-scale study (IJoC) found less agency/press-release reuse than earlier studies.
- CC-NEWS (Common Crawl) is public on S3, about 6 TiB/year of WARC files; terms not checked; too large, sample only.

Upgraded design (what changed):
- Hop-2 fix: text-reuse edges (deterministic n-gram shingles) between the sources cited for the SAME claim, plus their outbound links, plus Wayback copies for dead links. Cheap version: no CC-NEWS needed.
- Independence = node-disjoint paths to distinct origins (algo.maxFlow with node splitting); algo.WCC over COPIED_FROM for quick clustering. Honest note: in most cases WCC clusters give the same count; max flow matters when one source draws on several origins.
- Loop rule (Cypher, temporal): source published after the Wikipedia revision that added the sentence AND shares text with that sentence = citogenesis candidate.
- What-if ripple (passes table test): "if this source is discredited, which claims on which pages lose all independent support?" (reverse traversal across the lasting graph).
- Memory (Part H): Origin nodes, COPIED_FROM edges and verdicts are written back; the next claim citing the same sources is answered instantly; when a user marks a source unreliable, the agent re-checks every dependent claim.
- Agents sharing state: Tracer (builds paths), Skeptic (must find a shared upstream before "independent" is accepted), Timekeeper (deterministic date check overrides both, M6).
- Action: draft a talk-page note for a Wikipedia editor, human approval, never edits Wikipedia. Wording: "no independent linked path found", never "false".
- Free labels: syndicated copies carry bylines/datelines ("(AP)", "Reuters", "PTI") -> ground truth for the same-origin clustering. Plus the citogenesis list (~50 cases) and synthetic scenarios with exact truth.
- Legal: public repo stores URLs, hashes and shingles, not article text.

Scores: C1 4, C2 3, C3 3, C4 5, C5 3, C6 3, C7 5, C8 3, C9 5 = 59 (was 55; C8 down for prior art)
To reach 64+: C3 -> 4 (byline-labelled same-origin set, report precision/recall vs "count distinct domains" baseline); C6 -> 4 (first test shows co-cited sources often share text); C2 -> 4 (quote Wikipedia's own circular-sourcing guidance and editor complaints, U).
First test (the number we cannot see yet): 100 Wikipedia claims with 3+ news citations -> fetch the cited pages -> what share have 2+ citations that share text or a byline? If under ~10%, the "12 sources = 1" demo is rare and the idea falls back to 55.
```

---

### Calibration: Atrium (1st place, Memory Meets Motion, Aug 2026) scored on our rubric (Oct 5 2026)
Sources (V): FalkorDB blog "Memory Meets Motion: The FalkorDB Standouts"; README at github.com/nathansso/Atrium.
Facts: turns a search query into a cited curriculum (Firecrawl), then simulates a class. Graph nodes Student, Concept, Misconception, Room, Lesson, Source, Assignment, Support; the key query is the 2-hop Student -> Misconception -> Concept grouping into rooms. 9 agents. Human gates (low-confidence grades, lesson plans, curriculum drafts). **Synthetic student data only**, mock mode, no evaluation. Built in 8 hours with 4 required sponsor tools.
```
C1 2  (2-hop grouping; a table of (student, misconception) could do it; no algorithm)
C2 5  (teachers, same 40% for different reasons: instantly relatable)
C3 1  (synthetic data, no ground truth, no baseline)
C4 5  (lessons + rooms + three human gates + evidence_refs)
C5 3  (synthetic, legal, ready)
C6 5  (built in 8 hours)
C7 5  (defines the move)
C8 3  (misconception-based grouping is known in education research)
C9 5
Total = 6+10+2+10+6+10+5+3+5 = 57
```
**Lesson:** the winner scores 57 on our rubric. Judges rewarded C2, C4, C7, C9 (relatable pain, human gates, a hidden reasoning unit, a clear story) far more than C1/C3. Our rubric is harsher on graph depth and proof than those judges were. Keep it (Track 1 explicitly asks for multi-hop and algorithms), but read 60+ as "beats the last winner on paper", and never trade away C2/C7/C9 to gain C1/C3.

---

### Candidate 7 v2: "You already know this word" — cognate bridge planner (Oct 5 2026): ~63-65/80, strong candidate
Upgrade of Candidate 7 to pass Part H.
```
Hook: "If you speak Hindi, you already know thousands of Bengali words. You just don't know it yet." Plus the trap: Hindi शिक्षा = education, Marathi शिक्षा = punishment (false friend, U, check in data).
One sentence: For someone learning a new language, find the words they already know through a shared ancestor or loan, plan the highest-yield roots to learn next, warn about false friends, and remember progress across sessions.
User story: A student under India's three-language rule, or one of the many internal migrants moving to another state, has to learn a new Indian language. Today that means flat word lists with no link to what they already know. Global version: English/Spanish/Italian.
Graph model: nodes: Word (lang, script, gloss), Root/Ancestor (Sanskrit, Persian, Latin...), Concept (English gloss / translation set), Learner, FalseFriend.
  edges: INHERITED_FROM / BORROWED_FROM / DERIVED_FROM (typed, from Wiktionary etymology templates), TRANSLATES (from translation tables), KNOWS / STRUGGLED_WITH / CONFIRMED (learner memory, written back), FALSE_FRIEND_OF.
Hidden thing made a node (M1): the shared ancestor ("same root, different language") and the false friend ("same form, different meaning", the misconception, like Atrium).
Heavy graph work: shortest typed path known-word -> ancestor <- target-word (algo.SPpaths / bounded Cypher); PageRank or degree on Root nodes for "learn these 20 roots, unlock N words"; WCC for word families; per-learner graphs (multigraph) for memory.
FalkorDB-fit: strong. EtymDB 2.0 ~1.8M lexemes / 700k+ relations, typed edges given by structured templates (no ML). Lasting graph queried many ways (cognate lookup, root yield, false-friend check, explanation, learner memory), so it passes the table + library test.
SQL-awkward query: "every Bengali word whose ancestor chain meets the ancestor chain of a word this learner already knows, through typed edges of any depth, with the same meaning".
Data (V unless marked): EtymDB 2.0 CC BY-SA 4.0; Wiktionary category counts: Bengali terms derived from Sanskrit 3,807 (1,757 borrowed, 1,045 inherited, 377 Sanskritic formations, 90 by-root subcategories); Hindi from Classical Persian 2,673. Wiktextract/kaikki.org JSON of Wiktionary (CC BY-SA, believed, U) for glosses + translation tables. CogNet v2 (8.1M cognates, 338 languages) is CC BY-NC-SA: evaluation only, do not redistribute. Marathi counts not visible (U). Tamil coverage weak (33 terms from Classical Persian).
Objective check: (1) translation-table check: a predicted cognate pair must share a translation/gloss (deterministic verifier over the LLM, M6); precision/recall against held-out Wiktionary cognate/descendant links and CogNet. (2) Headline metric: share of the top-2,000 frequent target words reachable from the learner's language with matching meaning (phrase as "traceable in Wiktionary", not "of the language"). Learning benefit itself is not measured in 4 days.
Baseline: plain translation lists; string similarity (edit distance) cognate guessing; an LLM asked "which words are cognates" (hallucinates; we show where).
Action: today's plan (top roots + words + "via" path), Anki deck export, false-friend warnings, after human approval. Quiz results written back, next session adapts.
Agents sharing state: Planner (chooses next roots), Quizzer (tests, writes KNOWS/STRUGGLED_WITH), Verifier (deterministic meaning check overrides both).
MCP tools: known_bridges(learner, lang), explain_path(word_a, word_b), top_roots(lang, learner), false_friend_check(word, lang), record_result(learner, word, outcome), coverage(learner, lang).
Prior art: Indian-language apps (Indilingo, Bhol, Portal, Language Curry) teach flat lists; cognate detection research for Indian languages (wordnet-based); no cognate-graph planner with memory found (U).
Part H screen: question in one line yes; write-back yes; named algorithm yes; action + path yes. Tracks: 1 (primary) + 2 (per-learner memory).
Biggest risks + first tests: (a) coverage: count Hindi->Bengali and Hindi->Marathi pairs with a shared ancestor AND matching gloss in the kaikki dump; (b) sound change hides cognates (Sanskrit kṣetra -> Hindi khet): show the path so the link makes sense; (c) false-friend detection compares glosses (small model step, not the core).
Scores: C1 4, C2 4, C3 4, C4 4, C5 4, C6 4, C7 5, C8 3, C9 5 = 12+8+8+8+8+8+5+3+5 = 65 (63 if coverage test is weak and C3 drops)
```

#### Candidate 7 v2 stress test (Oct 5 2026): 64/80, strong-ish (C1 is the weak spot) — data test PASSED
Throwaway analysis on kaikki.org Wiktextract dumps (Hindi 35,881 words / 158 MB, Bengali 9,977 / 38 MB, Marathi 5,290 / 34 MB; downloaded in under a minute; Wiktionary CC BY-SA). Ancestors taken from typed etymology templates (inh/bor/lbor/der), meaning match = shared content word in English glosses.
```
Measured (V, our own counts):
- Hindi -> Bengali: 4,562 shared-ancestor pairs, 3,420 with matching meaning; 2,841 of 9,977 Bengali entries (28.5%) reachable (26.6% excluding English loans). Mostly via Sanskrit (2,318), then Classical Persian (520), Arabic (419).
- Hindi -> Marathi: 3,228 pairs, 2,465 with matching meaning; 2,063 of 5,290 Marathi entries (39.0%) reachable; 1,250 identical spellings.
- Basic vocabulary (110 Swadesh-style concepts with entries in both): Bengali 72% linked, Marathi 64% (one/two/five, man, bird, dog, I/you...).
- Ground truth: recall against Wiktionary's own explicit cognate labels (cog|hi in target entries): Bengali 64% (781 pairs), Marathi 62% (611); 57% with the meaning filter. ~60% of misses are Hindi entries with no etymology at all (data gap, not method error). Precision not formally measured; random samples look right.
- False friend CONFIRMED: Marathi शिक्षा = "punishment, chastisement"; Hindi शिक्षा = "education, lesson"; Bengali শিক্ষা = "education". Also found: Marathi मूल = "child" vs Hindi मूल = "root/basic". 851 (Bn) / 639 (Mr) same-Sanskrit-ancestor pairs with no gloss overlap: mix of real drift (कक्ष chamber vs Marathi कास udder; माथा forehead vs মাথা head) and gloss noise (inflection entries). False-friend detection needs a better meaning comparison than word overlap (review queue, not auto).
- Chain depth: most entries list ONE ancestor (Bengali 4,605 of 6,335; Hindi 10,910 of 14,508). Chains of 3+ steps: Bengali 8%, Hindi 6%, Marathi 17%. Sanskrit root templates: Hindi 1,910, Marathi 827, Bengali 536 entries.

Other verified facts:
- FalkorDB algo.SPpaths takes relDirection 'outgoing' | 'incoming' | 'both', plus relTypes, maxLen, pathCount, so word -> ancestor <- word paths work.
- Prior art: Etytree (Wikimedia tool, interactive etymology trees from Wiktionary), Etymap (MIT), wgraph, etymology-db: visualisers, no learner, no plan, no memory. DIY-MKG (arXiv 2507.01872): open-source personal vocabulary knowledge graph with LLM-suggested related words and LLM quizzes (no etymology, links guessed by LLM) — closest prior art; our difference is links given by data + verified meaning match + false friends. Spanish "words you already know" cognate lists are everywhere; nothing found for Indian languages (U).
- Pedagogy: cognate facilitation is established (cognates recognised more: median 0.71 vs 0.53 in one young-learner study); one-session awareness training did not raise learning rates (Otwinowska 2020). Claim "helps notice", not "proven to speed learning".

Make-or-break answers:
1 Real problem: yes (three-language rule, inter-state migrants, global cognate learning). Sensitive: language politics in India (e.g. 2025 Maharashtra third-language row, U); frame as any -> any (Bengali -> Marathi, Marathi -> Hindi), never "Hindi is the base".
2 Graph heavy? PARTLY. ~80% of matches are a 2-hop shared-ancestor join a SQL self-join could do. Graph value has to come from: ordered chains (6-17% deep), root families + PageRank/degree ("learn these roots"), 3-language bridges (Persian/Arabic/English/Sanskrit), learner memory overlay, what-if ("if I learn these 10 roots, what becomes reachable"). A judge can still say "self-join"; answer it in the demo.
3 Links given? Yes, typed templates. No ML for the core.
4 Proof: recall vs explicit cognate labels (62-64%), coverage numbers, basic-vocab %, precision via a hand-checked sample of 100 pairs (to do).
5 Prior art: visualisers + DIY-MKG; we add learner plan + memory + verified meanings + false friends for Indian languages.
6 Hardest step: false-friend meaning comparison (noise). Fallback: show only same-ancestor pairs with zero overlap as "check this", hand-curate 20 for the demo.
7 Embarrassment: a native speaker spots a wrong pair or a stiff Sanskrit tatsama nobody says. Mitigation: prefer inherited/common words, show frequency, let the user mark "wrong" (written back).
8 Ethics: language politics; Wiktionary attribution (CC BY-SA).

Scores: C1 3, C2 4, C3 4, C4 4, C5 5, C6 4, C7 5, C8 3, C9 5 = 9+8+8+8+10+8+5+3+5 = 64
To lift C1 to 4 (-> 67): store chains as ordered edges, Root nodes with PageRank, multi-language bridges, learner what-if coverage tool; show one query a self-join can't do cleanly (variable-depth typed path between two learner languages through any ancestor, returned as the explanation).
```

#### Candidate 7 v2 redesign around FalkorDB (Oct 5 2026): ~67/80 on paper
Full design in `cognate-graph-design.md` (sketch only; queries to be rewritten and tested during the event).
```
Reframed question: "I know these languages, I want to read Marathi: which words do I almost know and why, which are traps, and what is the cheapest order to learn the rest so each new word is explained by something I already know?"
Graph work per part: multi-source var-length up/down paths (Cypher, SPpaths relDirection 'both'), no-path rote words (WCC), curriculum = minimum spanning forest rooted at a virtual Known node (MSF, undirected per docs) + BFS lesson order, keystone roots (reachability gain + betweenness), lessons by word family (CDLP), what-if on GRAPH.COPY scratch graphs, traps via path + flex.text.jaroWinkler + flex.sim.jaccard, per-learner graphs + shared commons graph, read tools via GRAPH.RO_QUERY.
Verified FalkorDB docs (Oct 5): algo.MSF {nodeLabels, relationshipTypes, objective, weightAttribute} YIELD edges, nodes, treats edges as undirected; algo.labelPropagation {nodeLabels, relationshipTypes, maxIterations}; algo.WCC undirected; algo.betweenness {samplingSize, samplingSeed}; algo.HarmonicCentrality YIELD reachable (HLL); algo.pageRank(label, relType) unweighted, one label/type; algo.bfs(start, maxDepth, relType); SSpaths/SPpaths relDirection both; GRAPH.COPY src dest; vector index (HNSW, cosine/euclidean, db.idx.vector.queryNodes); full-text index (stemming, stopwords); FLEX UDFs flex.sim.jaccard, flex.text.levenshtein / jaroWinkler (named in docs FAQ, confirm).
Primary demo pair switched to Hindi -> Marathi (39% reachable, 17% deep chains, शिक्षा trap).
Re-score: C1 3 -> 4 (questions are now frontier / spanning-tree / component / community problems over a living per-learner graph). Total 67. Still at risk if judges see only the 2-hop lookup: lead the demo with the curriculum tree + what-if, not the lookup.
```

#### Candidate 20 full stress test with data (Oct 5 2026): ~51/80 (Wikipedia framing) — make-or-break test FAILED
```
Data test (our own throwaway analysis, V):
- 35 news-heavy English Wikipedia articles (Indian + global events/companies, via the MediaWiki API): 1,259 claims with 2+ citations, 309 with 3+.
- Citation metadata: only 54 of 2,935 citations (1.8%) fill the `agency` field (PTI 29, AFP 8, ANI 6, AP 6, Reuters 4). Same agency twice in one claim: 3 claims (0.2%). Near-identical titles across different outlets: 2.6%, but many are editor placeholder titles ("Pork challenge-02"), so noisy.
- Article text: sampled 70 claims with 3+ cited URLs -> 232 URLs, 152 fetched with text (66%; the rest paywalled, blocked or dead). 49 claims had 2+ fetched sources from different outlets. Max shared 8-word text between co-cited outlets (per-site boilerplate removed): >=5% in 5/49 (10%, mostly shared quotes), >=15% in 2/49 (4%), >=50% (near copy) in 1/49 (2%: Ratan Tata/Dogspot, The Hindu vs Business Today).
- Real one-origin cases seen: one press release covered by 3 outlets (Byju's buys TutorVista), the same repolling wire story under different headlines. They exist but are rare in what editors choose to cite.
=> "12 sources = 1" happens in about 2-4% of multi-cited claims in this sample. Below our 10% threshold. Sample is small (35 articles), so +/- a few points, but not 10x off.

Users (honest):
- Wikipedia editors (GA/FA reviewers, new-page patrollers, WikiProject Reliability): real but small group; WP:CIRCULAR already bans citing Wikipedia/mirrors; tools already exist for source reliability (Cite Unseen labels source types/reliability; Citation Watchlist flags unreliable URLs in edits). With a 2-4% base rate the tool is rarely useful to them.
- Fact-checkers (IFCN orgs) and journalists ("two-source rule" needs independent sources): real need, but they work on breaking news, not Wikipedia citations; would need a live news corpus.
- Everyday readers/students: "is this well-sourced?" is weak pull.
- OSINT/intelligence analysts: circular reporting is a classic failure, but their data is private.

Pivot with better evidence (not tested): **AI-answer independence check.** "This AI answer cites 6 sources; how many are independent?"
- Evidence (V): CJR Tow Center study: AI search engines often cite syndicated copies (Yahoo/AOL) instead of originals (Perplexity Pro cited syndicated Texas Tribune copies in 3 of 10 queries); arXiv 2410.22349 found answer engines citing multiple sources with identical or near-identical content as if distinct.
- Deterministic origin signals: canonical-URL tags on syndicated pages, wire bylines, text reuse.
- Problems: we must generate AI answers ourselves (our own API key; check engine terms); base rate for AI answers unknown; each answer is a tiny graph (5-10 sources), so FalkorDB is justified only by a lasting copy graph across many queries (memory). Rough score ~56.

Scores (Wikipedia framing): C1 3, C2 2, C3 3, C4 4, C5 3, C6 3, C7 5, C8 3, C9 4 = 9+4+6+8+6+6+5+3+4 = 51 (was 59)
Verdict: park. The insight is still the cleverest we have, but the problem is rare where the data is. Revisit only if a cheap test on ~30 AI answers shows a high duplicate rate.
```
