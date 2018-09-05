# Python function to print permutations of a given list
import random
import json
import networkx as nx
import jellyfish as jf
import enchant

d = enchant.Dict("en_US")


def getminHash(word, seed):
    random.seed(seed)
    word_dict = {}
    for i in range(26):
        word_dict[i] = chr(i + ord('a'))
    for i in range(ord('\u052f') - ord('\u0400')):
        word_dict[26 + i] = chr(i + ord('\u0400'))
    all_list = list(range(26 + ord('\u052f') - ord('\u0400')))
    hash_code = 0
    while len(all_list) > 0:
        idx = random.randint(0, len(all_list) - 1)
        if word_dict[all_list[idx]] in word:
            return hash_code
        all_list[idx] = all_list[len(all_list) - 1]
        all_list = all_list[:len(all_list) - 1]
        hash_code += 1
    return len(word_dict)


def get_blocking(path_to_cluster_heads, seed1, seed2, transDict, bn_prefix):
    blocks = {}

    cluster_heads = json.load(open(path_to_cluster_heads))
    IDs = list(cluster_heads.keys())
    print(len(IDs))
    count = 0
    for id1 in IDs:
        count += 1
        if count % 10000 == 0:
            print(count * 1.0 / len(IDs))
        word = cluster_heads[id1][0]
        block_name = bn_prefix + str(getminHash(word, seed1) * 100 + getminHash(word, seed2) * 1)
        if block_name not in blocks:
            blocks[block_name] = []
        blocks[block_name].append(id1)
    return blocks


def get_blocking_prefix(path_to_cluster_heads, transDict):
    blocks = {}
    cluster_heads = json.load(open(path_to_cluster_heads))
    IDs = list(cluster_heads.keys())
    for id1 in IDs:
        word = cluster_heads[id1][0]
        can = word.split(" ")
        for i in can:
            block_name = i.lower()[:2]
            if block_name not in blocks:
                blocks[block_name] = []
            blocks[block_name].append(id1)
    return blocks


def same_index(path_to_cluster_heads):
    blocks = {}
    cluster_heads = json.load(open(path_to_cluster_heads))
    IDs = list(cluster_heads.keys())
    for id1 in IDs:
        inx = cluster_heads[id1][2] + cluster_heads[id1][1]
        if "NIL" in inx:
            continue
        if inx not in blocks:
            blocks[inx] = []
        blocks[inx].append(id1)
    return blocks


def get_links_edge_list(path_to_cluster_heads, path_to_output):
    transDict = {}
    cluster_heads = json.load(open(path_to_cluster_heads))
    set_adding = set()
    IDs = list(cluster_heads.keys())

    G = nx.Graph()
    G.add_nodes_from(IDs)
    sid = same_index(path_to_cluster_heads)
    add = 0
    for id in sid:
        if id == '':
            continue
        for i in range(len(sid[id]) - 1):
            G.add_edge(sid[id][i], sid[id][i + 1])

    for ii in range(1, 3):
        block1 = get_blocking(path_to_cluster_heads, ii, ii * 19, transDict, "first")
        print("phase1_" + str(ii))
        count = 0
        print(len(block1))
        sum = 0
        for block in block1:
            sum += len(block1[block]) * (len(block1[block]) - 1) / 2
            count += 1
            if count % 5 == 0:
                print(count)
            for i, id1 in enumerate(block1[block]):
                if len(block1[block]) > 10000:
                    if i % 1000 == 0:
                        print(i)
                for j in range(i + 1, len(block1[block])):
                    id2 = block1[block][j]
                    if cluster_heads[id1][1] == cluster_heads[id2][1] and (cluster_heads[id1][2] != cluster_heads[id2][2] or "NIL" in cluster_heads[id1][2] or "NIL" in cluster_heads[id2][2]):
                        if "NIL" in cluster_heads[id1][2] or "NIL" in cluster_heads[id2][2] and cluster_heads[id1][1] == cluster_heads[id2][1]:
                            name1 = cluster_heads[id1][0]
                            name2 = cluster_heads[id2][0]
                            score = jf.jaro_distance(name1, name2)
                            if (name1[0].upper() != name1[0] or name2[0].upper() != name2[0] or d.check(name1.lower()) or d.check(name2.lower())):
                                continue
                            if score > 0.9:
                                G.add_edge(id1, id2)
        print(sum)
    block1 = get_blocking_prefix(path_to_cluster_heads, transDict)
    count = 0
    print(len(block1))
    sum = 0
    for block in block1:
        sum += len(block1[block]) * (len(block1[block]) - 1) / 2
        count += 1
        if count % 5 == 0:
            print(count)
        for i, id1 in enumerate(block1[block]):
            for j in range(i + 1, len(block1[block])):
                id2 = block1[block][j]
                if cluster_heads[id1][1] == cluster_heads[id2][1] and (
                        cluster_heads[id1][2] != cluster_heads[id2][2] or "NIL" in cluster_heads[id1][2] or "NIL" in
                        cluster_heads[id2][2]):
                    if "NIL" in cluster_heads[id1][2] or "NIL" in cluster_heads[id2][2] and cluster_heads[id1][1] == cluster_heads[id2][1]:

                        name1 = cluster_heads[id1][0]
                        name2 = cluster_heads[id2][0]
                        score = jf.jaro_distance(name1, name2)
                        if (name1[0].upper() != name1[0] or name2[0].upper() != name2[0] or d.check(
                                name1.lower()) or d.check(name2.lower())):
                            continue
                        if score > 0.9:
                            G.add_edge(id1, id2)

    with open(path_to_output, 'w') as output:
        output.write(str(G.nodes()) + '\n')
        for e in G.edges:
            output.write(str(e) + '\n')
