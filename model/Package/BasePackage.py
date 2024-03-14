import random

from model.Package.ABCPackage import ABCPackage


class BasePackage(ABCPackage):
    name = 'BaseLayer'
    index = 0

    def __init__(self, PATH, size=None):
        super().__init__()
        self.id = self.index
        self.index_add()
        self.PATH = PATH
        self.payload = self.gen_payload(size)
        self.packages = {}

    def add_package(self, source_layer, Package, **kwargs):
        package = Package(source_layer, self, **kwargs)
        self.packages[Package.get_layer()] = package
        return package

    def del_package(self, layer):
        del self.packages[layer]

    @staticmethod
    def gen_payload(size=None):
        size = random.randint(1, 65535) if size is None else size
        payload = random.randbytes(size)
        return payload

    @classmethod
    def index_add(cls):
        cls.index += 1

    def get_path(self):
        return self.PATH

    def get_package(self, name):
        return self.packages[name]
