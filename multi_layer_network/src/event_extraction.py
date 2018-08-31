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




def get_textjustification(path_to_KB_file,type_string,justification_string):
    justification_set = set()

    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if justification_string in line:
                triple = r2j.parse_line_into_triple(line)
                if unicode(triple["predicate"]) == type_string and unicode(triple["object"]) == justification_string:
                    justification_set.add(unicode(triple["subject"]))
    return justification_set

def get_justification2prefLabel(path_to_KB_file,justification_set,prefLabel_string):
    justification2label = {}
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if prefLabel_string in line:
                triple = r2j.parse_line_into_triple(line)
                justification = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                source = unicode(triple["object"])
                if (not justification in justification_set) or predicate != prefLabel_string:
                    continue
                justification2label[justification] = source
    return justification2label

def gef_justification2source(path_to_KB_file,justification_set,source_string):
    justification2source = {}
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if source_string in line:
                triple = r2j.parse_line_into_triple(line)
                justification = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                source = unicode(triple["object"])
                if (not justification in justification_set) or predicate !=source_string:
                    continue
                justification2source[justification] = source
    return justification2source

def get_event2entity(path_to_KB_file,statement_set,entity_set,event_set,object_string,subject_string):

    """
        :param path_to_KB_file:
        :param statement_set:
        :param subject_string:
        :return object_string:
    """
    hasEventasSubject = set()
    hasEnityasObject = set()
    statement2event = {}
    statement2entity = {}
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if subject_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                event = unicode(triple["object"])
                if statement in statement_set and event in event_set:
                    hasEventasSubject.add(statement)
                    statement2event[statement] = event
            if object_string in  line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                entity = unicode(triple["object"])
                if statement in statement_set and entity in entity_set:
                    hasEnityasObject.add(statement)
                    statement2entity[statement] = entity
    event2entity = {}
    for i in event_set:
        event2entity[i] = set()
    valid_set = hasEnityasObject.intersection(hasEventasSubject)
    for i in valid_set:
        event = statement2event[i]
        entity = statement2entity[i]
        event2entity[event].add(entity)
    return event2entity

def make_dict_precise(event2entity,entity2type,entity2name):
    res = {}
    for event in event2entity:
        entities = event2entity[event]
        dict_ = {}
        for type in list(entity2type.values()):
            dict_[type] = []
        for ent in entities:
            type = entity2type[ent]
            name = entity2name[ent]
            dict_[type].append((ent,name))
        res[event] = dict_
    return res



def get_event(path_to_KB_file, type_string, event_string):
    return get_statement(path_to_KB_file, type_string, event_string);


def get_event2type(path_to_KB_file,statement2type,event_set,defult_type,subject_string):

    """
        :param path_to_KB_file:
        :param type_string:
        :param statement_string:
        :return statement set:
    """

    event2type = {}
    for i in event_set:
        event2type[i] = set()
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if subject_string in line:
                triple = r2j.parse_line_into_triple(line)
                statement = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                entity = unicode(triple["object"])
                if (not statement in statement2type.keys()) or predicate != subject_string or entity not in event_set:
                    continue
                event2type[entity]=statement2type[statement]
    for i in event2type:
        if len(event2type[i]) == 0:
            event2type[i]= defult_type
    return  event2type





def extract_canonical_mentions_as_cluster_heads(event2doc,event2type,event2entity,event2name, path_to_output,print_counter=False):

    """

    :param path_to_KB_file:
    :param path_to_output:
    :param print_counter:
    :return:
    """
    answer_dict = {}
    assert(len(event2doc.keys()) == len(event2entity))
    assert (len(event2entity)==len(event2type))
    #assert (len(event2entity) == len(event2name))
    for event in event2entity:
        dict_ = {}
        dict_["doc"] = ""
        if len(event2doc[event])>0:
            dict_["doc"]=event2doc[event][0]

        entity_dict = event2entity[event]
        for i in entity_dict:
            dict_[i] = entity_dict[i]
        dict_["text"] = event2name[event]
        dict_["type"] = event2type[event]
        answer_dict[event] = dict_
    json.dump(answer_dict, codecs.open(path_to_output, 'w', 'utf-8'))


def get_event2doc(path_to_KB_file,event_set,justification_set,jusby_string,justification2doc):
    event2doc= {}
    for i in event_set:
        event2doc[i]  = []
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if jusby_string in line:
                triple = r2j.parse_line_into_triple(line)
                event = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                justification = unicode(triple["object"])
                if (event in  event_set) and (predicate == jusby_string) and (justification in justification_set) and (justification in justification2doc):
                    event2doc[event].append(justification2doc[justification])
    return event2doc


def get_event2prefName(path_to_KB_file, event_set, justification_set,jusby_string,justification2label):
    event2prefname = {}
    for i in event_set:
        event2prefname[i]  = []
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if jusby_string in line:
                triple = r2j.parse_line_into_triple(line)
                event = unicode(triple["subject"])
                predicate = unicode(triple["predicate"])
                justification = unicode(triple["object"])
                if (event in  event_set) and (predicate == jusby_string) and (justification in justification_set) and (justification in justification2label):
                    event2prefname[event].append(justification2label[justification])
    return event2prefname

def get_entity2prefName(path_to_KB_file, event_set ,prefname_string):
    event2prefname = {}
    with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
        for line in f:
            if prefname_string in line:
                triple = r2j.parse_line_into_triple(line)
                if triple is None:
                    continue
                event_name = unicode(triple['subject'])
                if event_name not in event_set:
                    continue
                if unicode(triple['predicate']) == prefname_string and triple['isObjectURI'] is False:
                    event2prefname[event_name] = unicode(triple['object'])
    return event2prefname