import sys
import os
import json
import networkx as nx
from ast import literal_eval
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import multi_layer_network.src.event_baseline2 as eb2



def run(entity_edgelist, entity_heads, event_heads, outputs_prefix):
    # entity_heads will be modified in eb2.get_resolved_entity: ('entity2.json')
    entity2cluster = eb2.get_resolved_entity(entity_edgelist, entity_heads)
    print(len(entity2cluster))
    path_to_output = outputs_prefix + "event.jl"
    event_jl = eb2.event_baseline_linking(event_heads, entity2cluster)
    with open(path_to_output, 'w') as f:
        for line in event_jl:
            json.dump(line, f)
            f.write('\n')
    return event_jl


def load_edgelist_from_file(edgelist_file):
    G = nx.Graph()
    with open(edgelist_file, "r") as edges:
        G.add_nodes_from(literal_eval(edges.readline()))
        for edge in edges:
            edge_nodes = literal_eval(edge)
            G.add_edge(edge_nodes[0], edge_nodes[1])
    return G


def run_with_file_io(edgelist_file, entity_head_file, event_head_file, outputs_prefix):
    '''

    :param edgelist_file: file path of the entity edgelist
    :param entity_head_file: file path of the entity json head
    :param event_head_file: file path of the event json head
    :param outputs_prefix: path of the output folder of jl file
    :return: event jl
    '''
    edgelist = load_edgelist_from_file(edgelist_file)
    with open(entity_head_file) as f:
        entity_head = json.load(f)
    with open(event_head_file) as f:
        event_head = json.load(f)
    event_jl = run(edgelist, entity_head, event_head, outputs_prefix)
    return event_jl

