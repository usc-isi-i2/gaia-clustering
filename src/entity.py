

class Entity(object):
    def __init__(self, uri, names, _type, link):
        # TODO: support more than a single name, but many text labels
        self._uri = uri
        self._names = names
        self._name = names[0] if names else ''
        self._type = _type
        self._link = link

        self._cluster = None

    @property
    def uri(self):
        return self._uri

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def link(self):
        return self._link

    @property
    def cluster(self):
        return self._cluster

    def set_cluster(self, cluster):
        self._cluster = cluster