from get_jsonhead import load_entity, load_event
from utils import dump_json
# import sys
# sys.path.append("..")
# from multi_layer_network.test.from_jsonhead2cluster import run_from_jsonhead
# from multi_layer_network.test.extract_event_cluster import extract_event

entity_jsonhead = load_entity()
event_jsonhead = load_event(entity_jsonhead)

dump_json(entity_jsonhead, '../outputs/entity0901.json')
dump_json(event_jsonhead, '../outputs/event0901.json')

# run_from_jsonhead(input_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/entity.json',
#                   output_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/entity_cluster.jl'
#                   )


# extract_event(path_to_KB_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/en_3.nt',
#               path_to_jsonhead='/Users/dongyuli/isi/repos/gaia-clustering/outputs/event.json'
#               )
