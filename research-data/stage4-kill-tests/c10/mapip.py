import json,ipaddress,urllib.request,urllib.parse,concurrent.futures as cf,time,sys,bisect
D=json.load(open('dns.json'))
ips=sorted({ip for r in D['res'] for ip in r.get('ips',[])})
print('unique IPs',len(ips),file=sys.stderr)
nets=[]
a=json.load(open('aws.json'))
for p in a['prefixes']:
    nets.append((ipaddress.ip_network(p['ip_prefix']),'Amazon',p['region'],p['service']))
g=json.load(open('gcp.json'))
for p in g['prefixes']:
    if 'ipv4Prefix' in p: nets.append((ipaddress.ip_network(p['ipv4Prefix']),'Google Cloud',p.get('scope'),p.get('service')))
for l in open('cf.txt').read().split(): nets.append((ipaddress.ip_network(l),'Cloudflare','GLOBAL','CDN'))
for l in json.load(open('fastly.json')).get('addresses',[]): nets.append((ipaddress.ip_network(l),'Fastly','GLOBAL','CDN'))
# most specific match wins; AWS lists AMAZON + specific service, prefer non-'AMAZON' service
def lookup(ip):
    x=ipaddress.ip_address(ip); best=None
    for n,org,reg,svc in nets:
        if x in n:
            cand=(n.prefixlen, svc!='AMAZON', org,reg,svc)
            if best is None or cand>best: best=cand
    return best
known={}
for ip in ips:
    b=lookup(ip)
    if b: known[ip]={'org':b[2],'region':b[3],'service':b[4]}
print('matched by published ranges',len(known),file=sys.stderr)
def doh_txt(name):
    for base in ('https://dns.google/resolve','https://cloudflare-dns.com/dns-query'):
        try:
            u=base+'?'+urllib.parse.urlencode({'name':name,'type':'TXT'})
            d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'accept':'application/dns-json'}),timeout=15))
            return [x['data'].strip('"') for x in d.get('Answer',[]) or []]
        except Exception: time.sleep(0.5)
    return []
def asn(ip):
    t=doh_txt('.'.join(reversed(ip.split('.')))+'.origin.asn.cymru.com')
    if not t: return ip,None
    return ip,t[0].split('|')[0].strip().split()[0]
rest=[ip for ip in ips if ip not in known]
with cf.ThreadPoolExecutor(24) as ex: asns=dict(ex.map(asn,rest))
uniq=sorted({v for v in asns.values() if v})
def asname(n):
    t=doh_txt(f'AS{n}.asn.cymru.com'); return n,(t[0].split('|')[-1].strip() if t else '')
with cf.ThreadPoolExecutor(24) as ex: names=dict(ex.map(asname,uniq))
for ip,n in asns.items():
    known[ip]={'org':('AS'+n+' '+names.get(n,'')) if n else 'unknown','region':None,'service':None,'asn':n}
json.dump(known,open('ipmap.json','w'))
from collections import Counter
c=Counter(v['org'].split(',')[0][:40] for v in known.values())
print(c.most_common(25))
