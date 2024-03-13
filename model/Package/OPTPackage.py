import random

from model.Package.ABCPackage import ABCPackage
from tools.tools import get_timestamp
from tools.tools import strcat


class OPTPackage(ABCPackage):
    layer = 'OPTLayer'

    def __init__(self, layer, package):
        self.opv = None
        self.pvf = None
        self.sessionid = None
        self.datahash = None
        self.id = package.id
        self.PATH = package.PATH
        self.payload = package.payload
        self.timestamp = get_timestamp()
        self.S_initialization(layer)

    def S_initialization(self, layer):
        self.negotiate_Ki(self.PATH)
        Ki = tuple(layer.get_Ki(self).values())  # 包含S、D
        self.datahash = layer.H(self.payload)
        self.sessionid = layer.H(strcat(self.PATH[0].PK, self.PATH, self.timestamp))
        self.pvf = layer.MAC(Ki[-1], self.datahash)
        pvf = self.pvf
        self.opv = [0 for i in range(len(self.PATH))]
        for i, pa in enumerate(self.PATH[1:], 1):
            self.opv[i] = layer.MAC(Ki[i - 1], strcat(pvf, self.datahash, self.PATH[i - 1], self.timestamp))
            pvf = layer.MAC(Ki[i - 1], pvf)

    def negotiate_Ki(self, PATH):
        Ki = []
        for _ in PATH:
            key = random.randbytes(32)
            Ki.append(key)  # aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        for i in range(1, len(Ki)):
            PATH[0].get_layer(self.layer).add_Ki(self.sessionid, PATH[i], Ki[i])
            PATH[-1].get_layer(self.layer).add_Ki(self.sessionid, PATH[i], Ki[i])
            PATH[i].get_layer(self.layer).add_Ki(self.sessionid, PATH[0], Ki[i])
        return Ki
