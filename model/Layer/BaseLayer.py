from model.Layer.DRKeyLayer import DRKeyLayer
from model.Layer.OPTLayer import OPTLayer


class BaseLayer(DRKeyLayer, OPTLayer):
    name = 'BaseLayer'

    def __init__(self, node):
        self.SK, self.PK = node.get_SK(), node.get_PK()
        self.node = node
        self.id = node.id
        super().__init__()

    def receive(self, node, package, PATH, index, protocol=None):
        super().receive(node, package, PATH, index, protocol)
        return True
