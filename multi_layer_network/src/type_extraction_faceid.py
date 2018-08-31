import codecs
import AIF_RPI_to_JSON as r2j
import  json


def get_statement(path_to_KB_file,type_string,statement_string):

    """
        :param path_to_KB_file:
        :param type_string:
        :param statement_string:
        :return statement set:
    """
    statement_set = set()

    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if statement_string  in line:
                triple = r2j.parse_line_into_triple(line)
                if unicode(triple["predicate"]) == type_string and unicode(triple["object"]) == statement_string:
                    statement_set.add(unicode(triple["subject"]))
    return statement_set

def get_cluster(path_to_KB_file,type_string,cluster_string):
    return get_statement(path_to_KB_file, type_string, cluster_string);


def get_entity2cluster(path_to_KB_file,clu_string,cluster_set,men_string):
    id2cluster = {}
    entity2cluster = {}
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if clu_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                cluster = unicode(triple["object"])
                if (not statement in cluster_set) or predicate != clu_string:
                    continue
                id2cluster[statement] = cluster.split("/")[-1]
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if men_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                entity = unicode(triple["object"])
                if (not statement in cluster_set) or predicate != men_string:
                    continue
                entity2cluster[entity] = id2cluster[statement]
    return entity2cluster


def get_statement2type(path_to_KB_file,statement_set,object_string,predicate_string,type_string):

    """
        :param path_to_KB_file:
        :param statement_set:
        :param subject_string:
        :return object_string:
    """
    statement2type = {}
    valideType = set()
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if predicate_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                type_str = unicode(triple["object"])
                if (not statement in statement_set) or predicate != predicate_string or type_str !=type_string:
                    continue
                valideType.add(statement)

            if object_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                type_exact = unicode(triple["object"])
                if (not statement in statement_set) or predicate != object_string:
                    continue
                statement2type[statement] = type_exact
    statement2type_valid = {}
    for i in statement2type:
        if i in valideType:
            statement2type_valid[i] = statement2type[i]
    return  statement2type_valid


def get_entity(path_to_KB_file, type_string, entity_string):
    return get_statement(path_to_KB_file, type_string, entity_string);


def get_entity2type(path_to_KB_file,statement2type,entity_set,defult_type,subject_string):

    """
        :param path_to_KB_file:
        :param type_string:
        :param statement_string:
        :return statement set:
    """

    entity2type = {}
    for i in entity_set:
        entity2type[i] = set()
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if subject_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                entity = unicode(triple["object"])
                if (not statement in statement2type.keys()) or predicate != subject_string or entity not in entity_set:
                    continue
                entity2type[entity] = statement2type[statement]
    for i in entity2type:
        if len(entity2type[i]) == 0:
            entity2type[i] = defult_type
    return  entity2type


def extract_canonical_mentions_as_cluster_heads(path_to_KB_file, path_to_output, entity2type,entity2cluster,print_counter=False):

    """

    :param path_to_KB_file:
    :param path_to_output:
    :param print_counter:
    :return:
    """
    entity_type_set = set()
    entity_type_set.add('http://darpa.mil/aida/interchangeOntology#Entity')
    skosLabelDict = dict()
    # EntitySet = set()
    LinkDict = dict()
    LinkTargetDict = dict()
    TypeDict = {}
    for i in entity2type:
        TypeDict[i] = entity2type[i]
    answer_dict = dict()

    #pass 1
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if 'http://darpa.mil/aida/interchangeOntology#linkTarget' not in line:
                continue
            else:
                triple = r2j.parse_line_into_triple(line)
                LinkTargetDict[str(triple['subject'])] = unicode(triple['object'])


    # pass 2
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if not ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in line or 'http://www.w3.org/2004/02/skos/core#prefLabel'\
                in line or 'http://darpa.mil/aida/interchangeOntology#link' in line or"http://www.w3.org/1999/02/22-rdf-syntax-ns#subject" in line):
                continue
            # print 'yes'
            triple = r2j.parse_line_into_triple(line)
            if triple is None:
                continue
            #if str(triple['predicate']) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'\
            #        and str(triple['object']) in entity_type_set:
            #    TypeDict[str(triple['subject'])] = str(triple['object'])
            '''
            if str(triple['predicate']) == 'http://www.w3.org/2004/02/skos/core#prefLabel'\
                    and triple['isObjectURI'] is False:
                skosLabelDict[str(triple['subject'])] = unicode(triple['object'])
            '''

            if str(triple['predicate']) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#subject' and "NamedPER" in str(triple['subject']):
                #print str(triple['subject'])
                skosLabelDict[str(triple['object'])] = unicode(triple['object'].split("/")[-1])

            if str(triple['predicate']) == 'http://darpa.mil/aida/interchangeOntology#link':
                # if '_:B53394235X2D5a76X2D455fX2D9066X2D28da330630b5' in line:
                #     print triple
                LinkDict[str(triple['subject'])] = LinkTargetDict[str(triple['object'])]

    # common_entities = set(skosLabelDict.keys()).intersection(set(LinkDict.keys())).intersection(set(TypeDict.keys()))
    # print 'found ',len(common_entities),' entities that have a prefLabel and link.'
    count = 0
    print skosLabelDict
    print TypeDict.keys()
    for e in TypeDict.keys():# these are all entities
        answer_dict[e] = list()
        if e in skosLabelDict:
            answer_dict[e].append(skosLabelDict[e])
        elif e in entity2cluster:
            answer_dict[e].append(entity2cluster[e])
        else:
            answer_dict[e].append('pref_name_missing'+str(count))
        if e in TypeDict:
            answer_dict[e].append(TypeDict[e])
        else:
            answer_dict[e].append("_")
        if e in LinkDict:
            answer_dict[e].append(LinkDict[e])
        else:
            answer_dict[e].append('DUMMY-NIL'+str(count))
            count += 1
    json.dump(answer_dict, codecs.open(path_to_output, 'w', encoding='utf-8'), encoding="utf-8",ensure_ascii=False)




