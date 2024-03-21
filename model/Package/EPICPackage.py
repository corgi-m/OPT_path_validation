from model.Package.ABCPackage import ABCPackage
from model.Protocol.EPICHelper import EPICHelper
from tools.tools import strcat, get_timestamp


class EPICPackage(ABCPackage, EPICHelper):

    def __init__(self, retrieval=False):
        self.Vi = []
        self.Si = []
        self.VSD = None
        self.tspkt = None
        self.retrieval = retrieval

    def EPIC_S_initialization(self, layer):
        KSD = layer.EPIC_get_KSD_by_id(self.PATH[-1])
        sigma = layer.EPIC_get_sigma_by_PATH(self.timestamp, self.PATH)
        KiS = layer.EPIC_get_KiS_by_PATH(self.PATH)
        self.tspkt = str(int(get_timestamp()) - int(self.timestamp))
        PPATH = strcat(self.timestamp, self.PATH[0], self.PATH[-1], self.PATH)

        Ci = []
        for i in range(len(self.PATH)):
            self.Si.append(sigma[i][:self.lseg])
            Ci.append(layer.MAC(KiS[self.PATH[i]], strcat(self.tspkt, self.PATH[0], sigma[i])))
        self.Vi = [i[:self.lval] for i in Ci]

        if not self.retrieval:
            Vil = [i[self.lval:2 * self.lval] for i in Ci]
            session = layer.H(strcat(self.timestamp, self.tspkt))
            layer.EPIC_set_Vil_by_session(Vil, session)
            self.VSD = layer.MAC(KSD, strcat(self.tspkt, PPATH, Vil, self.payload))
        else:
            self.VSD = layer.MAC(KSD, strcat(self.tspkt, PPATH, self.payload))

    def EPIC_get_retrieval_payload(self):
        return strcat(self.timestamp, self.tspkt, self.Vi)

    def EPIC_get_tspkt(self):
        return self.tspkt

    def EPIC_get_Si(self):
        return self.Si

    def EPIC_get_Vi(self):
        return self.Vi

    def EPIC_get_VSD(self):
        return self.VSD

    def EPIC_set_Vi_by_id(self, Vi, id):
        self.Vi[id] = Vi

    def EPIC_if_retrieval(self):
        return self.retrieval
