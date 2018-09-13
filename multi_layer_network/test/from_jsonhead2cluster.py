import sys
sys.path.append("..")
import src.minhash2 as lel
import networkx as nx
import json
import codecs
from ast import literal_eval
import time

start = time.clock()


intput_file = "/Users/xinhuang/Downloads/image_entity.json"
output_file = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/entityc.edgelist"

lel.get_links_edge_list(intput_file, output_file)
G = nx.Graph()
path_to_cluster_heads = intput_file
edgelist = output_file
outputfile = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/entityc.jl"

with open(edgelist,"r") as edges:
    G.add_nodes_from(literal_eval(edges.readline()))
    for edge in edges:
        edge_nodes = literal_eval(edge)
        G.add_edge(edge_nodes[0], edge_nodes[1])

cc = nx.connected_components(G)
cluster_heads = json.load(open(path_to_cluster_heads),encoding="utf-8")
with codecs.open(outputfile+"_with_attr", 'w',encoding="utf-8") as output:
    for c in cc:
        answer = dict()
        answer['entities'] = map(lambda x:cluster_heads[x],list(c))
        json.dump(answer, output, encoding="utf-8", ensure_ascii=False)
        output.write('\n')

cc = nx.connected_components(G)
with open(outputfile, 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = list(c)
        json.dump(answer, output,encoding="utf-8",ensure_ascii=False)
        output.write('\n')

elapsed = (time.clock() - start)
print("Time used:",elapsed)
