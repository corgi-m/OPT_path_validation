import logging

from model.Layer.ABCLayer import ABCLayer
from tools.tools import strcat


class OPTLayer(ABCLayer):
    name = 'OPTLayer'

    def __init__(self, node):
        super().__init__(node)
        self.Ki = {}

    def R_validation(self, package, PATH, index):
        Ki = self.Ki[package.sessionid][PATH[0]]
        opv_ = self.MAC(Ki, strcat(package.pvf, package.datahash, PATH[index - 1], package.timestamp))
        if package.opv[index] == opv_:
            package.pvf = self.MAC(Ki, package.pvf)
            return True
        else:
            logging.error(strcat(index, ': ', package.opv[index], ' = ', opv_))
            return False

    def D_validation(self, package, PATH, index):
        Ki = [self.Ki[package.sessionid][i] for i in PATH[1:-1]]
        Kd = self.Ki[package.sessionid][PATH[-1]]
        pvf_ = package.datahash
        for i in [Kd] + Ki:
            pvf_ = self.MAC(i, pvf_)
        opv_ = self.MAC(Kd, strcat(package.pvf, package.datahash, PATH[-2], package.timestamp))
        if pvf_ == package.pvf and opv_ == package.opv[-1]:
            return True
        else:
            return False

    def receive(self, node, package, PATH, index):
        if index == len(PATH) - 1:
            if self.D_validation(package, PATH, index):
                return True
        else:
            if self.R_validation(package, PATH, index):
                return True
        return False

    def add_Ki(self, sessionid, layer, Ki):
        if sessionid not in self.Ki:
            self.Ki[sessionid] = {}
        self.Ki[sessionid][layer] = Ki

    def get_Ki(self, package):
        return self.Ki[package.sessionid]
