import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
import src.event_baseline2 as eb2

# outputs_prefix = '/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/'
outputs_prefix = '/Users/dongyuli/isi/repos/gaia-clustering/outputs/' if len(sys.argv) < 2 else (sys.argv[1].rstrip('/') + '/')

edgelist = outputs_prefix + "entity.edgelist"
path_to_cluster_heads = outputs_prefix + "entity.json"
path_to_new_cluster_head = outputs_prefix + "entity2.json"
input_file = outputs_prefix + "event.json"
path_to_output = outputs_prefix + "event.jl"

entity2cluster = eb2.get_resolved_entity(edgelist,path_to_cluster_heads,path_to_new_cluster_head)
print len(entity2cluster)
eb2.event_baseline_linking(input_file, path_to_output,entity2cluster)
