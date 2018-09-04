from utils import *


def load_entity():
    entity_json = {}
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
    return entity_json


def load_event(entity_json=None):
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
        SELECT DISTINCT ?ent ?ent_name
        WHERE {
        ?r a rdf:Statement ;
           rdf:subject <%s> ;
           rdf:predicate ?p ;
           rdf:object ?ent .
        ?ent a aida:Entity ;
             aida:hasName ?ent_name .
        }
        ''' % evt_uri
        for record in select(q_ent):
            ent = record['ent']['value']
            ent_name = record['ent_name']['value']
            ent_type = entity_json[ent][1] if entity_json else select(query_type_sparql(ent))[0]['t']['value']
            event_json[evt_uri][ent_type].append([ent, ent_name])
        cnt += 1
        if cnt % 200 == 0:
            print('   %d of %d' % (cnt, total))
    print(' - load event done')
    return event_json

