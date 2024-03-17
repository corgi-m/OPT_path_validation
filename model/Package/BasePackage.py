from model.Package.DRKeyPackage import DRKeyPackage
from model.Package.OPTPackage import OPTPackage
from tools.tools import get_timestamp


class BasePackage(DRKeyPackage, OPTPackage):

    def __init__(self, PATH, size=None):
        self.id = self.index
        self.index_add()
        self.PATH = PATH
        self.payload = self.gen_payload(size)
        self.timestamp = get_timestamp()
        self.PROTOCOL = ['BaseLayer']

    def DRKey_init(self, layer, retrieval=False, prepackage=None):
        DRKeyPackage.__init__(self, retrieval)
        if not retrieval:
            self.DRKey_S_initialization(layer)
        else:
            self.DRKey_D_initialization(layer, prepackage)
        self.PROTOCOL.append('DRKeyLayer')

    def OPT_init(self, layer, sessionid=None):
        OPTPackage.__init__(self)
        self.OPT_S_initialization(layer, sessionid)
        self.PROTOCOL.append('OPTLayer')

    def get_timestamp(self):
        return self.timestamp
