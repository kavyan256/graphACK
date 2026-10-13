import networkx as nx, statistics, re
G=nx.read_gexf('g.gexf')
print('nodes',G.number_of_nodes(),'edges',G.number_of_edges())
# direction check: a basic lemma should be USED BY many theorems
for n in ['Nat.succ_le_iff','add_comm','mul_comm','le_refl','Nat.le_of_lt_succ']:
    if n in G: print(f'  {n}: in={G.in_degree(n)} out={G.out_degree(n)}')
famous=['Nat.exists_infinite_primes','irrational_sqrt_two','Complex.exists_root','ZMod.pow_card_sub_one_eq_one','Real.pi_gt_three','intermediate_value_Icc','IsCompact.exists_isMinOn','Nat.Prime.two_le','Finset.sum_range_id_mul_two','Real.exp_pos','Polynomial.card_roots','Nat.Prime.eq_one_or_self_of_dvd','Real.add_pow_le_pow_mul_pow_of_sq_le_sq','inner_mul_le_norm_mul_norm','MeasureTheory.integral_add','sq_nonneg','Cardinal.cantor','Nat.gcd_comm','Int.emod_emod_of_dvd','Real.sqrt_lt_sqrt']
found=[f for f in famous if f in G]
print('famous theorems found:',len(found),'of',len(famous))
# decide direction: if basic lemmas have high in-degree, edges are user -> dependency, so prerequisites = descendants
basic_in=sum(G.in_degree(n) for n in ['add_comm','mul_comm','le_refl'] if n in G); basic_out=sum(G.out_degree(n) for n in ['add_comm','mul_comm','le_refl'] if n in G)
prereq = nx.descendants if basic_in>basic_out else nx.ancestors
print('prerequisites computed with', prereq.__name__)
sizes=[]
for f in found:
    s=len(prereq(G,f)); sizes.append(s)
    files={G.nodes[x].get('file_path','').split('/')[1] if '/' in G.nodes[x].get('file_path','') else '?' for x in prereq(G,f)}
    print(f'  {f}: {s} prerequisite declarations across {len(files)} top-level areas')
if sizes: print('median closure:',statistics.median(sizes),'min',min(sizes),'max',max(sizes))
# overall distribution on a random sample
import random; random.seed(1); samp=random.sample(list(G.nodes),300)
allsz=[len(prereq(G,n)) for n in samp]
print('random 300 declarations: median closure',statistics.median(allsz),'| 90th pct',sorted(allsz)[270])
