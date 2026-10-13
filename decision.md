# Stage 7: decision (Oct 5 2026)

## Decision
**Build R1 "TieTrace"** (independent expert finder with a human verifier layer; editor/reviewer panel as a second use case).
**Backup: C01 "LayoverGuard"** (transit-visa route guard), only if TieTrace's data pipeline fails in the first hours of Oct 15.

**Tracks to declare:** Track 1 (Agents That Act on Connected Data, primary) **and** Track 2 (Agent Memory and Coordination): per-newsroom memory graphs, human verdicts shared between reporters, agent handoffs.

## Why (final scores on the `win-spec.md` rubric)
| | J1 Impact | J2 Originality | J3 Technical | J4 Use of FalkorDB | J5 Control/explain | J6 Presentation | Total | Build risk |
|---|---|---|---|---|---|---|---|---|
| **R1 TieTrace** | 5 | 4-5 | 4 | 5 | 5 | 4 | **27-28/30** | Medium |
| C01 LayoverGuard | 5 | 3 | 3 | 3 | 4 | 5 | 23/30 | Low |
| Past winners (calibration) | Atrium 27, Board of SuperVision 26 | | | | | | | |

Rule check from Stage 7 of the plan: R1 passes every gate and kill rule, has public evidence of real pain (links in `user-evidence.md`), and has a "that's clever" moment (verify once, apply everywhere; the GEBN case found from public data).

## Evidence trail (all measured or verified)
| Claim | Number | Where |
|---|---|---|
| Direct ties catch few, paths catch most | 16% direct vs **69% within 2 hops** (180 experts, 4 company/topic cases) | `round2-loop.md` |
| Tie strength is graded | 1 to 20+ linking co-authors per tied expert, median 8 | `round2-loop.md` |
| One human ruling changes many scores | One paper carries ties for 16-18 of 45 experts in a case | `design-r1.md` 5b |
| Reviewer use case | 1% direct vs 20.3% within 2 hops (311 candidates) | `kill-tests.md` |
| Real-case validation | GEBN scientists (Blair, Church, Hand, Shook, Hill) are authors of Coca-Cola-funded papers in OpenAlex | `design-r1.md` |
| Pain | 1,000 UK articles quoting 50 fake experts; 54% / 32% undisclosed conflicts among "independent" commenters | `user-evidence.md` |

---

## Final idea card

```
Idea name:   TieTrace
One sentence: An agent that checks how independent an expert is from the company in a story, by tracing ties through
             co-authors, employers (incl. parent companies) and funders in the open research graph, proving independence
             when no tie exists, and learning from human verifiers.
User story:  A health reporter must quote two independent experts on a new vaccine study by 5 pm. Today that means googling
             names and reading disclosure sections; most ties are two hops away and invisible (16% direct vs 69% within two
             hops). TieTrace ranks experts by tie strength with dated, evidence-backed paths, proves independence when no tie
             exists within 3 hops, asks a human about judgement calls, and drafts the sourcing note for an editor to approve.
Graph model: nodes: Person, Work, Institution (type), Funder, Topic; memory graph: Case, Check, Decision, Verdict, Policy.
             edges: AUTHORED, AFFILIATED_WITH (year, DOI), FUNDED_BY, PARENT_OF (corporate family), ABOUT, CO_AUTHORED
             (derived: count, first/last year, recency_cost), SAME_AS / DIFFERENT_FROM (human identity verdicts),
             Verdict -> ON_PAPER / ON_PERSON / FOR_COMPANY.
Hidden thing made a node (Atrium move): the tie, and the human Verdict on its evidence paper (verify once, apply everywhere).
Heavy graph work: algo.maxFlow (tie strength = edge-disjoint paths to the company circle), algo.SPpaths (dated explanation
             paths, relDirection 'both', recency weights), algo.bfs (k-hop independence proof), PARENT_OF* recursion
             (corporate families), algo.labelPropagation (communities for independent alternatives), algo.betweenness
             (bridges), full-text index (expert search), GRAPH.COPY (preview a verdict's impact before applying),
             GRAPH.RO_QUERY (model-chosen reads), multigraph (one memory graph per newsroom).
FalkorDB-fit: strong. Dense given network (co-authorship), typed edges, multi-hop, flow, negative proofs, per-tenant memory.
SQL-awkward query: rank 45 experts by the number of edge-disjoint co-authorship paths (papers since 2019, excluding papers this
             newsroom ruled out) to anyone in Pfizer's corporate family or any author of a Pfizer-funded paper.
Data:        OpenAlex (CC0) via API (free $1/day with a free account key; ~$0.10/day anonymous). Two topic graphs:
             obesity/physical activity + Coca-Cola (validation case), mRNA vaccines + Pfizer (live case); glyphosate + Bayer
             as reserve.
Objective check: (1) GEBN validation: the five named scientists come out tied to Coca-Cola, with paths;
             (2) baseline comparison: direct-tie check vs graph score (16% vs 69% coverage);
             (3) hold-out: hide real company co-authorship edges and check scores still flag the experts;
             (4) profile guard: share of merged/split profiles caught.
Baseline:    manual disclosure reading / direct co-authorship check (what existing reviewer tools do).
Action:      ranked expert list with paths, "no tie within k hops" proof, sourcing note + disclosure line (editor approves),
             re-check alerts, independent reviewer panel (editor use case).
MCP tools:   find_experts, tie_paths, tie_strength, prove_independence, bridges, independent_alternatives, profile_quality,
             verify_tie, review_queue, record_verdict, merge_profiles, split_profiles, impact_of_verdict, save_check,
             recheck, draft_note, build_panel.
Prior art:   SciLine / Science Media Centre (human matching), ProPublica Dollars for Docs / Open Payments (US money only),
             Prophy Referee Finder (paid reviewer conflicts), Semantic Scholar peer-review API, OpenReview conflicts.
             Ours: automated, explained tie paths for journalists + human verdicts that propagate through the graph.
Biggest risks + first tests:
             1. Implying misconduct -> wording ("ties in the research record"), evidence on every tie, human gates,
                named examples only from documented public cases; README ethics section.
             2. Author-profile quality -> ORCID / works-count guard; SAME_AS merges via human verdicts.
             3. Data pipeline time -> pull the GEBN topic graph first on Oct 15; test maxFlow/SPpaths/BFS direction on a
                10-node toy graph in hour 1.
Gate check (A): pass (FalkorDB central / removal test fails hard; CC0 public data; new work Oct 15-18; explainable;
                all deliverables possible)
Score (J1-J6): 27-28/30
```

## Scope
**Must ship (MVP)**
1. Loader: OpenAlex -> FalkorDB for two topic graphs, incl. corporate families and funders.
2. Tools: find_experts, tie_paths, tie_strength (max flow), prove_independence (BFS), profile_quality, verify_tie.
3. Human verifier layer: impact-ranked review queue, record_verdict (paper ruled out; same / different person), impact report ("changed N scores").
4. Memory: newsroom graph with saved checks and decisions; re-check diff.
5. Agent: LLM chooses MCP tools; all reads via GRAPH.RO_QUERY; Writer drafts the note; editor approval.
6. Minimal web UI (expert list, path view, review card) + FalkorDB Browser for graph screenshots.
7. Evaluation numbers, README (data model, queries/algorithms list, ethics, AI disclosure, licences), 90-second video.

**Stretch (only if MVP is done)**
Editor panel builder; independent alternatives via communities; bridges via betweenness; GRAPH.COPY verdict preview; live deployment (compact graph within FalkorDB Cloud's free 100 MB, or a small VM); blog post for the Best Blog Post award.

**Cut lines**
- End of Oct 17 not end-to-end -> drop panel builder, communities, bridges.
- Midday Oct 18 not stable -> skip live deployment; submit local setup + video.
- Data pipeline broken by end of Oct 15 hour 6 -> switch to backup C01 (small data, low risk).

## Licences and notes for the README
- FalkorDB: SSPLv1. OpenAlex data: CC0 (attribute as courtesy). Crossref funder data via OpenAlex.
- AI assistance disclosed. Named individuals appear only in documented public cases (GEBN); elsewhere the demo shows paths, not accusations.
