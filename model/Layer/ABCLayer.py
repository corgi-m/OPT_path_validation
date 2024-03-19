from abc import ABC, abstractmethod

from model.Layer.ABCLayerHelper import ABCLayerHelper


class ABCLayer(ABC, ABCLayerHelper):
    name = 'ABCLayer'

    def __init__(self):
        self.SK = None
        self.PK = None
        self.node = None
        self.id = None

    def receive(self, node, package, PATH, index, protocol):
        ...
