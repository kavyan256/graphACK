# Round 2: focused loop through Stages 2-4 (Oct 5 2026)

**Why:** Stage 4 left only two survivors (C24 pass, C01 marginal). The one clear graph win was **multi-hop proximity in a dense network whose links are given** (C24: direct co-authorship flags 1% of candidate reviewers, two hops flag 20%). This loop generated new candidates on that pattern only, screened them, and measured the survivors. Scripts and outputs: `research-data/stage4-kill-tests/r1/`, `r4/`.

---

## Stage 2 (round 2): candidates on the pattern

| ID | Candidate | Network |
|---|---|---|
| R1 | **Independent expert finder.** A journalist or fact-checker needs an expert on topic X with no ties to the company in the story, and proof of how close each expert is | OpenAlex co-authorship + company affiliations (+ funders) |
| R2 | Mutually independent review panel builder | OpenAlex co-authorship |
| R3 | Citation-cartel detector (journals citing each other abnormally) | Journal citation network |
| R4 | **Paper-mill co-author risk.** Do co-authors of known paper-mill papers produce more later retractions? | Retraction Watch + OpenAlex co-authorship |
| R5 | Revolving-door tracer (lobbyists who worked at the regulator) | US lobbying disclosures |
| R6 | Board-interlock independence ("independent" directors with hidden ties) | SEC insider filings |
| R7 | Study-funding independence | OpenAlex funders + affiliations |
| R8 | Paid-editing rings on Wikipedia | Co-editing network |

## Stage 3 (round 2): cheap screen

| ID | Result | Reason |
|---|---|---|
| R1 | **PASS** | Expert services are human-curated: SciLine, HealthNewsReview's list of ~100 experts without industry ties; ProPublica "Dollars for Profs" / Open Payments track money for US doctors. No automated "how close is this expert to the company" tool found |
| R2 | MERGED into C24 | Same engine; becomes a feature (pick a panel whose members are independent of the authors and of each other) |
| R3 | KILL (built-in) | Clarivate already publishes annual citation-stacking suppressions; detection research exists |
| R4 | PASS (prior art noted) | Clear Skies' commercial Papermill Alarm uses authorship-network analysis at submission for publishers; no open post-publication tool. Kept because Retraction Watch gives exact ground truth |
| R5 | KILL (prior art) | OpenSecrets runs a revolving-door database |
| R6 | KILL (prior art) | LittleSis maps power networks openly |
| R7 | MERGED into R1 | Funding ties become another edge type in R1 |
| R8 | KILL (ethics) | Personal data, accusation risk |

## Stage 4 (round 2): kill tests

Kill numbers were set before measuring.

### R1: Independent expert finder — **PASS**
**Kill if:** fewer than 20% of top topical experts are within 2 co-author hops of the company's researchers, or two hops find fewer than 2x the ties that direct links find.

**Method.** OpenAlex API (CC0), works since 2015. Four real cases: Pfizer + mRNA vaccine, Bayer + glyphosate, Monsanto + glyphosate, Google + large language models. "Company circle" = everyone who co-authored a company-affiliated paper on the topic. "Experts" = the 45 most prolific authors on the topic, excluding company employees. 1 hop = the expert is in the company circle; 2 hops = the expert co-authored with someone in it.

**Results.**

| Case | Company papers on topic | Company circle | Tied directly | Tied within 2 hops |
|---|---|---|---|---|
| Pfizer, mRNA vaccine | 458 | 3,866 | 6/45 | 37/45 |
| Bayer, glyphosate | 63 | 298 | 7/45 | 35/45 |
| Monsanto, glyphosate | 45 | 233 | 6/45 | 24/45 |
| Google, large language models | 600 | 2,760 | 9/45 | 29/45 |
| **Total** | | | **28/180 (16%)** | **125/180 (69%)** |

- Two hops find **4.5x** more ties than direct links.
- **Tie strength varies widely**: number of distinct "middle" co-authors linking a tied expert to the company circle: 1 path for 9 experts, 2-5 for 35, 6-20 for 57, over 20 for 23 (median 8). A graded score (how many independent paths, how recent) is far more informative than yes/no, and counting independent paths is a native graph computation (max flow).
- **Data quality:** 38/180 "experts" have over 1,000 works; in the LLM case several top "experts" (up to 21,948 works, no ORCID) are merged author profiles. 169/180 have an ORCID, so an ORCID / works-count filter is needed.

**Design implication.** Because ~70% of experts in a busy field are within two hops, the product should **rank by tie strength and show the paths**, not just say "tied / not tied". Ties are evidence for a human decision, never an accusation.

### R4: Paper-mill co-author risk — **KILL**
**Kill if:** later paper-mill retractions among the network's papers are under 10x the base rate, or two hops reach under 20% of later retractions that one hop misses.

**Method.** Retraction Watch via Crossref (72,870 records; 11,712 paper-mill retractions; 2,922 retracted from 2024 on = targets). 160 random seed papers retracted for paper-mill reasons by June 30 2023, all matched in OpenAlex (558 seed authors). One hop = the seed authors' other papers since 2015; two hops = papers of a random 400 of their 56,051 co-authors.

**Results.**
- One hop: 13 later paper-mill retractions among 10,176 papers = **0.13%** = 42x the overall base rate (12x vs health and life sciences only).
- Two hops: **0** among 7,485 papers.
- Base rate: 2,922 targets / 96.8M works published 2015-2023 = 0.003% (0.011% in health + life sciences).

**Why it dies.** The signal lives entirely in "other papers by the same author", a one-hop lookup that existing integrity tools already do; co-authors add nothing. Also, 0.13% means 99.87% of flagged papers would be fine.

---

## Outcome: finalists for Stages 5-6

| Finalist | Status | Note |
|---|---|---|
| **R1 Independent expert finder** | PASS (strong) | Graded tie strength over a dense CC0 graph; journalists / fact-checkers |
| **C24 Conflict-free (independent) reviewer finder** | PASS | Same engine as R1; editors / programme chairs; panel building (R2) as a feature |
| **C01 Transit-visa route guard** | PASS (marginal) | Different domain (everyday travel); stale route data; trap detection close to a join |

R1 and C24 could be one product with two front doors ("how independent is this person from that company / these authors?"), which would also let the demo show both a journalist and an editor use case. Stage 6 should test both framings.

## Sources
- OpenAlex: https://api.openalex.org ; snapshot https://help.openalex.org/access/snapshot/
- Retraction Watch via Crossref: https://gitlab.com/crossref/retraction-watch-data
- Expert services (prior art): https://www.theopennotebook.com/2021/11/02/dont-get-conflicted-what-to-do-when-your-source-has-a-coi/ ; https://www.journaliststoolbox.org/2023/05/03/expert_sources/ ; https://healthjournalism.org/blog/2016/03/check-out-your-sources-for-conflicts-of-interest
- Paper-mill tools (prior art): https://stm-assoc.org/stm-integrity-hub-incorporates-clear-skies-papermill-alarm-screening-tool/
