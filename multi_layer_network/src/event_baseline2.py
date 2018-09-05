import re
import sys
import json
import getopt
import numpy as np
import networkx as nx
from ast import literal_eval

from datetime import datetime

def main(argv):
    opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print(
                'Given events JSON file, outputs events linkings in the format of connected components according to baseline #1, usage: python event_baseline.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    event_baseline_linking(inputfile, outputfile)


def event_baseline_linking(path_to_events, path_to_output,entity2cluster):

    events = json.load(open(path_to_events))

    IDs = list(events.keys())

    G = nx.Graph()
    G.add_nodes_from(IDs)
    geo_str = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#GeopoliticalEntity"
    fil_str = "http://darpa.mil/ontologies/SeedlingOntology#FillerType"
    per_str = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#Person"
    org_str = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#Organization"
    fac_str = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#Facility"
    loc_str = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#Location"
    entity_type =[geo_str,per_str,org_str,fac_str,loc_str]
    for i, id1 in enumerate(IDs):
        for j in range(i + 1, len(IDs)):
            id2 = IDs[j]
            if events[id1]['type'] == events[id2]['type']:
                common = 0
                for t in entity_type:
                    set_1 = set()
                    set_2 = set()
                    for ent in events[id1][t]:
                        if isinstance(ent, list):
                            set_1.add(entity2cluster[ent[0]])
                        else:
                            set_1.add(entity2cluster[ent])
                    for ent in events[id2][t]:
                        if isinstance(ent, list):
                            set_2.add(entity2cluster[ent[0]])
                        else:
                            set_2.add(entity2cluster[ent])
                    if len(set_1.intersection(set_2))>0:
                        common+=1
                if common>1:
                    G.add_edge(id1, id2)
    print('Graph construction done!')

    cc = nx.connected_components(G)

    with open(path_to_output, 'w') as output:
        for c in cc:
            answer = dict()
            answer['events'] = list(c)
            json.dump(answer, output, encoding="utf-8", ensure_ascii=False)
            output.write("\n")
    cc = nx.connected_components(G)
    stat = {}
    size = {}
    # with open(path_to_output+"des", 'w') as output2:
    #     for c in cc:
    #         if len(c) not in size:
    #             size[len(c)] = 0
    #         size[len(c)] +=1
    #         check = True
    #         for i in c:
    #             if check:
    #                 type = str(events[i]["type"])
    #                 if type not in stat:
    #                     stat[type] = 0
    #                 stat[type] +=1
    #                 check = False
    #             output2.write(i+":")
    #             output2.write(str(events[i]))
    #             output2.write("\n")
    #             output2.write("\n")
    #         output2.write("\n\n\n\n")
    # with open("/Users/xinhuang/Documents/isi/gaia_proj/res/header/cluster/event_type2.csv", "w") as op:
    #     op.write("type,number\n")
    #     for i in stat:
    #         op.write(i.split("#")[-1])
    #         op.write(",")
    #         op.write(str(stat[i]))
    #         op.write("\n")
    # with open("/Users/xinhuang/Documents/isi/gaia_proj/res/header/cluster/event_size2.csv", "w") as op:
    #     op.write("size,number\n")
    #     for i in size:
    #         op.write(str(i))
    #         op.write(",")
    #         op.write(str(size[i]))
    #         op.write("\n")

if __name__ == '__main__':
    main(sys.argv[1:])

def get_resolved_entity(edgelist,path_to_cluster_heads,path_to_new_cluster_head):

    entity2clusters = {}
    G = nx.Graph()

    with open(edgelist) as edges:
        G.add_nodes_from(literal_eval(edges.readline()))
        for edge in edges:
            edge_nodes = literal_eval(edge)
            G.add_edge(edge_nodes[0], edge_nodes[1])

    cc = nx.connected_components(G)
    assigned_ent = 1
    cluster_heads = json.load(open(path_to_cluster_heads))

    for c in cc:
        for e in c:
            entity2clusters[e] = str(assigned_ent)
            cluster_heads[e].append("cluster_id_"+str(assigned_ent))
        assigned_ent +=1;

    with open(path_to_new_cluster_head, 'w') as output:
        json.dump(cluster_heads, output)
    return entity2clusters
