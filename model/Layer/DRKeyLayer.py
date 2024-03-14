import os

from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage
from model.Package.DRKeyPackage import DRKeyPackage
from tools.tools import strcat, load_obj, bytescat


class DRKeyLayer(ABCLayer):
    name = 'DRKeyLayer'
    package = DRKeyPackage

    def __init__(self, node):
        self.SK, self.PK = node.SK, node.PK
        self.node = node
        self.LK = self.SymKeyGen()
        self.KSD = {}
        self.SymK = {}

    def receive(self, node, package, PATH, index):
        if not package.retrieval:
            if index == len(PATH) - 1:
                if self.D_check(package, PATH, index):
                    retrieval_package = BasePackage(PATH[::-1])
                    retrieval_package.add_package(self, DRKeyPackage, retrieval=True, prepackage=package)
                    node.add_package(retrieval_package)
                    return True
            else:
                if self.R_sign(package, PATH, index):
                    return True
        else:
            if index == len(PATH) - 1:
                result = self.S_synchronize(package, PATH, index)
                if result:
                    return True
            else:
                return True
        return False

    def R_sign(self, package, PATH, index):
        SLayer = PATH[0].get_layer(self.get_name())
        Ki = self.MAC(self.LK, package.sessionid)
        self.node.OPTLayer.Ki[package.sessionid] = {}
        self.node.OPTLayer.Ki[package.sessionid][SLayer.node.OPTLayer] = Ki
        EncKEYRi = self.RSAEncrypt(package.PK, Ki)
        SignKeyRi = self.RSASign(self.SK, strcat(Ki, package.PK))
        package.add_enckey(self, EncKEYRi)
        package.add_signkey(self, SignKeyRi)
        return True

    def D_check(self, package, PATH, index):
        DLayer = PATH[-1].get_layer(self.get_name())
        SLayer = PATH[0].get_layer(self.get_name())
        RLayer = [i.get_layer(self.get_name()) for i in PATH[1:-1]]

        if self != PATH[-1].get_layer(self.name):
            return False

        sessionid = self.H(strcat(package.PK, PATH, package.timestamp))
        if sessionid != package.sessionid:
            return False

        KSD = self.MAC(self.KSD[SLayer], strcat(PATH[0], PATH[-1], package.sessionid))
        KDS = self.MAC(self.KSD[SLayer], strcat(PATH[-1], PATH[0], package.sessionid))
        self.SymK[sessionid] = (KSD, KDS)
        sessionid_sk = self.AESDecrypt(KSD, package.AUTH)
        SK = sessionid_sk[len(sessionid):]
        self.node.OPTLayer.Ki[package.sessionid] = {}

        for i in range(len(package.EncKey)):
            Ki = self.RSADecrypt(SK, package.EncKey[RLayer[i]])
            self.node.OPTLayer.Ki[package.sessionid][RLayer[i].node.OPTLayer] = Ki
            if not self.RSACheck(RLayer[i].PK, bytescat(Ki, package.PK), package.SignKey[RLayer[i]]):
                return False

        self.node.OPTLayer.Ki[package.sessionid][DLayer.node.OPTLayer] = self.MAC(self.LK, package.sessionid)
        return True

    def S_synchronize(self, package, PATH, index):
        AUTH = self.AESDecrypt(self.SymK[package.sessionid][1], package.KEYS)
        del self.SymK[package.sessionid]
        RLayer = [i.get_layer(self.get_name()) for i in PATH[:-1]][::-1]
        self.node.OPTLayer.Ki[package.sessionid] = {}
        Ki = {}
        for i in range(len(RLayer)):
            Ki[RLayer[i].node.OPTLayer] = AUTH[:32]
            AUTH = AUTH[32:]
        self.node.OPTLayer.Ki[package.sessionid] = Ki
        if AUTH != package.AUTH:
            return False
        return True

    def pre_share(self, DLayer):  # step 0
        if DLayer not in self.KSD:
            Key = self.SymKeyGen()
            self.KSD[DLayer] = Key
            DLayer.KSD[self] = Key

    def add_SymK(self, package):  # step 5
        DLayer = package.PATH[-1].get_layer(self.get_name())
        self.pre_share(DLayer)
        KSD = self.MAC(self.KSD[DLayer], strcat(package.PATH[0], package.PATH[-1], package.sessionid))
        KDS = self.MAC(self.KSD[DLayer], strcat(package.PATH[-1], package.PATH[0], package.sessionid))
        self.SymK[package.sessionid] = (KSD, KDS)
        return KSD, KDS

    def add_ASymK(self, package):  # step 1
        SK, PK = load_obj('record/DRKey/keys/pk_sk', os.getenv('RandomSeed'), package.id, self.ASymKeyGen)
        SK = SK.decode()
        PK = PK.decode()
        return SK, PK
