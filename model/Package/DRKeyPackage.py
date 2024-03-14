from model.Package.ABCPackage import ABCPackage
from tools.tools import get_timestamp, strcat, bytescat


class DRKeyPackage(ABCPackage):
    layer = 'DRKeyLayer'

    def __init__(self, layer, basepackage, retrieval=False, prepackage=None):
        super().__init__()
        self.PATH = basepackage.PATH
        self.id = basepackage.id
        self.timestamp = get_timestamp()
        self.sessionid = None
        self.AUTH = None
        self.retrieval = retrieval
        if not retrieval:
            self.PK = None
            self.EncKey = {}
            self.SignKey = {}
            self.S_initialization(layer)
        else:
            self.KEYS = None
            self.D_initialization(layer, prepackage)

    def S_initialization(self, layer):
        SK, self.PK = layer.add_ASymK(self)
        self.sessionid = layer.H(strcat(self.PK, self.PATH, self.timestamp))
        KSD, KDS = layer.add_SymK(self)
        self.AUTH = layer.AESEncrypt(KSD, bytescat(self.sessionid, SK))

    def D_initialization(self, layer, prepackage):
        self.AUTH = prepackage.AUTH
        self.sessionid = prepackage.sessionid
        PATH = self.PATH[::-1][1:]
        RLayer = [i.get_layer(self.get_layer()) for i in PATH]
        Ki = b''
        for i in RLayer:
            Ki += layer.node.OPTLayer.Ki[self.sessionid][i.node.OPTLayer]
        self.KEYS = layer.AESEncrypt(layer.SymK[self.sessionid][1], bytescat(Ki + self.AUTH))
        del layer.SymK[self.sessionid]


    def add_enckey(self, Layer, EncKey):
        self.EncKey[Layer] = EncKey

    def add_signkey(self, Layer, SignKey):
        self.SignKey[Layer] = SignKey
