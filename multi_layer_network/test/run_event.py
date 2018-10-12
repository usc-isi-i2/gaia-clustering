from baseline2_exe import run_with_file_io

# output = "/Users/dongyuli/isi/jsonhead/1003r2nl/"
# output = "/Users/dongyuli/isi/jsonhead/1003r1wl/"
output = "/Users/dongyuli/isi/jsonhead/1003r4nl/"
entity_edgelist = output + "entity.edgelist"
entity_json = output + "entity.json"
event_json = output + "event.json"

run_with_file_io(entity_edgelist, entity_json, event_json, output)
