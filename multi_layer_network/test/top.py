import json
from collections import Counter


def get_top_n(ent_attr, n):
    with open(ent_attr) as f:
        ent = f.readlines()

    start = 0
    res = []
    clusters = []
    for i in range(len(ent)):
        if ent[i].strip()[-1] == '}':
            cur = json.loads(''.join(ent[start:i+1]))['entities']
            clusters.append(cur)
            start = i + 1
            labels = [_[0] for _ in cur if _[0]]
            label = Counter(labels).most_common(1)[0][0] if labels else ''
            res.append((label, len(cur), len(res)-1))
    res.sort(key=lambda x: x[1], reverse=True)

    for i in range(min(len(res), n)):
        print(res[i])


# get_top_n("/Users/dongyuli/isi/data/jsonhead_r0nl/entity_with_attr.jl", 30)

# get_top_n("/Users/dongyuli/isi/data/jsonhead_r1aug/entity_with_attr.jl", 30)

# get_top_n("/Users/dongyuli/isi/jsonhead/1003r2nl/entity_with_attr.jl", 30)
# get_top_n("/Users/dongyuli/isi/jsonhead/1003r1wl/entity_with_attr.jl", 30)
get_top_n("/Users/dongyuli/isi/jsonhead/1003r4nl/entity_with_attr.jl", 30)
