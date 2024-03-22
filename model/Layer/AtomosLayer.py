from controller.PKI import AtomosPKI
from model.Layer.ABCLayer import ABCLayer
from model.Protocol.AtomosHelper import AtomosHelper
from tools.tools import strcat


class AtomosLayer(ABCLayer, AtomosHelper):
    def __init__(self):
        self.PK = None
        self.SK = None

    def Atomos_receive(self, node, package, PATH, index, protocol):
        if 'AtomosLayer' not in protocol:
            return True
        if index == len(PATH) - 1:
            if self.Atomos_R_Verification(package, PATH, index):
                return True
        else:
            if self.Atomos_R_Verification(package, PATH, index):
                return True
        return False

    def Atomos_R_Verification(self, package, PATH, id):
        sigma = package.Atomos_get_sigma()
        u = package.Atomos_get_u()
        Hh = package.Atomos_get_Hh()
        deltar = 0
        for j in range(0, id - 1):
            for k in range(0, j + 1):
                deltar += PATH[k]
        pai = 1
        for i in PATH[:id]:
            pai = (pai * AtomosPKI[i]) % self.p
        left = pow(self.g, sigma, self.p)
        right = pow(self.g, deltar, self.p)
        right = (right * pow(u, Hh, self.p)) % self.p
        right = (right * pai) % self.p
        if left != right:
            return False
        package.Atomos_R_Construction(self)
        return True

    def set_PK(self, PK):
        self.PK = PK

    def set_SK(self, SK):
        self.SK = SK

    def get_SK(self):
        return self.SK
