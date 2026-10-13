# Stage 3: cheap screen (Oct 5 2026)

Each candidate from `candidates.md` (plus 3 variants added during screening) went through, in order, stopping at the first kill:
1. **Brief fit** (Part H quick screen: one-line question answered by a path/set; something written back; a named algorithm or bounded traversal; an action with the path shown)
2. **SQL-join test** (could a plain join / lookup answer the core?)
3. **Built-in test** (does a free tool already give the core answer?)
4. **Prior art** (quick web check)
5. **Data check** (named dataset, licence OK, reachable)

Sources for every web check are listed at the end.

---

## Results

| ID | Candidate | Result | Stopped at | Reason (one line) |
|---|---|---|---|---|
| C01 | Transit-visa route guard | **PASS (risky)** | — | Per-itinerary visa checkers exist (MyTravelReady, Voyasee, Terrana) and **Layovered** routes via visa-free layover countries; our difference = "no legal route" proof, what-if visa, rule-change memory. **Route data: the weekly route file has no licence; fallback OpenFlights (ODbL, 2014) or synthetic network** |
| C02 | Visa unlock planner | MERGED into C01 | 2 | On its own it's a count of rules per visa (SQL group-by); useful as C01's what-if feature |
| C03 | Robust rail connection planner | KILL | 4 | **RailTC "Will I miss my connecting train?"** already gives miss probability from real delays; `railways-mcp` plans journeys |
| C04 | Missed-flight fallback map | KILL | 5 | Schedules and fares are proprietary |
| C05 | Step-free reachability | KILL | 4 | Scrapped before: StepFree NYC app, BetaNYC mta-mcp |
| C06 | Transit equity gaps | KILL | 3 | Conveyal / OpenTripPlanner already do accessibility + scenario edits; time-dependent routing in Cypher is also hard |
| C07 | Mechanism-path medicine explainer | KILL | 2 | Drug-drug interactions are given as direct edges (lookup); the mechanism is a 2-hop shared-target join; DrugPath prior art; no inhibitor/inducer direction in the data |
| C08 | Side-effect detective | KILL | 2 | Symptom <- drug is a 1-hop lookup; via-target is a 2-hop join |
| C09 | Deprescribing focus | KILL | 2 | A patient's subgraph is a handful of drugs (tiny graph, a table does it) |
| C10 | What goes down together | **PASS** | — | No consumer/dev tool found; research shows the shape is real: 89% of top-100K sites depend critically on third-party DNS/CDN/CA, and **indirect dependencies amplify impact up to 25x** (multi-hop). Enterprise monitors (Catchpoint, ThousandEyes) are paid |
| C11 | Single-maintainer risk | KILL | 3 | deps.dev already returns the resolved graph; OpenSSF Scorecard covers maintenance per package |
| C12 | One owner behind "independent" assets | KILL | 2 | GEM already records ultimate parents, so "shared owner" is a group-by |
| C13 | Removal impact simulator | KILL | 3 | deps.dev shows dependents; constraint evaluation is resolver work (Fix-Path lesson) |
| C14 | Upgrade-order planner | KILL | 3 | Resolvers do it |
| C15 | CI supply-chain ripple | KILL | 4 | Crowded security space, existing scanners; GitHub API needs a token for scale |
| C16 | Cycle-breaking plan | KILL | 1 | Minimum feedback arc set isn't a native algorithm; IDE tools exist |
| C17 | Vulnerability reachability | KILL | 5 | Needs call-graph extraction (research-level) |
| C18 | Ultimate-parent exposure (GLEIF) | KILL | 2 | GLEIF *gives* the ultimate parent directly, so "same parent" is a group-by (the clean ground truth is also what makes the graph unnecessary) |
| C19 | Sanctions 50%-rule checker | KILL | 5 | OpenSanctions: 199,383 ownership links, but **reliable percentages are rare**, so the aggregation can't run on real data |
| C20 | Who owns this brand | KILL | 3 | Wikidata property paths already answer it; boycott apps exist; politically sensitive |
| C21 | Climate liability tracer | **PASS (weak)** | — | GEM: 27,000+ entities, 25,000+ ownership links with %; weighted multi-path aggregation is graph-native. Weak public pain evidence; check whether GEM already publishes aggregates |
| C22 | Circular ownership loops | KILL | 4/5 | Only 328-487 UK companies (0.01%) and Global Witness already analysed them (base rate + prior art) |
| C23 | Fund look-through | KILL | 2 | Holdings -> issuer -> given ultimate parent is a 3-way join; Morningstar X-ray-style tools exist |
| C24 | Conflict-free reviewer finder | **PASS (weak)** | — | Strong prior art (Semantic Scholar peer-review API for partners, OpenReview conflict detection, VisConflicts) but nothing open + explainable for small journals found; OpenAlex data is excellent |
| C25 | Reference-list retraction exposure | KILL | 4 | Scrapped before (noisy indirect effect); Zotero flags direct retractions |
| C26 | Wikipedia citations to retractions | KILL | 3 | Likely already handled by a Wikipedia bot (unverified); 2-hop |
| C27 | Independent confirmation (research) | KILL | 4 | Scrapped before (citogenesis base-rate failure) |
| C28 | Precedent status checker | KILL | 2 | Direct status is a lookup; the indirect part has the same noise problem as the retraction ripple |
| C29 | UK law change ripple | KILL | 3 | legislation.gov.uk already shows effects and point-in-time text |
| C30 | Hallucinated legal citation check | KILL | 2 | Lookup |
| C31 | Formal-maths prerequisite planner | **PASS (weak)** | — | Exact data (137K nodes, 304K edges, CC BY 4.0); niche audience; Lean "blueprint" dependency graphs are partial prior art |
| C32 | Proof refactor impact | KILL | 3 | Lean tooling does it |
| C33 | Explain via real reader paths | KILL | — | Two warnings: no public pain evidence + Wikispeedia research prior art |
| C34 | Duplicate-question navigator | KILL | 3 | Stack Overflow duplicate finder; LLMs |
| C35 | Sample clearance map | KILL | 4 | **SampleSync** claims full ownership data (masters, publishers, contacts); WhoSampled, Tracklib; MusicBrainz rights data is partial |
| C36 | Collaborator-path discovery | KILL | — | Two warnings: weak pain + LOCAL GACHA pattern |
| C37 | Modpack conflict detective | KILL | 3 | Modrinth app already warns on declared incompatibilities; Crash Assistant mod; most crashes aren't declared in the data |
| C38 | Frozen-account explainer | KILL | 4 | Fraud = organiser example; banks are legally barred from telling customers about suspicious-activity reports ("tipping off") |
| C39 | Scam-shop network check | **PASS (risky)** | — | Shared infrastructure is real (one network: 20,000 domains on 36 IPs). Prior art: Guardio, ScamAdviser, Netcraft. Labelled set exists (Mendeley: 579 fake + 561 legit shops); Watchlist Internet lists can't be republished; fake domains die fast |
| C40 *(added)* | **Licence minimum-replacement set.** A developer or startup preparing for due diligence needs the smallest set of direct dependencies to swap so no copyleft code is reachable, with the paths that pull it in. Today scanners list copyleft packages but not the cheapest fix. Graph: transitive closure + minimum vertex cut (max flow with node splitting), what-if swaps. Data: deps.dev licences (CC BY). | **PASS** | — | Scanners (FOSSA, Black Duck, ORT) detect; Black Duck 2025: 30% of licence conflicts come from hidden transitive dependencies; no "minimum replacement set" tool found |
| C41 *(added)* | **Submarine cable what-if.** A journalist or policy student needs to know which countries lose most international capacity if certain cables or landing stations fail (Red Sea, Sept 2025). Graph: cuts, articulation points, what-if. Data: TeleGeography cable/landing GeoJSON. | **PASS (weak)** | — | Data is **CC BY-NC-SA 3.0** (non-commercial, share-alike); no capacity data (paid); ~thousands of nodes (small) |
| C42 *(added)* | **Drug single-source shortage risk.** | KILL | 5 | Which ingredient supplier each drug uses is confidential (links not given); USP Medicine Supply Map already does it |

**Survivors (8):** C10, C40, C01, C39, C21, C24, C41, C31.
Strongest on the screen: **C10** and **C40** (no direct tool found, links given, clear graph shape). C01 and C39 pass with data/prior-art risk. C21, C24, C41, C31 pass weakly.

---

## What each survivor must prove in Stage 4 (kill numbers set now, before measuring)

| ID | The number that would kill it | Kill if |
|---|---|---|
| C10 | (a) Share of popular services whose outage path runs through a **provider of a provider** (depth >= 2), not just their own DNS/CDN. (b) Backtest: share of services reported down in the AWS Oct 2025 outage that the graph links to us-east-1 | (a) < 20% or (b) recall < 50% |
| C40 | (a) Share of popular npm/PyPI packages whose closure contains copyleft at depth >= 2. (b) Among those, share where the minimum replacement set differs from the naive answer (replace each copyleft package). (c) Licence-field coverage in deps.dev | (a) < 10%, or (b) < 30%, or (c) < 80% |
| C01 | (a) Share of popular Indian outbound city pairs where a commonly offered 1-stop route needs a transit visa (the trap rate). (b) Share of hub countries whose transit rules can be parsed from structured tables without an LLM. (c) A route network with an acceptable licence | (a) < 20%, or (b) < 80%, or no acceptable route data |
| C39 | Share of known fake shops linked by shared infrastructure to another known fake, vs. share of legitimate shops falsely linked; share of fake domains still resolvable | Fakes linked < 50%, legit linked > 10%, or most domains dead |
| C21 | Share of assets where %-weighted multi-hop aggregation changes an owner's ranking vs GEM's direct listing; does GEM already publish aggregates? | < 30%, or GEM already publishes it |
| C24 | Conflict rate: share of topic-matched candidate reviewers within 2 co-author hops of the authors; author-disambiguation error rate on a sample | Conflict rate < 5% (trivial) or disambiguation too noisy |
| C41 | Number of countries with a non-trivial single point of failure (articulation point) that naive "count cables per country" misses | < 15 countries |
| C31 | Median ancestor-closure size of well-known theorems (is a planner needed?) and evidence of a real learner audience | Closures tiny, or no audience evidence |

---

## Sources (checked Oct 5 2026)
- Transit visa tools: https://www.mytravelready.ai/transit-visa-checker ; https://voyasee.com/transit-visa-layover-risk-checker/ ; https://apps.apple.com/ca/app/layovered/id6602894094
- Route data: https://github.com/Jonty/airline-route-data (no licence) ; https://openflights.org/data.php (ODbL)
- Third-party dependencies research: https://dl.acm.org/doi/10.1145/3419394.3423664 ; https://www.catchpoint.com/blog/invisible-dependencies-visible-impact-lessons-from-the-google-cloud-outage
- Reviewer conflicts: https://aclrollingreview.org/declaring-a-conflict-of-interest/ ; https://arxiv.org/pdf/2301.10140 ; https://repositum.tuwien.at/bitstream/20.500.12708/221841/1/graphical-abstract-235114.pdf
- Sample clearance: https://www.tracklib.com/blog/music-clearance ; https://en.wikipedia.org/wiki/Tracklib
- Scam shops: https://www.malwarebytes.com/blog/scams/2026/03/inside-a-network-of-20000-fake-shops ; https://data.mendeley.com/datasets/m7xtkx7g5m/1 ; https://www.fakeshop.at/en/about-us/data-sources/
- OFAC 50% rule + OpenSanctions coverage: https://natlawreview.com/article/ofac-50-percent-rule-ownership-aggregation-sdn-risk-and-sanctions-compliance ; https://www.opensanctions.org/faq/35/beneficial-ownership/
- Rail connections: https://app.railtc.in/connection-risk
- Modpacks: https://support.modrinth.com/en/articles/8792916-debugging-minecraft-crashes ; https://modrinth.com/mod/crash-assistant
- Circular ownership: https://www.globalwitness.org/en/campaigns/corruption-and-money-laundering/anonymous-company-owners/companies-we-keep/
- Copyleft in transitive dependencies: https://www.wiz.io/academy/compliance/copyleft
- Submarine cables: https://github.com/lintaojlu/submarine_cable_information (TeleGeography data, CC BY-NC-SA 3.0) ; https://www.medianama.com/2025/09/223-sub-sea-cable-outages-red-sea-connectivity-india/
- Drug supply: https://qualitymatters.usp.org/geographic-concentration-pharmaceutical-manufacturing
- GEM ownership tracker: https://globalenergymonitor.org/projects/global-energy-ownership-tracker
