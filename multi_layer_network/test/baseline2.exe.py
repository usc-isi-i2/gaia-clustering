import sys
sys.path.append("..")
import src.event_baseline2 as eb2
edgelist = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.edgelist"
path_to_cluster_heads = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.json"
path_to_new_cluster_head ="/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2_new.json"
input_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/extracted_even_2.json"
path_to_output = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/event_test_baseline2_2.jl"
entity2cluster = eb2.get_resolved_entity(edgelist,path_to_cluster_heads,path_to_new_cluster_head)
print len(entity2cluster)
eb2.event_baseline_linking(input_file, path_to_output,entity2cluster)