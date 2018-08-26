import sys
sys.path.append("..")
import src.event_baseline1 as eb
input_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/extracted_even_id.json"
path_to_output = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/event_test.nl"
eb.event_baseline_linking(input_file, path_to_output)
