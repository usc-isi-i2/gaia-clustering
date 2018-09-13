from SPARQLWrapper import SPARQLWrapper
import json
import os
from gaia_namespace import ENTITY_TYPE_STR


PREFIX = '''
PREFIX aida: <https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
'''

def query_type_sparql(uri):
    return 'SELECT ?t WHERE {?r a rdf:Statement; rdf:subject <%s>; rdf:predicate rdf:type; rdf:object ?t}' % uri


def select(query_str, endpoint):
    sw = SPARQLWrapper(endpoint.rstrip('/') + '/query')
    sw.setQuery(PREFIX + query_str)
    sw.setReturnFormat('json')
    return sw.query().convert()['results']['bindings']


def dump_json(json_dict, file_path):
    with open(os.path.join(os.path.dirname(__file__), file_path), 'w') as f:
        json.dump(json_dict, f, indent=2)


def load_entity_image(endpoint):
    entity_json = {}
    q = '''
    SELECT ?e ?cluster ?type ?linkTarget
    WHERE {
        ?e a aida:Entity.
        ?x aida:cluster ?cluster ;
           aida:clusterMember ?e .
        ?r a rdf:Statement ;
            rdf:subject ?e ;
            rdf:predicate rdf:type ;
            rdf:object ?type .
    }
    '''
    for x in select(q, endpoint):
        name = x['cluster']['value'].rsplit('/', 1)[-1]
        if name.isdigit():
            name = ''
        entity_json[x['e']['value']] = [name, x['type']['value'], '']
    return entity_json


def load_entity(endpoint):
    entity_json = {}
    q = '''
    SELECT DISTINCT ?e ?name ?translate ?type ?linkTarget
    WHERE {
        ?e a aida:Entity ;
           aida:hasName ?name ;
           aida:link ?link .
        ?link aida:linkTarget ?linkTarget .
        ?r a rdf:Statement ;
            rdf:subject ?e ;
            rdf:predicate rdf:type ;
            rdf:object ?type .
        OPTIONAL {
            ?e aida:justifiedBy ?j .
            ?j skos:prefLabel ?name ;
                aida:privateData ?pd .
            ?pd aida:jsonContent ?translate ;
                aida:system <http://www.rpi.edu/EDL_Translation>
        }
    } 
    '''
    for x in select(q, endpoint):
        try:
            trans_name = json.loads(x['translate']['value'])[0]
            entity_json[x['e']['value']] = [trans_name, x['type']['value'], x['linkTarget']['value']]
        except Exception:
            entity_json[x['e']['value']] = [x['name']['value'], x['type']['value'], x['linkTarget']['value']]
    return entity_json


def load_event(entity_json, endpoint):
    event_json = {}
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
    bindings = select(q, endpoint)
    cnt = 0
    total = len(bindings)
    for x in bindings:
        # evt_uri = http://www.isi.edu/gaia/events/44810d21-cefa-4853-a46e-becb8ba2b395
        evt_uri = x['e']['value']
        event_json[evt_uri] = {'type': x['type']['value'], 'doc': x['doc']['value']}
        q_text = '''
        SELECT DISTINCT ?text ?translate
        WHERE {
          <%s> a aida:Event ;
               aida:justifiedBy ?j .
          ?j skos:prefLabel ?text .
            OPTIONAL {
                ?j aida:privateData ?pd .
                ?pd aida:jsonContent ?translate ;
                    aida:system <http://www.rpi.edu/EDL_Translation>
            }
        }
        ''' % evt_uri
        try:
            event_json[evt_uri]['text'] = [json.loads(record['translate']['value'])[0] for record in select(q_text, endpoint)]
        except Exception:
            event_json[evt_uri]['text'] = [record['text']['value'] for record in select(q_text, endpoint)]

        for t in ENTITY_TYPE_STR:
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
        for record in select(q_ent, endpoint):
            ent = record['ent']['value']
            ent_name = entity_json[ent][0]
            ent_type = entity_json[ent][1] # if entity_json else select(query_type_sparql(ent), endpoint)[0]['t']['value']
            event_json[evt_uri][ent_type].append([ent, ent_name])
        cnt += 1
        if cnt % 1000 == 0:
            print('   %d of %d' % (cnt, total))
    print(' - load event done')
    return event_json

# after upload entity clusters:
# TODO: add into script
def generate_relation_jl(endpoint, output):
    groups = {}
    q = '''
    SELECT distinct ?e ?type
    WHERE {
        ?e a aida:Relation .
        ?r a rdf:Statement ;
           rdf:subject ?e ;
           rdf:predicate rdf:type ;
           rdf:object ?type .
    } 
    '''
    bindings = select(q, endpoint)
    cnt = 0
    total = len(bindings)
    for x in bindings:
        rel_uri = x['e']['value']
        links = []
        q_link = '''
        SELECT DISTINCT ?p ?cluster
        WHERE {
        ?r a rdf:Statement ;
           rdf:subject <%s> ;
           rdf:predicate ?p ;
           rdf:object ?ent .
        ?mem aida:cluster ?cluster ;
            aida:clusterMember ?ent .
        }
        ''' % rel_uri
        for record in select(q_link, endpoint):
            pred = record['p']['value']
            cluster = record['cluster']['value']
            links.append((pred.rsplit('#', 1)[-1], cluster.rsplit('#', 1)[-1]))
        attr = x['type']['value'].rsplit('#', 1)[-1] + str(sorted(links))
        if attr not in groups:
            groups[attr] = []
        groups[attr].append(rel_uri)
        cnt += 1
        if cnt % 200 == 0:
            print('   %d of %d' % (cnt, total))
    jl = []
    for v in groups.values():
        jl.append({'relations': v})
    with open(output.rstrip('/') + '/relation.jl', 'w') as f:
        for j in jl:
            json.dump(j, f)
            f.write('\n')

