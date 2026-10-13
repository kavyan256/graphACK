import csv
from collections import defaultdict,Counter
ap={}
for r in csv.reader(open('airports.dat',encoding='utf-8')):
    if len(r)>5 and r[4] and r[4]!='\\N': ap[r[4]]=r[3]   # IATA -> country
routes=set()
for r in csv.reader(open('routes.dat',encoding='utf-8')):
    if len(r)>7 and r[7]=='0' and r[2] in ap and r[4] in ap: routes.add((r[2],r[4]))   # nonstop only
out=defaultdict(set)
for a,b in routes: out[a].add(b)
IN=[a for a,c in ap.items() if c=='India' and a in out]
region={}
NA={'United States','Canada','Mexico'}
EU_SCHENGEN={'Germany','France','Spain','Netherlands','Italy','Switzerland','Belgium','Austria','Portugal','Greece','Sweden','Norway','Denmark','Finland','Poland','Czech Republic','Hungary','Ireland','United Kingdom'}
OCE={'Australia','New Zealand'}
def rule(hub_country,dest_country):
    """returns 'trap' if an Indian holding only a visa for the destination needs a visa to transit airside"""
    if hub_country=='United States': return 'trap'
    if hub_country=='Canada': return 'ok' if dest_country=='United States' else 'trap'
    if hub_country=='United Kingdom': return 'ok' if dest_country in ('United States','Canada','Australia','New Zealand') else 'trap'
    if hub_country=='Australia': return 'trap'
    if hub_country=='New Zealand': return 'ok' if dest_country=='Australia' else 'trap'
    if hub_country=='Mexico': return 'ok' if dest_country in ('United States','Canada','United Kingdom') or dest_country in EU_SCHENGEN else 'trap'
    if hub_country=='Kenya': return 'pre-auth'
    return 'ok'
def reg(c):
    if c in ('United States','Canada'): return 'US/Canada'
    if c in OCE: return 'Australia/NZ'
    if c in EU_SCHENGEN: return 'Europe'
    if c in ('Mexico','Brazil','Argentina','Chile','Peru','Colombia','Ecuador','Venezuela','Cuba','Jamaica','Trinidad and Tobago','Panama','Costa Rica','Dominican Republic','Guatemala','Bolivia','Uruguay','Paraguay'): return 'Latin America/Caribbean'
    return None
itins=[]
for o in IN:
    for h in out[o]:
        hc=ap[h]
        if hc=='India': continue
        for d in out.get(h,()):
            dc=ap[d]
            if d==o or dc=='India' or hc==dc or d in out[o]: continue   # skip if a direct flight exists
            R=reg(dc)
            if not R: continue
            itins.append((o,h,d,hc,dc,R,rule(hc,dc)))
print('Indian origin airports with routes:',len(IN),'| 1-stop itineraries to target regions (no direct):',len(itins))
by=defaultdict(Counter)
for it in itins: by[it[5]][it[6]]+=1; by['ALL'][it[6]]+=1
for R,c in by.items():
    n=sum(c.values()); print(f'  {R:26} n={n:6}  trap={c["trap"]:5} ({100*c["trap"]/n:.0f}%)  pre-auth={c["pre-auth"]} ok={c["ok"]}')
# destination-level: share of destinations where >=1 offered 1-stop option is a trap, and share where ALL options are traps
dest=defaultdict(Counter)
for it in itins: dest[(it[0],it[2])][it[6]]+=1
pairs=len(dest); anytrap=sum(1 for c in dest.values() if c['trap']); alltrap=sum(1 for c in dest.values() if c['trap'] and not c['ok'])
print(f'  origin-destination pairs: {pairs}; with at least one trap option: {anytrap} ({100*anytrap/pairs:.0f}%); where every 1-stop option is a trap: {alltrap} ({100*alltrap/pairs:.0f}%)')
hubs=Counter(it[3] for it in itins if it[6]=='trap'); print('  trap hubs by country:',hubs.most_common(6))
