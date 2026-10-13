import json,urllib.request,urllib.parse,time,sys
from collections import defaultdict,Counter
B='https://api.openalex.org/'; calls=0
def get(path,params):
    global calls
    u=B+path+'?'+urllib.parse.urlencode(params)
    for k in range(3):
        try:
            calls+=1; return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'graphhack-research'}),timeout=60))
        except urllib.error.HTTPError as e:
            print('HTTP',e.code,file=sys.stderr)
            if e.code in (402,429): return None
            time.sleep(2)
        except Exception: time.sleep(2)
    return None
short=lambda x:(x or '').rsplit('/',1)[-1]
MEGA=50
cases=[('Pfizer','mRNA vaccine'),('Bayer','glyphosate'),('Google','large language model')]
summary=[]
for comp,topic in cases:
    i=get('institutions',{'search':comp,'filter':'type:company','select':'id,display_name','per-page':1})
    iid=short(i['results'][0]['id']); iname=i['results'][0]['display_name']
    H0=set(); minN={}   # middle person -> smallest author count among company-affiliated topic works they are on
    paper_of={}         # middle person -> (work id, n) of that smallest work
    for page in (1,2,3):
        d=get('works',{'search':topic,'filter':f'institutions.id:{iid},from_publication_date:2015-01-01','select':'id,authorships','per-page':200,'page':page})
        if not d: break
        for w in d['results']:
            n=len(w['authorships'])
            for a in w['authorships']:
                aid=short((a.get('author') or {}).get('id'))
                if not aid: continue
                if aid not in minN or n<minN[aid]: minN[aid]=n; paper_of[aid]=(short(w['id']),n)
                if any(short(x.get('id',''))==iid for x in a.get('institutions',[])): H0.add(aid)
        if len(d['results'])<200: break
    g=get('works',{'search':topic,'filter':'from_publication_date:2015-01-01','group_by':'authorships.author.id','per-page':200})
    experts=[short(x['key']) for x in (g or {}).get('group_by',[]) if x.get('key') and short(x['key']) not in H0][:45]
    best={e:None for e in experts}   # smallest "mega-ness" over all 2-hop paths
    via_paper=defaultdict(Counter)   # expert -> papers carrying their ties
    for k in range(0,len(experts),15):
        ids='|'.join(experts[k:k+15])
        for page in (1,2,3):
            d=get('works',{'filter':f'author.id:{ids},from_publication_date:2015-01-01','select':'id,authorships','per-page':200,'page':page})
            if not d: break
            for w in d['results']:
                n=len(w['authorships']); au=[short((a.get('author') or {}).get('id')) for a in w['authorships']]
                for e in au:
                    if e not in best: continue
                    for c in au:
                        if c==e or c not in minN: continue
                        m=max(n,minN[c])
                        if best[e] is None or m<best[e]: best[e]=m
                        via_paper[e][short(w['id']) if n>=minN[c] else paper_of[c][0]]+=1
            if len(d['results'])<200: break
    tied=[e for e in experts if best[e] is not None]
    mega_only=[e for e in tied if best[e]>MEGA]
    # "verify once, apply everywhere": how many experts' ties run through each paper
    carry=Counter()
    for e in tied:
        for p in via_paper[e]: carry[p]+=1
    top=carry.most_common(3)
    summary.append((iname,topic,len(experts),len(tied),len(mega_only),top))
    print(f'{iname} / {topic}: experts {len(experts)} | tied (1-2 hops) {len(tied)} | tied ONLY through papers with >{MEGA} authors: {len(mega_only)} | papers carrying most experts\' ties: {top}',file=sys.stderr)
E=sum(s[2] for s in summary); T=sum(s[3] for s in summary); M=sum(s[4] for s in summary)
print(f'TOTAL experts {E} | tied {T} | tied only via >{MEGA}-author papers {M} ({100*M/max(1,T):.0f}% of tied) | API calls {calls}')
json.dump(summary,open('mega.json','w'),indent=1)
