from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage
from model.Protocol.EPICHelper import EPICHelper
from tools.tools import strcat, str_to_list


class EPICLayer(ABCLayer, EPICHelper):
    lseg = 10
    lval = 10

    def __init__(self):
        self.Ki = {}
        self.KSD = {}
        self.Vil = {}

    def EPIC_receive(self, node, package, PATH, index, protocol):
        if 'EPICLayer' not in protocol:
            return True
        if not package.DRKey_if_retrieval():
            if not self.EPIC_R_validation(package, PATH, index):
                return False
            if index == len(PATH) - 1:
                if not self.EPIC_D_validation(package, PATH, index):
                    return False
                else:
                    payload = package.EPIC_get_retrieval_payload()
                    retrieval_package = BasePackage(PATH[::-1], payload)
                    retrieval_package.EPIC_init(self, retrieval=True)
                    node.add_package(retrieval_package)
        else:
            if not self.EPIC_R_validation(package, PATH, index):
                return False
            if index == len(PATH) - 1:
                if not self.EPIC_D_validation(package, PATH, index):
                    return False
        return True

    def EPIC_R_validation(self, package, PATH, id):
        timestamp = package.get_timestamp()
        tspkt = package.EPIC_get_tspkt()
        Si = package.EPIC_get_Si()
        Vi = package.EPIC_get_Vi()
        Ki = self.Ki[PATH[0]]
        if not self.EPIC_check_HI(PATH):
            return False
        if not self.EPIC_check_time(timestamp, tspkt):
            return False
        KA1 = self.MAC(Ki, PATH[0])
        KiS = self.MAC(KA1, PATH[0])
        if id == 0:
            sigma = self.MAC(Ki, strcat(timestamp, PATH[id]))
        else:
            sigma = self.MAC(Ki, strcat(timestamp, PATH[id], Si[id - 1]))
        if Si[id] != sigma[:self.lseg]:
            return False
        Ci = self.MAC(KiS, strcat(tspkt, PATH[0], sigma))
        Ci1 = Ci[:self.lval]
        if Vi[id] != Ci1:
            return False
        if not package.DRKey_if_retrieval():
            Ci2 = Ci[self.lval:2 * self.lval]
            package.EPIC_set_Vi_by_id(Ci2, id)
        return True

    def EPIC_D_validation(self, package, PATH, index):
        KSD = self.KSD[PATH[0]]
        timestamp = package.get_timestamp()
        tspkt = package.EPIC_get_tspkt()
        PPATH = strcat(timestamp, PATH[0], PATH[-1], PATH)
        payload = package.get_payload()
        VSD = package.EPIC_get_VSD()
        Vi = package.EPIC_get_Vi()
        if not self.EPIC_check_time(timestamp, tspkt):
            return False

        if not package.DRKey_if_retrieval():
            VSD_ = self.MAC(KSD, strcat(tspkt, PPATH, Vi, payload))
            if VSD != VSD_:
                return False
            return True
        else:
            VSD_ = self.MAC(KSD, strcat(tspkt, PPATH, payload))

            if VSD != VSD_:
                return False

            P = payload
            timestamp_ = P[:len(timestamp)]
            P = P[len(timestamp_):]
            tspkt_ = P.split('[')[0]
            P = P[len(tspkt_):]
            Vi_ = str_to_list(P)

            session = self.H(strcat(timestamp_, tspkt_))
            if session not in self.Vil:
                return False
            Vil = self.Vil[session]

            for i in range(len(Vi_)):
                if Vi_[i] != Vil[i]:
                    return False
            return True

    def EPIC_check_HI(self, param):
        return True

    def EPIC_check_time(self, param, param1):
        return True

    def EPIC_get_KSD_by_id(self, id):
        return self.KSD[id]

    def EPIC_get_sigma_by_PATH(self, timestamp, PATH):
        sigmas = []
        sigma = self.MAC(self.Ki[PATH[0]], strcat(timestamp, PATH[0]))
        S = sigma[:self.lseg]
        sigmas.append(sigma)
        for i in PATH[1:]:
            sigma = self.MAC(self.Ki[i], strcat(timestamp, i, S))
            S = sigma[:self.lseg]
            sigmas.append(sigma)
        return sigmas

    def EPIC_get_KiS_by_PATH(self, PATH):
        KiS = {}
        A1 = H = PATH[0]
        for i in PATH:
            Ki = self.Ki[i]
            KAi_A1 = self.MAC(Ki, A1)
            kis = self.MAC(KAi_A1, H)
            KiS[i] = kis
        return KiS

    def EPIC_set_Ki_by_id(self, Ki, id):
        if id not in self.Ki:
            self.Ki[id] = Ki

    def EPIC_set_Vil_by_session(self, Vil, session):
        self.Vil[session] = Vil
