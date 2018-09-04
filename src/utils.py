from SPARQLWrapper import SPARQLWrapper
import json, os

ENDPOINT = 'http://gaiadev01.isi.edu:3030/rpi0901aida9979/query'
PREFIX = '''
PREFIX aida: <https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xij: <http://isi.edu/xij-rule-set#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ldcOnt: <https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#>
'''
ldcOnt = "https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#"
ENTITY_TYPE = [
    ldcOnt + "Organization",
    ldcOnt + "Person",
    ldcOnt + "GeopoliticalEntity",
    ldcOnt + "Location",
    ldcOnt + "Facility",
    ldcOnt + "Weapon",
    ldcOnt + "Vehicle"
]

sw = SPARQLWrapper(ENDPOINT)


def query_type_sparql(uri):
    return 'SELECT ?t WHERE {?r a rdf:Statement; rdf:subject <%s>; rdf:predicate rdf:type; rdf:object ?t}' % uri


def select(query_str):
    sw.setQuery(PREFIX + query_str)
    sw.setReturnFormat('json')
    return sw.query().convert()['results']['bindings']


def dump_json(json_dict, file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'w') as f:
        json.dump(json_dict, f, indent=2)

