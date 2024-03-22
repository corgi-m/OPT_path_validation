from model.Package.AtomosPackage import AtomosPackage
from model.Package.DRKeyPackage import DRKeyPackage
from model.Package.EPICPackage import EPICPackage
from model.Package.OPTPackage import OPTPackage
from model.Package.PPVPackage import PPVPackage
from tools.tools import get_timestamp


class BasePackage(DRKeyPackage, OPTPackage, EPICPackage, PPVPackage, AtomosPackage):

    def __init__(self, PATH, payload=None):
        self.id = self.index
        self.index_add()
        self.PATH = PATH
        self.payload = self.gen_payload() if payload is None else payload
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

    def EPIC_init(self, layer, retrieval=False):
        EPICPackage.__init__(self, retrieval)
        self.EPIC_S_initialization(layer)
        self.PROTOCOL.append('EPICLayer')

    def PPV_init(self, layer, sessionid=None):
        PPVPackage.__init__(self)
        self.PPV_S_initialization(layer, sessionid)
        self.PROTOCOL.append('PPVLayer')
    def Atomos_init(self, layer, sessionid=None):
        AtomosPackage.__init__(self)
        self.Atomos_S_Construction(layer, sessionid)
        self.PROTOCOL.append('AtomosLayer')

    def get_timestamp(self):
        return self.timestamp
