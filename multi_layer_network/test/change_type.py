from src.type_extraction import *
statement_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement")
type_string= unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
subject_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")
object_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")
entity_string = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity")
default_type = unicode('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity')
predicate_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")

path_to_KB_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.nt"


statement_set =  get_statement(path_to_KB_file,type_string,statement_string)
print len(statement_set)

statement2type = get_statement2type(path_to_KB_file,statement_set,object_string,predicate_string,type_string)
print len(statement2type)

entity_string = get_entity(path_to_KB_file,type_string,entity_string)
print len(entity_string)

entity2type = get_entity2type(path_to_KB_file,statement2type,entity_string,default_type,subject_string)
print len(entity2type)


input_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.nt"
output_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.json"

extract_canonical_mentions_as_cluster_heads(input_file,output_file,entity2type)