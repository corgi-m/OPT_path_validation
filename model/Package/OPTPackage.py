from model.Package.ABCPackage import ABCPackage
from tools.tools import strcat


class OPTPackage(ABCPackage):

    def __init__(self):
        self.opv = None
        self.pvf = None
        self.datahash = None

    def OPT_S_initialization(self, layer, sessionid):
        self.sessionid = sessionid
        Ki = tuple(layer.DRKey_get_Ki_by_session(self.sessionid).values())  # 包含S、D
        self.datahash = layer.H(self.payload)
        self.pvf = layer.MAC(Ki[-1], self.datahash)
        pvf = self.pvf
        self.opv = [0 for i in range(len(self.PATH))]
        for i, pa in enumerate(self.PATH[1:], 1):
            self.opv[i] = layer.MAC(Ki[i - 1], strcat(pvf, self.datahash, self.PATH[i - 1], self.timestamp))
            pvf = layer.MAC(Ki[i - 1], pvf)

    def OPT_get_session(self):
        return self.sessionid

    def OPT_get_pvf(self):
        return self.pvf

    def OPT_get_opv_by_id(self, id):
        return self.opv[id]

    def OPT_get_datahash(self):
        return self.datahash
