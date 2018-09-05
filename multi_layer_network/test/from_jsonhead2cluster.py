import os
import multi_layer_network.src.minhash2 as lel
import networkx as nx
import json
from ast import literal_eval
import time

start = time.clock()

output_dir = os.path.join(os.path.dirname(__file__), '../../outputs')
intput_file = output_dir + '/entity.json'
output_file = output_dir + 'entity.edgelist'

lel.get_links_edge_list(intput_file, output_file)
G = nx.Graph()
path_to_cluster_heads = intput_file
edgelist = output_file
outputfile = output_dir + '/entity.jl'

with open(edgelist, "r") as edges:
    G.add_nodes_from(literal_eval(edges.readline()))
    for edge in edges:
        edge_nodes = literal_eval(edge)
        G.add_edge(edge_nodes[0], edge_nodes[1])

cc = nx.connected_components(G)
cluster_heads = json.load(open(path_to_cluster_heads))
with open(outputfile + '_with_attr', 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = [cluster_heads[x] for x in c]
        json.dump(answer, output)
        output.write('\n')

cc = nx.connected_components(G)
with open(outputfile, 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = list(c)
        json.dump(answer, output)
        output.write('\n')

elapsed = (time.clock() - start)
print("Time used:", elapsed)
