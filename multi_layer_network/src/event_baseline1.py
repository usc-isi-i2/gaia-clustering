import re
import sys
import json
import getopt
import numpy as np
import networkx as nx

from datetime import datetime

def main(argv):
    opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print(
                'Given events JSON file, outputs events linkings in the format of connected components according to baseline #1, usage: python event_baseline.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    event_baseline_linking(inputfile, outputfile)


def event_baseline_linking(path_to_events, path_to_output):

    events = json.load(open(path_to_events))

    IDs = list(events.keys())

    G = nx.Graph()
    G.add_nodes_from(IDs)
    geo_str = "http://darpa.mil/ontologies/SeedlingOntology#GeopoliticalEntity"
    fil_str = "http://darpa.mil/ontologies/SeedlingOntology#FillerType"
    per_str = "http://darpa.mil/ontologies/SeedlingOntology#Person"
    org_str = "http://darpa.mil/ontologies/SeedlingOntology#Organization"
    fac_str = "http://darpa.mil/ontologies/SeedlingOntology#Facility"
    loc_str = "http://darpa.mil/ontologies/SeedlingOntology#Location"
    entity_type =[geo_str,per_str,org_str,fac_str,loc_str]
    for i, id1 in enumerate(IDs):
        for j in range(i + 1, len(IDs)):
            id2 = IDs[j]
            if events[id1]['type'] == events[id2]['type']:
                common = 0

                for t in entity_type:
                    set_1 = set()
                    set_2 = set()
                    for ent in events[id1][t]:
                        set_1.add(ent[0])
                    for ent in events[id2][t]:
                        set_2.add(ent[0])
                    if len(set_1.intersection(set_2)) > 0:
                        common += 1
                if common >=0:
                    G.add_edge(id1, id2)

    print('Graph construction done!')

    cc = nx.connected_components(G)

    with open(path_to_output, 'w') as output:
        for c in cc:
            answer = dict()
            answer['events'] = list(c)
            json.dump(answer, output, encoding="utf-8", ensure_ascii=False)
            output.write("\n")
    cc = nx.connected_components(G)
    with open(path_to_output+"des", 'w') as output2:
        for c in cc:
            if(len(c)==1):
                continue
            for i in c:
                output2.write(i+":")
                output2.write(str(events[i]))
                output2.write("\n")
                output2.write("\n")
            output2.write("\n\n\n\n")


if __name__ == '__main__':
    main(sys.argv[1:])
