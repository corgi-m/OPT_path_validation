from model.Package.ABCPackage import ABCPackage
from tools.tools import strcat, bytescat


class DRKeyPackage(ABCPackage):

    def __init__(self, retrieval=False):
        self.sessionid = None
        self.AUTH = None
        self.retrieval = retrieval
        if not retrieval:
            self.PK = None
            self.EncKey = {}
            self.SignKey = {}
        else:
            self.KEYS = None

    def DRKey_S_initialization(self, layer):
        SK, self.PK = layer.add_ASymK(self)
        self.sessionid = layer.H(strcat(self.PK, self.PATH, self.timestamp))
        KSD, KDS = layer.add_SymK(self)
        self.AUTH = layer.AESEncrypt(KSD, bytescat(self.sessionid, SK))

    def DRKey_D_initialization(self, layer, prepackage):
        self.AUTH = prepackage.get_AUTH()
        self.sessionid = prepackage.get_session()
        Rid = self.PATH[::-1][1:]
        Ki = b''
        for i in Rid:
            Ki += layer.get_Ki_by_session_id(self.sessionid, i)
        self.KEYS = layer.AESEncrypt(layer.get_KDS_by_session(self.sessionid), bytescat(Ki + self.AUTH))
        layer.del_SymK_by_session(self.sessionid)

    def add_enckey(self, id, EncKey):
        self.EncKey[id] = EncKey

    def add_signkey(self, id, SignKey):
        self.SignKey[id] = SignKey

    def get_session(self):
        return self.sessionid

    def get_AUTH(self):
        return self.AUTH

    def get_PK(self):
        return self.PK

    def get_EncKey(self):
        return self.EncKey

    def get_SignKey(self):
        return self.SignKey

    def if_retrieval(self):
        return self.retrieval

    def get_KEYS(self):
        return self.KEYS
