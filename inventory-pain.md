# Inventory 1C: public evidence of connection-shaped pain (Stage 1, Oct 5 2026)

Internet only. No interviews. Evidence comes from:
- **Stack Exchange API**: count of questions containing an exact phrase (quoted search; relative signal, not an absolute census), plus the top-voted questions and their **view counts** (how many people hit the problem).
- **Hacker News (Algolia API)**: stories and comments containing a phrase.
- **Reddit** via the PullPush archive (direct Reddit access is blocked): used for **examples only**, because subreddit filters were unreliable.
- **Incident reports and statistics** from news and official sources (links at the end).

Raw outputs are in the session scratchpad (`se_grid.json`, `se_examples.json`, `hn.json`, `pp.json`).

---

## 1. Raw signal tables

### Stack Exchange: exact-phrase question counts
| Phrase (shape) | Stack Overflow | SW Eng | Server Fault | Ask Ubuntu | DBA | DevOps |
|---|---|---|---|---|---|---|
| "root cause" (S3) | 15,821 | 50 | 624 | 403 | 261 | 13 |
| "circular dependency" (S12) | 4,020 | 80 | 18 | 16 | 9 | 0 |
| "single point of failure" (S5) | 546 | 44 | 234 | 4 | 38 | 5 |
| "safe to remove" (S1) | 487 | 2 | 65 | 178 | 19 | 0 |
| "impact analysis" (S1) | 90 | 7 | 1 | 0 | 1 | 0 |
| "find all usages" (S1) | 64 | 1 | 0 | 0 | 0 | 0 |
| "what depends on" (S1) | 61 | 2 | 2 | 1 | 0 | 0 |
| "reverse dependencies" (S1) | 52 | 1 | 3 | 11 | 0 | 0 |
| "what will break" (S1/S10) | 34 | 1 | 6 | 3 | 0 | 0 |
| "why is this package" (S3) | 19 | 0 | 1 | 7 | 0 | 0 |

| Other sites | Count |
|---|---|
| Travel: "connecting flight" | 828 |
| Travel: "missed connection" | 36 |
| GIS: "shortest path" / Stack Overflow: "shortest path" | 564 / 5,508 |
| Stack Overflow: "graph database" | 2,118 |
| Genealogy: "related to" / "common ancestor" | 145 / 38 |
| Academia: "retracted" | 99 |
| Law: "subsidiary" / "beneficial owner" | 49 / 4 |
| Money: "parent company" | 38 |
| Music: "sampled" / Music Fans: "sampled" | 25 / 6 |
| Medical Sciences: "interact with" / "drug interaction" | 11 / 6 (small site) |

### Most-viewed real questions (top results by votes)
| Question | Site | Views |
|---|---|---|
| How to list dependent packages (reverse dependencies)? | Ask Ubuntu | **403,247** |
| Resolve build errors due to circular dependency amongst classes | Stack Overflow | **337,349** |
| Do I need a US visa to transit (or layover) through an American airport? | Travel | **329,375** |
| Circular dependency in Spring | Stack Overflow | 198,834 |
| How do I remove cached .deb files? ("safe to remove") | Ask Ubuntu | 176,084 |
| Rediscovery of calculus in 1994: what should have happened to that paper? (retraction) | Academia | 147,219 |
| Do you have to take the second leg of a domestic flight? | Travel | 128,193 |
| Find all occurrences of a function in Eclipse | Stack Overflow | 58,141 |
| Why do airlines offer flight itineraries with unrealistically short layovers? | Travel | 23,821 |
| Is AWS's Elastic Load Balancer a single point of failure? | Server Fault | 15,374 |
| No transit zone at Linate airport. Couldn't get on connecting flight. Whose responsibility is it? | Travel | 9,674 |

### Hacker News: phrase counts
| Phrase | Stories | Comments |
|---|---|---|
| "root cause" | 622 | 19,908 |
| "who owns" | 801 | 11,444 (ambiguous: data, code, companies) |
| "single point of failure" | 155 | 5,678 |
| "blast radius" | 109 | 2,743 |
| "knowledge graph" | 653 | 2,235 |
| "dependency hell" | 89 | 2,065 |
| "graph database" | 537 | 1,913 |
| "single source of truth" | 130 | 1,670 |
| "supply chain attack" | 432 | 1,283 |
| "circular dependency" | 13 | 404 |
| "is there a tool" | 166 | 308 |
| "agent memory" | 277 | 203 |
| "impact analysis" | 55 | 215 |
| "what depends on" | 14 | 154 |
| "drug interaction" | 9 | 107 |
| "transit visa" | 2 | 78 |

### Reddit examples (PullPush archive; examples, not counts)
- r/india (Jun 2026, 201 pts): "After France, Germany scraps Schengen transit visa requirement for Indians."
- r/indiatravel (Nov 2025): "Booked India-Canada-Austin flight without knowing i need a transit visa. Stuck"
- r/KLM (Apr 2026, 36 comments): "wrongfully denied boarding" (transit visa)
- r/indianrailways (Dec 2025, 519 pts): "Couldn't board the train!!"; (Apr 2025) "Waiting for connecting train. Last leg 3 hour."
- r/cfs (Dec 2022, 70 pts, 70 comments): "A ME/CFS expert told me my main problem was that I was on 'too many medicines.' Is polypharmacy..."
- r/PromptEngineering (Jun 2026, 338 pts): AI agent tutorials post; agent memory is a hot topic.

### Real-world incidents and statistics (verified)
| Event / statistic | Number | Shape it illustrates |
|---|---|---|
| AWS us-east-1 outage, Oct 19-20 2025 (DynamoDB DNS race condition) | 15 hours; **17M+ outage reports; 1,000+ companies; 142+ AWS services** | Hidden shared dependency, cascade (S1, S5) |
| Log4Shell (Dec 2021), Google Open Source Insights | **35,863 Maven packages (~8% of Maven Central)**; only ~7,000 direct; **>80% more than one level deep, most 5 levels, up to 9** | Deep transitive ripple (S1) |
| WHO: medication-related harm | ~**1 in 20 patients**; medication errors cost ~**$42B/year** globally | Interaction paths (S3) |
| Polypharmacy | 45.2% of older adults in a European study; ADRs cause 5-8% of unplanned UK hospital admissions | Multi-drug combinations (S3, S12) |
| Transit visa rules for Indians | Spain, France, Germany dropped airport transit visas for Indians: **Mar 4, Apr 10, Jun 3 2026** | Rules change over time -> memory + what-if (S2, S10, S11) |

---

## 2. Pain areas, ranked

Scored 1-5 on: **Freq** (how often people hit it), **Sev** (cost when it happens), **Gap** (how badly existing tools serve it; 5 = big gap), **Data** (links given + licence OK, from `inventory-data.md`). Total out of 20.

| # | Pain area | Shape | Evidence | Existing tools (the baseline) | Freq | Sev | Gap | Data | Total |
|---|---|---|---|---|---|---|---|---|---|
| P1 | **Transit / connection traps when travelling** ("can I route through X with my passport?") | S2 no-path proof, S3 constrained path, S10 what-if, S11 memory (rules change) | 329K-view US transit question; 828 "connecting flight" questions; Reddit "stuck", "denied boarding"; 3 EU rule changes for Indians in 2026 | IATA Timatic (proprietary, airline-side), visa-checker sites (per country, not per route), flight search ignores visas (U) | 4 | 4 | 4 | 2 (visa rules: Wikipedia tables CC BY-SA; **flight route data is the gap**: OpenFlights is 2014) | **14** |
| P2 | **Medicines that clash through a hidden mechanism** | S3 explanation path, S12 pattern | WHO 1 in 20 harmed, $42B/yr; polypharmacy 45%; Reddit worries | Drugs.com / Medscape checkers (pairwise lists) | 4 | 5 | 2 (checkers exist; graph adds "why" + multi-drug) | 4 (PrimeKG, Hetionet CC0) | **15**, but medical-advice risk and DrugPath prior art |
| P3 | **Hidden shared single points of failure** ("these look independent but go down together") | S5 redundancy, S1 ripple, S10 what-if | AWS outage 17M reports / 1,000+ companies; HN "single point of failure" 5,678 comments, "blast radius" 2,743 | Cloud vendor tools, aegis-graph (peer), SRE tooling | 3 | 5 | 2 (crowded in cloud ops) | 2 (dependency maps of real services aren't public; would have to be collected or synthetic) | **12** |
| P4 | **What depends on X / is it safe to remove X** (packages, code) | S1 ripple | 403K-view reverse-deps question; "safe to remove" 487 + 178 questions; "dependency hell" 2,065 HN comments | `apt rdepends`, `npm why`, IDE "find usages", resolvers | 5 | 3 | 1 (built-ins answer the closure) | 5 (deps.dev, Debian) | **14**, but Gap = 1 (kill rule 4 unless the value is beyond the closure) |
| P5 | **Deep transitive vulnerability exposure** | S1, S2 | Log4Shell: 35,863 packages, >80% indirect, up to 9 levels | Snyk, Dependabot, OSV-Scanner, Hopper, aegis-graph | 3 | 5 | 1 | 5 | **14**, crowded |
| P6 | **Circular dependencies** | S12 cycles | 4,020 SO questions; 337K-view top question | IDEs, madge, compilers | 4 | 2 | 1 | 4 | **11** |
| P7 | **Who really owns this company/brand** | S1 up-chain, S12 loops | HN "who owns" 11,444 comments (ambiguous); money SE "parent company" 38; GLEIF has exact parent data | Consumer brand-ownership apps (U); KYC vendors for professionals | 2 | 2 (consumers) / 4 (compliance) | 3 | 5 (GLEIF CC0, exact truth) | **12-14** depending on user |
| P8 | **Agent forgets context across sessions** | S11 memory | HN "agent memory" 277 stories; Reddit trend; FalkorDB's own marketing theme | Graphiti, Mem0, Cognee, many peers (Track 2) | 4 | 3 | 1 (crowded) | 4 (own/synthetic) | **12** |
| P9 | **Root cause of a failure** | S3, S1 | "root cause": 15,821 SO, 19,908 HN comments | APM/RCA tools, aegis-graph | 5 | 4 | 2 | 2 (real incident graphs aren't public) | **13** |
| P10 | **Citing retracted/unreliable research** | S1 | Academia "retracted" 99, top 147K views | Retraction Watch, Zotero/EndNote retraction alerts | 2 | 3 | 2 | 5 (OpenAlex + RW CC0) | **12**; indirect version already killed (noisy) |
| P11 | **Missed train/bus connections (India)** | S3, S9 | r/indianrailways posts; data exists (8,990 stations, 5,208 trains) | IRCTC, apps, `railways-mcp` (prior art) | 4 | 3 | 2 | 3 | **12** |
| P12 | **How are these two people/things related** (genealogy, trivia) | S3 | Genealogy "related to" 145 | Ancestry/FamilySearch (login data) | 2 | 1 | 2 | 3 (Wikidata family links) | **8** |

---

## 3. What this tells Stage 2

1. **The biggest, best-documented pain is "what depends on / what breaks / root cause" in software and infrastructure**, but it is also the most crowded and the best served by built-in tools (P4, P5, P6, P9). Any idea there needs a new user or a new question, not a better closure.
2. **Two everyday pains have strong public evidence and weaker incumbents:**
   - **P1 travel connections / transit visas**: huge view counts, frequent rule changes (perfect for memory and what-if), and a natural "no path" proof. Main blocker: open flight-route data.
   - **P2 medicine clashes**: huge harm statistics and CC0 graphs with deep typed links. Main blockers: medical-advice risk and prior art (DrugPath agent on Hetionet).
3. **GLEIF (P7) has the cleanest data in the whole inventory** (CC0, exact ground truth, no personal data) but its strongest pain is professional (compliance), not everyday. A consumer angle ("who owns this brand") needs evidence of demand.
4. **Agent memory (P8) is FalkorDB's own theme but is where peers already cluster**. Use memory as a feature of a Track 1 idea, not as the idea.
5. **Counts are relative signals.** Stack Exchange phrase search and HN counts measure how often people *write* a phrase, not how many people have the problem. View counts on top questions are the better proxy for how many people hit it.

## Sources
- Stack Exchange API: https://api.stackexchange.com/docs/advanced-search ; top questions: https://askubuntu.com/questions/128524/how-to-list-dependent-packages-reverse-dependencies ; https://stackoverflow.com/questions/625799/resolve-build-errors-due-to-circular-dependency-amongst-classes ; https://travel.stackexchange.com/questions/4859/do-i-need-a-us-visa-to-transit-or-layover-through-an-american-airport
- Hacker News search: https://hn.algolia.com/api
- PullPush Reddit archive: https://api.pullpush.io
- AWS outage: https://www.thousandeyes.com/blog/aws-outage-analysis-october-20-2025 ; https://www.gremlin.com/blog/reliability-lessons-from-the-2025-aws-dynamodb-outage ; https://www.red94.net/news/73023-aws-outage-knocked-out-us-east-1-region-last-night-peak-disruptions-around-3-am/
- Log4Shell: https://blog.deps.dev/log4j/ ; https://therecord.media/google-more-than-35000-java-packages-impacted-by-log4j-vulnerabilities
- WHO Medication Without Harm: https://www.who.int/initiatives/medication-without-harm ; polypharmacy: https://bmcgeriatr.biomedcentral.com/articles/10.1186/s12877-022-03536-z ; https://www.ncbi.nlm.nih.gov/books/NBK574550/
- Transit visas for Indians: https://www.visaroots.in/post/germany-drops-transit-visa-requirement-indian-travellers-2026 ; https://www.hdfcergo.com/news/travel-insurance/france-waives-airport-transit-visa-requirement-for-indian-passport-holders-from-april-2026 ; https://en.wikipedia.org/wiki/Visa_requirements_for_Indian_citizens
