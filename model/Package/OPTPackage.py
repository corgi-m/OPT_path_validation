import random
from time import sleep

from model.Layer.DRKeyLayer import DRKeyLayer
from model.Package.ABCPackage import ABCPackage
from model.Package.DRKeyPackage import DRKeyPackage
from tools.tools import get_timestamp
from tools.tools import strcat


class OPTPackage(ABCPackage):
    layer = 'OPTLayer'

    def __init__(self, layer, basepackage):
        super().__init__()
        self.opv = None
        self.pvf = None
        self.sessionid = None
        self.datahash = None
        self.id = basepackage.id
        self.PATH = basepackage.PATH
        self.payload = basepackage.payload
        self.timestamp = get_timestamp()
        self.sessionid = layer.gen_DRKeyPackage(basepackage)
        self.S_initialization(layer)

    def S_initialization(self, layer):
        Ki = tuple(layer.Ki[self.sessionid].values())  # 包含S、D
        self.datahash = layer.H(self.payload)
        self.pvf = layer.MAC(Ki[-1], self.datahash)
        pvf = self.pvf
        self.opv = [0 for i in range(len(self.PATH))]
        for i, pa in enumerate(self.PATH[1:], 1):
            self.opv[i] = layer.MAC(Ki[i - 1], strcat(pvf, self.datahash, self.PATH[i - 1], self.timestamp))
            pvf = layer.MAC(Ki[i - 1], pvf)

