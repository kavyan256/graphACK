import json,urllib.request,urllib.parse,time,sys
B='https://api.openalex.org/'; calls=0
def get(path,params):
    global calls
    u=B+path+'?'+urllib.parse.urlencode(params)
    for k in range(3):
        try:
            calls+=1; return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'graphhack-research'}),timeout=60))
        except urllib.error.HTTPError as e:
            print('HTTP',e.code,u[:140],file=sys.stderr)
            if e.code in (402,429): return None
            time.sleep(2)
        except Exception: time.sleep(2)
    return None
short=lambda x:(x or '').rsplit('/',1)[-1]
def inst(name):
    d=get('institutions',{'search':name,'filter':'type:company','select':'id,display_name,country_code,works_count','per-page':3})
    return [(short(r['id']),r['display_name'],r['works_count']) for r in (d or {}).get('results',[])]
cases=[('Pfizer','mRNA vaccine'),('Bayer','glyphosate'),('Monsanto','glyphosate'),('Google','large language model')]
out=[]
for comp,topic in cases:
    I=inst(comp)
    if not I: continue
    iid,iname,_=I[0]
    # H0/H1: authors on company-affiliated works in the topic
    H0=set(); H1=set(); nworks=0
    for page in (1,2,3):
        d=get('works',{'search':topic,'filter':f'institutions.id:{iid},from_publication_date:2015-01-01','select':'authorships','per-page':200,'page':page})
        if not d: break
        for w in d['results']:
            nworks+=1
            for a in w['authorships']:
                aid=(a.get('author') or {}).get('id')
                if not aid: continue
                H1.add(short(aid))
                if any(short(i.get('id',''))==iid for i in a.get('institutions',[])): H0.add(short(aid))
        if len(d['results'])<200: break
    # topical experts: most prolific authors on the topic
    g=get('works',{'search':topic,'filter':'from_publication_date:2015-01-01','group_by':'authorships.author.id','per-page':200})
    experts=[short(x['key']) for x in (g or {}).get('group_by',[]) if x.get('key') and short(x['key']) not in H0][:45]
    one=[e for e in experts if e in H1]
    co={e:set() for e in experts}
    for i in range(0,len(experts),15):
        ids='|'.join(experts[i:i+15])
        for page in (1,2,3):
            d=get('works',{'filter':f'author.id:{ids},from_publication_date:2015-01-01','select':'authorships','per-page':200,'page':page})
            if not d: break
            for w in d['results']:
                au=[short((a.get('author') or {}).get('id','')) for a in w['authorships']]
                for a in au:
                    if a in co: co[a].update(x for x in au if x!=a)
            if len(d['results'])<200: break
    two=[e for e in experts if e not in H1 and co[e]&H1]
    paths={e:len(co[e]&H1) for e in experts}
    a=get('authors',{'filter':'openalex:'+'|'.join(experts),'select':'id,works_count,orcid','per-page':50})
    wc={short(x['id']):(x.get('works_count'),bool(x.get('orcid'))) for x in (a or {}).get('results',[])}
    r={'company':iname,'topic':topic,'company_works_in_topic':nworks,'company_authors':len(H0),'one_hop_set':len(H1),'experts':len(experts),'tied_1hop':len(one),'tied_2hop_extra':len(two),'paths':paths,'wc':wc}
    out.append(r); print(r,file=sys.stderr)
json.dump(out,open('r1b.json','w'),indent=1)
import statistics
P=[v for r in out for v in r['paths'].values()]
T=[v for v in P if v>0]
print('distinct middle co-authors per tied expert (2-hop paths): median',statistics.median(T),'| 1 path:',sum(1 for v in T if v==1),'| 2-5:',sum(1 for v in T if 2<=v<=5),'| 6-20:',sum(1 for v in T if 6<=v<=20),'| >20:',sum(1 for v in T if v>20),'of',len(T))
W=[x for r in out for x in r['wc'].values()]
print('experts with >1000 works (possible merged profiles):',sum(1 for w,o in W if (w or 0)>1000),'of',len(W),'| with ORCID:',sum(1 for w,o in W if o))
E=sum(r['experts'] for r in out); t1=sum(r['tied_1hop'] for r in out); t2=sum(r['tied_2hop_extra'] for r in out)
print(f'experts {E} | tied directly (co-authored a company paper on the topic): {t1} ({100*t1/max(1,E):.0f}%) | tied within 2 hops: {t1+t2} ({100*(t1+t2)/max(1,E):.0f}%) | 2-hop/1-hop ratio: {(t1+t2)/max(1,t1):.1f}x | calls {calls}')
