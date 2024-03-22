from model.Layer.ABCLayer import ABCLayer
from model.Protocol.PPVHelper import PPVHelper
from tools.tools import strcat, check_probability


class PPVLayer(ABCLayer, PPVHelper):

    def __init__(self):
        self.KSD = {}
        self.Ki = {}

    def PPV_receive(self, node, package, PATH, index, protocol):
        if 'PPVLayer' not in protocol:
            return True
        package.PPV_sub_TTL()
        if index == len(PATH) - 1:
            if self.PPV_D_validation(package, PATH, index):
                return True
        else:
            if self.PPV_R_sign(package, PATH, index):
                return True
        return False

    def PPV_R_sign(self, package, PATH, index):

        if package.PPV_is_mf1_empty():
            L = len(PATH[1:-1]) - index
            if L == 0:
                return True
            P = 1 / L
            if check_probability(P):
                message = strcat(PATH[0], package.PPV_get_TTL(), PATH[index - 1], package.PPV_get_flowid())
                Mi = self.MAC(self.Ki[package.PPV_get_flowid()][PATH[-1]], message)
                message = strcat(package.PPV_get_mvf(), PATH[index], Mi, PATH[index + 1])
                mvf1 = self.MAC(self.Ki[package.PPV_get_flowid()][PATH[-1]], message)
                package.PPV_set_add1(PATH[index])
                package.PPV_set_mf1(Mi)
                package.PPV_set_mvf(mvf1)
        else:
            if package.PPV_is_mf2_empty():
                message = strcat(PATH[0], package.PPV_get_TTL(), PATH[index - 1], package.PPV_get_flowid())
                Mi = self.MAC(self.Ki[package.PPV_get_flowid()][PATH[-1]], message)
                message = strcat(package.PPV_get_mvf(), Mi)
                mvf2 = self.MAC(self.Ki[package.PPV_get_flowid()][PATH[-1]], message)
                package.PPV_set_add2(PATH[index])
                package.PPV_set_mf2(Mi)
                package.PPV_set_mvf(mvf2)
        return True

    def PPV_D_validation(self, package, PATH, index):
        src, srcp, dst, dstp, prtl = self.packet_info(PATH)
        mvf = package.PPV_get_mvf()
        KSD = self.PPV_get_KSD(PATH[0])
        hsd = self.H(strcat(KSD))
        flowid = self.H(strcat(src, srcp, dst, dstp, prtl, hsd))

        if flowid != package.PPV_get_flowid():
            return False
        packetid = self.MAC(KSD, strcat(flowid, package.get_payload()))
        if packetid != package.PPV_get_packetid():
            return False
        if package.PPV_is_mf2_empty():
            return True

        add1 = package.PPV_get_add1()
        Ki1 = self.Ki[flowid][add1]
        Mi1 = self.MAC(Ki1, self.verify_info(add1, package, index, PATH, flowid, src))

        add2 = package.PPV_get_add2()
        Ki2 = self.Ki[flowid][add2]
        Mi2 = self.MAC(Ki2, self.verify_info(add2, package, index, PATH, flowid, src))

        if Mi1 != package.PPV_get_mf1() or Mi2 != package.PPV_get_mf2():
            return False

        mvf_ = self.MAC(KSD, strcat(packetid))
        message = strcat(mvf_, add1, Mi1, add2)
        mvf_ = self.MAC(Ki1, message)
        message = strcat(mvf_, Mi2)
        mvf_ = self.MAC(Ki2, message)
        if mvf_ != mvf:
            return False
        return True

    def PPV_get_KSD(self, id):
        return self.KSD[id]
