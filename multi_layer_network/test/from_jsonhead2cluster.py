import sys
sys.path.append("..")
import  src.AIF_RPI_to_JSON as rtj
import src.minhash2 as lel
import getopt
import networkx as nx
import json
import codecs
from ast import literal_eval
import time

start = time.clock()
#output_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/dryrun_large//RPI_clusters_seedling_cluster_heads_with_type.json"
#output_file2 = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/dryrun_large/RPI_clusters_seedling_same_link_with_nil_test.edgelist"

#outputfile = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/dryrun_large//RPI_clusters_seedling_same_link_clusters_with_blocking3.jl"

output_file = "/Users/xinhuang/Documents/isi/gaia_proj/en_2.json"
output_file2 = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.edgelist"

lel.get_links_edge_list(output_file, output_file2)
G = nx.Graph()
path_to_cluster_heads = output_file
edgelist = output_file2
outputfile = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.jl"

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
            # output.write(str(c) + '\n')
cc = nx.connected_components(G)
with open(outputfile, 'w') as output:
    for c in cc:
        answer = dict()
        answer['entities'] = list(c)
        json.dump(answer, output,encoding="utf-8",ensure_ascii=False)
        output.write('\n')

elapsed = (time.clock() - start)
print("Time used:",elapsed)
