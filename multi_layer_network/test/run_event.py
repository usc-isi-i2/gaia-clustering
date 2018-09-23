from baseline2_exe import run_with_file_io

output = "/Users/xinhuang/Documents/isi/clustering/run1_test_new/"
entity_edgelist = output + "fri_entity.edgelist"
entity_json = output + "run1_entity.json"
event_json = output + "run1_event.json"

run_with_file_io(entity_edgelist, entity_json, event_json, output)
