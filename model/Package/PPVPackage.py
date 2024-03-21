from model.Package.ABCPackage import ABCPackage
from model.Protocol.PPVHelper import PPVHelper
from tools.tools import strcat


class PPVPackage(ABCPackage, PPVHelper):

    def __init__(self):
        self.TTL = 64
        self.flowid = None
        self.packetid = None
        self.mvf = None
        self.add1 = None
        self.mf1 = None
        self.add2 = None
        self.mf2 = None

    def PPV_S_initialization(self, layer, flowid):
        src, srcp, dst, dstp, prtl = self.packet_info(self.PATH)
        KSD = layer.PPV_get_KSD(self.PATH[-1])
        hsd = layer.H(strcat(KSD))

        self.flowid = layer.H(strcat(src, srcp, dst, dstp, prtl, hsd)) if flowid is None else flowid
        self.packetid = layer.MAC(KSD, strcat(self.flowid, self.payload))
        self.mvf = layer.MAC(KSD, strcat(self.packetid))

    def sub_TTL(self):
        self.TTL -= 1

    def get_TTL(self):
        return self.TTL

    def get_flowid(self):
        return self.flowid

    def get_packetid(self):
        return self.packetid

    def get_add1(self):
        return self.add1

    def get_add2(self):
        return self.add2

    def get_mf1(self):
        return self.mf1

    def get_mf2(self):
        return self.mf2

    def get_mvf(self):
        return self.mvf

    def is_mf1_empty(self):
        if self.mf1 is None:
            return True
        return False

    def is_mf2_empty(self):
        if self.mf2 is None:
            return True
        return False

    def set_add1(self, add1):
        self.add1 = add1

    def set_add2(self, add2):
        self.add2 = add2

    def set_mf1(self, mf1):
        self.mf1 = mf1

    def set_mf2(self, mf2):
        self.mf2 = mf2

    def set_mvf(self, mvf):
        self.mvf = mvf
