# Finding the idea: a step-by-step plan (Graph Hacks, Track 1)

Written Oct 5 2026. Event: Oct 15 12:01 AM IST to Oct 18 11:59 PM IST. Decision deadline: **Oct 11**.
All earlier candidates are scrapped (archived in `idea-rating-criteria.md`). Their lessons are kept below.

**Constraint (Oct 5): internet only.** No interviews, no asking people, no posting. Every piece of evidence must come from public sources (pages, datasets, forums, issue trackers, app reviews, papers, videos).

---

## Why the last round didn't work

We guessed a clever topic first, then checked whether it held up. Each idea died on a check we could have run on day 1:

| What went wrong | Example | Fix in this plan |
|---|---|---|
| Topic first, data second | Citogenesis: the problem shows up in only 2-4% of real claims | Data and base rate are checked **before** an idea gets a name (Stage 4) |
| Links had to be guessed or were missing | Fix-Path Finder: only 42% of issues link to a fix commit | Only use data where the **links are given** (Stage 1B) |
| Graph dependence checked last | Cognate planner: ~80% of it was a two-hop self-join | Start from **question shapes the graph is best at** (Stage 1A) |
| Prior art found late | Step-free routing (StepFree NYC app), flood routing (HeiGIT) | 10-minute prior-art check in the cheap screen (Stage 3) |
| Pain assumed, never checked | Most ideas | Evidence mined from public questions, complaints and issue trackers (Stage 1C, 5) |
| Rubric not calibrated to judges | Atrium (the winner) scores 57 on our rubric | Recalibrate the rubric on past winners first (Stage 0) |

**Core principle: work backwards from three things that must all be true at once** (what judges reward, what FalkorDB is uniquely good at, data with given links + a real user), then generate ideas only inside that overlap.

---

## Stage 0: Lock the target (Oct 5-6, half a day)

Goal: know exactly what "a good idea" means before looking for one.

- [x] **0.1 Read what the organisers have published.** Event page, rules page, FAQ, WeMakeDevs past hackathon judging criteria, any kickoff/workshop videos, and public Discord announcements if readable. Looking for: judging criteria, judges, demo vs video weight. No posting.
- [x] **0.2 Collect judge signals.** List the judges (event page, Discord). Skim what FalkorDB is pushing right now (last ~10 blog posts, docs home page, case studies, the MCP server and GraphRAG-SDK pages). A sponsor's judges reward entries that show off what they are marketing.
- [x] **0.3 Recalibrate the rubric.** Score all 13 Memory Meets Motion standouts (Atrium, Hopper, AgentCourt, Drift, Nous, ...) on our rubric. Adjust the weights until **Atrium lands at or near the top**. Likely change: raise C2 (real pain), C7 (hidden reasoning unit) and C9 (demo), and turn C1 into a **gate** (must pass) instead of a x3 weight. Write the new weights into the criteria file.
- [x] **0.4 Write the win spec (one page).** Must-haves, taken from the brief and the Track 1 list:
  - The agent **acts** on connected data, **remembers** (writes back to the graph and reuses it next session), **shows its path**.
  - All five Track 1 focus areas are visible in the demo: multi-hop, graph algorithms as tools, MCP tool selection, actions, explainable results.
  - A FalkorDB strength is on screen: many multi-hop queries per question in an agent loop (the Securin pattern: 5-10 queries, up to 7 hops), in-database algorithms, one graph per user/case, `GRAPH.COPY` what-ifs, read-only queries for the model.
  - A user a judge recognises in 10 seconds, and a "that's clever" moment.
- [x] **0.5 Set the kill rules now, before any idea exists** (so we can't bend them later):
  - Core answer is a lookup, or a SQL self-join does 80% of it -> kill.
  - Links must be extracted by an LLM/ML model for the core -> kill.
  - Measured base rate of the problem is under ~10% where our data is -> kill.
  - An existing free tool already gives the core answer, and we can't name what we add -> kill.
  - Data licence blocks a public repo, or the data is login-protected or someone else's personal data -> kill.
  - No user we can actually reach to ask -> warning.

**Output:** `win-spec.md` + recalibrated weights in the criteria file.

**Done Oct 5:** `win-spec.md` written. No published judging criteria or judges; best proxy is WeMakeDevs' standard six equal criteria (impact, originality, technical, use of sponsor, control/safety, presentation). New rubric J1-J6 (max 30) puts both past winners on top (Atrium 27, Board of SuperVision 26). Target 25+.

---

## Stage 1: Build three inventories (Oct 6-7, about one day, can run in parallel)

Ideas come from where these three lists overlap.

### 1A. FalkorDB question shapes (what the graph is best at)
For each FalkorDB strength, write the **question shape** it answers and one plain-language example. Target 10-12 shapes. Starting list:

| Shape | FalkorDB feature | Example question |
|---|---|---|
| Reachability / "what is affected" | var-length Cypher, `algo.bfs` | What depends on this, at any depth? |
| "No path" as proof | BFS / SPpaths returns nothing | Can this ever reach that? Prove it can't. |
| Best explanation path | `algo.SPpaths` / `SSpaths` with weights, `relDirection` | Why is A connected to B, cheapest reason first? |
| Bottleneck / cut | `algo.maxFlow` (+ derived min cut), betweenness | What is the fewest things to fix or block? |
| Hidden groups | `algo.WCC`, `algo.labelPropagation` | Which of these are really one cluster? |
| Most influential / central | PageRank, harmonic, betweenness | What matters most in this network? |
| Cheapest way to connect everything | `algo.MSF` | Minimum set of links that ties it all together |
| Independent routes | max flow (Menger) | How many truly separate paths exist? |
| What-if scenarios | `GRAPH.COPY` + edit + re-query | What changes if this node disappears? |
| Per-user / per-case memory | multigraph (one graph per key) | What did we learn about *this* user/case before? |
| Pattern / motif | Cypher patterns (cycles, triangles) | Find loops, rings, round trips |
| Meaning + structure together | vector / full-text index + traversal | Find similar things, then follow how they connect |

### 1B. Data inventory (links given by the data, not guessed)
List 25-40 open datasets. For each record: links given? (yes / partly / no), typed edges?, size (nodes/edges), licence, ground truth available?, download time, freshness.
Places to look: Wikidata (CC0, typed links), OpenAlex (CC0), OpenStreetMap (ODbL), GTFS feeds, deps.dev (CC BY 4.0), Debian/CRAN metadata, Wiktionary/kaikki (CC BY-SA), Hetionet, Reactome (CC0), CourtListener, Companies House PSC ownership data (UK, OGL), ICIJ Offshore Leaks (ODbL), OpenSanctions (check licence), Stack Exchange dumps (CC BY-SA), Wikipedia link graph + clickstream, GitHub Archive, Cricsheet, StatsBomb, ClinicalTrials.gov, data.gov.in (OGD licence), Lichess (CC0).
- Rule: only keep datasets where the core links are **in the data** and that load in under a day.
- Note datasets that come with **free ground truth** (labels, known cases, exact simulation) — they are rare and valuable.

### 1C. Pain inventory (real questions, not imagined ones)
Collect **evidence** that people ask connection-shaped questions:
- Mine Stack Exchange / Reddit / forum titles for phrases like "depends on", "what breaks if", "connected to", "chain of", "prerequisite", "who else", "trace back", "root cause", "which ... affected". Count which shapes come up most and in which communities.
- The FalkorDB case studies (security, legal, healthcare, code) and the Track 1 example questions tell us what the sponsor already sees as valuable.
- Public complaint sources instead of conversations: app-store reviews of existing tools, GitHub issues with many thumbs-up, "is there a tool that..." posts, news reports of failures caused by a missed connection. Record links and exact quotes.

**Output:** `inventory-shapes.md`, `inventory-data.md`, `inventory-pain.md`.

**Done Oct 5:** all three written. 13 question shapes + anti-shapes + FalkorDB gotchas; ~35 datasets with verified licences (best raw material: GLEIF L2 CC0 with exact parent truth, PrimeKG CC0, OpenAlex+Retraction Watch, MusicBrainz CC0, CourtListener/legislation.gov.uk, GTFS/OSM); 12 pain areas ranked from Stack Exchange/HN counts, view counts and incidents (top everyday pains: transit-visa/connection traps, medicine clashes; top dev pains are well served by built-ins).

---

## Stage 2: Generate candidates systematically (Oct 7, half a day)

- [ ] Build a grid: **pain (1C) x question shape (1A) x dataset (1B)**. Every cell where all three fit is a candidate.
- [ ] Also run each Part G move (hidden reasoning unit as a node, evidence on the edge, precedent nodes, "no path" proof, "via" explanation, deterministic check over the LLM, native algorithm as a tool) over the strongest pains.
- [ ] Aim for **30-50 one-liners** in the format: "A [user] needs to [task]. Today [pain]. The graph answers it with [shape] over [dataset]."
- [ ] No scoring, no favourites yet. Quantity first.

**Output:** `candidates.md` (one line each).

**Done Oct 5:** 39 candidates in `candidates.md`.

---

## Stage 3: Cheap screen (Oct 7-8, half a day; about 5-10 minutes per idea)

Run each one-liner through, in this order, and stop at the first kill:
1. **Part H quick screen:** one-line question whose answer is a path or set? What gets written back? Which named algorithm or bounded traversal? What action + what path shown?
2. **Self-join test:** could a plain SQL join answer the core? Kill if yes.
3. **Built-in test:** does a free tool already answer it (a resolver, Google Maps, an existing app)? Kill unless we can name what we add.
4. **Prior-art check (10 minutes):** GitHub, Product Hunt, Google Scholar, past FalkorDB hackathon entries, Graph Hacks peers (Discord, GitHub search "falkordb" sorted by newest).
5. **Data check:** dataset named, licence OK, downloadable in under an hour?

Keep the **top ~8**. Record why each killed idea died (one line), so we don't revisit it.

**Output:** `screen.md` (table: idea, pass/kill, reason).

**Done Oct 5:** 42 screened (3 variants added). 8 survivors: C10 what goes down together, C40 licence minimum-replacement set, C01 transit-visa route guard, C39 scam-shop network, C21 climate liability, C24 conflict-free reviewers, C41 submarine cable what-if, C31 maths prerequisite planner. Kill numbers for Stage 4 are fixed in `screen.md`.

---

## Stage 4: Measure the number that would kill it (Oct 8-9, about 1.5 days)

This is the step that taught us the most last time. For each of the top ~8:

- [ ] Write down **the one number that would kill the idea** and the threshold, *before* measuring. Typical numbers:
  - **Base rate:** how often the problem actually occurs in the data (citogenesis failed here: 2-4%).
  - **Link coverage:** what share of the needed links exist in the data (Fix-Path failed: 42%).
  - **Graph depth:** what share of answers really need 3+ hops (cognate: only 6-17%).
  - **Algorithm adds value:** does the algorithm's answer differ from the naive baseline? (e.g. does the PageRank top 10 differ from simply counting links? If not, the algorithm is decoration.)
  - **Ground truth size:** how many labelled cases we can check against.
- [ ] Measure it on real data with a **throwaway script in the scratchpad** (analysis, not project code).
- [ ] Also record graph size (nodes/edges) and confirm it fits in RAM.

Keep the **top 3** that pass.

**Output:** `kill-tests.md` (idea, number, threshold, measured value, pass/fail).

**Done Oct 5:** `kill-tests.md`. 2 pass (C24 conflict-free reviewers: 2-hop proximity 20.3% vs 1% direct; C01 transit-visa trap: 24% of pairs, marginal), 1 blocked (C21, email-gated data), 5 killed (C10 11.8%/25%; C40 0% strong copyleft, cut beats naive 3%; C41 cut = counting; C31 closures tiny; C39 84% of fakes dead, 4% linked). Lesson: the only clear graph win was multi-hop proximity in a dense given network.

**Round 2 (Oct 5, `round2-loop.md`):** focused Stages 2-4 on that pattern. 8 generated, 4 killed at screen, 2 merged, 2 measured: R1 independent expert finder PASS (16% direct ties vs 69% within 2 hops, 4.5x; tie strength median 8 paths, wide spread; ORCID filter needed), R4 paper-mill co-author risk KILL (2-hop: 0 hits). Finalists for Stages 5-6: R1, C24 (same engine), C01 (marginal).

---

## Stage 5: Public evidence of real use (Oct 8-10, in parallel with Stage 4)

For the top 3, internet only:
- [ ] **Past behaviour, not opinions:** find at least 5 public posts/issues where someone actually hit this problem (what they did, how long it took, what it cost). Count recurring threads, upvotes, issue thumbs-up, duplicate questions.
- [ ] **Workarounds people pay for or build:** existing tools, scripts, paid services, browser extensions, spreadsheets people share. Their reviews and complaints show what is missing.
- [ ] **Scale signal:** how many people are in this situation (official statistics, community sizes, download counts).
- [ ] **10-second test without people:** write the one-sentence pitch and check it against the judges' own words (event brief, past winner write-ups). If it needs domain knowledge to understand, simplify or drop.

**Output:** `user-evidence.md` with links and exact quotes.

**Done Oct 5:** `user-evidence.md`. R1 strong (Press Gazette: 1,000 articles quoting 50 fake experts; NZ study: 54%/32% undisclosed conflicts among 'independent' experts; Coca-Cola GEBN; no automated tie-explaining tool). C24 strong pain (21,713 peer-review retractions, 32%) but Prophy Referee Finder does the core job commercially -> use as R1's second front door. C01 strong (32.7M departures, ~17M via foreign hubs; denied-boarding cases show path-dependent rules). Lead into Stage 6: R1 (+C24); alternative C01.

---

## Stage 6: Paper prototype and red team (Oct 10)

For the top 2-3 (sketches only, allowed before the event):
- [ ] Graph model sketch: nodes, typed edges, where the "hidden reasoning unit" lives.
- [ ] The 5 key questions the agent asks the graph, and which FalkorDB feature answers each.
- [ ] Memory: what is written back, and how session 2 is better because of session 1.
- [ ] 90-second demo storyboard: setup, question, graph lights up, action, evidence, memory.
- [ ] **Red team:** spend 20 minutes arguing *against* each one as a sceptical judge would ("a table does this", "X already exists", "nobody needs this", "the graph is decoration"). Write the best answer to each attack, or admit it has none.

**Output:** one `design-<idea>.md` per finalist.

**Done Oct 5:** `design-r1.md` (TieTrace: independent expert finder + reviewer panel front door) and `design-c01.md` (LayoverGuard). New evidence: OpenAlex has corporate families (Genentech -> Roche) and funder links (831 Coca-Cola-funded papers); the GEBN scientists the NYT named (Blair, Church, Hand, Shook, Hill) appear as authors of Coca-Cola-funded papers -> built-in validation case. Provisional scores: R1 27/30 (build risk medium; biggest risk: wrongly implying misconduct), C01 23/30 (build risk low; weak graph role, 2014 routes).

---

## Stage 7: Decide (Oct 11)

- [ ] Score the finalists on the **recalibrated** rubric, plus the win spec checklist.
- [ ] Rule: the winner must pass every gate and every kill rule, have public evidence of real pain (links + quotes), and have a demo moment that makes people say "that's clever".
- [ ] If two are within a few points, pick the one with **better data and an easier build** (the scoring is noisy; build risk is not).
- [ ] Pick **one idea + one backup**. Write the final idea card.

**Output:** decision note in the criteria file.

**Done Oct 5:** `decision.md`. Build **R1 TieTrace** (27-28/30), backup **C01 LayoverGuard** (23/30), declare Tracks 1 + 2. Final idea card, MVP/stretch scope and cut lines in `decision.md`; prep list (Oct 6-14) and day-by-day build plan (Oct 15-18) in `prep-and-build-plan.md`. Constraints found: OpenAlex free $1/day with a free account key (~$0.10 anonymous); FalkorDB Cloud free tier 100 MB RAM, no persistence, stops after 1 idle day.

---

## Stage 8: Prepare without coding (Oct 12-14)

Allowed before the start: notes, sketches, diagrams, reading docs.
- [ ] Final graph model diagram and README outline (data model section, list of queries/algorithms used, AI-use disclosure).
- [ ] List of data download URLs and licences (download during the event).
- [ ] Install Docker + FalkorDB, read the docs for every planned algorithm, plan the 10-node direction test for hour 1.
- [ ] Day-by-day build plan for Oct 15-18 in layers: data + queries -> MCP tools + agents -> memory + checks -> demo video + README (+ optional blog post for the separate Best Blog award).

---

## Calendar at a glance

| Date | Stage | Output |
|---|---|---|
| Oct 5-6 | 0: target, judge signals (read only), rubric recalibration, kill rules | `win-spec.md` |
| Oct 6-7 | 1: three inventories | `inventory-*.md` |
| Oct 7 | 2: generate 30-50 candidates | `candidates.md` |
| Oct 7-8 | 3: cheap screen -> top 8 | `screen.md` |
| Oct 8-9 | 4: kill-number tests -> top 3 | `kill-tests.md` |
| Oct 8-10 | 5: public evidence of real use (parallel) | `user-evidence.md` |
| Oct 10 | 6: paper prototype + red team | `design-*.md` |
| Oct 11 | 7: decide (one + backup) | decision note |
| Oct 12-14 | 8: non-code prep | diagrams, README outline, build plan |
| Oct 15-18 | Build | submission |

---

## Lessons carried over (from the scrapped round)

- Exact ground truth is rare and valuable; prefer ideas that have it.
- A FalkorDB-native algorithm should do real work, and its answer must differ from a naive count.
- Tiny graphs (tens of nodes) fail the "why a graph database?" test; aim for thousands to millions of edges.
- LLM extraction as the core step kept failing; the graph must come from links already in the data.
- Copying a past winner's domain lowers originality; borrow the move, not the problem.
- Peers will all have "LLM picks a tool -> read-only Cypher -> show the query". That is the baseline, not a difference.
- Check edge direction for every algorithm (betweenness returned zeros for a peer until edges went both ways).
- FalkorDB is SSPLv1; say so in the README.
