import json,re,urllib.request,urllib.parse,concurrent.futures as cf,time,sys
B='https://api.deps.dev/v3/systems/'
def get(url):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'graphhack-research'}),timeout=25))
        except urllib.error.HTTPError as e:
            if e.code==404: return None
            time.sleep(1+i)
        except Exception: time.sleep(1+i)
    return None
q=lambda s: urllib.parse.quote(s,safe='')
def deps(system,name):
    p=get(B+f'{system}/packages/{q(name)}')
    if not p: return name,None
    dv=[v['versionKey']['version'] for v in p.get('versions',[]) if v.get('isDefault')]
    if not dv: return name,None
    v=dv[0]
    g=get(B+f'{system}/packages/{q(name)}/versions/{q(v)}:dependencies')
    return name,{'version':v,'graph':g}
pypi=[r['project'] for r in json.load(open('pypi_top.json'))['rows'][:400]]
npm=re.findall(r"'([^']+)'",open('npm_top_download.js').read())[:400]
out={}
for system,names in (('pypi',pypi),('npm',npm)):
    with cf.ThreadPoolExecutor(16) as ex: res=dict(ex.map(lambda n: deps(system,n),names))
    out[system]=res
    print(system,'graphs ok',sum(1 for v in res.values() if v and v['graph']),'of',len(names),file=sys.stderr)
keys=set()
for system,res in out.items():
    for v in res.values():
        if v and v['graph']:
            for n in v['graph'].get('nodes',[]):
                vk=n['versionKey']; keys.add((vk['system'].lower(),vk['name'],vk['version']))
print('unique version nodes',len(keys),file=sys.stderr)
def lic(k):
    s,n,v=k; d=get(B+f'{s}/packages/{q(n)}/versions/{q(v)}')
    return k,(d or {}).get('licenses') if d else None
with cf.ThreadPoolExecutor(24) as ex: L=dict(ex.map(lic,sorted(keys)))
json.dump({'graphs':out,'licenses':{'|'.join(k):v for k,v in L.items()}},open('c40.json','w'))
print('licence lookups done; with licence field:',sum(1 for v in L.values() if v),'of',len(L),file=sys.stderr)
