import re
import sys
import json
import getopt
from collections import defaultdict


# Given RPI ColdStart input, the Entity strings JSON file, and the String strings JSON file,
# produces the events JSON file.

def main(argv):
    opts, _ = getopt.getopt(argv, "hi:e:s:o:", ["ifile=", "efile=", "sfile=", "ofile="])

    for opt, arg in opts:
        if opt == '-h':
            print('Given RPI ColdStart input, the Entity strings JSON file, and the String strings JSON file, produces '
                  'the events JSON file, usage: python extract_events.py -i <inputfile> -e <entitystringsfile> '
                  '-s <stringstringsfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-e", "--efile"):
            entity_strings = arg
        elif opt in ("-s", "--sfile"):
            string_strings = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    extract_events(inputfile, outputfile, entity_strings, string_strings)


def extract_events(path_to_KB_file, path_to_output, path_to_entity_strings, path_to_string_strings, excep):
    entity_strings = json.load(open(path_to_entity_strings))
    string_strings = json.load(open(path_to_string_strings))
    # entity_type_to_dict_key = {'PER': 'PER_entities'} --> I didn't use this.

    events = defaultdict(lambda: dict())
    type_look_up_table = {}
    unabletofind = []
    with open(path_to_KB_file) as KB:
        count = 0
        for line in KB:
            count += 1
            if count % 2000000 == 0:
                print(count)
            fields = re.split('\t', line)
            if len(fields) < 2: continue
            if fields[1] == 'type':
                type_look_up_table[fields[0]] = fields[2][:-1]

    with open(path_to_KB_file) as KB:
        count = 0
        for line in KB:
            fields = re.split('\t', line)
            if len(fields) < 2:
                continue
            if 'mention' in fields[1]:
                if fields[0][1:6] != 'Event':
                    continue
                if len(events) > 10000:
                    continue
                print(line)
                # type
                events[fields[0][1:] + ':' + fields[3]]['type'] = type_look_up_table[fields[0]]

                # text
                events[fields[0][1:] + ':' + fields[3]]['text'] = fields[2]

                # doc
                events[fields[0][1:] + ':' + fields[3]]['doc'] = re.split(':', fields[3])[0]

                # # Date --> not serializable, there are some tricks, but I prefer to use the doc id later.
                # if len(re.split('_', re.split(':', fields[3])[0])) == 5:
                # 	temporal_info = re.split('_', re.split(':', fields[3])[0])[3]
                # # NYT Exception
                # elif re.split(':', fields[3])[0][0:3] == 'NYT':
                # 	temporal_info = re.split('_', re.split(':', fields[3])[0])[2][0:8]
                # event_date = datetime.strptime(temporal_info, '%Y%m%d')
                # events[fields[0][1:] + ':' + fields[3]]['date'] = event_date

                # entities
                events[fields[0][1:] + ':' + fields[3]]['STR_entities'] = []
                events[fields[0][1:] + ':' + fields[3]]['PER_entities'] = []
                events[fields[0][1:] + ':' + fields[3]]['ORG_entities'] = []
                events[fields[0][1:] + ':' + fields[3]]['GPE_entities'] = []
                events[fields[0][1:] + ':' + fields[3]]['LOC_entities'] = []
                events[fields[0][1:] + ':' + fields[3]]['FAC_entities'] = []

            # finding entities #
            elif fields[2].startswith(':Entity'):
                if fields[0][1:6] != 'Event':
                    continue
                count += 1
                if count % 20000 == 0:
                    print(count)
                for event in events:
                    if event.startswith(fields[0][1:]):
                        if fields[2] in entity_strings:
                            print(fields[2])
                            print(event)
                            print('')
                            entity_type = entity_strings[fields[2]]['type'] + '_entities'
                            events[event][entity_type].append(entity_strings[fields[2]]['selected_string'])
                        else:
                            unabletofind.append((event, fields[2]))
            '''
            elif fields[2].startswith(':String'):
                if fields[0][1:6] != 'Event': continue

                for event in events:
                    if event.startswith(fields[0][1:]):
                        events[event]['STR_entities'].append(string_strings[fields[2]]['selected_string'])
            '''
    with open(path_to_output, 'w') as output:
        json.dump(events, output)


if __name__ == '__main__':
    main(sys.argv[1:])
