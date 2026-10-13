import csv,json,urllib.request,urllib.parse,concurrent.futures as cf,time,ipaddress
from collections import defaultdict,Counter
from urllib.parse import urlparse
rows=list(csv.DictReader(open('shops.csv',encoding='utf-8',errors='ignore')))
def host(u):
    h=urlparse(u.strip()).netloc.lower() or u.strip().lower()
    return h[4:] if h.startswith('www.') else h
S=[(host(r['Online shop URL']),r['Label'].strip()) for r in rows]
def doh(name,typ):
    for base in ('https://dns.google/resolve','https://cloudflare-dns.com/dns-query'):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(base+'?'+urllib.parse.urlencode({'name':name,'type':typ}),headers={'accept':'application/dns-json'}),timeout=15))
            return d
        except Exception: time.sleep(0.4)
    return None
def res(h):
    a=doh(h,'A'); n=doh(h,'NS')
    ips=[x['data'] for x in (a or {}).get('Answer',[]) or [] if x.get('type')==1]
    ns=sorted(x['data'].rstrip('.').lower() for x in (n or {}).get('Answer',[]) or [] if x.get('type')==2)
    return h,{'ips':ips,'ns':ns,'status':(a or {}).get('Status')}
with cf.ThreadPoolExecutor(24) as ex: R=dict(ex.map(res,[h for h,_ in S]))
json.dump(R,open('shops_dns.json','w'))
# big shared providers (exclude from linking)
nets=[]
for p in json.load(open('aws.json'))['prefixes']: nets.append(ipaddress.ip_network(p['ip_prefix']))
for p in json.load(open('gcp.json'))['prefixes']:
    if 'ipv4Prefix' in p: nets.append(ipaddress.ip_network(p['ipv4Prefix']))
for l in open('cf.txt').read().split(): nets.append(ipaddress.ip_network(l))
for l in json.load(open('fastly.json'))['addresses']: nets.append(ipaddress.ip_network(l))
nets.append(ipaddress.ip_network('23.227.38.0/24'))  # Shopify shared storefront IPs
def big(ip):
    x=ipaddress.ip_address(ip); return any(x in n for n in nets)
BIG_NS=('cloudflare.com','awsdns','domaincontrol.com','googledomains','registrar-servers.com','shopify','dns-parking','namebrightdns','hostinger','ns.cloudflare','nsone','azure-dns','wixdns','squarespacedns','dnsowl')
alive={h for h,v in R.items() if v['ips']}
lab=dict(S)
print('domains',len(S),'| resolvable now:',len(alive),'| fake alive',sum(1 for h in alive if lab[h]=='fraudulent'),'of',sum(1 for _,l in S if l=='fraudulent'),'| legit alive',sum(1 for h in alive if lab[h]=='legitimate'),'of',sum(1 for _,l in S if l=='legitimate'))
# link keys: exact non-big IP; NS set not from big providers
keys=defaultdict(set)
for h in alive:
    v=R[h]
    for ip in v['ips']:
        if not big(ip): keys['ip:'+ip].add(h)
    nsset=tuple(v['ns'])
    if nsset and not any(b in ''.join(nsset) for b in BIG_NS): keys['ns:'+'|'.join(nsset)].add(h)
linked=defaultdict(set)
for k,hs in keys.items():
    if len(hs)>1:
        for h in hs: linked[h].update(hs-{h})
def rate(label,to):
    A=[h for h in alive if lab[h]==label]
    k=sum(1 for h in A if any(lab[x]==to for x in linked[h]))
    return k,len(A)
for a,b in (('fraudulent','fraudulent'),('legitimate','legitimate'),('legitimate','fraudulent'),('fraudulent','legitimate')):
    k,n=rate(a,b); print(f'  alive {a} shops linked (non-big shared IP or NS) to another {b} shop: {k}/{n} = {100*k/max(1,n):.0f}%')
big_share=Counter('big' if all(big(ip) for ip in R[h]['ips']) else 'own/other' for h in alive if lab[h]=='fraudulent')
print('  hosting of alive fakes:',dict(big_share))
