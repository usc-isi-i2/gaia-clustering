import re
import sys
import json
import getopt
import gzip
from rdflib import Graph
from rdflib.term import Literal, URIRef, BNode
import codecs

from collections import defaultdict


### Given RPI ColdStart input, produces the JSON file that will be used by the rest of the pipeline. ###

def main(argv):
	opts, _ = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

	for opt, arg in opts:
		if opt == '-h':
			print('Given RPI ColdStart input, produces the JSON file that will be used by the rest of the pipeline, usage: python AIF_RPI_to_JSON.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	if '.gz' in inputfile:
		extract_canonical_mentions_as_cluster_heads_GZIP(inputfile, outputfile)
	else:
		extract_canonical_mentions_as_cluster_heads(inputfile, outputfile)


def parse_line_into_triple(line):
	"""
    Convert a line into subject, predicate, object, and also a flag on whether object is a literal or URI.
    At present we assume all objects are URIs. Later this will have to be changed.
    :param line:
    :return:
    """
	# fields = re.split('> <', line[1:-2])
	# print fields
	answer = dict()
	g = Graph().parse(data=line, format='nt')
	for s, p, o in g:
		answer['subject'] = s
		answer['predicate'] = p
		answer['object'] = o

	if 'subject' not in answer:
		return None
	else:
		answer['isObjectURI'] = (type(answer['object']) != Literal)
		return answer

def extract_canonical_mentions_as_cluster_heads(path_to_KB_file, path_to_output, print_counter=False):

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
	TypeDict = dict()
	answer_dict = dict()

	#pass 1
	with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
		for line in f:
			if 'http://darpa.mil/aida/interchangeOntology#linkTarget' not in line:
				continue
			else:
				triple = parse_line_into_triple(line)
				LinkTargetDict[str(triple['subject'])] = unicode(triple['object'])
				# if '_:B53394235X2D5a76X2D455fX2D9066X2D28da330630b5' in line:
				# 	print line
				# 	print triple
				# break

	# sys.exit(-1)
	# pass 2
	with codecs.open(path_to_KB_file, 'r', 'utf-8') as f:
		for line in f:
			if not ('http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in line or 'http://www.w3.org/2004/02/skos/core#prefLabel'\
				in line or 'http://darpa.mil/aida/interchangeOntology#link' in line):
				continue
			# print 'yes'
			triple = parse_line_into_triple(line)
			if triple is None:
				continue
			if str(triple['predicate']) == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'\
					and str(triple['object']) in entity_type_set:
				TypeDict[str(triple['subject'])] = str(triple['object'])
			if str(triple['predicate']) == 'http://www.w3.org/2004/02/skos/core#prefLabel'\
					and triple['isObjectURI'] is False:
				skosLabelDict[str(triple['subject'])] = unicode(triple['object'])
			if str(triple['predicate']) == 'http://darpa.mil/aida/interchangeOntology#link':
				# if '_:B53394235X2D5a76X2D455fX2D9066X2D28da330630b5' in line:
				# 	print triple
				LinkDict[str(triple['subject'])] = LinkTargetDict[str(triple['object'])]

	# common_entities = set(skosLabelDict.keys()).intersection(set(LinkDict.keys())).intersection(set(TypeDict.keys()))
	# print 'found ',len(common_entities),' entities that have a prefLabel and link.'
	count = 0
	for e in TypeDict.keys(): # these are all entities
		answer_dict[e] = list()
		answer_dict[e].append(skosLabelDict[e])
		answer_dict[e].append(TypeDict[e])
		if e in LinkDict:
			answer_dict[e].append(LinkDict[e])
		else:
			answer_dict[e].append('DUMMY-NIL'+str(count))
			count += 1
	json.dump(answer_dict, codecs.open(path_to_output, 'w', 'utf-8'))

def extract_canonical_mentions_as_cluster_heads_GZIP(path_to_KB_file, path_to_output, print_counter=True):
	cluster_heads = defaultdict(list)
	type_look_up_table = {}
	link_look_up_table = defaultdict(lambda: '')
	count = 0

	with gzip.open(path_to_KB_file, 'r') as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'type':
				type_look_up_table[fields[0]] = fields[2][:-1]
			if fields[1] == 'link':
				link_look_up_table[fields[0]] = fields[2][:-1]

	count = 0
	with gzip.open(path_to_KB_file) as KB:
		for line in KB:
			if print_counter:
				count += 1
				if count % 100000 == 0:
					print 'processing line ',str(count)
			fields = re.split('\t', line)
			if len(fields) < 2: continue
			if fields[1] == 'canonical_mention':
				if fields[0][1:7] != 'Entity': continue

				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(fields[2].lower())
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(type_look_up_table[fields[0]])
				cluster_heads[fields[0][1:] + ':' + re.split(':', fields[3])[0]].append(link_look_up_table[fields[0]])

	print(len(cluster_heads)) # each cluster head contains three elements: canonical mention, type, EDL link

	with open(path_to_output, 'w') as output:
		json.dump(cluster_heads, output)

# if __name__ == '__main__':
# 	main(sys.argv[1:])
# http://darpa.mil/aida/interchangeOntology#Event
#extract_canonical_mentions_as_cluster_heads('/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling.nt',
#	'/Users/mayankkejriwal/Dropbox/gaia-private/seedling-corpus/coldstart-to-interchange/RPI_clusters_seedling_cluster_heads.json',)


