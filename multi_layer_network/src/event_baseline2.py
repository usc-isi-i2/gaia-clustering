import sys
import json
import getopt
import networkx as nx
from src.namespaces import ENTITY_TYPE_STR



def jaccard_similarity(list1, list2):
    intersection = len((set(list1).intersection(set(list2))))
    union = (len(list1) + len(list2)) - intersection
    if union == 0:
        return 0
    return float(intersection / union)



def event_baseline_linking(events, entity2cluster, stat_output=None, path_output = None):

    IDs = list(events.keys())
    type_event_map = {}
    for i in IDs:
        type_ = events[i]['type']
        if type_ not in type_event_map:
            type_event_map[type_] = []
        type_event_map[type_].append(i)
    print(len(type_event_map))
    G = nx.Graph()
    G.add_nodes_from(IDs)
    count = 0
    for id_type in type_event_map:
        print(count)
        count += 1
        id_in_Type = type_event_map[id_type]
        for i, id1 in enumerate(id_in_Type):
            for j in range(i + 1, len(id_in_Type)):
                id2 = id_in_Type[j]
                if events[id1]['type'] == events[id2]['type']:
                    all_entity_1 = set()
                    all_entity_2 = set()
                    for x in events[id1]["entities"]:
                         all_entity_1.add(entity2cluster[x])
                    for x in events[id2]["entities"]:
                         all_entity_2.add(entity2cluster[x])
                    if jaccard_similarity(all_entity_1, all_entity_2) >= 0.3:
                        G.add_edge(id1, id2)
                    # # for ii in ENTITY_TYPE_STR:
                    #     for x in events[id1][ii]:
                    #         all_entity_1.add(entity2cluster[x[0]])
                    # #    for x in events[id2][ii]:
                    #         all_entity_2.add(entity2cluster[x[0]])
                    #         if jaccard_similarity(all_entity_1,all_entity_2)>=0.1:
                    #             G.add_edge(id1, id2)
    print('Graph construction done!')



    if stat_output:
        cc = nx.connected_components(G)
        stat = {}
        size = {}
        with open(path_output, 'w') as output2:
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
                
    cc = nx.connected_components(G)
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
