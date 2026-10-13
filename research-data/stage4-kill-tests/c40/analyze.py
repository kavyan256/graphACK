import json,re,networkx as nx
from collections import Counter
D=json.load(open('c40.json')); L=D['licenses']
STRONG=re.compile(r'\b(A?GPL|SSPL|OSL|EUPL|CPAL|RPL|Sleepycat)',re.I)
WEAK=re.compile(r'\b(LGPL|MPL|EPL|CDDL|CPL|MS-RL|LPL|APSL)',re.I)
def classify(exprs):
    """exprs: list of SPDX expressions; copyleft only if every OR-alternative is copyleft"""
    if not exprs: return 'unknown'
    worst='permissive'
    for e in exprs:
        alts=re.split(r'\s+OR\s+',e.replace('(','').replace(')',''))
        cls=[]
        for a in alts:
            if STRONG.search(a) and not re.search(r'\bLGPL',a,re.I): cls.append('strong')
            elif WEAK.search(a) or re.search(r'\bLGPL',a,re.I): cls.append('weak')
            elif re.search(r'non-standard|unknown',a,re.I): cls.append('unknown')
            else: cls.append('permissive')
        # user may pick the most permissive alternative
        order={'permissive':0,'unknown':1,'weak':2,'strong':3}
        best=min(cls,key=lambda c:order[c])
        if order[best]>order[worst]: worst=best
    return worst
def lic_of(vk): return L.get('|'.join([vk['system'].lower(),vk['name'],vk['version']]))
res={}
for system,graphs in D['graphs'].items():
    rows=[]
    for name,v in graphs.items():
        if not v or not v['graph']: continue
        g=v['graph']; nodes=g.get('nodes',[]); edges=g.get('edges',[])
        G=nx.DiGraph(); G.add_nodes_from(range(len(nodes)))
        for e in edges: G.add_edge(e['fromNode'],e['toNode'])
        root=next((i for i,n in enumerate(nodes) if n.get('relation')=='SELF'),0)
        dist=nx.single_source_shortest_path_length(G,root)
        cls={i:classify(lic_of(n['versionKey'])) for i,n in enumerate(nodes)}
        for level in ('strong','weak_or_strong'):
            C=[i for i in range(len(nodes)) if i!=root and i in dist and (cls[i]=='strong' if level=='strong' else cls[i] in ('strong','weak'))]
            deep=[i for i in C if dist[i]>=2]
            row={'pkg':name,'level':level,'n':len(nodes)-1,'copyleft':len(C),'deep':len(deep),'names':[nodes[i]['versionKey']['name']+'('+(lic_of(nodes[i]['versionKey']) or ['?'])[0]+')' for i in C]}
            if C:
                # min vertex cut root -> C (cut vertices: any non-root node, copyleft nodes allowed)
                H=nx.DiGraph()
                for u in G.nodes:
                    H.add_edge(('in',u),('out',u),capacity=(10**9 if u==root else 1))
                for a,b in G.edges: H.add_edge(('out',a),('in',b),capacity=10**9)
                for c in C: H.add_edge(('out',c),'T',capacity=10**9)
                cut,_=nx.minimum_cut(H,('out',root),'T')
                row['mincut']=int(cut)
                direct=[s for s in G.successors(root) if any(nx.has_path(G,s,c) for c in C)]
                row['direct_swaps']=len(direct)
            rows.append(row)
    res[system]=rows
cov_total=len(L); cov=sum(1 for v in L.values() if v)
print(f'(c) licence coverage: {cov}/{cov_total} = {100*cov/cov_total:.1f}% of version nodes have a licence field')
allcls=Counter(classify(v) for v in L.values()); print('    node licence classes:',dict(allcls))
for system,rows in res.items():
    for level in ('strong','weak_or_strong'):
        R=[r for r in rows if r['level']==level]
        big=[r for r in R if r['n']>=10]
        for label,S in (('all',R),('>=10 deps',big)):
            aff=[r for r in S if r['copyleft']>0]; deep=[r for r in S if r['deep']>0]
            nontriv=[r for r in aff if r['mincut']<r['copyleft']]
            print(f'{system:5} {level:15} {label:10} n={len(S):4} | any copyleft {len(aff):4} ({100*len(aff)/max(1,len(S)):.1f}%) | copyleft at depth>=2 {len(deep):4} ({100*len(deep)/max(1,len(S)):.1f}%) | mincut < naive in {len(nontriv)}/{len(aff)} ({100*len(nontriv)/max(1,len(aff)):.0f}%)')
    top=Counter(nm for r in rows if r['level']=='weak_or_strong' for nm in r['names']).most_common(12)
    print('   most common copyleft deps:',top)
    ex=[r for r in rows if r['level']=='weak_or_strong' and r['copyleft']>0 and r['mincut']<r['copyleft']][:6]
    for r in ex: print('   e.g.',r['pkg'],'copyleft nodes',r['copyleft'],'-> min cut',r['mincut'],'| direct swaps needed',r['direct_swaps'],r['names'][:5])
json.dump(res,open('c40_analysis.json','w'),indent=1)
