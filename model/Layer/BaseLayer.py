from model.Layer.AtomosLayer import AtomosLayer
from model.Layer.DRKeyLayer import DRKeyLayer
from model.Layer.EPICLayer import EPICLayer
from model.Layer.OPTLayer import OPTLayer
from model.Layer.PPVLayer import PPVLayer


class BaseLayer(DRKeyLayer, OPTLayer, EPICLayer, PPVLayer, AtomosLayer):
    name = 'BaseLayer'

    def __init__(self, node):
        self.SK, self.PK = node.get_SK(), node.get_PK()
        self.node = node
        self.id = node.id
        DRKeyLayer.__init__(self)
        OPTLayer.__init__(self)
        EPICLayer.__init__(self)
        PPVLayer.__init__(self)
        AtomosLayer.__init__(self)
    def receive(self, node, package, PATH, index, protocol=None):
        if not self.DRKey_receive(node, package, PATH, index, protocol):
            return False
        if not self.OPT_receive(node, package, PATH, index, protocol):
            return False
        if not self.EPIC_receive(node, package, PATH, index, protocol):
            return False
        if not self.PPV_receive(node, package, PATH, index, protocol):
            return False
        if not self.Atomos_receive(node, package, PATH, index, protocol):
            return False
        return True

    def get_id(self):
        return self.id

    def get_PK(self):
        return self.PK
