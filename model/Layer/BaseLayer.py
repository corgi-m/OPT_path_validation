from model.Layer.DRKeyLayer import DRKeyLayer
from model.Layer.EPICLayer import EPICLayer
from model.Layer.OPTLayer import OPTLayer


class BaseLayer(DRKeyLayer, OPTLayer, EPICLayer):
    name = 'BaseLayer'

    def __init__(self, node):
        self.SK, self.PK = node.get_SK(), node.get_PK()
        self.node = node
        self.id = node.id
        DRKeyLayer.__init__(self)
        OPTLayer.__init__(self)
        EPICLayer.__init__(self)

    def receive(self, node, package, PATH, index, protocol=None):
        if not self.DRKey_receive(node, package, PATH, index, protocol):
            return False
        if not self.OPT_receive(node, package, PATH, index, protocol):
            return False
        if not self.EPIC_receive(node, package, PATH, index, protocol):
            return False
        return True

    def get_id(self):
        return self.id

    def get_PK(self):
        return self.PK
