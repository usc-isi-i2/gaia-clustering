from SPARQLWrapper import SPARQLWrapper
import json
import os


ENDPOINT = 'http://gaiadev01.isi.edu:3030/rpi0826aif0830/query'
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
    ldcOnt + "Facility"
]
OUTPUT_ENTITY = os.path.join(os.path.dirname(__file__), '../outputs/entity_head.json')
OUTPUT_EVENT = os.path.join(os.path.dirname(__file__), '../outputs/event_head.json')

sw = SPARQLWrapper(ENDPOINT)
entity_json = {}
event_json = {}


def dump_file(head_json, out_file):
    with open(out_file, 'w') as f:
        json.dump(head_json, f, indent=2)


def select(query_str):
    sw.setQuery(PREFIX + query_str)
    sw.setReturnFormat('json')
    return sw.query().convert()['results']['bindings']


def load_entity():
    print(' - start - load entity')
    q = '''
    SELECT ?e (MAX(?label) as ?name) ?type ?linkTarget
    WHERE {
        ?e a aida:Entity.
        ?e aida:justifiedBy ?j.
        ?j skos:prefLabel ?label .
        ?r a rdf:Statement ;
            rdf:subject ?e ;
            rdf:predicate rdf:type ;
            rdf:object ?type .
        ?e aida:link ?link .
        ?link aida:linkTarget ?linkTarget .
    } GROUPBY ?e ?type ?linkTarget
    '''
    for x in select(q):
        entity_json[x['e']['value']] = [x['name']['value'], x['type']['value'], x['linkTarget']['value']]
    print(' - done - load entity')


def load_event():
    print(' - start - load event')
    q = '''
    SELECT distinct ?e ?type ?doc
    WHERE {
        ?e a aida:Event; 
           aida:justifiedBy ?j .
        ?j aida:source ?doc .
        ?r a rdf:Statement ;
           rdf:subject ?e ;
           rdf:predicate rdf:type ;
           rdf:object ?type .
    } 
    '''
    bindings = select(q)
    cnt = 0
    total = len(bindings)
    for x in bindings:
        # evt_uri = http://www.isi.edu/gaia/events/44810d21-cefa-4853-a46e-becb8ba2b395
        evt_uri = x['e']['value']
        event_json[evt_uri] = {'type': x['type']['value'], 'doc': x['doc']['value']}
        q_text = '''
        SELECT DISTINCT ?text
        WHERE {
          <%s> a aida:Event ;
               aida:justifiedBy ?j .
          ?j skos:prefLabel ?text .
        }
        ''' % evt_uri
        event_json[evt_uri]['text'] = [record['text']['value'] for record in select(q_text)]

        for t in ENTITY_TYPE:
            event_json[evt_uri][t] = []
        q_ent = '''
        SELECT DISTINCT ?ent
        WHERE {
        ?r a rdf:Statement ;
           rdf:subject <%s> ;
           rdf:predicate ?p ;
           rdf:object ?ent .
        ?ent a aida:Entity .
        }
        ''' % evt_uri
        for record in select(q_ent):
            ent = record['ent']['value']
            ent_type = entity_json[ent][1]
            event_json[evt_uri][ent_type].append(ent)
        cnt += 1
        if cnt % 200 == 0:
            print('   %d of %d' % (cnt, total))
    print(' - done - load event')


def run():
    load_entity()
    dump_file(entity_json, OUTPUT_ENTITY)
    load_event()
    dump_file(event_json, OUTPUT_EVENT)


run()
