from baseline2_exe import run_with_file_io

output = ""
entity_edgelist = output + "edgelist"
entity_json = output + "run1_entity.json"
event_json = output + "run1_event.json"

run_with_file_io(entity_edgelist, entity_json, event_json, output)
