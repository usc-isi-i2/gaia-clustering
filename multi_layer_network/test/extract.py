import src.event_extraction  as ee
import src.type_extraction as te
import json
import codecs

statement_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement")
type_string= unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
subject_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")
object_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")
entity_string = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity")
event_type = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Event")
default_type = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#Entity")
predicate_string = unicode("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")
prefname_string = unicode("http://www.w3.org/2004/02/skos/core#prefLabel")
path_to_KB_file = "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/en_2.nt"
justification_string = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#TextJustification")
source_string = unicode("https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#source")
jusby_string = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#justifiedBy"
hasname_string = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#hasName"

statement_set =  te.get_statement(path_to_KB_file,type_string,statement_string)

print len(statement_set)

statement2type = te.get_statement2type(path_to_KB_file,statement_set,object_string,predicate_string,type_string)
print len(statement2type)

entity_string = te.get_entity(path_to_KB_file,type_string,entity_string)
print len(entity_string)

entity2type = te.get_entity2type(path_to_KB_file,statement2type,entity_string,default_type,subject_string)
print len(entity2type)

event_string = ee.get_event(path_to_KB_file,type_string,event_type)
print len(event_string)


event2type = ee.get_event2type(path_to_KB_file,statement2type,event_string,event_type,subject_string)
print len(event2type)



event2entity = ee.get_event2entity(path_to_KB_file,statement_set,entity_string,event_string,object_string,subject_string)
print len(event2entity)

entity2name = ee.get_entity2prefName(path_to_KB_file,entity_string,hasname_string)
event2ep = ee.make_dict_precise(event2entity, entity2type, entity2name)


justification_set = ee.get_textjustification(path_to_KB_file,type_string,justification_string)
justification2source = ee.gef_justification2source(path_to_KB_file,justification_set,source_string)
justification2label = ee.get_justification2prefLabel(path_to_KB_file,justification_set,prefname_string)
event2prefName = ee.get_event2prefName(path_to_KB_file,event_string,justification_set,jusby_string,justification2label)
event2doc = ee.get_event2doc(path_to_KB_file,event_string,justification_set,jusby_string,justification2source)
print len(event2doc)
print len(event2prefName)



doc2event = {}
for i in event2doc:
    event = i;
    doc = event2doc[i][0]
    if doc not in doc2event:
        doc2event[doc] = []
    doc2event[doc].append(event);
json.dump(doc2event, codecs.open("/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/doc2event_2.json", 'w', 'utf-8'))


ee.extract_canonical_mentions_as_cluster_heads(event2doc,
                                               event2type,
                                               event2ep,
                                               event2prefName,
                                               "/Users/xinhuang/Documents/isi/gaia_proj/ta1/rpi/rpi_dryrun_background_non_eval_result_v0.1/extracted_even_2.json"
                                               )
