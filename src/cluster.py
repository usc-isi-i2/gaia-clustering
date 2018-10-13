from jellyfish import jaro_distance
from src.entity import Entity


class Cluster(object):
    def __init__(self, members: list):
        self.members = {}
        self.groupby_attr = {}
        self.links = {}
        self.types = {}
        self.names = {}
        for mem in members:
            self.add_member(mem)
        self.unique_link = self.check_unique_link()

    def check_unique_link(self):
        if len(self.links) == 1:
            return list(self.links.keys())[0]
        if len(self.links) == 2 and 'others' in self.links:
            a, b = list(self.links.keys())
            return a if b == 'others' else b

    def calc_similarity(self, target: Entity or any, distance_table: dict, threshold: float=1) -> float:
        """
        to calculate the similarity between this cluster and an entity,
        i.e the possibility of an entity to be a member of this cluster
        :param target: the target entity to be compared with, or the target Cluster to be compared with
                        (error when put Cluster in param type T_T)
        :param distance_table: {(ent_1_uri, ent_2_uri): distance_float} where ent_1_uri < ent_2_uri
        :param threshold: float, return if over this threshold
        :return: float number in [0, 1] to represent the similarity
        """
        # TODO: ignore outliers? or use more sophisticated methods
        max_similarity = 0
        if isinstance(target, Entity):
            if target.type in self.types:
                for name, cnt in self.names.items():
                    _key = (name, target.name) if name < target.name else (target.name, name)
                    if _key not in distance_table:
                        distance_table[_key] = jaro_distance(name, target.name)
                    if max_similarity < distance_table[_key]:
                        max_similarity = distance_table[_key]
                        if max_similarity > threshold:
                            return max_similarity
        else:
            if set(target.types.keys()).union(self.types.keys()):
                for ent_uri, ent in target.members.items():
                    similarity = self.calc_similarity(ent, distance_table)
                    if max_similarity < similarity:
                        max_similarity = similarity
                        if max_similarity > threshold:
                            return max_similarity
        return max_similarity

    def calc_similarity_cluster(self, target, distance_table: dict, threshold: float=1) -> float:
        """
        to calculate the similarity between this cluster and an entity,
        i.e the possibility of an entity to be a member of this cluster
        :param target:
        :param distance_table: {(ent_1_uri, ent_2_uri): distance_float} where ent_1_uri < ent_2_uri
        :param threshold: float, return if over this threshold
        :return: float number in [0, 1] to represent the similarity
        """
        # TODO: ignore outliers? or use more sophisticated methods

    def add_member(self, mem: Entity):
        if mem.uri in self.members:
            return 'EXIST'

        self.members[mem.uri] = mem
        if mem.type not in self.groupby_attr:
            self.groupby_attr[mem.type] = {}
        if mem.link not in self.groupby_attr[mem.type]:
            self.groupby_attr[mem.type][mem.link] = {}
        if mem.name not in self.groupby_attr[mem.type][mem.link]:
            self.groupby_attr[mem.type][mem.link][mem.name] = set()
        self.groupby_attr[mem.type][mem.link][mem.name].add(mem.uri)

        for _key, _dict in ((mem.type, self.types),
                         (mem.link, self.links),
                         (mem.name, self.names)):
            if _key not in _dict:
                _dict[_key] = 0
            _dict[_key] += 1
        mem.set_cluster(self)
        self.unique_link = self.check_unique_link()

    def remove_member(self, mem: Entity):
        if mem.uri not in self.members:
            return
        del self.members[mem.uri]
        self.groupby_attr[mem.type][mem.link][mem.name].remove(mem.uri)

        for _key, _dict in ((mem.type, self.types),
                         (mem.link, self.links),
                         (mem.name, self.names)):
            if _key in _dict:
                _dict[_key] -= 1
                if len(_dict[_key]) <= 0:
                    del _dict[_key]
            else:
                print('WIRED, NOT COUNT ', mem.uri)

        self.unique_link = self.check_unique_link()

    def dump_members(self):
        return '\n'.join(list(self.members.keys()))


