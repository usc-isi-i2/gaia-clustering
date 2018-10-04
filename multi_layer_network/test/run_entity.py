from from_jsonhead2cluster import run_with_file_io


output = "/Users/dongyuli/isi/data/jl_1003r1nl/"

entity_json = output + "entity.json"
entity_file = output + "cluster.json"

run_with_file_io(entity_json, entity_file, output)
