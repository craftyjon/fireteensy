import logging as log

from jsonloader import JSONLoader
from fixture import Fixture

class Scene(JSONLoader):

    def __init__(self, filename=None):
        JSONLoader.__init__(self, filename)
        self._fixtures = None
        self._fixture_hierarchy = None

    def extents(self):
        return tuple(self._data.get("extents", (100, 100)))

    def bounding_box(self):
        return tuple(self._data.get("bounding_box", self.extents()))

    def center(self):
        return tuple(self._data.get("center", (50, 50)))

    def set_center(self, point):
        self._data["center"] = point

    def name(self):
        return self._data.get("name", "")

    def set_fixture_data(self, fd):
        self._data["fixtures"] = fd
        self._fixture_hierarchy = None
        self._fixtures = None

    def fixtures(self):
        if self._fixtures is None and self._data.get("fixtures", None):
            self._fixtures = [Fixture(fd) for fd in self._data["fixtures"]]
        else:
            self._fixtures = []
        return self._fixtures

    def fixture(self, strand, address):
        for f in self.fixtures():
            if f.strand() == strand and f.address() == address:
                return f
        return None

    def fixture_hierarchy(self):
        if self._fixture_hierarchy is None:
            self._fixture_hierarchy = dict()
            for f in self.fixtures():
                if not self._fixture_hierarchy.get(f.strand(), None):
                    self._fixture_hierarchy[f.strand()] = dict()
                self._fixture_hierarchy[f.strand()][f.address()] = f
        return self._fixture_hierarchy
