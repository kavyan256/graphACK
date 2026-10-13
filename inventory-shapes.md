# Inventory 1A: question shapes FalkorDB is good at (Stage 1, Oct 5 2026)

Source: FalkorDB docs pages read on Oct 5 2026 (algorithms, Cypher functions, known limitations, Cypher support, MCP server, agentic memory, GRAPH.COPY, vector and full-text indexes). "(V)" = checked in the docs.

How to use this file: every candidate idea in Stage 2 must name **at least one shape from section 1 as its core**, and its core must not be an anti-shape from section 3.

---

## 1. The shapes

| # | Shape | Question template | FalkorDB feature (V) | The graph does real work when... | Naive baseline it must beat |
|---|---|---|---|---|---|
| S1 | **Ripple / reachability** | "What is affected by X, at any depth?" / "What does X depend on?" | Cypher variable-length paths `-[:T*1..k]->`; `algo.bfs(start, maxDepth, relType)` | Depth is unknown or large, edges are typed, and the answer is a *set* with paths | One-level lookup; a tool that already lists the closure (e.g. `apt rdepends`) |
| S2 | **"No path" as proof** | "Can X ever reach Y? Prove it can't." | Same as S1 + `shortestPath(...)` / `algo.SPpaths` returning nothing | Absence of a path is the valuable answer (safe, unsupported, isolated) | Similarity search (can only say "nothing similar found") |
| S3 | **Best explanation path** | "Why is A connected to B? Cheapest / most likely reason first." | `algo.SPpaths` / `algo.SSpaths` {relTypes, weightProp, costProp, maxCost, maxLen, `relDirection: outgoing/incoming/both`, pathCount}; `shortestPath()` / `allShortestPaths()` (endpoints bound first, no property filters inside) | Several competing paths exist and the weights mean something (effort, risk, time, trust) | Listing direct links |
| S4 | **Bottleneck / cut** | "What is the fewest set of things to fix/block/protect?" | `algo.maxFlow` {sourceNodes[], targetNodes[], relationshipTypes, capacityProperty} -> maxFlow, edges, edgeFlows. Many sources and sinks allowed. **No min-cut output: derive it** (saturated edges reachable from source) | The answer is a small cut in a large network; capacities are given | Picking the highest-degree nodes |
| S5 | **Independent routes / redundancy** | "How many truly separate ways are there? Is this a single point of failure?" | Max flow with capacity 1 (node-disjoint needs node splitting); betweenness for chokepoints | "Looks redundant" but actually shares one hidden node | Counting sources or providers |
| S6 | **Hidden groups** | "Which of these are really one cluster / ring / family?" | `algo.WCC` (ignores direction), `algo.labelPropagation` {nodeLabels, relationshipTypes, maxIterations} | Groups are not labelled in the data and emerge only from links | Grouping by a shared column value |
| S7 | **What matters most** | "Which node is most influential / most load-bearing?" | `algo.pageRank(label, relType)` (**unweighted, one label, one type**); `algo.betweenness` {samplingSize, samplingSeed}; `algo.HarmonicCentrality` (yields `reachable`, an HLL estimate) | The ranking differs from a simple count of links (check this!) | Sorting by number of links |
| S8 | **Cheapest way to connect everything** | "Minimum set of links that ties all of these together." | `algo.MSF` {nodeLabels, relationshipTypes, objective, weightAttribute}; **treats edges as undirected** | Many possible links with costs; the tree itself is the plan | Greedy nearest-neighbour by hand |
| S9 | **Geographic route** | "Best route from A to B on a map network." | `algo.AStar` {latitudeProperty, longitudeProperty, heuristicScale, relDirection, pathCount}; `point()`, `distance()` | Real map network with costs; what-if closures | Google Maps (usually wins: needs a twist) |
| S10 | **What-if scenario** | "What changes if this node/edge disappears or is added?" | `GRAPH.COPY src dest` (src stays readable during copy), edit the copy, re-run S1-S8, compare | Many scenarios; each needs the full traversal again | Re-running a script on a file |
| S11 | **Per-user / per-case memory** | "What did we learn about *this* user/case before?" | Multigraph: one graph key per user/case/tenant; MERGE write-back; Graphiti (temporal memory), Mem0 (per-user graphs), Cognee | Memory is linked (not a chat log) and changes the next answer | Storing chat history |
| S12 | **Pattern / motif** | "Find loops, rings, round-trips, triangles, forbidden combinations." | Cypher patterns (cycles via var-length back to start), path variables | The pattern spans several hops and types | Pairwise checks |
| S13 | **Meaning + structure together** | "Find things similar to this, then follow how they connect." | Vector index (HNSW, cosine/euclidean, 1-4096 dims, `db.idx.vector.queryNodes`), `vec.cosineDistance`, full-text index (stemming, stopwords), then traversal | Search finds the entry point; traversal produces the answer | Pure vector search (no explanation, no negative proof) |

### Cross-cutting FalkorDB strengths (show off whichever the idea genuinely needs)
- **Agent loop with many queries per question.** FalkorDB's pitch is fast multi-hop (Securin case: 5-10 queries per interaction, up to 7 hops). An agent that explores step by step (query, look, decide the next query) shows this better than one big query.
- **Read-only model access:** `GRAPH.RO_QUERY`; the FalkorDB MCP server has `FALKORDB_DEFAULT_READONLY=true`, stdio and HTTP transports, lists and explores multiple graphs.
- **FalkorDB 6.0 (Sep 29 2026):** Rust engine, MVCC so reads never block writes. Real reason to mention it only if several agents read and write at once.
- **Temporal types** (Date, DateTime, Duration) are supported, but **temporal arithmetic functions are not**: precompute time differences at load.

---

## 2. Strong combinations (where judges are most likely to say "a table can't do that")

| Combo | Example question shape |
|---|---|
| S1 + S2 + S10 | "If X fails, what breaks? Prove what is safe. Try the fix on a copy first." |
| S5 + S7 | "These look independent, but they share one load-bearing node." |
| S6 + S7 | "Find the hidden clusters, then the key node in each." |
| S3 + S11 | "Explain the answer with a path, and remember what this user already knows / accepted." |
| S4 + S10 | "Smallest set of changes that cuts the risk, simulated before applying." |
| S13 + S1/S3 | "Find the entry point by meaning, then answer by traversal (with a negative proof when nothing connects)." |

---

## 3. Anti-shapes (judges call these "a table would do")

| Anti-shape | Why it fails | Seen in |
|---|---|---|
| Lookup by key | One record answers it | Most chatbot-over-graph demos |
| One-hop join ("items with property P") | SQL join | Can I Park Here? scored 2nd on UX/impact, not graph depth |
| Two-hop shared-neighbour as the *only* query | SQL self-join | Our cognate planner (~80% of its value) |
| Top-k by count | `ORDER BY count` | Any "most popular" ranking |
| Graph as storage behind RAG | Fails the removal test | Generic GraphRAG entries |
| Visualisation on top of ordinary storage | Explicitly banned by the rules | — |
| One fixed computation (one max-flow, one colouring) | networkx on a table does it; no reason for a database | Exam-clash scheduling |

**Test every core claim with the naive baseline:** if PageRank's top 10 equals "most links", or the cut equals "highest-degree nodes", the algorithm is decoration (kill rule 6 in `win-spec.md`).

---

## 4. Technical gotchas to plan around (from the docs and a peer)

| Gotcha | Consequence |
|---|---|
| Direction matters per algorithm: SPpaths/SSpaths/AStar take `relDirection`; WCC and MSF ignore direction; betweenness on one-way edges can return all zeros (ClashBuddy) | Test direction on a 10-node toy graph in hour 1 |
| `algo.pageRank` is unweighted and takes one label + one relationship type | Use betweenness/harmonic or weighted Cypher scoring when weights matter |
| `algo.maxFlow` has no min-cut output | Derive the cut: edges at capacity on the boundary of what's reachable from the source in the residual graph |
| `shortestPath()`: endpoints must be bound first; no property filters inside the pattern | Filter before/after, or use SPpaths with weights |
| Unreferenced relationships in a MATCH count once (relationship uniqueness optimisation) | Reference the edge alias when counting edges |
| LIMIT doesn't stop eager operations (CREATE/MERGE/aggregations) | Batch writes explicitly |
| No label expressions; no aggregation inside pattern comprehensions; no `<>` index use | Write queries the plain way |
| Memory frameworks (Graphiti, Cognee, Mem0) need an LLM to extract entities | Fine for memory of conversations; never let LLM extraction become the core graph (kill rule 2) |
