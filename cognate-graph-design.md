# Bridge: graph design for the cognate planner (pre-event notes, Oct 5 2026)

Status: **design sketch only.** Allowed before Oct 15 (notes, graph model sketches, diagrams). The Cypher below is sketch-level, to be rewritten and tested on FalkorDB during the event. No project code before Oct 15.

Working name: **Bridge** ("you already know this word").
Primary demo pair: **Hindi -> Marathi** (39% of Marathi entries reachable, deeper chains: 17% have 3+ steps, and the शिक्षा trap is in Marathi). Second pair: Hindi -> Bengali.

---

## 1. Making the problem need a graph

The weak version is "find cognates": about 80% of it is a two-hop shared-ancestor lookup, which a SQL self-join can do (C1 = 3 in the stress test).

The graph version asks a different question:

> **"I know these languages. I want to read Marathi. Which words do I already (almost) know and *why*, which ones are traps, and what is the cheapest order to learn the rest so each new word is explained by something I already know?"**

Each part of that answer is a graph computation, not a lookup:

| Part of the answer | Graph computation | FalkorDB feature |
|---|---|---|
| Words I almost know, with the reason | Variable-depth typed path *up* to a shared ancestor and *down* to the target word, from **many** known words at once | Cypher var-length patterns, `algo.SPpaths` with `relDirection: 'both'` |
| Words with no bridge at all ("learn by rote") | Not in the same component as anything I know: a **no-path proof** | `algo.WCC` |
| Cheapest learning order where each new word explains the next | **Minimum spanning forest** rooted at what I know; lesson order = BFS over the tree | `algo.MSF` (treats edges as undirected), `algo.bfs` |
| Keystone roots ("learn these 10 roots, unlock N words") | Gain in reachable words per root; bridge roots between word families | Cypher reachability counts, `algo.betweenness`, `algo.HarmonicCentrality` (`reachable`) |
| Lessons grouped by word family, not A-Z | Community detection over the target-language subgraph | `algo.labelPropagation` (CDLP) |
| "What if I learn these roots first?" | Re-run coverage on a scratch copy of my graph | `GRAPH.COPY` (multigraph) |
| Traps (false friends) | Shared ancestor + similar form + different meaning | Path query + `flex.text.jaroWinkler` / `flex.sim.jaccard` (FLEX UDFs) |
| Memory across sessions | Learner's known/struggled words written back, frontier recomputed | One graph per learner (multigraph), `MERGE` |

**Why it isn't a self-join:** the plan depends on the learner's *whole* known set and changes as they learn. A word they learned yesterday becomes the stepping stone that explains another word today. That is a spanning-tree / frontier problem over a living graph, not a fixed pair table.

---

## 2. Graph layout (FalkorDB multigraph)

One FalkorDB instance, several graph keys:

| Graph key | Contents | Who writes |
|---|---|---|
| `lex` | Full lexicon: all words, ancestors, roots, inflected forms, held-out cognate labels | Loader only (read-only at runtime) |
| `pair:hi-mr`, `pair:hi-bn` | Language-pair template: both languages' words + only the ancestors/roots that connect them, with `effort` weights precomputed | Loader |
| `learner:<id>` | `GRAPH.COPY` of a pair template at onboarding + Learner, KNOWS, STRUGGLED, Session, Plan edges | Quizzer, Planner (write tools) |
| `learner:<id>:whatif` | Scratch copy for what-if, deleted after use | Planner |
| `commons` | Traps and "wrong pair" reports confirmed by a human; shared by all learners (precedents) | Curator, after human approval |

Cross-graph joins are not possible in FalkorDB, so `commons` is checked with a second query (Verifier step), and confirmed traps are merged into pair templates by the loader.

---

## 3. Schema

### Nodes
| Label | Key properties | Notes |
|---|---|---|
| `Word` | `id`, `lang` (hi, mr, bn, sa, pra, fa-cls, ar, en...), `text`, `roman` (common romanisation across scripts), `gloss`, `gloss_terms` (list), `gloss_vec` (embedding), `pos`, `freq` | Ancestor-language words (Sanskrit, Prakrit, Persian...) are `Word` too, with an extra label `:Ancestor` |
| `Root` | `id`, `text` (e.g. Sanskrit √kṛ), `gloss` | From Wiktionary `root` templates (Hindi 1,910 entries, Marathi 827, Bengali 536) |
| `Form` | `text`, `lang`, `tags` | Inflected forms from the Wiktextract `forms` field, so real text can be matched to its base word |
| `Trap` | `id`, `form`, `meaning_a`, `meaning_b`, `status` (candidate / confirmed) | The misconception node (Atrium move): "same word, different meaning" |
| `Learner` | `id`, `languages_known` | Per-learner graph only |
| `Known` | (one per learner graph) | Virtual root: links to every known word with `effort 0`, so one source node stands for "everything I know" |
| `Session`, `QuizItem` | `date`, `result` | Memory |

### Edges
| Type | From -> To | Properties | Source |
|---|---|---|---|
| `INHERITED_FROM` | Word -> Word(:Ancestor) | `effort`, `order` | `inh` templates (ordered chains, hop by hop) |
| `BORROWED_FROM` | Word -> Word | `effort` | `bor` templates |
| `LEARNED_BORROWING_FROM` | Word -> Word | `effort` | `lbor` templates (tatsama words: easiest to recognise) |
| `DERIVED_FROM` | Word -> Word | `effort` | `der` templates |
| `FROM_ROOT` | Word -> Root | `effort` | `root` templates |
| `FORM_OF` | Form -> Word | | `forms` field |
| `COGNATE_LABEL` | Word -> Word | | `cog` templates. **Held out for evaluation; never used for planning** |
| `TRAP_MEMBER` | Word -> Trap | | Verifier / Curator |
| `KNOWS` | Learner -> Word | `strength`, `source` (self / quiz), `due` | Quizzer |
| `ANCHOR` | Known -> Word | `effort: 0` | Rebuilt from KNOWS each session |
| `STRUGGLED` | Learner -> Word | `count` | Quizzer |
| `STUMBLED_ON` | Learner -> Trap | | Quizzer |
| `PLAN` | Word -> Word | `lesson`, `step` | Planner (MSF tree written back) |

### The `effort` weight (deterministic, computed at load)
`effort = type_cost + form_cost + meaning_cost`
- `type_cost`: learned borrowing 0.1, borrowing 0.2, inherited 0.3 per hop, derived 0.4, root 0.5
- `form_cost`: 1 - Jaro-Winkler(roman(a), roman(b)), using one romanisation for all scripts so Devanagari and Bengali script compare fairly (e.g. ISO 15919 via an Indic transliteration library)
- `meaning_cost`: 1 - gloss similarity (embedding cosine, stored at load)

Low effort = "you'll recognise it". This weight drives SPpaths, MSF and the frontier ranking.

---

## 4. Query sketches (to test during the event)

**Q1. Frontier: what I almost know, from everything I know** (the SQL-awkward query: variable depth on both sides, typed edges, meeting at any shared ancestor, many sources)
```cypher
MATCH (l:Learner)-[:KNOWS]->(k:Word)
MATCH p = (k)-[:INHERITED_FROM|BORROWED_FROM|LEARNED_BORROWING_FROM|DERIVED_FROM*1..4]->(a:Ancestor)
          <-[:INHERITED_FROM|BORROWED_FROM|LEARNED_BORROWING_FROM|DERIVED_FROM*1..4]-(t:Word {lang:$target})
WHERE NOT (l)-[:KNOWS]->(t) AND NOT (t)-[:TRAP_MEMBER]->(:Trap)
WITH t, p, reduce(c = 0.0, r IN relationships(p) | c + r.effort) AS cost
ORDER BY cost
WITH t, head(collect(p)) AS best, min(cost) AS cost
RETURN t.text, t.gloss, cost, [n IN nodes(best) | n.text] AS via
ORDER BY cost LIMIT 50
```

**Q2. Explain one word** (alternative explanations, ranked)
```cypher
MATCH (k:Known), (t:Word {text:$word, lang:$target})
CALL algo.SPpaths({sourceNode:k, targetNode:t,
  relTypes:['ANCHOR','INHERITED_FROM','BORROWED_FROM','LEARNED_BORROWING_FROM','DERIVED_FROM','FROM_ROOT'],
  weightProp:'effort', relDirection:'both', maxLen:8, pathCount:3})
YIELD path, pathWeight
RETURN [n IN nodes(path) | n.text] AS via, pathWeight
```

**Q3. No-path proof: rote words**
```cypher
CALL algo.WCC({relationshipTypes:['ANCHOR','INHERITED_FROM','BORROWED_FROM','LEARNED_BORROWING_FROM','DERIVED_FROM','FROM_ROOT']})
YIELD node, componentId
WITH node, componentId
MATCH (k:Known) ...   // component of Known vs target words outside it
```
Output: "No bridge exists in the data from anything you know: learn these by heart." Worded as "no path in Wiktionary data", never "unrelated".

**Q4. Curriculum = minimum spanning forest rooted at what I know**
```cypher
CALL algo.MSF({nodeLabels:['Known','Word','Root'],
  relationshipTypes:['ANCHOR','INHERITED_FROM','BORROWED_FROM','LEARNED_BORROWING_FROM','DERIVED_FROM','FROM_ROOT'],
  weightAttribute:'effort', objective:'minimize'})
YIELD nodes, edges
```
Keep the tree that contains `Known`, write its edges back as `PLAN`, then `algo.bfs(known, 12, 'PLAN')` gives the lesson order. Words learned early become the explainers for later ones. (Honest note: an MSF minimises *total* effort, not each word's own distance; Q2 gives the per-word shortest explanation. Use both and say which is which.)

**Q5. Keystone roots: biggest gain per root**
```cypher
MATCH (r:Root)<-[:FROM_ROOT]-(t:Word {lang:$target}), (l:Learner)
WHERE NOT (l)-[:KNOWS]->(t)
RETURN r.text, r.gloss, count(t) AS unlocks ORDER BY unlocks DESC LIMIT 10
```
Plus `algo.betweenness` on Root/Ancestor nodes to find bridge roots that connect several word families.

**Q6. Lessons by word family**
```cypher
CALL algo.labelPropagation({nodeLabels:['Word','Root','Ancestor'],
  relationshipTypes:['INHERITED_FROM','BORROWED_FROM','LEARNED_BORROWING_FROM','DERIVED_FROM','FROM_ROOT']})
YIELD node, communityId
WITH communityId, collect(node) AS fam
RETURN communityId, [n IN fam WHERE n.lang = $target | n.text] AS lesson
```

**Q7. Trap finder** (form close, meaning far, same ancestor)
```cypher
MATCH (a:Word {lang:$src})-[:INHERITED_FROM|BORROWED_FROM|LEARNED_BORROWING_FROM*1..3]->(x:Ancestor)
      <-[:INHERITED_FROM|BORROWED_FROM|LEARNED_BORROWING_FROM*1..3]-(b:Word {lang:$target})
WHERE flex.text.jaroWinkler(a.roman, b.roman) > 0.85
  AND flex.sim.jaccard(a.gloss_terms, b.gloss_terms) < 0.1
RETURN a.text, a.gloss, b.text, b.gloss, x.text AS shared_ancestor
```
Candidates go to a human review queue; confirmed ones become `Trap` nodes in `commons`.

**Q8. What-if**
`GRAPH.COPY learner:42 learner:42:whatif` -> add KNOWS for the chosen roots' easiest words -> re-run Q1/Q3 counts -> report "+N words, coverage 41% -> 58%" -> `GRAPH.DELETE` the copy.

**Q9. Reading mode** (the hook): split a Marathi paragraph into tokens -> `MATCH (f:Form {text:$tok})-[:FORM_OF]->(w)` or a direct Word match -> label each token **bridged / trap / rote / known** using Q1-Q3 -> "learn these 5 roots to understand 90% of this paragraph" (Q5 restricted to the paragraph's words).

**Q10. Memory write-back**
```cypher
MATCH (l:Learner {id:$lid}), (w:Word {id:$wid})
MERGE (l)-[k:KNOWS]->(w)
SET k.strength = coalesce(k.strength,0) + $delta, k.source = 'quiz', k.due = $due
```

**Q11. Evaluation** (held-out labels): precision/recall of Q1 bridges against `COGNATE_LABEL` edges (stress test baseline: 62-64% recall).

**Fuzzy input:** full-text index on `Word.roman` so a learner can type "shiksha" and find शिक्षा; vector index on `gloss_vec` so "where is the word for *school*?" finds the target word by meaning.

---

## 5. Agents and MCP tools

| Agent | Job | Tools |
|---|---|---|
| **Reader** | Labels a pasted paragraph, explains words on request | `read_paragraph`, `explain_word` (Q2), `lookup` (full-text / vector) |
| **Planner** | Keystones, curriculum, what-if | `frontier` (Q1), `keystone_roots` (Q5), `curriculum` (Q4), `what_if` (Q8), `rote_words` (Q3), `lessons` (Q6) |
| **Quizzer** | Tests the learner and writes results | `make_quiz`, `record_result` (Q10, write) |
| **Verifier** (deterministic, no LLM) | Before anything is shown: the path must exist (re-run Q2), meaning similarity above the threshold, not a confirmed trap in `commons`. Overrides the LLM | `verify_bridge` |
| **Curator** | Proposes trap candidates (Q7); writes to `commons` only after human approval | `trap_candidates`, `confirm_trap` (write, gated) |

- All read tools run through **`GRAPH.RO_QUERY`**, so the LLM physically cannot write with them (the "model gets read-only Cypher" pattern judges liked). Write tools are separate, fixed queries with parameters.
- Built on FalkorDB's MCP server, or a thin MCP server of our own exposing the fixed queries above.

---

## 6. Brief and track fit (Part H)

- **Acts:** paragraph labelling, daily plan, Anki deck export, trap warnings; human approval before a deck is exported or a trap is confirmed.
- **Remembers:** KNOWS/STRUGGLED/STUMBLED_ON per learner; confirmed traps in `commons` help every later learner; the frontier and plan change each session.
- **Shows the path:** every word comes with its chain, e.g. हिन्दी शिक्षा -> Sanskrit शिक्षा <- मराठी शिक्षा ("punishment": trap).
- **Agents share state:** Reader, Planner, Quizzer read and write the same learner graph; Verifier and Curator guard it.
- **Tracks:** 1 (primary: algorithms as tools, multi-hop, MCP, actions, explanations) + 2 (per-learner memory, shared state, one graph per user).

---

## 7. Demo story (90 seconds)

1. Priya speaks Hindi and has just moved to Pune. She pastes a Marathi news paragraph.
2. The paragraph lights up: 60-70% green (bridged), each with a hover path through Sanskrit, Prakrit or Persian; a few red (rote).
3. One word glows amber: शिक्षा. "In Hindi it's *education*. In Marathi it's *punishment*." The trap node and its two meanings appear.
4. Planner: "Learn these 5 roots and you'll understand 90% of this paragraph." What-if: coverage jumps on a scratch copy of her graph.
5. Curriculum tree (MSF) grows from her known words; lesson 1 is a word family found by community detection.
6. Quiz, two misses, written back. Next day, the agent picks up exactly where she struggled.
7. Closing line: "Same root, different language. Same word, different meaning. Both are paths in a graph."

---

## 8. Day-1 checks during the event (first hours)

1. Every query above runs on FalkorDB as written (openCypher subset; var-length patterns with typed alternatives; `reduce`; FLEX function names `flex.text.jaroWinkler`, `flex.sim.jaccard`).
2. Direction behaviour of SPpaths / MSF / WCC / betweenness on a 10-node toy graph (MSF and WCC ignore direction per docs; SPpaths takes `relDirection`).
3. `algo.pageRank` is unweighted and takes one label + one relationship type: do not rely on it for root ranking; use Q5 + betweenness.
4. `GRAPH.COPY` time for a pair graph (~60-80k nodes): must be well under a second for the what-if to feel live.
5. Romanisation across Devanagari and Bengali scripts gives sensible Jaro-Winkler scores (spot-check 20 pairs).
6. Hand-check 100 random bridges for precision (ask a Marathi and a Bengali speaker).
