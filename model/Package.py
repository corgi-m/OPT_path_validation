import logging
import threading

from controller.HASHManager import HASHManager
from tools.tools import get_timestamp
from tools.tools import strcat


class OPTPackage:
    packages = []
    index = 0

    def __init__(self, **kwargs):
        self.id = self.index
        self.index_add()
        self.packages.append(self)
        self.datahash = kwargs.get('datahash')
        self.sessionid = kwargs.get('sessionid')
        self.timestamp = kwargs.get('timestamp')
        self.pvf = kwargs.get('pvf')
        self.opv = kwargs.get('opv')
        self.R = kwargs.get('path')
        self.payload = kwargs.get('payload')

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(f'{key}={value}' for key, value in self.__dict__.items())
        return f'{class_name}({attributes})'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def H(message):
        return HASHManager.calc_md5(message)

    @staticmethod
    def MAC(key, message):
        return HASHManager.calc_hmac(key, message)
    @classmethod
    def index_add(cls):
        cls.index += 1

    def initialization(self, PK, Ki, PATH, payload):
        self.R = PATH[1:]# 包含D
        self.PATH = PATH# 包含SD
        self.payload = payload
        self.datahash = self.H(payload)
        self.timestamp = get_timestamp()
        self.sessionid = self.H(strcat(PK, self.R, self.timestamp))
        self.pvf = self.MAC(Ki[-1], self.datahash)
        pvf = self.pvf
        self.opv = [0 for i in range(len(self.R) + 1)]
        for i, pa in enumerate(self.R, 1):
            self.opv[i] = self.MAC(Ki[i], strcat(pvf, self.datahash, self.PATH[i - 1], self.timestamp))
            pvf = self.MAC(Ki[i], pvf)

    def R_validation(self, Ki, i):
        opv_ = self.MAC(Ki, strcat(self.pvf, self.datahash, self.PATH[i - 1], self.timestamp))
        if self.opv[i] == opv_:
            self.pvf = self.MAC(Ki, self.pvf)
            return True
        else:
            logging.error(strcat(i, ': ', self.opv[i], ' = ', opv_))
            return False

    def D_validation(self, Ki, Kd):
        K_ = [Kd] + Ki
        pvf_ = self.datahash
        for i in K_:
            pvf_ = self.MAC(i, pvf_)
        opv_ = self.MAC(Kd, strcat(self.pvf, self.datahash, self.PATH[-2], self.timestamp))
        if pvf_ == self.pvf and opv_ == self.opv[-1]:
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def get_path(self):
        return self.PATH
