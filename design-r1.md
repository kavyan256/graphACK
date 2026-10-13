# Stage 6 design: R1 Independent expert finder (+ C24 reviewer use case)

Working name: **TieTrace**. Pre-event **sketch only** (notes, graph model, diagrams). Every Cypher/procedure below is a sketch to be written and tested during the event (Oct 15-18).

**One line:** *Before you quote an expert, see how close they are to the company in your story, with every tie shown as a path through co-authors, employers and funders.*

**Users:** journalists and fact-checkers (lead); journal editors / programme chairs picking reviewers (second front door, same engine).

---

## 1. What the measurements and evidence say (inputs to this design)

| Finding | Source |
|---|---|
| In 4 real company/topic cases, 16% of top experts are directly tied to the company's researchers, but **69% are within two co-author hops** (4.5x) | `round2-loop.md` |
| Tie strength varies widely: 1 to 20+ distinct linking co-authors (median 8), so a **graded score beats yes/no** | `round2-loop.md` |
| Reviewer case: direct co-authorship flags 1% of candidates, two hops 20% | `kill-tests.md` (C24) |
| OpenAlex has **corporate families** (Genentech -> parent Roche) and **funder links** (831 Coca-Cola / Coca-Cola Foundation funded papers, 2015-2026) | checked Oct 5 |
| **Validation case:** the scientists named around the Coca-Cola-funded Global Energy Balance Network (NYT, 2015) appear directly as authors of Coca-Cola-funded papers in OpenAlex: Steven N. Blair (45, plus a split duplicate profile), Timothy S. Church (32), Gregory A. Hand (27), Robin P. Shook (17), James O. Hill (7) | checked Oct 5 |
| Pain: 1,000 UK articles quoted 50 fake experts; 54% / 32% undisclosed academic / financial conflicts among "independent" commenters | `user-evidence.md` |
| Data quality: 38/180 "experts" had over 1,000 works; merged and split author profiles exist; 169/180 had an ORCID | `round2-loop.md` |

---

## 2. Graph model

### Shared research graph (one per topic domain, e.g. `research:nutrition`, `research:vaccines`)
| Node | Key properties |
|---|---|
| `Person` | OpenAlex author id, name, ORCID, works_count, quality flag (ok / possible merged profile / no ORCID) |
| `Work` | DOI, year, title, topics |
| `Institution` | id, name, **type** (company / education / government / nonprofit / funder) |
| `Funder` | id, name (e.g. Coca-Cola Foundation) |
| `Topic` | OpenAlex topic id, name |

| Edge | Meaning (evidence carried on the edge, M2) |
|---|---|
| `AUTHORED` (Person -> Work) | position, year |
| `AFFILIATED_WITH` (Person -> Institution) | year (from the authorship), DOI it came from |
| `FUNDED_BY` (Work -> Funder) | award id if given |
| `PARENT_OF` (Institution -> Institution) | corporate family from OpenAlex `associated_institutions` |
| `ABOUT` (Work -> Topic) | score |
| `CO_AUTHORED` (Person - Person, derived) | number of joint papers, first/last year, `recency_cost` precomputed at load (FalkorDB has no temporal arithmetic) |

### Per-newsroom memory graph (`newsroom:<id>`, multigraph)
`Case` (a story), `Check` (one independence check: expert x company x date, score, paths snapshot), `Decision` (used / declined / quoted with disclosure, by whom, why), linked by person/company ids. Checks are **precedents** (M3): the next reporter who checks the same expert sees the earlier result and what changed since.

### The hidden reasoning unit (M1)
The **tie**: a concrete, dated, evidence-backed path (expert -> co-author -> company scientist; expert -> paper -> funder; expert -> employer -> parent company). Ties are shown as **evidence for a human decision**, never as an accusation.

---

## 3. The questions the agent asks the graph

| # | Question | FalkorDB feature (sketch) | Why a table won't do |
|---|---|---|---|
| Q1 | Who are the most active experts on topic T, excluding the company's own staff? | Full-text index on `Work.title` (`db.idx.fulltext.queryNodes`) or `Topic` nodes -> aggregate authors; optional vector index on titles | Entry point only (search) |
| Q2 | **How tied is expert E to company C, including C's corporate family and funding?** | Company circle = `(c)-[:PARENT_OF*0..3]->(:Institution)<-[:AFFILIATED_WITH]-(p)` plus authors of works `FUNDED_BY` C; paths via `algo.SPpaths` (relDirection 'both', weightProp `recency_cost`, maxLen 4, pathCount 5); **tie strength = number of edge-disjoint paths** via `algo.maxFlow` (sourceNodes [E], targetNodes = circle, capacity 1 per `CO_AUTHORED` edge) | Variable-depth typed paths, corporate family recursion, many-source flow |
| Q3 | **Prove independence**: is there any path within k hops? | `algo.bfs(E, k, ...)` and check the circle is not reached -> "no tie found within k hops in the research record" (M4) | Negative proof over a traversal |
| Q4 | Who are the bridges between E and C? | Intermediaries on Q2's paths; `algo.betweenness` on the E-C subgraph | Ranking depends on graph structure |
| Q5 | Suggest independent alternatives in the same field | `algo.labelPropagation` for research communities; rank candidates by topic relevance x low tie strength | Combines community structure + distance |
| Q6 | (Editors) Pick k reviewers independent of the authors **and of each other** | Greedy: Q3 against authors, then exclude each pick's k-hop neighbourhood | Pairwise k-hop exclusion |
| Q7 | Is this "expert" in the research record at all, and is the profile trustworthy? | ORCID present?, works_count anomaly, split/merged profile hints | Guard against fake experts and bad profiles |

All model-chosen read queries go through `GRAPH.RO_QUERY` (the model suggests, a read-only query decides). Writes (checks, decisions) are fixed, parameterised queries in the memory graph.

## 4. Agents (MCP tools)
| Agent | Does | Tools |
|---|---|---|
| **Scout** | Finds topical experts and alternatives | `find_experts` (Q1), `independent_alternatives` (Q5) |
| **Tie-Checker** (deterministic) | Paths, tie strength, negative proof, bridges | `tie_paths` (Q2), `tie_strength` (Q2), `prove_independence` (Q3), `bridges` (Q4) |
| **Verifier** (deterministic, no LLM) | Every claimed tie must map to stored edges with DOIs; profile-quality guard; overrides the LLM | `verify_tie`, `profile_quality` (Q7) |
| **Writer** | Drafts the sourcing note: who, score, top paths, suggested disclosure line; **human approves** | `draft_note` |
| **Panel** (editor front door) | Builds an independent reviewer panel | `build_panel` (Q6) |
| **Memory** | Saves checks/decisions; flags changes since the last check | `save_check`, `recheck` |

## 5. Memory story (session 2 is better because of session 1)
1. Monday: a reporter checks Dr. B for a vaccine story: "no tie within 3 hops"; decision saved (used as source).
2. Two weeks later, a colleague's follow-up story: the agent recalls the earlier check instantly and runs a **re-check diff**: "since your last check, Dr. B co-authored a paper with a company scientist (2026-10-01): new path, score 0 -> 3." The newsroom decides whether to disclose.

## 5b. Human verifier layer (Atrium-style gates)

Atrium paused low-confidence grades for an educator and required sign-off on lesson plans. TieTrace does the same for ties: **the graph proposes, a human verifies, and the verdict is written back into the graph so it applies everywhere.**

### Measured basis (Oct 5)
In three company/topic cases (135 experts, 100 tied):
- Only **3% of tied experts** are tied *only* through huge (50+ author) papers, so auto-discounting mega-papers is not the main job.
- But **a single evidence paper often carries the ties of many experts**: one 35-author paper carries ties for **18 of 45** mRNA-vaccine experts; a 43-author community paper ("Current status of community resources and priorities for weed genomics research", 2024) carries ties for **16 of 45** glyphosate experts. Whether such a paper should count is a judgement call, and **one human ruling on it changes up to 40% of the scores in a case**.

### When the agent pauses for a human
| Gate | Triggered by | Human chooses |
|---|---|---|
| **Identity check** | Possible split or merged author profile (no ORCID, works-count anomaly, same name + shared co-authors across profiles) | Same person / different people |
| **Tie check** | A tie that would change a verdict: carried by a community/position paper, an old paper (e.g. 10+ years), a foundation grant vs the company itself, a mega-author paper | Counts / doesn't count (with reason) / needs more evidence |
| **Independence sign-off** | Any "no tie within k hops" claim before it is used | Approve, with the caveat "within the research record only" |
| **Publication sign-off** | Any sourcing note or disclosure line before it leaves the tool | Editor approves (two-person rule for "strongly tied" wording) |
| **Right of reply** | The expert (or anyone) disputes a tie ("that's a different person") | Routed to the same queue; accepted corrections become graph facts |

The deterministic **Verifier** still runs first: no tie reaches a human (or a note) unless it maps to stored edges with DOIs.

### What a verdict writes back (memory that makes the next session better)
| Verdict | Graph write | Effect everywhere |
|---|---|---|
| Same person | `SAME_AS` edge between two `Person` profiles | Hidden ties from split profiles appear (e.g. the two Steven N. Blair profiles merge) |
| Different people | `DIFFERENT_FROM` edge | Stops a false tie from a name clash, permanently |
| Paper doesn't count | `Verdict` node -> `ON_PAPER` -> `Work` (reason, reviewer, date, newsroom) | Every tie path through that paper is discounted for that newsroom |
| Tie confirmed | `Verdict` node linked to person, company, paper | Reused instantly as a precedent in later checks |
| Newsroom rule | `Policy` node (e.g. "foundation grants count as company ties") | Applied to all future checks in that newsroom graph (each newsroom keeps its own rules: multigraph) |

### Graph-native parts (why this isn't a to-do list)
1. **Review queue ordered by impact:** papers and profiles are ranked by how many open checks' tie paths run through them (a traversal over current cases), so reviewers see "the 3 decisions that matter most" first.
2. **Verify once, apply everywhere:** after a ruling, the agent re-scores every affected expert and case and reports it: *"Your decision on this paper changed 16 tie scores across 3 open stories."*
3. **Identity resolution as edges:** `SAME_AS` / `DIFFERENT_FROM` are traversed by every later path query.

### New MCP tools / agent
- **Review Desk** agent: `review_queue` (ranked by impact), `record_verdict`, `merge_profiles`, `split_profiles`, `impact_of_verdict` (what changed), `reply_intake` (right of reply).

## 6. Evaluation plan (J3)
1. **Historical validation:** on a nutrition/obesity graph, do the documented Global Energy Balance Network scientists come out tied to Coca-Cola (via funding and co-authorship)? Already confirmed for Blair, Church, Hand, Shook, Hill as direct authors of Coca-Cola-funded papers; report recall and the path for each.
2. **Hold-out test:** hide a sample of real company co-authorship edges, re-run, and measure how often tie scores still flag those experts (graph robustness).
3. **Profile-quality test:** fraction of flagged "experts" with merged/split profiles caught by the guard.
4. **Baseline comparison:** direct-tie-only check (what manual checks and existing tools do) vs graph score: 16% vs 69% tie coverage measured already.

## 7. Demo storyboard (90 seconds)
1. **Problem (10 s):** "News quotes 'independent' experts who often aren't. Press Gazette found 1,000 articles quoting fake experts."
2. **Historical proof (20 s):** obesity story, 2014: the agent scores the experts; the GEBN scientists light up with paths to Coca-Cola funding. "This is what the New York Times uncovered in 2015, from public data."
3. **Live check (25 s):** mRNA vaccine story: the agent lists experts; one has 14 paths to the company's circle (graph lights up, newest path 2024), another has **no tie within 3 hops** (green proof); a third profile is flagged as a likely merged profile.
4. **Action + human verifier (15 s):** the Review Desk asks one question: "Does this 2024 community paper count as a tie?" The reporter says no; the agent replies "this changed 16 tie scores across 3 stories". The Writer drafts the sourcing note; the editor signs off.
5. **Memory (10 s):** two weeks later, the re-check shows a new tie.
6. **Second front door (10 s):** an editor builds a 3-reviewer panel independent of the authors and of each other.

## 8. Red team (arguing against it as a sceptical judge)
| Attack | Best answer | Still open? |
|---|---|---|
| "A SQL self-join does this." | Direct ties are a join, but they catch 16% vs 69%; graded tie strength = edge-disjoint path count via max flow, corporate-family recursion and k-hop negative proofs are graph-native, asked live per story | Show one query a judge can read (Q2) |
| "Prophy / SciLine / Open Payments already do this." | Prophy serves publishers/funders (reviewer conflicts, paid); SciLine is human matching; Open Payments covers money to US doctors only. None shows a journalist *how* an expert is tied | Prior art for the editor use case is real: keep it secondary |
| "Two hops is everyone in a small world." | Yes (69%), which is why the output is a graded score with dated paths and recency, not a binary flag | Need a sensible default threshold; test on the validation case |
| "You could wrongly smear a scientist." | Wording: "ties found in the research record", never "conflicted"; every tie shows its DOI evidence; Verifier blocks unsupported claims; **human verifier layer (5b)**: identity check, tie check, independence and publication sign-off, right of reply; demo uses a documented public case for names | Reduced from biggest risk to managed risk; still needs a README ethics section |
| "Author profiles are messy." | ORCID filter, works-count anomaly flag, show profile quality; measured 169/180 have ORCID | Split profiles (e.g. two Blair profiles) can hide ties: merge by ORCID where possible |
| "OpenAlex API is metered." | Free daily allowance (~1,000 list calls x 200 works); full snapshot is free on S3 (CC0); build 2 topic graphs at event start | Plan the download on day 1 |
| "Is FalkorDB essential?" | Removal test: without the graph, the core questions (paths, flow, k-hop proofs, communities, per-newsroom memory) can't be answered interactively | — |
| "Can one person build it in 4 days?" | Layers: day 1 data + graph, day 2 queries + MCP tools, day 3 agents + memory + UI, day 4 eval + video | Moderate risk (data pipeline) |

## 9. Provisional scores (win-spec J1-J6)
| J1 Impact | J2 Originality | J3 Technical | J4 Use of FalkorDB | J5 Control/explain | J6 Presentation | Total | Build risk |
|---|---|---|---|---|---|---|---|
| 5 | 4-5 | 4 | 5 | 5 | 4 | **27-28/30** | 3 (medium) |

The human verifier layer (5b) keeps J5 at 5 with much stronger evidence, and "verify once, apply everywhere" is a candidate "that's clever" moment (J2 4 -> 5 if it lands in the demo).
Tracks: 1 (primary); 2 also fits (per-newsroom memory, shared state between agents/reporters).

## Sources
- OpenAlex API / snapshot: https://api.openalex.org ; https://help.openalex.org/access/snapshot/
- GEBN: https://en.wikipedia.org/wiki/Global_Energy_Balance_Network ; https://www.npr.org/2015/08/10/431343137/coca-cola-funds-scientists-who-downplay-diets-role-in-obesity
- Fake experts: https://pressgazette.co.uk/news/faces-of-fakery-more-fake-and-ai-generated-experts-con-their-way-into-media/
- Prior art: https://www.prophy.ai/referee-finder/ ; https://www.theopennotebook.com/2021/11/02/dont-get-conflicted-what-to-do-when-your-source-has-a-coi/
