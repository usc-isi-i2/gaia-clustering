from from_jsonhead2cluster import run_with_file_io


# output = "/Users/dongyuli/isi/jsonhead/1003r2nl/"
# output = "/Users/dongyuli/isi/jsonhead/1003r1wl/"
output = "/Users/dongyuli/isi/jsonhead/1003r4nl/"

entity_json = output + "entity.json"
entity_file = output + "cluster.json"

run_with_file_io(entity_json, entity_file, output)
