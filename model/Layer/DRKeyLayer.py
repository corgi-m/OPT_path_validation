import os

from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage
from model.Package.DRKeyPackage import DRKeyPackage
from tools.tools import strcat, load_obj, bytescat


class DRKeyLayer(ABCLayer):
    name = 'DRKeyLayer'
    package = DRKeyPackage

    def __init__(self, node):
        super().__init__(node)
        self.SymK = {}
        self.ASymK = {}
        self.SK, self.PK = node.SK, node.PK
        self.Ki = {}
        self.LK = self.SymKeyGen()
        self.KSD = {}

    def receive(self, node, package, PATH, index):
        # logging.debug(strcat(index, ': ', len(PATH) - 1))
        if package.retrieval == False:
            if index == len(PATH) - 1:
                if self.D_check(package, PATH, index):
                    retrieval_package = BasePackage(path=PATH[::-1])
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
        self.Ki[package.sessionid] = {}
        self.Ki[package.sessionid][SLayer] = Ki
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
        sessionidsk = self.AESDecrypt(KSD, package.AUTH)
        SK = sessionidsk[len(sessionid):]
        self.Ki[package.sessionid] = {}
        for i in range(len(package.EncKey)):
            Ki = self.RSADecrypt(SK, package.EncKey[RLayer[i]])
            self.Ki[package.sessionid][RLayer[i]] = Ki
            if not self.RSACheck(RLayer[i].PK, bytescat(Ki, package.PK), package.SignKey[RLayer[i]]):
                return False
        self.Ki[package.sessionid][DLayer] = self.MAC(self.LK, package.sessionid)
        return True

    def S_synchronize(self, package, PATH, index):
        AUTH = self.AESDecrypt(self.SymK[package.sessionid][1], package.KEYS)
        RLayer = [i.get_layer(self.get_name()) for i in PATH[:-1]][::-1]
        self.Ki[package.sessionid] = {}
        for i in range(len(RLayer)):
            self.Ki[package.sessionid][RLayer[i]] = AUTH[:32]
            AUTH = AUTH[32:]
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
        self.ASymK[package.sessionid] = (SK, PK)
        return SK, PK
