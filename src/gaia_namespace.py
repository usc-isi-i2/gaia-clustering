from rdflib import URIRef
from rdflib.namespace import Namespace

AidaDomainOntologiesCommon = Namespace('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/AidaDomainOntologiesCommon#')
AidaSeedling = Namespace('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/SeedlingOntology#')
AidaInterchange = Namespace('https://tac.nist.gov/tracks/SM-KBP/2018/ontologies/InterchangeOntology#')

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
    # AidaSeedling.Money,
    # AidaSeedling.NumericalValue,
    # AidaSeedling.Results,
    # AidaSeedling.Sentence,
    # AidaSeedling.Sides,
    # AidaSeedling.Time,
    # AidaSeedling.Title,
    # AidaSeedling.URL,
    AidaSeedling.Weapon,
    AidaSeedling.Vehicle
]

ENTITY_TYPE_STR = [t.toPython() for t in ENTITY_TYPE]