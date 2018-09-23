import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import multi_layer_network.src.minhash2 as lel
import networkx as nx
import json
# from ast import literal_eval
import time


def read_cluster_prototype_file(file_dir):
    if isinstance(file_dir, str):
        cluster_file = json.load(open(file_dir))
        cluster_to_entity = {}
        cluster_to_prototype  = {}
        for i in cluster_file:
            cluster_to_entity[i] = cluster_file[i][0]
            #cluster_to_prototype[i] = cluster_file[i][0]+cluster_file[i][1]
    return cluster_to_entity


def run(cluster_heads,cluster_file, outputs_prefix):
    if isinstance(cluster_heads, str):
        cluster_heads = json.load(open(cluster_heads))
    cluster2entity = read_cluster_prototype_file(cluster_file)
    start = time.clock()

    # outputs_prefix = os.path.join(os.path.dirname(__file__), '../../outputs/') if len(sys.argv) < 2 else (sys.argv[1].rstrip('/') + '/')

    output_file = outputs_prefix + "entity.jl"
    output_file_with_attr = outputs_prefix + "entity_with_attr.jl"

    G = lel.get_links_edge_list(cluster_heads)
    G = lel.add_edges_via_cluster(cluster2entity ,G)
    cc = nx.connected_components(G)
    ret = []
    with open(output_file, 'w') as output:
        for c in cc:
            answer = dict()
            answer['entities'] = list(c)
            ret.append(answer)
            json.dump(answer, output, indent=4, ensure_ascii=False)
            output.write('\n')
    cc = nx.connected_components(G)
    with open(output_file_with_attr, 'w') as output:
        for c in cc:
            answer = dict()
            answer['entities'] = [cluster_heads[x] for x in c]
            json.dump(answer, output, indent=4, ensure_ascii=False)
            output.write('\n')


    elapsed = (time.clock() - start)
    print("Time used:", elapsed)

    return ret, G


def dump_edgelist_to_file(G, outputs_prefix):
    with open(outputs_prefix + 'entity.edgelist',  'w') as f:
        f.write(str(G.nodes()) + '\n')
        for e in G.edges:
            f.write(str(e) + '\n')


def run_with_file_io(input_json_head, input_cluster_file, outputs_prefix):
    '''

    :param input_json_head: the json file path of the entity json heads
    :param outputs_prefix: the directory(folder) to put output jl file and the entity edgelist file
    :return: enity cluster jl
    '''
    with open(input_json_head) as f:
        cluster_heads = json.load(f)
    jl, edgelist = run(cluster_heads,input_cluster_file, outputs_prefix)
    dump_edgelist_to_file(edgelist, outputs_prefix)
    return jl










