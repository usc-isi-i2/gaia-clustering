import sys
import json
import getopt
import networkx as nx
from namespaces import ENTITY_TYPE_STR

def main(argv):
    opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print('Given events JSON file, outputs events linkings in the format of connected components according to '
                  'baseline #1, usage: python event_baseline.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    event_baseline_linking(inputfile, outputfile)

def jaccard_similarity(list1, list2):
    intersection = len((set(list1).intersection(set(list2))))
    union = (len(list1) + len(list2)) - intersection
    if union == 0:
        return 0
    return float(intersection / union)


def event_baseline_linking(events, entity2cluster, stat_output=None):

    IDs = list(events.keys())
    G = nx.Graph()
    G.add_nodes_from(IDs)
    for i, id1 in enumerate(IDs):
        for j in range(i + 1, len(IDs)):
            id2 = IDs[j]
            if events[id1]['type'] == events[id2]['type']:
                common = 0
#                 What is this ? :
#                             set_1.add(entity2cluster[ent])
                all_entity_1 = set()
                all_entity_2 = set()
                for ii in ENTITY_TYPE_STR:
                    for x in events[id1][ii]:
                        all_entity_1.add(entity2cluster[x[0]])
                    for x in events[id2][ii]:
                        all_entity_2.add(entity2cluster[x[0]])
                        if jaccard_similarity(all_entity_1,all_entity_2)>=0.1:
                            G.add_edge(id1, id2)
    print('Graph construction done!')

    cc = nx.connected_components(G)


#     with open(path_to_output, 'w') as output:
#         for c in cc:
#             answer = dict()
#             answer['events'] = list(c)
#             json.dump(answer, output)
#             output.write("\n")
#     cc = nx.connected_components(G)
    if stat_output:
        stat = {}
        size = {}
        with open(path_to_output+"des", 'w') as output2:
            for c in cc:
                if len(c) not in size:
                    size[len(c)] = 0
                size[len(c)] +=1
                check = True
                if len(c) == 1:
                    continue
                for i in c:
                    if check:
                        type = str(events[i]["type"])
                        if type not in stat:
                            stat[type] = 0
                        stat[type] +=1
                        check = False
                    output2.write(i+":")
                    output2.write(str(events[i]))
                    output2.write("\n")
                    output2.write("\n")
                output2.write("\n\n\n\n")

    ret = [{'events': list(c)} for c in cc]
    return ret


def get_resolved_entity(G, cluster_heads):
    entity2clusters = {}
    cc = nx.connected_components(G)
    assigned_ent = 1

    for c in cc:
        for e in c:
            entity2clusters[e] = str(assigned_ent)
            cluster_heads[e].append("cluster_id_" + str(assigned_ent))
        assigned_ent += 1

    return entity2clusters
