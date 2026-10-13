import json,urllib.request,urllib.parse,time,concurrent.futures as cf,csv,sys
def doh(name,typ):
    for base in ('https://dns.google/resolve','https://cloudflare-dns.com/dns-query'):
        try:
            u=base+'?'+urllib.parse.urlencode({'name':name,'type':typ})
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'accept':'application/dns-json','User-Agent':'graphhack-research'}),timeout=15)
            return json.load(r)
        except Exception as e:
            time.sleep(0.5)
    return None
def chain(host):
    d=doh(host,'A')
    if not d: return {'host':host,'status':'err'}
    ans=d.get('Answer',[]) or []
    cn=[a['data'].rstrip('.') for a in ans if a.get('type')==5]
    ips=[a['data'] for a in ans if a.get('type')==1]
    return {'host':host,'status':d.get('Status'),'cnames':cn,'ips':ips}
pos="""amazon.com primevideo.com music.apple.com asana.com att.com chime.com delta.com store.epicgames.com fortnite.com imdb.com lyft.com max.com mcdonalds.com reddit.com ring.com robinhood.com roblox.com roku.com playstation.com signal.org snapchat.com spectrum.net starbucks.com store.steampowered.com ubisoft.com venmo.com xbox.com xfinity.com zoom.us instructure.com crunchyroll.com whatnot.com coinbase.com canva.com duolingo.com goodreads.com nytimes.com life360.com tv.apple.com verizon.com perplexity.ai collegeboard.org pubg.com pinterest.com ancestry.com hinge.co lloydsbank.com halifax.co.uk bankofscotland.co.uk flickr.com slack.com""".split()
neg="""google.com youtube.com facebook.com instagram.com whatsapp.com x.com tiktok.com netflix.com spotify.com microsoft.com linkedin.com github.com wikipedia.org discord.com twitch.tv airbnb.com uber.com doordash.com shopify.com paypal.com ebay.com walmart.com target.com bing.com yahoo.com cnn.com bbc.co.uk espn.com hulu.com disneyplus.com dropbox.com notion.so figma.com openai.com chatgpt.com telegram.org quora.com stackoverflow.com medium.com etsy.com booking.com expedia.com tripadvisor.com zillow.com indeed.com salesforce.com adobe.com wellsfargo.com chase.com bankofamerica.com""".split()
tr=[r[1] for r in csv.reader(open('top-1m.csv'))][:1000]
targets=set()
for d in tr: targets.update([d,'www.'+d])
for d in pos+neg:
    base=d
    targets.update([base,'www.'+base if not base.startswith(('www.','store.','music.','tv.')) else base,'api.'+base.split('.',1)[-1] if base.count('.')>1 else 'api.'+base,'app.'+(base if base.count('.')==1 else base.split('.',1)[1]),'auth.'+(base if base.count('.')==1 else base.split('.',1)[1])])
targets=sorted(targets)
print('hosts to resolve',len(targets),file=sys.stderr)
with cf.ThreadPoolExecutor(24) as ex: res=list(ex.map(chain,targets))
ns={}
apexes=sorted(set(tr+[d if d.count('.')==1 else d.split('.',1)[1] for d in pos+neg]))
def nsq(a):
    d=doh(a,'NS'); return a,[x['data'].rstrip('.') for x in (d or {}).get('Answer',[]) or [] if x.get('type')==2]
with cf.ThreadPoolExecutor(24) as ex: ns=dict(ex.map(nsq,apexes))
json.dump({'pos':pos,'neg':neg,'tranco':tr,'res':res,'ns':ns},open('dns.json','w'))
ok=sum(1 for r in res if r.get('ips')); print('resolved with IPs',ok,'of',len(res),file=sys.stderr)
