# Stage 5: public evidence of real use (Oct 5 2026)

Internet only (no interviews). For each finalist: real past cases, what people use today (workarounds and their gaps), scale, and a "10-second test" of the pitch against the judges' own wording. Evidence strength: **Strong / Medium / Weak**.

Finalists from Stage 4 + round 2: **R1** independent expert finder, **C24** independent reviewer finder, **C01** transit-visa route guard.

---

## R1: Independent expert finder (journalists, fact-checkers) — evidence: **Strong**

**Real past cases**
1. **Fake experts in the press.** Press Gazette found **1,000 UK press articles attributed to 50 fake, non-existent or AI-enhanced experts**; in a 2025 sample of 250 expert-quoting articles (Sun, Express, Mirror, Mail, Star), **24 experts did not exist or could not be verified**. Outlets duped included the BBC, Newsweek and Fortune. Many fake experts came through journalist source-request services.
2. **Industry response.** The UK's two PR trade bodies (CIPR, PRCA) launched a campaign urging journalists to check sources; **Qwoted banned AI-generated expert profiles**.
3. **"Independent" experts who aren't.** A New Zealand study of news coverage of medical studies: only 1 in 6 stories quoted independent commenters, and among those **54% had academic and 32% financial conflicts of interest, mostly undisclosed**.
4. **Industry-funded expert networks.** Coca-Cola funded the Global Energy Balance Network (New York Times, 2015): $1.5M to start it and almost $4M to two founders; the network's website was registered to Coca-Cola, and the funding wasn't acknowledged until challenged. The network shut down within months.
5. **Undisclosed ties in research itself.** Reports of undisclosed financial conflicts among physician-authors in leading US psychiatry journals, and of medical journal editors' conflicts being largely undisclosed (Public Citizen; KFF Health News).

**What journalists use today**
| Workaround | Gap |
|---|---|
| SciLine (AAAS), Science Media Centre | Human matchmaking; doesn't show *how* an expert is connected to the company in the story |
| HealthNewsReview's list of ~100 experts without industry ties | Static, small, health only |
| ProPublica Dollars for Docs/Profs, US Open Payments | Money paid to US doctors/professors only; no co-authorship or affiliation ties; nothing outside the US |
| ExpertFile, Qwoted, other source-request platforms | Self-submitted profiles; this is where fake experts came in |
| Reading paper disclosure sections by hand | Slow; disclosures are often missing (cases 3 and 5) |

**Scale.** Every outlet that quotes experts; fact-checking organisations worldwide (the IFCN network has roughly 170+ signatories, B). Measured in Stage 4: in four real company/topic cases, **69% of top experts are within two co-author hops of the company's researchers**, but only 16% are directly tied, so manual checks miss most ties.

**10-second test.** *"Before you quote an expert, see how close they are to the company in your story, with every tie shown as a path."* Matches the judges' own words: "miss how people, systems, and records relate", "connect people, projects, and decisions", "show the path behind an answer". A non-expert gets it immediately. **Pass.**

**Extra angle the evidence suggests:** the same graph can also answer "does this expert exist in the research record at all?" (an ORCID profile and publications), which addresses the fake-expert problem. Absence from the record is not proof of fakery (many practitioners don't publish), so this must be worded as "no research record found", for a human to judge.

---

## C24: Independent reviewer finder (editors, programme chairs) — evidence: **Strong pain, but strong commercial prior art**

**Real past cases / scale**
1. **Compromised peer review is huge.** In the Retraction Watch database (via Crossref), **21,713 retractions (32% of all retractions) cite compromised peer review or peer-review concerns**: 10,417 in 2023, 3,675 in 2024, 2,485 in 2025. Hindawi alone accounts for 11,081.
2. **Editors struggle to find reviewers.** In 2025 one journal reported **58% of review requests ignored and 29% declined (86% no positive response)**; another had to double invitations per acceptance over a decade.
3. **Mismatched requests.** In one survey, 32.5% of reviewers reported being asked to review outside their expertise.

**What editors use today**
| Workaround | Gap |
|---|---|
| **Prophy Referee Finder** (commercial): conflict-free reviewer matching over 102M+ researcher profiles, flags co-authorship and co-affiliation conflicts; used by 70+ funders and publishers (DFG, NWO, Oxford University Press, EMBO) | Already does the core job for big customers; paid |
| Semantic Scholar peer-review API (partners), OpenReview conflict detection, publisher reviewer finders, JANE (free, no conflict check) | Direct conflicts only; mostly closed or partner-only |

**10-second test.** *"Find reviewers who know the topic but aren't connected to the authors, with the proof."* Clear to academics; judges may see it as niche, and **Prophy is a close commercial match**. **Weak pass.**

**Implication.** C24 works best as a **second use case of R1's engine** (same graph, same queries), not as the lead pitch.

---

## C01: Transit-visa route guard (travellers, especially Indian passports) — evidence: **Strong**

**Real past cases**
1. Mumbai-Manchester passengers diverted to Kuwait were **stranded because they lacked transit visas**, while UK and US passport holders could leave.
2. **Four Indian travellers denied boarding at Bengaluru** by Air France: their US itinerary went via Paris and Amsterdam (two Schengen stops), which breaks airside-transit rules.
3. An Indian couple **denied boarding by IndiGo** for a Singapore -> Bali trip on separate tickets: changing planes on a self-transfer at Changi needs a visa.
4. An elderly Indian couple sent back halfway to the USA over a visa issue (later won against the airline).
5. Reddit and Stack Exchange cases from Stage 1: "Booked India-Canada-Austin flight without knowing i need a transit visa. Stuck"; "Do I need a US visa to transit...?" (329K views).

**What travellers use today**
| Workaround | Gap |
|---|---|
| IATA Timatic (via airline sites) | Checks one itinerary; doesn't suggest a legal alternative |
| Visa checkers (MyTravelReady, Voyasee, Terrana) | Per itinerary; no route search, no what-if |
| Layovered app | Routes via visa-accessible layover countries (closest prior art); no proof or explanation shown |
| Travel agents, forums | Manual, inconsistent |

**Scale.** Indian nationals made **32.7M international departures in 2025**; about 20M long-haul travellers a year connect, and ~85% (~17M) change planes at foreign hubs. Rules keep changing (Spain, France, Germany dropped transit visas for Indians in Mar-Jun 2026).

**10-second test.** *"Before you book, check every layover is legal for your passport, and see which visa would unlock better routes."* Instantly clear. **Pass.**

**What the cases add to the graph argument.** The traps depend on the *shape of the trip*, not just the hub: two Schengen stops, separate tickets (self-transfer means going landside), a terminal change. Checking a rule that depends on the whole path (state carried hop to hop) is more graph-like than the simple join that worried us in Stage 4. Still, stale open route data (OpenFlights, 2014) remains the weakest point.

---

## Summary

| Finalist | Pain evidence | Workaround gap | 10-second test | Main risk |
|---|---|---|---|---|
| **R1** Independent expert finder | Strong (fake experts, undisclosed ties, industry-funded networks) | Large: nothing automated shows *how* an expert is tied | Pass, matches the judges' wording | Accusation risk: ties are evidence, not guilt; author-profile quality |
| **C24** Independent reviewer finder | Strong (21,713 peer-review retractions) | Small: Prophy does the core job commercially | Weak pass | Prior art |
| **C01** Transit-visa route guard | Strong (17M connecting travellers, denied-boarding cases) | Medium: checkers verify one itinerary; Layovered routes without proof | Pass | Stale route data; graph role must come from path-dependent rules |

**Going into Stage 6:** lead candidate **R1, with C24 as a second "front door" on the same engine**; **C01** as the alternative from a different domain.

## Sources
- Fake experts: https://pressgazette.co.uk/news/faces-of-fakery-more-fake-and-ai-generated-experts-con-their-way-into-media/ ; https://pressgazette.co.uk/news/pr-bodies-launch-campaign-against-fake-experts-after-press-gazette-investigation/ ; https://cybernews.com/ai-news/fake-ai-experts-media-journalism-investigation/ ; https://mediacopilot.ai/fake-ai-experts-major-newsrooms/
- Independent commenters' conflicts: https://www.sciencedaily.com/releases/2016/12/161219134513.htm ; https://kffhealthnews.org/health-industry/financial-ties-that-bind-studies-often-fall-short-on-conflict-of-interest-disclosures/ ; https://www.citizen.org/news/medical-journal-editors-conflicts-of-interest-largely-undisclosed/ ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12612769/
- Coca-Cola GEBN: https://en.wikipedia.org/wiki/Global_Energy_Balance_Network ; https://www.npr.org/2015/08/10/431343137/coca-cola-funds-scientists-who-downplay-diets-role-in-obesity
- Journalist workarounds: https://www.theopennotebook.com/2021/11/02/dont-get-conflicted-what-to-do-when-your-source-has-a-coi/ ; https://healthjournalism.org/blog/2016/03/check-out-your-sources-for-conflicts-of-interest ; https://www.journaliststoolbox.org/2023/05/03/expert_sources/
- Peer review: Retraction Watch data via Crossref (https://gitlab.com/crossref/retraction-watch-data), our own count; https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11808811/ ; https://cyberpsychology.eu/announcement/view/4006 ; Prophy: https://www.prophy.ai/referee-finder/
- Transit visas: https://www.indianeagle.com/travelbeats/paris-amsterdam-transit-schengen-visa/ ; https://www.indianeagle.com/travelbeats/indian-passengers-denied-boarding-for-us-visa-issues ; https://gulfnews.com/world/asia/india/indian-passengers-stranded-at-kuwait-airport-for-13-hours-after-flight-diversion-1.1733078523982 ; Indian outbound numbers: https://www.hotelierindia.com/operations/india-outbound-travel-2025 ; https://www.airindia.com/in/en/newsroom/press-release/air-india-launches-easy-connect-flights-bringing-the-world-closer-to-every-indian-.html
