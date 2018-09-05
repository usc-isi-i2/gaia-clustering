import sys
import json
import getopt
import networkx as nx
from ast import literal_eval
from src.gaia_namespace import ENTITY_TYPE_STR

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


def event_baseline_linking(path_to_events, path_to_output,entity2cluster):

    events = json.load(open(path_to_events))

    IDs = list(events.keys())

    G = nx.Graph()
    G.add_nodes_from(IDs)
    for i, id1 in enumerate(IDs):
        for j in range(i + 1, len(IDs)):
            id2 = IDs[j]
            if events[id1]['type'] == events[id2]['type']:
                common = 0
                for t in ENTITY_TYPE_STR:
                    set_1 = set()
                    set_2 = set()
                    for ent in events[id1].get(t, list()):
                        if isinstance(ent, list):
                            set_1.add(entity2cluster[ent[0]])
                        else:
                            set_1.add(entity2cluster[ent])
                    for ent in events[id2].get(t, list()):
                        if isinstance(ent, list):
                            set_2.add(entity2cluster[ent[0]])
                        else:
                            set_2.add(entity2cluster[ent])
                    if len(set_1.intersection(set_2)) > 0:
                        common += 1
                if common > 1:
                    G.add_edge(id1, id2)
    print('Graph construction done!')

    cc = nx.connected_components(G)

    with open(path_to_output, 'w') as output:
        for c in cc:
            answer = dict()
            answer['events'] = list(c)
            json.dump(answer, output)
            output.write("\n")


if __name__ == '__main__':
    main(sys.argv[1:])


def get_resolved_entity(edgelist, path_to_cluster_heads, path_to_new_cluster_head):
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
            cluster_heads[e].append("cluster_id_" + str(assigned_ent))
        assigned_ent += 1

    with open(path_to_new_cluster_head, 'w') as output:
        json.dump(cluster_heads, output)
    return entity2clusters
