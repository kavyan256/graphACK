# Stage 4: kill-number tests (Oct 5 2026)

For each of the 8 survivors from Stage 3 (`screen.md`), we measured the number that would kill it, on real public data, with throwaway research scripts. **The thresholds were fixed in `screen.md` before measuring.** Scripts and outputs: `research-data/stage4-kill-tests/`.

## Summary

| ID | Candidate | Kill number(s) | Measured | Verdict |
|---|---|---|---|---|
| C10 | What goes down together | (a) depth >= 2 dependencies >= 20% of top sites; (b) AWS outage backtest recall >= 50% | (a) **11.8%**; (b) **25%** (13/51) | **KILL** |
| C40 | Licence minimum-replacement set | (a) copyleft at depth >= 2 in >= 10% of packages; (b) min cut beats naive in >= 30%; (c) licence coverage >= 80% | (a) strong copyleft **0%** (weak/MPL 6.9%, PyPI only); (b) **3%** (1/35); (c) 99.8% | **KILL** |
| C01 | Transit-visa route guard | (a) trap rate >= 20%; (b) rules obtainable without an LLM; (c) usable route data | (a) **24%** of origin-destination pairs have a trap option (10% of itineraries); (b) yes, hand-curated from official pages; (c) only OpenFlights (2014, ODbL) | **PASS (marginal)** |
| C41 | Submarine cable what-if | >= 15 countries with a hidden single point of failure | 23 vs. counting cables, but the cut equals simply counting landing cities for 154/185 countries; hidden SPOF beyond counting: **1** | **KILL** (algorithm = decoration) |
| C21 | Climate liability tracer | weighted aggregation changes rankings for >= 30% of assets | Not measured: GEM download needs an email form; OpenSanctions mirror has no export | **BLOCKED** |
| C24 | Conflict-free reviewer finder | conflict rate >= 5% | Within 2 co-author hops: **20.3%** (63/311); within 1 hop: 1.0% | **PASS** |
| C31 | Maths prerequisite planner | closures not tiny | Median closure of famous theorems **6**; Euclid's theorem shows 0 prerequisites (data only has traced premises) | **KILL** |
| C39 | Scam-shop network check | >= 50% of fakes linked; <= 10% legit falsely linked; domains alive | Fakes alive **16%** (93/579); fakes linked **4%**; legit linked to legit 24% | **KILL** |

**Result: 2 pass (C24, C01 marginal), 1 blocked (C21), 5 killed.** Both Stage 3 favourites (C10, C40) died on measurement.

---

## Details

### C10: What goes down together — KILL
**Method.** Resolved public DNS (CNAME chains + A records, via DNS-over-HTTPS) for the Tranco top-1,000 sites and for 51 services named as impacted by the AWS us-east-1 outage of Oct 20 2025 (Newsweek's list) plus 50 popular services not named. Hosts checked per service: apex, www, api, app, auth. Mapped every IP to a provider and region using the providers' published IP ranges (AWS `ip-ranges.json` with regions, Google Cloud, Cloudflare, Fastly) and, for the rest, the network owner (Team Cymru IP-to-ASN). "Depth >= 2" = two or more distinct third-party organisations on the path (e.g. site -> Heroku -> AWS).

**Results.**
- Top-1,000: 824 resolved. Visible third-party depth: 0 = 72, 1 = 655, 2 = 85, 3+ = 12. **Depth >= 2: 11.8%.** 53.4% are behind a CDN, which hides where the origin actually runs.
- Backtest: outage victims pointing at AWS us-east-1 in public DNS: **13/51 (25%)**; non-reported services flagged: 1/50 (2%). Any-AWS: 51% of victims vs 26% of non-reported.
- Victims missed include Snapchat, Roblox, Signal, Coinbase, Reddit, Slack, Zoom: they failed through backend APIs that public DNS doesn't show.

**Why it dies.** The dependencies that matter are internal; outside-in data sees a quarter of them. The us-east-1 signal is precise but misses most victims.

### C40: Licence minimum-replacement set — KILL
**Method.** Top 400 PyPI packages (hugovk/top-pypi-packages, Oct 1 2026) and top 400 npm packages (wooorm/npm-high-impact, by downloads). For each default version: resolved dependency graph and every node's licence from the deps.dev API (785 graphs, 1,153 package versions). SPDX expressions classified strong copyleft (GPL/AGPL/SSPL/...), weak (LGPL/MPL/EPL/...), permissive; an "OR" licence counts as permissive if any option is. Minimum vertex cut between the root and all copyleft nodes computed with max flow (node splitting), compared with the naive fix (replace each copyleft package).

**Results.**
- Licence coverage: 99.8% of versions (passes).
- Strong copyleft at any depth: **0 of 785** packages (PyPI and npm).
- Weak copyleft (PyPI only): 9.0% of packages (6.9% at depth >= 2), almost entirely `certifi` (MPL-2.0, file-level copyleft that doesn't affect your own code). npm: 0.
- Minimum cut smaller than the naive fix: **1 of 35** affected packages (3%).

**Why it dies.** In mainstream ecosystems strong copyleft is essentially absent from popular dependency trees, and when copyleft appears it is usually one package on one path, so a cut algorithm adds nothing.

### C01: Transit-visa route guard — PASS (marginal)
**Method.** OpenFlights routes (ODbL; last broad update 2014) and airports. All 1-stop itineraries from 71 Indian airports to Europe, US/Canada, Australia/NZ and Latin America/Caribbean where no direct flight exists (4,839 itineraries, 1,553 origin-destination pairs). Hand-curated Oct 2026 airside-transit rules for Indian ordinary passports, from official/news sources: transit visa needed in the US (always), Canada (unless US-bound with a US visa), UK DATV (unless holding a US/Canada/Australia/NZ visa), Australia, New Zealand, Mexico (exempt with US/Canada/UK/Schengen visas); not needed in Germany, France, Spain (dropped 2026), Netherlands, Italy, Switzerland, Gulf, Istanbul, Asian hubs. Traveller assumed to hold only the destination visa.

**Results.**
- Itineraries needing a transit visa: **10%** overall (Europe 11%, US/Canada 5%, Australia/NZ 2%, Latin America 30%). Trap hubs: UK 307, US 178, Australia 16.
- Origin-destination pairs with at least one trap option: **24%**; pairs where every 1-stop option is a trap: 5%.
- Rules: obtainable without an LLM by hand-curating ~8 hub rules from official pages.
- Route data: only stale OpenFlights has an acceptable licence (the weekly-updated route file has none).

**Concerns for Stage 6.** Passes on the pair-level number, but most popular corridors (US/Canada, Australia) have low trap rates because travellers usually hold visas that exempt them. Detecting a trap on a 1-stop route is a join (origin -> hub -> destination + rules), so the graph's role must come from conditional exemptions, multi-stop search and what-if. Prior art: per-itinerary visa checkers and the Layovered app.

### C41: Submarine cable what-if — KILL
**Method.** All 712 cables from the Submarine Cable Map API (TeleGeography; CC BY-NC-SA 3.0); kept 350 in-service international cables, 792 landing points, 185 countries. For each country, maximum flow (unit capacity per cable and landing point) to all other countries.

**Results.** 30 countries have one international cable (obvious). 23 have 2+ cables but a cut of 1 (e.g. Argentina, Pakistan, Ghana, Jordan), **but in every case except Ukraine that's because all cables land in one city**, which a simple count of landing cities reveals. For 154 of 185 countries the cut equals min(#cables, #landing cities). No capacity data (paid), so real impact can't be measured.

**Why it dies.** Kill rule 6: the algorithm's answer equals a naive count.

### C21: Climate liability tracer — BLOCKED
GEM's ownership tracker (CC BY 4.0; the OpenSanctions mirror lists 48,324 entities) downloads only through a form that requires an email address. We did not submit the user's email to a third party. The OpenSanctions mirror exposes no bulk export for this dataset. Pain evidence was already weak.

### C24: Conflict-free reviewer finder — PASS
**Method.** OpenAlex API (CC0; now metered beyond a free daily allowance, 88 calls used). 15 highly cited 2024+ articles in three fields (graph neural networks for drug discovery, retrieval-augmented generation, perovskite solar cells); 14 usable. Candidate reviewers = most frequent authors of each paper's "related works" (up to 30, excluding the paper's authors). Co-authorship from works since 2016.

**Results.** 311 candidates. Directly co-authored with a paper author (1 hop): **3 (1.0%)**. Within 2 hops: **63 (20.3%)**. Spread is uneven: one perovskite paper had 23/30 candidates within 2 hops, an AI-in-classroom paper 0/14.

**Concerns for Stage 6.** Two-hop closeness isn't a formal conflict in most policies (they check direct co-authors, advisors, institutions), so the honest pitch is reviewer *independence*, not *conflict*. Author disambiguation quality not yet measured. Strong prior art (Semantic Scholar peer-review API, OpenReview conflict detection). Data: CC0 snapshot free on S3 (~330 GB); API metered.

### C31: Maths prerequisite planner — KILL
**Method.** Mathlib4 theorem dependency graph (LeanDojo Benchmark 4, CC BY 4.0, 137,046 nodes, 304,433 edges; edges point from a lemma to the theorems that use it). Prerequisite closure = all ancestors.

**Results.** 17 of 20 famous theorems found; median closure **6**; Euclid's infinitude of primes, the intermediate value theorem and pi > 3 show **0** prerequisites; random declarations: median 0, 90th percentile 57.

**Why it dies.** The graph records only premises used in traced tactic proofs, so prerequisite chains are tiny and incomplete.

### C39: Scam-shop network check — KILL
**Method.** "Fraudulent and Legitimate Online Shops Dataset" (Mendeley, CC BY 4.0; 579 fake + 561 legitimate shops, collected 2023). Resolved A and NS records now. Linked two shops if they share an IP outside the big shared providers (AWS, Google Cloud, Cloudflare, Fastly, Shopify storefront range) or an identical name-server set outside big DNS hosts.

**Results.** Still resolving: fakes **93/579 (16%)**, legit 548/561. Alive fakes linked to another fake: **4%**. Legit linked to another legit: 24% (shared hosting). Two-thirds of alive fakes sit behind big providers.

**Why it dies.** Fake shops vanish quickly, and in this labelled data shared infrastructure doesn't separate fakes from legitimate shops. (Large single campaigns like the 20,000-domain network Malwarebytes found are a different, investigator-facing case.)

---

## What Stage 4 taught us

1. **Measuring beats reasoning.** The two candidates that looked strongest on paper (C10, C40) failed hard; Stage 3's checks were necessary but nowhere near sufficient.
2. **Outside-in data rarely shows the hidden links that matter** (C10: internal backends; C39: fakes hide behind big providers and die).
3. **Algorithms often collapse to counting** (C41 cut = count of landing cities; C40 cut = naive fix). Always compute the naive baseline next to the algorithm.
4. **The one clear graph win was multi-hop proximity in a dense, given network** (C24: direct links catch 1%, two hops catch 20%). Worth remembering when generating new ideas.

## Sources
- AWS outage victims: https://www.newsweek.com/amazon-web-services-down-full-list-of-sites-impacted-10904177 ; cloud ranges: https://ip-ranges.amazonaws.com/ip-ranges.json , https://www.gstatic.com/ipranges/cloud.json , https://www.cloudflare.com/ips-v4 , https://api.fastly.com/public-ip-list ; Tranco: https://tranco-list.eu
- deps.dev API: https://docs.deps.dev/api/v3/ ; top PyPI: https://github.com/hugovk/top-pypi-packages ; top npm: https://github.com/wooorm/npm-high-impact
- OpenFlights: https://openflights.org/data.php ; transit rules: https://in.diplomatie.gouv.fr/en/france-lifts-airport-transit-visa-requirements-indian-nationals , https://india.diplo.de/in-en/2752166-2752166 , https://www.davidsonmorris.com/transit-visa-uk/ , https://www.indianeagle.com/travelbeats/do-indians-need-canada-transit-visa/ , https://www.tataaig.com/travel-insurance/australia-transit-visa-for-indians
- Submarine Cable Map: https://www.submarinecablemap.com (API v3; TeleGeography, CC BY-NC-SA 3.0)
- GEM ownership tracker: https://globalenergymonitor.org/projects/global-energy-ownership-tracker
- OpenAlex: https://api.openalex.org ; https://help.openalex.org/access/snapshot/
- Mathlib4 dependency graph: https://zenodo.org/records/19837332
- Fake/legit shops: https://data.mendeley.com/datasets/m7xtkx7g5m/1
