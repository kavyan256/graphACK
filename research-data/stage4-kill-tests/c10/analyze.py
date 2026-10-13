import json,re
from collections import Counter,defaultdict
D=json.load(open('dns.json')); IP=json.load(open('ipmap.json'))
R={r['host']:r for r in D['res']}
MULTI=('co.uk','com.au','co.in','co.jp','com.br','com.cn','co.kr','com.tr','com.mx','org.uk','gov.uk','ac.uk','com.sg','net.au')
def reg(h):
    p=h.lower().rstrip('.').split('.')
    if '.'.join(p[-2:]) in MULTI: return '.'.join(p[-3:])
    return '.'.join(p[-2:])
CN_ORG={'cloudfront.net':'Amazon','amazonaws.com':'Amazon','awsdns':'Amazon','elb.amazonaws.com':'Amazon','akamaiedge.net':'Akamai','edgekey.net':'Akamai','akamai.net':'Akamai','edgesuite.net':'Akamai','akadns.net':'Akamai','akamaized.net':'Akamai','akamaihd.net':'Akamai',
 'fastly.net':'Fastly','fastlylb.net':'Fastly','cloudflare.net':'Cloudflare','cdn.cloudflare.net':'Cloudflare','azureedge.net':'Microsoft','azurefd.net':'Microsoft','trafficmanager.net':'Microsoft','windows.net':'Microsoft','msedge.net':'Microsoft','azurewebsites.net':'Microsoft','cloudapp.net':'Microsoft','azure.com':'Microsoft','t-msedge.net':'Microsoft',
 'googleusercontent.com':'Google','googlehosted.com':'Google','google.com':'Google','ghs.googlehosted.com':'Google','appspot.com':'Google','run.app':'Google','web.app':'Google','firebaseapp.com':'Google',
 'herokudns.com':'Heroku','herokuapp.com':'Heroku','vercel-dns.com':'Vercel','vercel.app':'Vercel','netlify.app':'Netlify','netlify.com':'Netlify','myshopify.com':'Shopify','shopify.com':'Shopify','wpengine.com':'WP Engine','wpenginepowered.com':'WP Engine','github.io':'GitHub','githubusercontent.com':'GitHub',
 'impervadns.net':'Imperva','incapdns.net':'Imperva','cdn77.org':'CDN77','b-cdn.net':'Bunny','squarespace.com':'Squarespace','wixdns.net':'Wix','zendesk.com':'Zendesk','hubspot.net':'HubSpot','edgecastcdn.net':'Edgio','llnwd.net':'Edgio','alikunlun.com':'Alibaba','kunlunca.com':'Alibaba','alicdn.com':'Alibaba','tbcache.com':'Alibaba','gslb.taobao.com':'Alibaba','cdngslb.com':'Alibaba','chinacache.net':'ChinaCache','wsglb0.com':'Wangsu','wscloudcdn.com':'Wangsu','qiniudns.com':'Qiniu','dnsv1.com':'Tencent','tdnsv5.com':'Tencent','sucuri.net':'Sucuri','pantheonsite.io':'Pantheon','acquia-sites.com':'Acquia','sitecorecloud.io':'Sitecore','adobeaemcloud.com':'Adobe','salesforce-sites.com':'Salesforce','force.com':'Salesforce','ghost.io':'Ghost','webflow.io':'Webflow','proxy-ssl.webflow.com':'Webflow','gitlab.io':'GitLab','render.com':'Render','onrender.com':'Render','fly.dev':'Fly.io','pages.dev':'Cloudflare','workers.dev':'Cloudflare'}
def cn_org(h):
    h=h.lower()
    for k,v in CN_ORG.items():
        if h.endswith(k): return v
    return None
def ip_org(ip):
    v=IP.get(ip)
    if not v: return 'unknown',None,None
    o=v['org']; ol=o.lower()
    for key,name in [('amazon','Amazon'),('google','Google'),('akamai','Akamai'),('cloudflare','Cloudflare'),('fastly','Fastly'),('microsoft','Microsoft'),('alibaba','Alibaba'),('taobao','Alibaba'),('cdn77','CDN77'),('ovh','OVH'),('automattic','Automattic'),('facebook','Meta'),('apple','Apple'),('netflix','Netflix'),('tencent','Tencent'),('baidu','Baidu'),('vk','VK'),('yandex','Yandex'),('leaseweb','Leaseweb'),('hetzner','Hetzner'),('digitalocean','DigitalOcean'),('linode','Akamai'),('oracle','Oracle'),('github','GitHub'),('twitter','X'),('bytedance','ByteDance')]:
        if key in ol: return name,v.get('region'),v.get('service')
    return o.split(' - ')[-1][:30] if ' - ' in o else o[:30],v.get('region'),v.get('service')
CDN_ORGS={'Cloudflare','Fastly','Akamai','CDN77','Edgio','Imperva','Bunny','Wangsu','ChinaCache','Sucuri'}
def analyze_host(host,site):
    r=R.get(host)
    if not r or not r.get('ips'): return None
    brand=reg(site).split('.')[0]
    steps=[]
    for c in r.get('cnames',[]):
        o=cn_org(c) or ( None if reg(c)==reg(site) or brand in reg(c) else 'other:'+reg(c))
        if o: steps.append(o)
    orgs=[ip_org(ip) for ip in r['ips']]
    final=orgs[0][0]; regions={o[1] for o in orgs if o[1]}; svcs={o[2] for o in orgs if o[2]}
    selfhost = brand in final.lower() or (final=='Amazon' and brand in ('amazon','imdb','primevideo','twitch','ring','audible','goodreads')) or (final=='Google' and brand in ('google','youtube','gmail','blogger','android')) or (final=='Microsoft' and brand in ('microsoft','bing','live','office','xbox','linkedin','msn','skype','outlook','azure','github'))
    third=[]
    for s in steps+[final]:
        if selfhost and s==final: continue
        if s not in third: third.append(s)
    cdn_front = final in CDN_ORGS or 'CLOUDFRONT' in svcs or any(s in CDN_ORGS for s in steps)
    us_east = 'us-east-1' in regions or any('us-east-1' in c for c in r.get('cnames',[]))
    return {'host':host,'third':third,'depth':len(third),'final':final,'regions':sorted(regions),'svcs':sorted(svcs),'cdn_front':cdn_front,'us_east1':us_east,'self':selfhost,'cnames':r.get('cnames',[])}
# (a) Tranco top 1000
rows=[]
for d in D['tranco']:
    a=analyze_host('www.'+d,d) or analyze_host(d,d)
    if a: rows.append(a)
n=len(rows); dep=Counter(min(r['depth'],3) for r in rows)
d2=[r for r in rows if r['depth']>=2]
print(f'(a) Tranco top-1000: {n} resolved')
print('   visible third-party depth distribution:',dict(sorted(dep.items())))
print(f'   depth>=2 (provider of a provider visible in DNS): {len(d2)} = {100*len(d2)/n:.1f}%')
cf_=[r for r in rows if r['cdn_front'] and not r['self']]
print(f'   fronted by a CDN (origin hidden from DNS): {len(cf_)} = {100*len(cf_)/n:.1f}%')
print(f'   self-hosted (own network): {sum(r["self"] for r in rows)} ; final provider top:',Counter(r['final'] for r in rows).most_common(10))
print('   examples depth>=2:',[(r['host'],r['third']) for r in d2[:12]])
ns=D['ns']; nsorg=Counter()
for d in D['tranco']:
    names=ns.get(d,[])
    o='none'
    for x in names:
        o=cn_org(x) or ('Amazon' if 'awsdns' in x else 'Cloudflare' if 'cloudflare' in x else 'Akamai' if 'akam' in x else 'NS1' if 'nsone' in x else 'UltraDNS' if 'ultradns' in x else 'Dyn' if 'dynect' in x else 'Google' if 'google' in x else 'Microsoft' if 'azure-dns' in x else 'self/other')
        break
    nsorg[o]+=1
print('   DNS provider (first NS):',nsorg.most_common(8))
# (b) backtest
def svc_hosts(base):
    apex=base if base.count('.')==1 or base.endswith(('co.uk',)) else base.split('.',1)[1]
    hs=[base,'www.'+apex,apex,'api.'+apex,'app.'+apex,'auth.'+apex]
    return list(dict.fromkeys(hs)),apex
def svc(base):
    hs,apex=svc_hosts(base); out=[analyze_host(h,apex) for h in hs]; out=[o for o in out if o]
    return {'svc':base,'resolved':bool(out),'us_east1':any(o['us_east1'] for o in out),'aws_any':any(o['final']=='Amazon' or 'Amazon' in o['third'] for o in out),'aws_regional':any(o['final']=='Amazon' and o['regions'] and o['regions']!=['GLOBAL'] for o in out),'detail':[(o['host'],o['final'],o['regions'],o['third']) for o in out]}
P=[svc(b) for b in D['pos']]; N=[svc(b) for b in D['neg']]
def rate(L,k): L=[x for x in L if x['resolved']]; return sum(x[k] for x in L),len(L)
for k in ('us_east1','aws_regional','aws_any'):
    a,b=rate(P,k); c,d=rate(N,k)
    print(f'(b) {k:12}: outage victims flagged {a}/{b} = {100*a/b:.0f}%   |  not-reported services flagged {c}/{d} = {100*c/d:.0f}%')
print('   victims NOT flagged us-east-1:',[x['svc'] for x in P if x['resolved'] and not x['us_east1']])
print('   not-reported but flagged us-east-1:',[x['svc'] for x in N if x['us_east1']])
json.dump({'tranco_rows':rows,'pos':P,'neg':N},open('analysis.json','w'),indent=1)
