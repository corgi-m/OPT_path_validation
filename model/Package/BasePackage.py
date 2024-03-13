import logging
import random

from model.Package.ABCPackage import ABCPackage


class BasePackage(ABCPackage):
    name = 'BaseLayer'
    index = 0

    def __init__(self, **kwargs):
        super().__init__()
        self.id = self.index
        self.index_add()
        self.PATH = kwargs.get('path')
        self.payload = self.gen_payload(kwargs.get('size'))
        self.package = {}

    def add_package(self, source, Package, **kwargs):
        self.package[Package.get_layer()] = Package(source, self, **kwargs)

    def gen_payload(self, size=None):
        size = random.randint(1, 65535) if size is None else size
        payload = random.randbytes(size)
        return payload

    @classmethod
    def index_add(cls):
        cls.index += 1

    def get_path(self):
        return self.PATH

    def get_package(self, name):
        return self.package[name]


