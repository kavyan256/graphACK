# Stage 6 design: C01 Transit-visa route guard

Working name: **LayoverGuard**. Pre-event **sketch only**; all queries are sketches to be written and tested during the event.

**One line:** *Before you book, check every layover is legal for your passport and the visas you hold, see why, and see which visa would unlock better routes.*

**Users:** travellers on non-visa-free passports (Indian passports as the lead case: 32.7M departures in 2025, ~17M connect via foreign hubs), travel agents, student-visa holders.

---

## 1. Inputs from earlier stages
| Finding | Source |
|---|---|
| 24% of Indian origin-destination pairs have a trap option among 1-stop routes; 10% of itineraries; Latin America 30%, Europe 11%, US/Canada 5% | `kill-tests.md` |
| Rules change often (Spain, France, Germany dropped airport transit visas for Indians Mar-Jun 2026) | `inventory-pain.md` |
| Denied-boarding cases depend on the **shape of the trip**: two Schengen stops (Bengaluru, Paris + Amsterdam), separate tickets (Singapore self-transfer), diversions (Kuwait) | `user-evidence.md` |
| Route data: OpenFlights (ODbL) 7,698 airports / 67,663 routes, last broad update 2014; the weekly route file has no licence | `kill-tests.md` |

## 2. Graph model
| Node | Properties |
|---|---|
| `Airport` | IATA, country, lat/lon, `schengen` flag |
| `Country` | ISO code, Schengen member? |
| `Rule` | **the hidden reasoning unit (M1)**: e.g. "UK DATV for Indian nationals", valid_from / valid_to, source URL, airside vs landside |
| `Exemption` | e.g. "holds valid US/Canada/Australia/NZ visa", "holds residence permit X" |
| `Passport`, `Visa` | nationality; visa type + country |
| `Traveller` (per-user graph) | passports, visas held, past trips |
| `Trip` (precedent, M3) | a checked or reported itinerary + outcome (e.g. a documented denied boarding) |

| Edge | Meaning |
|---|---|
| `ROUTE` (Airport -> Airport) | airline, distance (OpenFlights) |
| `IN` (Airport -> Country) | |
| `REQUIRES` (Country -> Rule) / `APPLIES_TO` (Rule -> Passport) | rule scope, with dates and source (M2) |
| `UNLESS` (Rule -> Exemption) / `SATISFIED_BY` (Exemption -> Visa) | conditional edges |
| `HOLDS` (Traveller -> Visa / Passport) | |

## 3. Questions and FalkorDB features
| # | Question | Feature (sketch) |
|---|---|---|
| Q1 | Which routes from A to B (up to 2-3 stops) are legal for *this* traveller? | **Per-traveller graph via `GRAPH.COPY`**, then remove transit airports whose rules aren't satisfied by the traveller's visas; `algo.SSpaths` / `algo.SPpaths` (maxLen, pathCount) on the cleaned copy |
| Q2 | Prove there is no legal route | BFS on the cleaned copy reaches nothing -> "no legal route within 3 stops" (M4) |
| Q3 | Why is this itinerary a trap? | Explanation path: hub -> Rule -> missing Exemption -> what would satisfy it (M5) |
| Q4 | Trip-shape traps (two Schengen stops, separate tickets, airport change) | Cypher pattern over the path: count Schengen airports on the route; self-transfer flag forces the landside rule |
| Q5 | What-if: which visa would unlock the most routes? / what did a rule change unlock? | Graph copies with an added visa or a rule's valid_to date; diff the reachable sets; `algo.betweenness` to rank hubs that matter most for this traveller |

## 4. Agents and memory
- **Planner** (route options), **Rule-Checker** (deterministic, overrides the LLM: every "legal" verdict must cite the rules and exemptions used), **Explainer** (why/why not), **Watcher** (memory: when a rule affecting a saved trip changes, notify).
- Memory: traveller profile and saved trips; rule versions with dates; documented denied-boarding precedents shown when a trip matches their pattern.

## 5. Evaluation plan
1. **Documented cases:** the Bengaluru Paris + Amsterdam case, the Singapore self-transfer case, the Kuwait diversion: does the checker flag each one? (Expected yes by construction: they define the patterns.)
2. **Rule accuracy:** spot-check curated rules against official pages (UK, US, Canada, Schengen states, Australia, NZ, Mexico).
3. **Trap rate:** 24% of pairs / 10% of itineraries (measured).

## 6. Demo storyboard (90 seconds)
1. Priya (Indian passport, Canadian student visa) searches Delhi -> Toronto.
2. Options light up: via London **OK** (her Canadian visa exempts her from the UK DATV, rule shown); via New York **trap** (US has no airside transit); via Frankfurt **OK since June 3 2026** (rule history shown); via Paris + Amsterdam **trap** (two Schengen stops).
3. What-if: "if you get a US visa, 12 more routes open."
4. Memory: a rule change notification for a saved trip.

## 7. Red team
| Attack | Best answer | Still open? |
|---|---|---|
| "1-2 stop route search is a SQL join." | Per-traveller graph copies, conditional exemption edges and trip-shape patterns go beyond a join | **Mostly true for the core**: weak J4 |
| "Timatic / visa checkers / Layovered already do this." | Checkers verify one itinerary; Layovered routes without proof; we add proof, explanation, what-if | Prior art is close |
| "Your routes are from 2014." | Only open-licensed source; could use a synthetic network for the demo | **Serious**: judges may try real routes |
| "Wrong advice strands people." | Disclaimers; "verify with your airline"; show sources and dates | Liability framing needed |
| "Who maintains the rules?" | Hand-curated from official pages for ~10 key hubs | Doesn't scale beyond a demo |
| "Can one person build it?" | Yes: small data, simple model | Low build risk |

## 8. Provisional scores (win-spec J1-J6)
| J1 | J2 | J3 | J4 | J5 | J6 | Total | Build risk |
|---|---|---|---|---|---|---|---|
| 5 | 3 | 3 | 3 | 4 | 5 | **23/30** | 2 (low) |

## Sources
- OpenFlights: https://openflights.org/data.php
- Transit rules: https://in.diplomatie.gouv.fr/en/france-lifts-airport-transit-visa-requirements-indian-nationals ; https://india.diplo.de/in-en/2752166-2752166 ; https://www.davidsonmorris.com/transit-visa-uk/
- Cases: https://www.indianeagle.com/travelbeats/paris-amsterdam-transit-schengen-visa/ ; https://gulfnews.com/world/asia/india/indian-passengers-stranded-at-kuwait-airport-for-13-hours-after-flight-diversion-1.1733078523982
- Scale: https://www.hotelierindia.com/operations/india-outbound-travel-2025
