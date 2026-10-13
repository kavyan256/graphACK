# Stages 1-3: how we ran them and what we found (Oct 5 2026)

Graph Hacks (FalkorDB x WeMakeDevs), Track 1: Agents That Act on Connected Data. Event Oct 15-18 2026. Decision deadline Oct 11.

This report covers the first three research stages of `idea-discovery-plan.md`. Stage 0 (`win-spec.md`) set the target beforehand: the likely judging criteria (six equal WeMakeDevs-style criteria), the J1-J6 rubric, and seven kill rules fixed before any idea existed.

**Constraint for all stages: internet only.** No interviews, no asking organisers or users, no posting. Every claim comes from public pages, datasets, APIs, forums, issue trackers or papers. Verified facts are marked **V**, things believed but not re-checked **B**, unknowns **U**.

**Why this process:** in the earlier (scrapped) round we picked clever topics first and checked them later. Each died on a check we could have run on day 1: how often the problem really occurs (citogenesis: 2-4%), whether the links exist in the data (fix-path: 42%), graph depth (cognate planner: mostly two hops), prior art, and assumed pain. This round works backwards: find where **what FalkorDB is good at**, **data with given links**, and **evidence of real pain** overlap, then generate ideas only there.

---

## Stage 1: three inventories

Goal: build the raw material ideas would be made from, before naming any idea.

### 1A. Question shapes FalkorDB is good at
File: `inventory-shapes.md`

**How we ran it**
- Read FalkorDB's own documentation pages (Oct 5): every algorithm page (BFS, SPpaths, SSpaths, A*, MSF, PageRank, betweenness, harmonic centrality, WCC, label propagation, max flow), Cypher functions, known limitations, Cypher support, `GRAPH.COPY`, vector index, full-text index, the MCP server and the agentic-memory section.
- For each capability, wrote the kind of question it answers, when the graph does real work, and the naive baseline it has to beat.

**Results**
- **13 question shapes**: ripple/reachability (S1), "no path" as proof (S2), best explanation path (S3), bottleneck/cut (S4), independent routes / hidden shared node (S5), hidden groups (S6), what matters most (S7), cheapest way to connect everything (S8), geographic route (S9), what-if on a graph copy (S10), per-user/per-case memory (S11), patterns/motifs (S12), meaning + structure (S13).
- **Strong combinations** (most likely to make a judge say "a table can't do that"): ripple + "no path" proof + what-if; hidden shared node + centrality; explanation path + memory; cut + what-if.
- **Anti-shapes** (judges call these "a table would do"): lookups, one-hop joins, a two-hop shared neighbour as the only query, top-k counts, graph as storage behind RAG, a visualisation on top of ordinary storage, one fixed computation that networkx would do.
- **Technical gotchas** found in the docs:
  - `algo.pageRank` is unweighted and takes one label + one relationship type.
  - `algo.maxFlow` accepts several sources and sinks but returns no min cut (derive it).
  - WCC and MSF ignore edge direction; SPpaths, SSpaths and A* take `relDirection`.
  - `shortestPath()` needs both endpoints bound first and allows no property filters inside the pattern.
  - Unreferenced relationships in a MATCH are counted once; LIMIT doesn't stop eager writes; no label expressions; no aggregation inside pattern comprehensions; no temporal arithmetic.
  - Useful extras: `vec.cosineDistance`, `point()`/`distance()`, MCP server read-only mode (`FALKORDB_DEFAULT_READONLY=true`), `GRAPH.COPY` for what-if graphs.
  - Memory frameworks (Graphiti, Mem0, Cognee) need an LLM to extract entities: fine for conversation memory, never as the core graph.

### 1B. Open datasets where the links are given
File: `inventory-data.md`

**How we ran it**
- Listed ~50 candidate datasets across domains, then verified licence, size, access method and built-in ground truth with web searches (about 30 checks).
- Kept only datasets whose core links are in the data (no LLM extraction), whose licence allows a public repo, and which load in about a day.

**Results: ~35 datasets in 8 groups**

| Group | Verified highlights |
|---|---|
| Ownership & money | **GLEIF Level 2**: CC0, 672,239 ownership relationship records (Oct 3 2026), reports both direct and ultimate parent (exact ground truth), no personal data. **GEM ownership tracker**: CC BY 4.0, 27,000+ entities, 25,000+ ownership links with %. Companies House PSC: OGL, daily JSON (contains individuals). OpenSanctions: CC BY-NC 4.0, bulk download without login |
| Software & security | deps.dev: CC BY 4.0, free API. OSV.dev: CC BY 4.0 for major sources. CISA KEV: CC0, 1,723 entries (Sep 24 2026). Mathlib4 dependency graph: CC BY 4.0, 137,046 nodes, 304,433 edges. LeanDojo: CC BY 2.0 |
| Knowledge & research | OpenAlex: CC0, ~330 GB, S3 without login. Retraction Watch via Crossref: 60,000+ records, open (exact licence U). Wikipedia clickstream: CC0. CourtListener: public domain, citation map with depth. legislation.gov.uk effects: OGL v3 (somewhat out of date). Stack Exchange: CC BY-SA; official dumps need login since 2024, community copies on archive.org to 2025-12-31. Open Library: CC0 |
| Health | **PrimeKG**: CC0, 129,375 nodes, 4,050,249 edges, 30 edge types. Hetionet: CC0 original content, 47,031 nodes, 2,250,197 edges (prior art: "DrugPath" agent at a Neo4j hackathon). ClinicalTrials.gov: free. Synthea synthetic patients: Apache 2.0 |
| Transport | Mobility Database: 6,000+ GTFS feeds in 99+ countries. Delhi Open Transit Data: free static GTFS, but stop times are rough estimates. Indian Railways: MIT dataset with 8,990+ stations and 5,208+ trains (prior art: `railways-mcp`) |
| Culture & games | MusicBrainz: CC0 core data incl. "samples material" relationships. Lichess CC0, Cricsheet ODC-BY, StatsBomb (free with agreement) |
| Synthetic generators | Synthea, LDBC FinBench, LDBC SNB (Apache 2.0): exact ground truth by construction |
| Own data | Allowed by the rules; needs a synthetic stand-in for a public demo |

**Best raw material (data only):** 1 GLEIF, 2 PrimeKG, 3 OpenAlex + Retraction Watch, 4 MusicBrainz, 5 CourtListener / legislation.gov.uk, 6 GTFS / OSM, 7 Stack Exchange, 8 Synthea / LDBC.

### 1C. Public evidence of connection-shaped pain
File: `inventory-pain.md`. Raw outputs: `research-data/stage1c-pain/` (`se_grid.json`, `se_examples.json`, `hn.json`, `pp.json`).

**How we ran it**
1. **Stack Exchange API** (no key): exact-phrase searches (quoted phrases behave as exact matches: "what depends on" = 61 hits vs 226,671 unquoted) for 10 connection-shaped phrases across 6 developer sites, plus domain phrases on 10 other sites (Travel, Genealogy, Medical Sciences, Money, Law, Academia, Music, GIS). Then the top 5 questions by votes for 15 combinations, with **view counts** as the best proxy for how many people hit a problem. About 100 API calls.
2. **Hacker News** (Algolia API): 18 phrases, counted in stories and comments.
3. **Reddit**: direct access returns HTTP 403, so used the PullPush archive. Subreddit filters were unreliable, so Reddit was used for **examples only**, not counts.
4. **Incidents and statistics**: web searches for verified numbers on large failures caused by missed connections.

**Results**

Stack Exchange exact-phrase counts (selected):

| Phrase | Stack Overflow | Server Fault | Ask Ubuntu |
|---|---|---|---|
| "root cause" | 15,821 | 624 | 403 |
| "circular dependency" | 4,020 | 18 | 16 |
| "single point of failure" | 546 | 234 | 4 |
| "safe to remove" | 487 | 65 | 178 |
| "reverse dependencies" | 52 | 3 | 11 |

Other sites: Travel "connecting flight" 828; GIS "shortest path" 564; Academia "retracted" 99; Genealogy "common ancestor" 38.

Most-viewed real questions:
- "How to list dependent packages (reverse dependencies)?" (Ask Ubuntu): **403,247 views**
- "Resolve build errors due to circular dependency amongst classes" (Stack Overflow): **337,349**
- "Do I need a US visa to transit (or layover) through an American airport?" (Travel): **329,375**
- "Rediscovery of calculus in 1994: what should have happened to that paper?" (Academia, retraction): 147,219

Hacker News (comments): "root cause" 19,908; "who owns" 11,444 (ambiguous); "single point of failure" 5,678; "blast radius" 2,743; "dependency hell" 2,065; "supply chain attack" 1,283 (432 stories); "agent memory" 203 (277 stories).

Reddit examples: Indians stuck without transit visas ("Booked India-Canada-Austin flight without knowing i need a transit visa. Stuck"), "wrongfully denied boarding", polypharmacy worries, missed Indian Railways connections.

Verified incidents and statistics:
- **AWS us-east-1 outage (Oct 19-20 2025)**: 15 hours, 17M+ outage reports, 1,000+ companies, 142+ AWS services.
- **Log4Shell**: 35,863 Maven packages (~8% of Maven Central); only ~7,000 direct; over 80% more than one level deep, most five levels, up to nine.
- **Medication harm (WHO)**: ~1 in 20 patients; medication errors ~$42B/year. Polypharmacy in 45.2% of older adults (European study); adverse reactions cause 5-8% of unplanned UK admissions.
- **Transit visas for Indians**: Spain, France and Germany dropped airport transit visas on Mar 4, Apr 10 and Jun 3 2026.

**12 pain areas ranked** (frequency + severity + gap in existing tools + data availability, out of 20): medicine clashes 15; transit/connection traps 14; "what depends on / safe to remove" 14 (but gap 1: built-ins answer it); transitive vulnerabilities 14 (crowded); root cause 13; hidden single points of failure 12; ownership 12-14; agent memory 12 (crowded); retracted research 12; Indian rail connections 12; circular dependencies 11; "how are these related" 8.

**What Stage 1 told us**
1. The biggest, best-documented pain is software/infrastructure "what depends on / what breaks / root cause", but it is also the most crowded and best served by built-in tools.
2. Two everyday pains have strong evidence and weaker incumbents: transit/connection traps and medicine clashes.
3. GLEIF has the cleanest data in the inventory, but its strongest pain is professional.
4. Agent memory is FalkorDB's own theme but peers cluster there: use it as a feature, not the idea.
5. Phrase counts measure how often people *write* something; view counts are the better proxy for how many people hit a problem.

---

## Stage 2: generate candidates
File: `candidates.md`

**How we ran it**
- Crossed the 12 pain areas x 13 shapes x the datasets; kept every cell where all three fit.
- Ran the past-winner "moves" over the strongest pains: M1 hidden reasoning unit as a node, M2 evidence on the edge, M3 precedents, M4 "no path" proof, M5 "via" explanation, M6 deterministic check over the LLM, M7 native algorithm as a tool.
- One line each: *A [user] needs to [task]. Today [pain]. Graph: [shape] over [data].* No scoring and no favourites; weak-looking ideas kept on purpose so Stage 3 records why they die. Notes recorded known prior art, resemblance to scrapped ideas, and data gaps.

**Results: 39 candidates in 8 areas**

| Area | Candidates |
|---|---|
| Travel & transport | C01 transit-visa route guard, C02 visa unlock planner, C03 robust rail connections, C04 missed-flight fallback, C05 step-free reachability, C06 transit equity gaps |
| Medicines & health | C07 mechanism-path medicine explainer, C08 side-effect detective, C09 deprescribing focus |
| Hidden shared failure points | C10 what goes down together, C11 single-maintainer risk, C12 one owner behind "independent" assets |
| Software dependencies | C13 removal impact simulator, C14 upgrade-order planner, C15 CI supply-chain ripple, C16 cycle-breaking plan, C17 vulnerability reachability |
| Ownership & money | C18 ultimate-parent exposure, C19 sanctions 50% rule, C20 who owns this brand, C21 climate liability tracer, C22 circular ownership loops, C23 fund look-through |
| Research, law, knowledge | C24 conflict-free reviewer finder, C25 retraction exposure, C26 Wikipedia citations to retractions, C27 independent confirmation, C28 precedent status, C29 UK law change ripple, C30 hallucinated legal citations |
| Learning | C31 maths prerequisite planner, C32 proof refactor impact, C33 real-reader explanation paths, C34 duplicate-question navigator |
| Culture, games, organiser examples | C35 sample clearance map, C36 collaborator-path discovery, C37 modpack conflict detective, C38 frozen-account explainer, C39 scam-shop network check |

Every shape was used at least once; S1 (ripple), S2 ("no path") and S10 (what-if) appeared most often.

---

## Stage 3: cheap screen
File: `screen.md`

**How we ran it**
Each candidate went through five checks in order, stopping at the first kill:
1. **Brief fit** (Part H quick screen): is the answer a path or set? What is written back? Which named algorithm or bounded traversal? What action, with what path shown?
2. **SQL-join test**: could a plain join or lookup answer the core?
3. **Built-in test**: does a free existing tool already give the core answer?
4. **Prior art**: quick web searches (about 15 searches for the candidates that passed checks 1-3).
5. **Data check**: dataset named, licence OK, reachable (about 8 searches/API checks).

During screening, the survivors' strongest shapes (hidden shared dependency, cuts, what-if) inspired **3 extra variants** (C40-C42), screened the same way.

**Results: 42 screened -> 8 survivors**

Where candidates died:

| Check | Killed | Examples |
|---|---|---|
| 1. Brief fit | 1 | C16 cycle breaking (not a native algorithm) |
| 2. SQL-join test | 8 (+ C02 merged into C01) | Medicine explainer (interactions are direct edges; mechanism = 2-hop join), GLEIF parent exposure (ultimate parent is given, so it's a group-by), fund look-through (3-way join) |
| 3. Built-in test | 10 | Single-maintainer risk (deps.dev + OpenSSF Scorecard), UK law ripple (legislation.gov.uk shows effects), modpack conflicts (Modrinth app warns), transit equity (Conveyal) |
| 4. Prior art | 7 | Rail connections (**RailTC already computes miss probability from real delays**), sample clearance (SampleSync), frozen-account explainer (fraud is an organiser example; banks may not tell customers about suspicious-activity reports) |
| 5. Data | 4 | Sanctions 50% rule (**OpenSanctions has 199,383 ownership links but says reliable percentages are rare**), drug single-source risk (supplier links are confidential; USP already maps it), missed-flight fallback (proprietary schedules) |
| Prior art + base rate | 1 | Circular ownership (only 328-487 UK companies, 0.01%; Global Witness already analysed) |
| Two warnings (no pain evidence + prior art) | 2 | Real-reader explanation paths, collaborator-path discovery |

**The 8 survivors**

| ID | Candidate | Why it survived | Main risk |
|---|---|---|---|
| **C10** | **What goes down together**: which services you rely on share a hidden provider (cloud region, DNS, CDN, login); what-if "us-east-1 down" | No consumer/dev tool found; research: 89% of top-100K sites depend critically on third-party DNS/CDN/CA providers, and **indirect dependencies amplify impact up to 25x** | We must collect the dependency data ourselves (public DNS lookups) |
| **C40** | **Licence minimum-replacement set**: fewest direct dependencies to swap so no copyleft code is reachable | Scanners only list copyleft; Black Duck 2025: 30% of licence conflicts come from hidden transitive dependencies; no "cheapest fix" tool found | The cheapest fix may usually equal the obvious one |
| C01 | Transit-visa route guard ("no legal route" proof, what-if visa, rule-change memory) | Largest everyday pain evidence | Visa checkers + Layovered app exist; current route file has no licence (fallback: OpenFlights 2014 or synthetic network) |
| C39 | Scam-shop network check | Shared infrastructure is real (one network: 20,000 domains on 36 IPs); labelled set of 579 fake + 561 legit shops exists | Guardio/ScamAdviser exist; fake domains die quickly |
| C21 | Climate liability tracer (% ownership multiplied along chains) | Weighted multi-path aggregation is graph-native; GEM data CC BY 4.0 | Weak pain evidence; GEM may already publish aggregates |
| C24 | Conflict-free reviewer finder | Excellent OpenAlex data; "no path within 2 hops" as proof | Heavy prior art (Semantic Scholar, OpenReview) |
| C41 | Submarine cable what-if (Red Sea cuts, Sept 2025) | Cuts and single points of failure are native shapes | Data CC BY-NC-SA 3.0, no capacities, small graph |
| C31 | Maths prerequisite planner (Lean mathlib) | Exact dependency data | Niche audience |

**Kill numbers for Stage 4 (fixed before measuring)**

| ID | Kill if |
|---|---|
| C10 | Fewer than 20% of popular services reach an outage through a provider of a provider, or a backtest against the AWS Oct 2025 outage finds fewer than half the services that went down |
| C40 | Fewer than 10% of popular packages have copyleft 2+ hops deep, or the cheapest fix equals the obvious one in more than 70% of those, or licence data covers less than 80% |
| C01 | Trap rate below 20% on popular Indian outbound routes, transit rules not parseable without an LLM for 80% of hubs, or no route network with an acceptable licence |
| C39 | Fewer than 50% of known fake shops linked to another fake, more than 10% of legit shops falsely linked, or most fake domains already dead |
| C21 | Weighted aggregation changes an owner's ranking for fewer than 30% of assets, or GEM already publishes the aggregates |
| C24 | Conflict rate under 5% (trivial) or author disambiguation too noisy |
| C41 | Fewer than 15 countries with a hidden single point of failure that counting cables per country misses |
| C31 | Prerequisite closures are tiny, or no evidence of a learner audience |

---

## What Stages 1-3 taught us

1. **Most kills came from "a join does it" (8) and "a tool already does it" (10).** Survivors cluster where the answer needs several hops through *hidden* links (C10, C40) or a cut/what-if over a network.
2. **The cleanest ground truth can make the graph unnecessary.** GLEIF gives the ultimate parent directly, which is great for checking answers but turns the core into a group-by.
3. **Many everyday pains already have a niche app** (RailTC, Layovered, Modrinth warnings, SampleSync). Prior-art checks belong early, which is why Stage 3 runs them before any deep work.
4. **Data gaps are often about values, not links.** OpenSanctions has the ownership links but not the percentages; route data exists but without a licence.
5. **These stages used reasoning and quick checks, not measurement.** Stage 4 measures the kill numbers on real data before anything is trusted.

## Caveats
- Phrase counts are relative signals, not a census; Reddit was used for examples only.
- Prior-art checks were quick searches; a tool we didn't find may exist.
- Items marked U in the inventories still need checking before use.

## File map
| File | Contents |
|---|---|
| `idea-discovery-plan.md` | The staged plan (Stages 0-8) with progress notes |
| `win-spec.md` | Stage 0: judging proxy, J1-J6 rubric, gates, kill rules, must-haves |
| `inventory-shapes.md` | Stage 1A |
| `inventory-data.md` | Stage 1B |
| `inventory-pain.md` | Stage 1C |
| `research-data/stage1c-pain/` | Raw Stage 1C API outputs |
| `candidates.md` | Stage 2 |
| `screen.md` | Stage 3, with all sources |
| `stages-1-3-report.md` | This report |
| `idea-rating-criteria.md`, `cognate-graph-design.md`, `falkordb-usage-landscape.md` | Earlier round (archived ideas, lessons, landscape) |
