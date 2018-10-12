import json
from src.Entity import Entity
from src.Cluster import Cluster
map_to_freebase = {}
OTHERS = 'others'


def parse_name(name):
    if name.startswith('{'):
        return json.loads('name').get('translation', [''])
    return [name]


def parse_link(link):
    # http://dbpedia.org/resource/Vladimir_Potanin
    # LDC2015E42:NIL00132305
    # LDC2015E42:m.083kb
    if link.startswith('http://dbpedia'):
        return map_to_freebase.get(link, link)
    if link.split(':', 1)[-1].startswith('m.'):
        return link
    return OTHERS


def get_best(elinks, ent: Entity, el2cluster):
    if len(elinks) == 1:
        return el2cluster[list(elinks)[0]]
    max_simi = 0
    max_el = None
    for el in elinks:
        cur_simi = el2cluster[el].calc_similarity(ent)
        if cur_simi > max_simi:
            max_simi = cur_simi
            max_el = el
    return el2cluster[max_el]


def init(entity_json: dict, cluster_json: dict):
    """
    init clusters by external links and original clusters.
    only consider the freebase id and dbpedia link as valid external links.
    need to map the external links in to a same system.
    if entities with same valid external link, cluster them together.
    if a ta1 cluster has 0~1 distinct valid external link, cluster them together.
    remove overlapped clusters .
    :param entity_json: {entity_uri: [name_or_{translation:[tran1,tran2]}, type, external_link]}
    :param cluster_json: {cluster_uri: [[member1, member2], [prototype1]]}
    :return: init clusters and un-clustered entities
    """
    entities = {}
    ta2_clusters = {}
    no_link = {}

    # init all entities
    # init ta2 clusters, group by external links(skip 'others')
    for ent, attr in entity_json.items():
        name, _type, link = attr
        name = parse_name(name)
        _type = _type.rsplit('#', 1)[-1]
        link = parse_link(link)
        entities[ent] = Entity(ent, name, _type, link)
        if link != OTHERS:
            if link not in ta2_clusters:
                ta2_clusters[link] = Cluster([])
            ta2_clusters[link].add_member(entities[ent])
            entities[ent].set_ta2_cluster(ta2_clusters[link])
        else:
            no_link[ent] = [set(), set()]


    '''
    now we have:
    entities - dict, each key is an entity uri, each value is the corresponding Entity object
    ta2_clusters - dict, each key is a real external link, each value is the corresponding Cluster object
    no_link - dict, each key is an entity uri, each value is two sets:
            one to store elinks related to the entity, the other to store the ta1 cluster uri
    
    then all the entities are either in ta2_clusters's Clusters, or in no_link's keys
    '''

    # process ta1 clusters
    cluster_to_ent = {} # ta1_cluster_uri: set(entities_with_no_link)
    for cluster, mems in cluster_json.items():
        cluster_to_ent[cluster] = set()
        cur = Cluster([])
        members, prototypes = mems
        cur_no_link = set()
        for m in members:
            cur.add_member(entities[m])
            if entities[m].link == OTHERS:
                cur_no_link.add(m)
        for m in prototypes:
            if m in entities:
                cur.add_member(entities[m])
                if entities[m].link == OTHERS:
                    cur_no_link.add(m)

        for elink in cur.links:
            '''
            all others may be in this ta2 external link cluster 
            '''
            if elink == OTHERS:
                for m in cur_no_link:
                    cluster_to_ent[cluster].add(m)
                    no_link[m][1].add(cluster)
            else:
                for m in cur_no_link:
                    cluster_to_ent[cluster].add(m)
                    no_link[m][0].add(elink)

    '''
    now we have filled no_links, it becomes: {entity_uri: [(some_external_links), (some_ta1_cluster_uris)], ... }
    and cluster_to_ent - dict : {ta1_cluster_uri: (entities_with_no_link_uris), ... }
    '''

    # for each entity in no_link, try to find a best place to go
    no_where_to_go = set()
    for ent_uri, tuple in no_link.items():
        elinks, ta1s = tuple
        cur_ent = entities[ent_uri]
        if not len(elinks):
            # no elinks, try to find chained elinks, otherwise no where to go
            elinks = set()
            added = set(ta1s.keys())
            to_check = list(ta1s.keys())
            while to_check:
                cur_cluster = to_check.pop()
                for sibling in cluster_to_ent[cur_cluster]:
                    if len(no_link[sibling][0]):
                        # find external links
                        elinks = elinks.union(no_link[sibling][0])
                    for next_hop_cluster in no_link[sibling][1]:
                        # add other chained clusters to check
                        if next_hop_cluster not in added:
                            added.add(next_hop_cluster)
                            to_check.append(next_hop_cluster)
        if len(elinks):
            cur_cluster = get_best(elinks, cur_ent, ta2_clusters)
            cur_cluster.add_member(cur_ent)
            cur_ent.set_ta2_cluster(cur_cluster)
        else:
            no_where_to_go.add(ent_uri)

    '''
    now we put all entities related to one or more external links to a ta2 cluster
    may still have some entities is no where to go
    '''
    for ent_uri in no_where_to_go:
        pass









