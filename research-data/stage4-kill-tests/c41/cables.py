import json,urllib.request,concurrent.futures as cf,time,networkx as nx
from collections import defaultdict
ids=[c['id'] for c in json.load(open('all.json'))]
def get(i):
    for k in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(f'https://www.submarinecablemap.com/api/v3/cable/{i}.json',headers={'User-Agent':'graphhack-research'}),timeout=20))
        except Exception: time.sleep(1)
    return None
with cf.ThreadPoolExecutor(12) as ex: cabs=[c for c in ex.map(get,ids) if c]
json.dump(cabs,open('cables_full.json','w'))
print('cables fetched',len(cabs),'of',len(ids))
# keep cables in service (rfs year <= 2026) if the field exists
def inservice(c):
    y=c.get('rfs_year') or c.get('rfs')
    try: return int(str(y)[:4])<=2026
    except: return True
cabs=[c for c in cabs if inservice(c)]
G=nx.Graph()
country_lp=defaultdict(set); country_cab=defaultdict(set)
for c in cabs:
    lps=[lp for lp in c.get('landing_points',[]) if lp.get('country')]
    if len({lp['country'] for lp in lps})<2: continue   # domestic-only cables don't give international links
    for lp in lps:
        G.add_edge(('cable',c['id']),('lp',lp['id'])); G.add_edge(('lp',lp['id']),('country',lp['country']))
        country_lp[lp['country']].add(lp['id']); country_cab[lp['country']].add(c['id'])
countries=sorted(country_cab)
print('in-service international cables used:',len({n for n in G if n[0]=='cable'}),'| countries:',len(countries),'| landing points:',len({n for n in G if n[0]=='lp'}))
res=[]
for ct in countries:
    # node-capacity graph: cables and landing points capacity 1; country nodes infinite; sink = all OTHER countries
    H=nx.DiGraph()
    for u,v in G.edges:
        for a,b in ((u,v),(v,u)):
            H.add_edge(('out',a),('in',b),capacity=10**9)
    for n in G.nodes:
        cap=10**9 if n[0]=='country' else 1
        H.add_edge(('in',n),('out',n),capacity=cap)
    for other in countries:
        if other!=ct: H.add_edge(('out',('country',other)),'WORLD',capacity=10**9)
    # remove passing THROUGH other countries? allowed (traffic transits other countries' stations) -> keep
    f,_=nx.maximum_flow(H,('out',('country',ct)),'WORLD')
    res.append((ct,len(country_cab[ct]),len(country_lp[ct]),int(f)))
naive1=[r for r in res if r[1]==1]
hidden=[r for r in res if r[1]>=2 and r[3]==1]
lower=[r for r in res if r[3]<r[1]]
print(f'countries with exactly 1 international cable (obvious SPOF): {len(naive1)}')
print(f'countries with >=2 cables but min cut = 1 (HIDDEN single point of failure): {len(hidden)}')
for r in sorted(hidden,key=lambda r:-r[1])[:25]: print('   ',r)
print(f'countries where min cut < cable count (any hidden concentration): {len(lower)}')
for r in sorted(lower,key=lambda r:(r[3]-r[1]))[:15]: print('   ',r)
json.dump(res,open('c41_res.json','w'))
