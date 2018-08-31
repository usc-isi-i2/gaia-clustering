import sys
sys.path.append("..")
import  src.AIF_RPI_to_JSON as rtj
import src.links_edge_list_with_nil as lel
import getopt
import networkx as nx
import json
import codecs
import time
from ast import literal_eval
start = time.clock()
output_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/RPI_clusters_seedling_cluster_heads_with_type.json"
output_file2 = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1//RPI_clusters_seedling_same_link_with_nil.edgelist"
    #rtj.extract_canonical_mentions_as_cluster_heads(input_file, output_file)
lel.get_links_edge_list(output_file, output_file2)

G = nx.Graph()
path_to_cluster_heads = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1//RPI_clusters_seedling_cluster_heads_with_type.json"
edgelist = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/RPI_clusters_seedling_same_link_with_nil.edgelist"
outputfile = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/RPI_clusters_seedling_same_link_clusters_with_nil.jl"

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