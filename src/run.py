from get_jsonhead import *

import sys
# sys.path.append("..")
# from multi_layer_network.test.from_jsonhead2cluster import run_from_jsonhead
# from multi_layer_network.test.extract_event_cluster import extract_event

endpoint = 'http://gaiadev01.isi.edu:3030/rpi0901aida9979' if len(sys.argv) < 3 else sys.argv[1].rstrip('/')
entity_jsonhead = load_entity(endpoint)
event_jsonhead = load_event(entity_jsonhead, endpoint)

json_output = '../outputs' if len(sys.argv) < 3 else sys.argv[2].rstrip('/')
dump_json(entity_jsonhead, '%s/entity.json' % json_output)
dump_json(event_jsonhead, '%s/event.json' % json_output)

# run_from_jsonhead(input_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/entity.json',
#                   output_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/entity_cluster.jl'
#                   )


# extract_event(path_to_KB_file='/Users/dongyuli/isi/repos/gaia-clustering/outputs/en_3.nt',
#               path_to_jsonhead='/Users/dongyuli/isi/repos/gaia-clustering/outputs/event.json'
#               )
