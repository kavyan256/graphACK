import json,urllib.request,urllib.parse,time,sys
from collections import Counter
B='https://api.openalex.org/'
calls=0
def get(path,params):
    global calls
    u=B+path+'?'+urllib.parse.urlencode(params)
    for k in range(3):
        try:
            calls+=1
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'graphhack-research'}),timeout=40))
        except urllib.error.HTTPError as e:
            print('HTTP',e.code,u[:120],file=sys.stderr); time.sleep(2)
            if e.code in (402,429): return None
        except Exception as e: time.sleep(2)
    return None
def short(x): return x.rsplit('/',1)[-1]
def works_of(author_ids, since=2016):
    """co-author sets for a group of authors (OR filter, up to ~40 ids), one or two pages"""
    co={a:set() for a in author_ids}
    ids='|'.join(author_ids)
    for page in (1,2):
        d=get('works',{'filter':f'author.id:{ids},from_publication_date:{since}-01-01','select':'authorships','per-page':200,'page':page})
        if not d: break
        for w in d['results']:
            au=[short(a['author']['id']) for a in w['authorships'] if a.get('author',{}).get('id')]
            for a in au:
                if a in co: co[a].update(x for x in au if x!=a)
        if len(d['results'])<200: break
    return co
# sample papers: recent, multi-author, in three fields
papers=[]
for q in ('graph neural network drug discovery','retrieval augmented generation evaluation','solar cell perovskite stability'):
    d=get('works',{'search':q,'filter':'from_publication_date:2024-01-01,type:article','select':'id,title,authorships,related_works','per-page':5,'sort':'cited_by_count:desc'})
    papers+= (d or {}).get('results',[])
print('papers',len(papers),file=sys.stderr)
rows=[]
for p in papers:
    A=[short(a['author']['id']) for a in p['authorships'] if a.get('author',{}).get('id')][:10]
    rel=[short(x) for x in p.get('related_works',[])][:40]
    if not A or not rel: continue
    d=get('works',{'filter':'openalex_id:'+'|'.join(rel),'select':'authorships','per-page':50})
    cand=Counter()
    for w in (d or {}).get('results',[]):
        for a in w['authorships']:
            aid=a.get('author',{}).get('id')
            if aid and short(aid) not in A: cand[short(aid)]+=1
    C=[c for c,_ in cand.most_common(30)]
    if not C: continue
    coA=works_of(A)
    one=set().union(*coA.values())
    coC={}
    for i in range(0,len(C),15): coC.update(works_of(C[i:i+15]))
    d1=[c for c in C if c in one]
    d2=[c for c in C if c not in one and (coC.get(c,set()) & (one|set(A)))]
    rows.append({'title':p['title'][:70],'authors':len(A),'candidates':len(C),'dist1':len(d1),'dist2':len(d2)})
    print(rows[-1],file=sys.stderr)
tot=sum(r['candidates'] for r in rows); c1=sum(r['dist1'] for r in rows); c2=sum(r['dist2'] for r in rows)
print(f'papers measured: {len(rows)} | candidates: {tot} | within 1 hop (co-authored with an author): {c1} ({100*c1/max(1,tot):.1f}%) | within 2 hops: {c1+c2} ({100*(c1+c2)/max(1,tot):.1f}%) | API calls: {calls}')
json.dump(rows,open('c24.json','w'),indent=1)
