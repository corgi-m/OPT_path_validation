import os

from controller.PKI import PKI
from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage
from tools.tools import strcat, load_obj, bytescat


class DRKeyLayer(ABCLayer):

    def __init__(self):
        self.LK = self.SymKeyGen()
        self.Ki = {}
        self.KSD = {}
        self.SymK = {}

    def DRKey_receive(self, node, package, PATH, index, protocol):
        if 'DRKeyLayer' not in protocol:
            return True
        if not package.DRKey_if_retrieval():
            if index == len(PATH) - 1:
                if self.DRKey_D_check(package, PATH, index):
                    retrieval_package = BasePackage(PATH[::-1])
                    retrieval_package.DRKey_init(self, retrieval=True, prepackage=package)
                    node.add_package(retrieval_package)
                    return True
            else:
                if self.DRKey_R_sign(package, PATH, index):
                    return True
        else:
            if index == len(PATH) - 1:
                result = self.DRKey_S_synchronize(package, PATH, index)
                if result:
                    return True
            else:
                return True
        return False

    def DRKey_R_sign(self, package, PATH, index):
        Sid = PATH[0]
        session = package.DRKey_get_session()
        PK = package.DRKey_get_PK()

        Ki = self.MAC(self.LK, session)
        self.Ki[session] = {}
        self.Ki[session][Sid] = Ki
        EncKEYRi = self.RSAEncrypt(PK, Ki)
        SignKeyRi = self.RSASign(self.SK, strcat(Ki, PK))

        package.DRKey_add_enckey(self.id, EncKEYRi)
        package.DRKey_add_signkey(self.id, SignKeyRi)
        return True

    def DRKey_D_check(self, package, PATH, index):
        Did = PATH[-1]
        Sid = PATH[0]
        Rid = PATH[1:-1]
        PK = package.DRKey_get_PK()
        timestamp = package.get_timestamp()
        AUTH = package.DRKey_get_AUTH()
        EncKey = package.DRKey_get_EncKey()
        SignKey = package.DRKey_get_SignKey()
        session = package.DRKey_get_session()

        if self.node.id != Did:
            return False

        sessionid = self.H(strcat(PK, PATH, timestamp))
        if sessionid != session:
            return False

        KSD = self.MAC(self.KSD[Sid], strcat(Sid, Did, session))
        KDS = self.MAC(self.KSD[Sid], strcat(Did, Sid, session))
        self.SymK[session] = (KSD, KDS)

        sessionid_sk = self.AESDecrypt(KSD, AUTH)
        SK = sessionid_sk[len(session):]
        self.Ki[session] = {}

        for i in Rid:
            Ki = self.RSADecrypt(SK, EncKey[i])
            self.Ki[session][i] = Ki
            if not self.RSACheck(PKI[i], bytescat(Ki, PK), SignKey[i]):
                return False

        self.Ki[session][Did] = self.MAC(self.LK, session)
        return True

    def DRKey_S_synchronize(self, package, PATH, index):
        session = package.DRKey_get_session()
        KEYS = package.DRKey_get_KEYS()
        Rid = PATH[:-1][::-1]

        AUTH = self.AESDecrypt(self.SymK[session][1], KEYS)
        del self.SymK[session]

        Ki = {}
        for i in Rid:
            Ki[i] = AUTH[:32]
            AUTH = AUTH[32:]
        self.Ki[session] = Ki

        if AUTH != package.AUTH:
            return False
        return True

    def DRKey_get_Ki_by_session_id(self, session, id):
        return self.Ki[session][id]

    def DRKey_get_Ki_by_session(self, session):
        return self.Ki[session]

    def DRKey_get_KDS_by_session(self, session):
        return self.SymK[session][1]

    def DRKey_set_KSD(self, Did, Key):  # step 0
        if Did not in self.KSD:
            self.KSD[Did] = Key

    def DRKey_set_Ki_by_session_id(self, Ki, session, id):
        if session not in self.Ki:
            self.Ki[session] = {}
        self.Ki[session][id] = Ki

    def DRKey_add_SymK(self, package):  # step 5
        PATH = package.get_PATH()
        Did = PATH[-1]
        Sid = PATH[0]
        session = package.DRKey_get_session()

        KSD = self.MAC(self.KSD[Did], strcat(Sid, Did, session))
        KDS = self.MAC(self.KSD[Did], strcat(Sid, Did, session))
        self.SymK[session] = (KSD, KDS)
        return KSD, KDS

    def DRKey_add_ASymK(self, package):  # step 1
        id = package.get_id()

        SK, PK = load_obj('record/DRKey/keys/pk_sk', os.getenv('RandomSeed'), id, self.ASymKeyGen)
        SK = SK.decode()
        PK = PK.decode()
        return SK, PK

    def DRKey_del_SymK_by_session(self, session):
        del self.SymK[session]

    def DRKey_has_Ki_by_session(self, session):
        if session in self.Ki:
            return True
        return False
