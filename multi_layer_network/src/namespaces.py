from rdflib.namespace import Namespace, RDF, XSD

AidaDomainOntologiesCommon = Namespace('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/AidaDomainOntologiesCommon#')
AidaSeedling = Namespace('https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/SeedlingOntology#')
AidaInterchange = Namespace('https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#')

namespaces = {
    'aida': Namespace('https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/InterchangeOntology#'),
    'rdf': RDF,
    'xij': Namespace('http://isi.edu/xij-rule-set#'),
    'skos': Namespace('http://www.w3.org/2004/02/skos/core#'),
    'xsd': XSD
}

ENTITY_TYPE = [
    AidaSeedling.Facility,
    # AidaSeedling.FillerType,
    AidaSeedling.GeopoliticalEntity,
    AidaSeedling.Location,
    AidaSeedling.Organization,
    AidaSeedling.Person,
    # AidaSeedling.Age,
    # AidaSeedling.Ballot,
    # AidaSeedling.Commodity,
    # AidaSeedling.Crime,
    # AidaSeedling.Law,
    AidaSeedling.Money,
    AidaSeedling.NumericalValue,
    # AidaSeedling.Results,
    # AidaSeedling.Sentence,
    # AidaSeedling.Sides,
    AidaSeedling.Time,
    AidaSeedling.Title,
    AidaSeedling.URL,
    AidaSeedling.Weapon,
    AidaSeedling.Vehicle
]

COMMON_TYPE = [
    AidaSeedling.Weapon,
    AidaSeedling.Vehicle
]

REAL_ENTTYPE = [
    AidaSeedling.Facility,
    AidaSeedling.GeopoliticalEntity,
    AidaSeedling.Location,
    AidaSeedling.Organization,
    AidaSeedling.Person
]

ENTITY_TYPE_STR = [t.toPython() for t in ENTITY_TYPE]
COMMON_TYPE_STR = [t.toPython() for t in COMMON_TYPE]

REAL_ENTTYPE_STR = [t.toPython() for t in REAL_ENTTYPE]
