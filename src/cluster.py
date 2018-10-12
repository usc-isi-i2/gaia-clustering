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

    def calc_similarity(self, entity: Entity) -> float:
        """
        to calculate the similarity between this cluster and an entity,
        i.e the possibility of an entity to be a member of this cluster
        :param entity: the target entity to be compared with
        :return: float number in [0, 1] to represent the similarity
        """
        return 1.0

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




