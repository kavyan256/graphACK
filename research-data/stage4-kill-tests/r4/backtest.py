import csv,json,random,urllib.request,urllib.parse,time,sys
from datetime import datetime
B='https://api.openalex.org/'; calls=0
def get(path,params):
    global calls
    u=B+path+'?'+urllib.parse.urlencode(params)
    for k in range(3):
        try:
            calls+=1; return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'graphhack-research'}),timeout=60))
        except urllib.error.HTTPError as e:
            print('HTTP',e.code,u[:120],file=sys.stderr)
            if e.code in (402,429): return None
            time.sleep(2)
        except Exception: time.sleep(2)
    return None
short=lambda x:(x or '').rsplit('/',1)[-1]
def d(s):
    try: return datetime.strptime(s.split()[0],'%m/%d/%Y')
    except: return None
rows=list(csv.DictReader(open('rw.csv',encoding='utf-8',errors='ignore')))
pm=[r for r in rows if 'Paper Mill' in (r.get('Reason') or '') and (r.get('RetractionNature') or '').strip()=='Retraction' and (r.get('OriginalPaperDOI') or '').startswith('10.')]
seeds_all=[r for r in pm if d(r['RetractionDate']) and d(r['RetractionDate'])<=datetime(2023,6,30)]
T={r['OriginalPaperDOI'].lower().strip() for r in pm if d(r['RetractionDate']) and d(r['RetractionDate'])>=datetime(2024,1,1)}
ANY_RET={r['OriginalPaperDOI'].lower().strip() for r in rows if (r.get('OriginalPaperDOI') or '').startswith('10.')}
print('seed pool',len(seeds_all),'| targets (paper-mill retractions from 2024)',len(T),file=sys.stderr)
random.seed(42); seeds=random.sample(seeds_all,160)
seed_dois={r['OriginalPaperDOI'].lower() for r in seeds}
A1=set(); matched=0
L=sorted(seed_dois)
for i in range(0,len(L),40):
    r=get('works',{'filter':'doi:'+'|'.join(L[i:i+40]),'select':'doi,authorships','per-page':50})
    for w in (r or {}).get('results',[]):
        matched+=1
        for a in w['authorships']:
            aid=short((a.get('author') or {}).get('id'))
            if aid: A1.add(aid)
print('seed papers matched in OpenAlex',matched,'of',len(L),'| seed authors',len(A1),file=sys.stderr)
def works_of(authors,cap_pages=2):
    W={}  # doi -> set(authors)
    L=sorted(authors)
    for i in range(0,len(L),20):
        for page in range(1,cap_pages+1):
            r=get('works',{'filter':f'author.id:{"|".join(L[i:i+20])},from_publication_date:2015-01-01','select':'doi,authorships','per-page':200,'page':page})
            if not r: break
            for w in r['results']:
                if not w.get('doi'): continue
                doi=w['doi'].lower().replace('https://doi.org/','')
                W[doi]={short((a.get('author') or {}).get('id')) for a in w['authorships']}
            if len(r['results'])<200: break
    return W
W1=works_of(A1)
W1={k:v for k,v in W1.items() if k not in seed_dois}
hit1={k for k in W1 if k in T}
A2=set().union(*W1.values())-A1 if W1 else set()
random.seed(7); A2s=set(random.sample(sorted(A2),min(400,len(A2))))
W2=works_of(A2s)
W2={k:v for k,v in W2.items() if k not in seed_dois and k not in W1}
hit2={k for k in W2 if k in T}
# base rate: targets / all works 2015-2023 (OpenAlex count), and among health+life sciences
tot=get('works',{'filter':'from_publication_date:2015-01-01,to_publication_date:2023-12-31','per-page':1})['meta']['count']
tot_bio=get('works',{'filter':'from_publication_date:2015-01-01,to_publication_date:2023-12-31,primary_topic.domain.id:1|4','per-page':1})['meta']['count']
base=len(T)/tot; base_bio=len(T)/tot_bio
r1=len(hit1)/max(1,len(W1)); r2=len(hit2)/max(1,len(W2))
print(f'1-hop: seed authors other works {len(W1)}, later paper-mill retractions {len(hit1)} = {100*r1:.2f}%')
print(f'2-hop: co-author sample {len(A2s)} of {len(A2)}, works {len(W2)}, later paper-mill retractions {len(hit2)} = {100*r2:.2f}%')
print(f'base rate: {len(T)} targets / {tot:,} works 2015-2023 = {100*base:.4f}% | health+life sciences only: {100*base_bio:.4f}%')
print(f'enrichment 1-hop: {r1/base:.0f}x (vs bio {r1/base_bio:.0f}x) | 2-hop: {r2/base:.0f}x (vs bio {r2/base_bio:.0f}x)')
scale=len(A2)/max(1,len(A2s))
print(f'added reach: 2-hop hits in sample {len(hit2)} -> est. {len(hit2)*scale:.0f} across all co-authors, vs {len(hit1)} via 1-hop')
print('API calls',calls)
json.dump({'W1':len(W1),'hit1':sorted(hit1),'W2':len(W2),'hit2':sorted(hit2),'A1':len(A1),'A2':len(A2),'tot':tot,'tot_bio':tot_bio,'T':len(T)},open('r4.json','w'),indent=1)
