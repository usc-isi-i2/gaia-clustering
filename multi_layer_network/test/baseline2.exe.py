import sys

sys.path.append("..")
import src.event_baseline2 as eb2

edgelist = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/entity.edgelist"
path_to_cluster_heads = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/entity.json"
path_to_new_cluster_head = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/entity2.json"
input_file = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/event.json"
path_to_output = "/Users/xinhuang/Documents/isi/clustering/gaia-clustering/outputs/event.jl"

entity2cluster = eb2.get_resolved_entity(edgelist, path_to_cluster_heads, path_to_new_cluster_head)
print(len(entity2cluster))
eb2.event_baseline_linking(input_file, path_to_output, entity2cluster)
