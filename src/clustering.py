import json
from src.entity import Entity
from src.cluster import Cluster
MAP_TO_FREEBASE = {}
OTHERS = 'others'


class Clustering(object):
    def __init__(self, entity_json: dict, cluster_json: dict):
        """
        init
        :param entity_json: raw info {entity_uri: [name_or_{translation:[tran1,tran2]}, type, external_link], ... }
        :param cluster_json: raw info {cluster_uri: [[member1, member2], [prototype1]], ... }
        """

        self.entities = {}              # self.entities:        {entity_uri: Entity instance}
        self.ta2_clusters = {}          # self.ta2_clusters:    {external_link: Cluster instance}
        self.no_link = {}               # self.no_link:         {entity_no_elink_uri: [(elinks), (ta1_cluster_uris)]}
        self.cluster_to_ent = {}        # self.cluster_to_ent:  {ta1_cluster_uri: set(entity_no_elink_uris)}
        self.no_where_to_go = set()     # self.no_where_to_go:  (entity_uris)

        self.init_el_based_clusters(entity_json, cluster_json)

    def init_el_based_clusters(self, entity_json, cluster_json):
        """
        create Entity instance for each entity and put in self.entities ;
        create Cluster instance for each external link and put entities with elink to corresponding ta2_clusters;
        go over ta1 clusters and put every no-elink entity to self.no_link, record siblings' elinks or ta1 cluster uri.
        :param entity_json: raw info {entity_uri: [name_or_{translation:[tran1,tran2]}, type, external_link], ... }
        :param cluster_json: raw info {cluster_uri: [[member1, member2], [prototype1]], ... }
        :return: None
        """

        # init all entities
        # init ta2 clusters, group by external links(skip 'others')
        for ent, attr in entity_json.items():
            name, _type, link = attr
            names = self.parse_name(name)
            _type = _type.rsplit('#', 1)[-1]
            link = self.parse_link(link)
            self.entities[ent] = Entity(ent, names, _type, link)
            if link != OTHERS:
                if link not in self.ta2_clusters:
                    self.ta2_clusters[link] = Cluster([])
                self.ta2_clusters[link].add_member(self.entities[ent])
                self.entities[ent].set_cluster(self.ta2_clusters[link])
            else:
                self.no_link[ent] = [set(), set()]

        '''
        now we have:
        self.entities - dict, each key is an entity uri, each value is the corresponding Entity object
        self.ta2_clusters - dict, each key is a real external link, each value is the corresponding Cluster object
        self.no_link - dict, each key is an entity uri, each value is two sets:
                one to store elinks related to the entity, the other to store the ta1 cluster uri
        then all the entities are either in ta2_clusters's Clusters, or in no_link's keys
        '''

        # process ta1 clusters
        for cluster, mems in cluster_json.items():
            self.cluster_to_ent[cluster] = set()
            cur = Cluster([])
            members, prototypes = mems
            cur_no_link = set()
            for m in members:
                cur.add_member(self.entities[m])
                if self.entities[m].link == OTHERS:
                    cur_no_link.add(m)
            for m in prototypes:
                if m in self.entities:
                    cur.add_member(self.entities[m])
                    if self.entities[m].link == OTHERS:
                        cur_no_link.add(m)
            for elink in cur.links:
                if elink == OTHERS:
                    for m in cur_no_link:
                        self.cluster_to_ent[cluster].add(m)
                        self.no_link[m][1].add(cluster)
                else:
                    for m in cur_no_link:
                        self.cluster_to_ent[cluster].add(m)
                        self.no_link[m][0].add(elink)

    def assign_chained_elink(self):
        """
        now we have filled self.no_links: {entity_uri: [(some_external_links), (some_ta1_cluster_uris)], ... }
        and self.cluster_to_ent - dict: {ta1_cluster_uri: (entities_with_no_link_uris), ... }
        :return: None
        """
        # for each entity in no_link, try to find a best place to go
        no_where_to_go = set()
        for ent_uri, elink_ta1cluster in self.no_link.items():
            elinks, ta1s = elink_ta1cluster
            cur_ent = self.entities[ent_uri]
            if not len(elinks):
                # no elinks, try to find chained elinks, otherwise no where to go
                elinks = set()
                added = ta1s
                to_check = list(ta1s)
                while to_check:
                    cur_cluster = to_check.pop()
                    for sibling in self.cluster_to_ent[cur_cluster]:
                        if len(self.no_link[sibling][0]):
                            # find external links
                            elinks = elinks.union(self.no_link[sibling][0])
                        for next_hop_cluster in self.no_link[sibling][1]:
                            # add other chained clusters to check
                            if next_hop_cluster not in added:
                                added.add(next_hop_cluster)
                                to_check.append(next_hop_cluster)
            if len(elinks):
                cur_cluster = self.get_best(elinks, cur_ent)
                cur_cluster.add_member(cur_ent)
                cur_ent.set_cluster(cur_cluster)
            else:
                no_where_to_go.add(ent_uri)

    def assign_no_where_to_go(self):
        """
        now we put all entities related to one or more external links to a ta2 cluster
        may still have some entities is no where to go, run in Xin's algorithm
        :return: None
        """
        for ent_uri in self.no_where_to_go:
            # 1. merge chained clusters
            # 2. run in Xin's connected component
            pass

    def get_best(self, elinks: set, ent: Entity):
        if len(elinks) == 1:
            return self.ta2_clusters[list(elinks)[0]]
        max_simi = 0
        max_el = None
        for el in elinks:
            cur_simi = self.ta2_clusters[el].calc_similarity(ent)
            if cur_simi > max_simi:
                max_simi = cur_simi
                max_el = el
        return self.ta2_clusters[max_el]

    def dump_ta2_cluster(self):
        res = []
        for el, cluster in self.ta2_clusters.items():
            res.append(el)
            res.append(cluster.dump_members())
        return '\n'.join(res)

    @staticmethod
    def parse_name(name: str):
        if name.startswith('{'):
            return json.loads('name').get('translation', [''])
        return [name]

    @staticmethod
    def parse_link(link: str):
        # http://dbpedia.org/resource/Vladimir_Potanin
        # LDC2015E42:NIL00132305
        # LDC2015E42:m.083kb
        if link.startswith('http://dbpedia'):
            return MAP_TO_FREEBASE.get(link, link)
        if link.split(':', 1)[-1].strip().startswith('m.'):
            return link
        return OTHERS






