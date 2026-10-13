# Inventory 1B: open datasets where the links are given (Stage 1, Oct 5 2026)

Internet-only research. **V** = verified from a source on Oct 5 2026 (link in the Sources section). **B** = believed from memory, not re-checked today. **U** = unknown, check before use.

Rules for this list (from `win-spec.md`): the core links must be **in the data** (no LLM/ML extraction), the data must be public/synthetic/own, the licence must allow a public repo, and it must load in about a day.

Column key:
- **Links**: Y = typed links given; P = partly given / need joining; N = would need extraction
- **Truth**: built-in ground truth we could check answers against
- **Who cares**: E = everyday people, S = students, D = developers, P = professionals/specialists
- **Risk**: gate or practical problems

---

## A. Ownership, money, organisations

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **GLEIF LEI Level 2 ("who owns whom")** | Y: direct + ultimate accounting parent, typed | 672,239 relationship records (Oct 3 2026); entity file of LEIs (count U, ~millions) | **CC0 (V)** | Free CSV golden copy, daily, no login | **Yes: entities report both direct and ultimate parent, so a traversal can be checked exactly** | P | Only entities with LEIs; no individuals (good: no personal data) |
| **GEM Global Energy Ownership Tracker** | Y: asset -> owner -> parent chains with **ownership %** (>=5%) | Coal/oil-gas/bioenergy/steel plants, coal mines (count U) | **CC BY 4.0 (V)** | Download page (form? U) | Partial: ultimate parents listed | P, E (climate) | Climate/energy angle is relatable; check download form |
| **Companies House PSC (UK)** | Y: company -> person/company with significant control | Millions of companies (B) | **OGL (V)**, daily JSON bulk, free | No login | Weak | P | **Contains named individuals** (personal data risk); corporate-only subgraph is safer |
| **OpenSanctions** | Y: sanctioned entities, ownership, family/associates | Large (U) | **CC BY-NC 4.0 (V)**, bulk with no login | Free download | Lists are ground truth for "is this sanctioned" | P | Non-commercial only; personal data of listed persons; fraud/AML space is crowded |
| USAspending (US federal awards, subawards) | Y: agency -> recipient -> subrecipient | Very large (B) | Public domain (B) | API/bulk | Weak | P, E (civic) | US-centric |

## B. Software and security

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **deps.dev** | Y: package version -> dependency (resolved graphs for npm, Cargo, Maven, PyPI); requirements for 7 systems | Very large | **CC BY 4.0 (V)** | Free API, no key | Exact: package manager resolution | D | Resolvers already do much of it (Fix-Path lesson) |
| **OSV.dev** | Y: vulnerability -> package -> affected version ranges | All ecosystems (`all.zip`) | **CC BY 4.0 for major sources (V)** (GitHub Advisory DB, PyPI, Go, PSF) | Public bucket download | Exact affected ranges | D | Security triage = organiser example; crowded (Hopper, aegis-graph) |
| **CISA KEV** | P: CVE -> vendor/product (join to OSV/NVD) | 1,723 entries (Sep 24 2026) | **CC0 (V)** | JSON/CSV, GitHub mirror | "Actually exploited" label | D, P | Small; useful as a label set |
| **Mathlib4 theorem dependency graph** | Y: theorem -> theorem it uses | 137,046 nodes, 304,433 edges (Oct 2023 commit) | **CC BY 4.0 (V)** | Zenodo / Mendeley | **Exact dependencies** | S (niche: formal maths) | Niche audience |
| LeanDojo Benchmark 4 | Y: theorems, tactics, premises | 102,514 theorems, 152,695 premises | **CC BY 2.0 (V)** | Zenodo | Exact premise use | S, P (AI-for-maths) | Niche |
| Debian package metadata (Packages, UDD) | Y: depends/recommends/conflicts | ~60k+ packages (B) | U | Mirrors, no login | Exact: `apt-get --simulate` | D | `apt rdepends` already gives the closure |
| MITRE ATT&CK / CWE / CAPEC; NVD | Y: technique <-> mitigation, weakness <-> attack pattern | Thousands of nodes | Free with attribution (B); NVD public domain (B) | Download | Weak | P | Security space crowded |

## C. Knowledge, research, encyclopedic

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **Wikidata** | Y: typed statements, thousands of properties | ~100M+ items (B) | CC0 (B) | Public SPARQL endpoint (timeouts), dumps | Constraints, references | E, S, P | Huge; extract a domain subgraph via SPARQL |
| **Wikipedia clickstream** | Y: (referrer -> article, count) | ~25M pairs/month for English (2016 figure) | **CC0 (V)** | Monthly TSV dumps | Real human navigation | E, S | Pairs with <=10 views removed |
| **OpenAlex** | Y: works, authors, institutions, citations, topics, funders | ~330 GB snapshot | **CC0 (V)** | S3, **no login** (V) | Citations, retractions (with RW) | S, P | Big; sample a field |
| **Retraction Watch (via Crossref)** | P: retracted DOI -> reasons (join to OpenAlex citations) | 60,000+ records | Open, updated daily (V); exact licence U | GitLab CSV, Crossref API | Exact retraction labels | S, P | Earlier "retraction ripple" idea killed for noisy indirect effects |
| **CourtListener** | Y: opinion -> cited opinion, **with citation depth** | Large (US case law) | **Public domain (V)** (US court records) | Quarterly bulk, free | Overruled-case lists exist elsewhere | P, S (law) | US-centric; legal advice risk |
| **legislation.gov.uk effects** | Y: affecting provision -> affected provision, effect type (repealed, substituted...) | All UK legislation | **OGL v3 (V)** | API | Effects are the ground truth | P | "Somewhat out of date" for recent years (V) |
| **Stack Exchange dumps** | Y: PostLinks (**duplicate** and related links), tags, answers | All sites | **CC BY-SA 4.0 (V)** | **Official = login + terms since 2024; community copies on archive.org up to 2025-12-31 (V)** | Duplicate links are ground truth | D, S | Watermarking since 2025-06; ToS controversy; use archive.org copy |
| **Open Library** | Y: work -> edition -> author, subjects | Editions ~9 GB, works ~3 GB | **CC0 (V)** | Monthly dumps | Weak | E | Mostly catalogue; few deep links |
| **Wiktionary (kaikki.org)** | Y: etymology templates (inherited/borrowed/derived), translations, forms | Hindi 35,881 words etc. | CC BY-SA (V, earlier) | Free JSONL | Cognate labels (62-64% recall measured) | E, S | Tested in the scrapped cognate idea: mostly 2-hop |
| ConceptNet | Y: commonsense relations | ~34M edges (B) | CC BY-SA 4.0 (B) | Download | Weak | — | Stale (last release ~2019, B) |

## D. Health and biology

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **PrimeKG** | Y: 30 edge types (drug, disease, gene, phenotype, side effect...) | 129,375 nodes, 4,050,249 edges | **CC0 (V)** | Harvard Dataverse (edges.csv 369 MB) | Known indications / contraindications | E (patients), P | Medical-advice risk; needs careful wording |
| **Hetionet v1.0** | Y: 24 edge types | 47,031 nodes, 2,250,197 edges | **CC0 for original content (V)**; sources vary | GitHub / Neo4j dump | PharmacotherapyDB indications (B) | P | **Prior art: "DrugPath" agent over Hetionet won attention at a Neo4j Aura Agent Hackathon 2026 (V)** |
| **ClinicalTrials.gov** | Y: trial -> condition, intervention, sponsor, site | ~500k+ studies (B) | Free; US public domain with caveats (V) | API v2 + bulk JSON | Trial status/results | E (patients), P | Mostly attributes, fewer deep links |
| **Synthea (synthetic patients)** | Y: patient -> encounters, conditions, meds, providers | Generate any size (100 patients = 7 MB CSV) | **Apache 2.0 (V)** | Generator, run locally | **Exact (we generate it)** | E, P | Synthetic: realistic but no real-world truth |
| Reactome | Y: pathways, reactions | Large | CC0 (V, earlier) | Download | Curated pathways | P | Specialist |

## E. Transport, places, infrastructure

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **OpenStreetMap** | Y: roads, junctions, transit relations | Any region (Geofabrik extracts) | ODbL (B) | Free download | Exact routing on the network | E | Google Maps is the baseline to beat |
| **Mobility Database (GTFS catalog)** | Y: stops, trips, transfers, schedules | 6,000+ feeds, 99+ countries (V) | Per-feed licence in feed.json (V) | Free | Exact timetables | E | Journey planners exist everywhere |
| **Delhi Open Transit Data (GTFS)** | Y: DTC/DIMTS bus stops, routes, trips | City-wide | Licence at opendata.iiitd.edu.in/terms (V link; terms U) | Static GTFS free | Timetable | E (India) | **Stop times are rough estimates at constant speed (V)** |
| Indian Railways datasets (datameet, others) | Y: stations, train routes, halts | 8,990+ stations, 5,208+ trains in one MIT-licensed dataset (V; repo name U) | MIT (V) / datameet licence U | GitHub | Timetables | E (India) | **Prior art: `railways-mcp` (journey planning MCP server) (V)** |
| Wikipedia-derived / OSM power & water networks | P | Varies | ODbL / varies | — | Weak | P | Grid data quality uncertain |

## F. Culture, sport, games

| Dataset | Links | Size | Licence | Access | Truth | Who cares | Risk / notes |
|---|---|---|---|---|---|---|---|
| **MusicBrainz** | Y: very rich typed relationships (performer, producer, member of, **"samples material"**, covers, remix...) | Millions of recordings (B) | **CC0 core data (V)**; supplementary data CC BY-NC-SA | Monthly PostgreSQL/JSON dumps | Weak (WhoSampled is proprietary) | E | Huge, relatable; need a sharp question |
| Discogs dumps | Y: release -> artist, label, credits | Very large (B) | CC0 (B) | Monthly dumps | Weak | E | Overlaps MusicBrainz |
| **Lichess** | Y: games, positions, puzzles | Huge (sample) | CC0 (V, earlier) | Dumps | **Exact (FEN, puzzle solutions)** | E | Chess repertoire tools crowded |
| **Cricsheet** | Y: ball-by-ball (bowler, batter, match) | 22,905 matches | ODC-BY (V, earlier) | Download | Match outcomes | E (India!) | Much of it is aggregation (table) |
| StatsBomb open data | Y: passes, pressures, 360 freeze frames | Hundreds of matches | Free with attribution/agreement (V, earlier) | GitHub | Event outcomes | E | Per-match graphs are tiny |

## G. Synthetic generators (exact truth, no privacy issues; allowed by the rules)

| Generator | What it makes | Licence | Truth | Note |
|---|---|---|---|---|
| **Synthea** | Patients, encounters, conditions, medications, providers | Apache 2.0 (V) | Exact | See D |
| **LDBC FinBench datagen** | Temporal financial graph (accounts, loans, transfers, hub vertices, multi-edges) + official query workload | Apache 2.0 (V) | Exact | Fraud = organiser example; needs a twist |
| LDBC SNB datagen | Social network + official queries | Apache 2.0 (B) | Exact | Generic |
| AMLSim (IBM) | Money-laundering transactions with labelled typologies | Apache 2.0 (B) | Labelled | Kaggle copy needs login; the generator doesn't |

## H. "Your own data" (allowed by the rules)

The rules allow "personal data you own" (e.g. your own Google Takeout, your own GitHub activity, your own notes). A public repo and demo can't include it, so pair it with a synthetic stand-in for the demo. Worth keeping in mind for personal-assistant style ideas.

---

## Best raw material so far (links given + licence clean + some built-in truth)

| Rank | Dataset | Why it stands out | Main worry |
|---|---|---|---|
| 1 | **GLEIF Level 2** | CC0, no personal data, typed ownership, and **exact ground truth** (reported ultimate parent vs our traversal) | Audience is professional (compliance, finance) |
| 2 | **PrimeKG** | CC0, 4M typed edges, deep multi-hop, relatable (medicines) | Medical-advice risk; Hetionet agent prior art |
| 3 | **OpenAlex + Retraction Watch** | CC0, huge, exact retraction labels | Retraction ripple already killed once (noisy) |
| 4 | **MusicBrainz** | CC0, rich typed links, everyday audience | No ground truth; needs a sharp question |
| 5 | **CourtListener / legislation.gov.uk** | Public domain / OGL, typed citation/effect links | Legal advice risk; professional audience |
| 6 | **GTFS / OSM** | Everyday pain, exact network | Strong incumbents (Google Maps, journey planners) |
| 7 | **Stack Exchange** | Duplicate links = labelled truth; developer audience | Access controversy; mostly text |
| 8 | **Synthea / LDBC** | Exact truth by construction | Synthetic = weaker impact story |

This ranking is about the *data only*. Stage 2 combines it with pain (1C) and shapes (1A).

---

## Sources (checked Oct 5 2026)
- GLEIF: https://www.gleif.org/en/lei-data/gleif-concatenated-file/download-the-concatenated-file ; https://www.gleif.org/en/lei-data/access-and-use-lei-data/level-2-data-who-owns-whom
- GEM ownership tracker: https://globalenergymonitor.org/projects/global-energy-ownership-tracker/download-data/ ; https://globalenergymonitor.org/creative-commons-public-license/
- Companies House PSC: https://chguide.co.uk/bulk-data/psc
- OpenSanctions: https://www.opensanctions.org/licensing/ ; https://www.opensanctions.org/docs/bulk/
- deps.dev: https://docs.deps.dev/api/v3/
- OSV: https://google.github.io/osv.dev/data/
- CISA KEV: https://github.com/cisagov/kev-data ; https://www.cisa.gov/sites/default/files/licenses/kev/license.txt
- Mathlib4 dependency graph: https://zenodo.org/records/19837332 ; LeanDojo: https://zenodo.org/records/18815372
- Wikipedia clickstream: https://dumps.wikimedia.org/other/clickstream/readme.html
- OpenAlex: https://help.openalex.org/access/snapshot/ ; https://registry.opendata.aws/openalex/
- Retraction Watch via Crossref: https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
- CourtListener: https://www.courtlistener.com/help/api/bulk-data/
- legislation.gov.uk: https://legislation.github.io/data-documentation/api/overview.html
- Stack Exchange dumps: https://archive.org/details/stackexchange_20251231 ; https://devclass.com/2024/07/30/stack-exchange-restricts-access-to-dump-of-user-contributed-data-as-critics-complain-license-permits-reuse-for-any-purpose/
- Open Library: https://openlibrary.org/developers/dumps
- PrimeKG: https://github.com/mims-harvard/PrimeKG ; https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM
- Hetionet: https://github.com/hetio/hetionet ; prior art https://github.com/qualv13/neo4j-agent
- ClinicalTrials.gov: https://clinicaltrials.gov/about-site/terms-conditions
- Synthea: https://github.com/synthetichealth/synthea
- LDBC FinBench: https://github.com/ldbc/ldbc_finbench_docs
- Mobility Database: https://mobilitydatabase.org/about
- Delhi OTD: https://otd.delhi.gov.in/documentation/
- Indian Railways: https://github.com/datameet/railways ; prior art https://github.com/shubhamyadav8901/railways-mcp
- MusicBrainz: https://musicbrainz.org/doc/About/Data_License ; https://musicbrainz.org/relationships/recording-recording
