from model.Package.ABCPackage import ABCPackage
from tools.tools import strcat, bytescat


class DRKeyPackage(ABCPackage):

    def __init__(self, retrieval=False):
        self.AUTH = None
        self.retrieval = retrieval
        if not retrieval:
            self.PK = None
            self.EncKey = {}
            self.SignKey = {}
        else:
            self.KEYS = None

    def DRKey_S_initialization(self, layer):
        SK, self.PK = layer.DRKey_add_ASymK(self)
        self.sessionid = layer.H(strcat(self.PK, self.PATH, self.timestamp))
        KSD, KDS = layer.DRKey_add_SymK(self)
        self.AUTH = layer.AESEncrypt(KSD, bytescat(self.sessionid, SK))

    def DRKey_D_initialization(self, layer, prepackage):
        self.AUTH = prepackage.DRKey_get_AUTH()
        self.sessionid = prepackage.DRKey_get_session()
        Rid = self.PATH[::-1][1:]
        Ki = b''
        for i in Rid:
            Ki += layer.DRKey_get_Ki_by_session_id(self.sessionid, i)
        self.KEYS = layer.AESEncrypt(layer.DRKey_get_KDS_by_session(self.sessionid), bytescat(Ki + self.AUTH))
        layer.DRKey_del_SymK_by_session(self.sessionid)

    def DRKey_add_enckey(self, id, EncKey):
        self.EncKey[id] = EncKey

    def DRKey_add_signkey(self, id, SignKey):
        self.SignKey[id] = SignKey

    def DRKey_get_session(self):
        return self.sessionid

    def DRKey_get_AUTH(self):
        return self.AUTH

    def DRKey_get_PK(self):
        return self.PK

    def DRKey_get_EncKey(self):
        return self.EncKey

    def DRKey_get_SignKey(self):
        return self.SignKey

    def DRKey_if_retrieval(self):
        return self.retrieval

    def DRKey_get_KEYS(self):
        return self.KEYS
