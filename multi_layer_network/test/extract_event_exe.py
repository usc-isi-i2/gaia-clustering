import sys
sys.path.append("..")
import src.extract_events as ee


inputfile =  "/Users/xinhuang/Downloads/gaia-entity-resolution/multi_layer_network/data/final_kb_xling1.tac"
outputfile =  "../data_out/extracted_event2.json"
entity_strings = "/Users/xinhuang/Downloads/gaia-entity-resolution/multi_layer_network/data/Entity_strings.json"
string_strings = "/Users/xinhuang/Downloads/gaia-entity-resolution/multi_layer_network/data/String_strings.json"
excep =  "../data_out/unable.txt"
ee.extract_events(inputfile, outputfile, entity_strings, string_strings,excep)