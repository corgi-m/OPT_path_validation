import logging

from model.Layer.ABCLayer import ABCLayer
from tools.tools import strcat


class OPTLayer(ABCLayer):

    def __init__(self):
        self.Ki = {}

    def OPT_receive(self, node, package, PATH, index, protocol):
        if 'OPTLayer' not in protocol:
            return True
        if index == len(PATH) - 1:
            if self.OPT_D_validation(package, PATH, index):
                return True
        else:
            if self.OPT_R_validation(package, PATH, index):
                return True
        return False

    def OPT_R_validation(self, package, PATH, id):
        session = package.DRKey_get_session()
        Sid = PATH[0]
        pvf = package.OPT_get_pvf()
        opv = package.OPT_get_opv_by_id(id)
        datahash = package.OPT_get_datahash()
        timestamp = package.get_timestamp()

        Ki = self.Ki[session][Sid]
        opv_ = self.MAC(Ki, strcat(pvf, datahash, PATH[id - 1], timestamp))

        if opv == opv_:
            package.pvf = self.MAC(Ki, pvf)
            return True
        else:
            logging.error(strcat(id, ': ', opv, ' = ', opv_))
            return False

    def OPT_D_validation(self, package, PATH, index):
        session = package.DRKey_get_session()
        datahash = package.OPT_get_datahash()
        pvf = package.OPT_get_pvf()
        timestamp = package.get_timestamp()
        opv = package.OPT_get_opv_by_id(-1)

        Ki = [self.Ki[session][i] for i in PATH[1:-1]]
        Kd = self.Ki[session][PATH[-1]]
        pvf_ = datahash
        for i in [Kd] + Ki:
            pvf_ = self.MAC(i, pvf_)
        opv_ = self.MAC(Kd, strcat(pvf, datahash, PATH[-2], timestamp))

        if pvf_ == pvf and opv_ == opv:
            return True
        else:
            return False
