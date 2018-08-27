import sys
sys.path.append("..")
from src.change_type_for_multi_file import *
statement_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement")
type_string= unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
subject_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")
object_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")
entity_string = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity")
default_type = unicode('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity')
predicate_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")
cluster_string = unicode("http://www.isi.edu/aida/interchangeOntology#ClusterMembership")
clu_string = unicode("http://www.isi.edu/aida/interchangeOntology#cluster")
men_string = unicode("http://www.isi.edu/aida/interchangeOntology#clusterMember")
path_to_KB_files = ["/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.nt"#,
                    #"/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/ru_2.nt",
                    #"/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/uk_2.nt"
                    ]

entity2cluster_list = []
entity2type_list = []
for path_to_KB_file in path_to_KB_files:
    statement_set =  get_statement(path_to_KB_file,type_string,statement_string)
    print len(statement_set)

    cluster_set = get_cluster(path_to_KB_file,type_string,cluster_string)
    print len(cluster_set)

    entity2cluster = get_entity2cluster(path_to_KB_file,clu_string,cluster_set,men_string)
    print entity2cluster
    entity2cluster_list.append(entity2cluster)

    statement2type = get_statement2type(path_to_KB_file,statement_set,object_string,predicate_string,type_string)
    print len(statement2type)


    entity_set = get_entity(path_to_KB_file,type_string,entity_string)
    print len(entity_set)

    entity2type = get_entity2type(path_to_KB_file,statement2type,entity_set,entity_string,subject_string)
    print len(entity2type)
    entity2type_list.append(entity2type)


output_file = "/Users/xinhuang/Documents/isi/gaia_proj/en_2.json"

extract_canonical_mentions_as_cluster_heads(path_to_KB_files,output_file,entity2type_list,entity2cluster_list)
