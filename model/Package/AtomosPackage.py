from controller.PKI import AtomosPKI
from model.Package.ABCPackage import ABCPackage
from model.Protocol.AtomosHelper import AtomosHelper
from tools.tools import strcat, bytes_to_int


class AtomosPackage(ABCPackage, AtomosHelper):
    def __init__(self):
        self.datahash = None
        self.sessionid = None
        self.proof = None
        self.r = None
        self.sigma = None
        self.u = None

    def Atomos_S_Construction(self, layer, sessionid):
        self.sessionid = sessionid
        self.datahash = layer.H(self.payload)
        self.r = self.PATH[0]
        c1 = self.RandomGen()
        Hh = self.Atomos_get_Hh()
        self.sigma = (layer.get_SK() + c1 * Hh) % (self.p - 1)
        self.u = pow(self.g, c1, self.p)
        self.proof = strcat((self.r, self.sigma), self.u)

    def Atomos_R_Construction(self, layer):
        r = layer.get_id()
        ci = self.RandomGen()
        Hh = self.Atomos_get_Hh()
        sigma = (layer.get_SK() + ci * Hh) % (self.p - 1)
        u = pow(self.g, ci, self.p)
        self.r, self.sigma = self.SemiDirect(self.p, (self.r, self.sigma), (r, sigma))
        self.u = self.u * u % self.p

    def Atomos_get_sigma(self):
        return self.sigma

    def Atomos_get_datahash(self):
        return self.datahash

    def Atomos_get_u(self):
        return self.u

    def Atomos_get_r(self):
        return self.r

    def Atomos_get_sessionid(self):
        return self.sessionid

    def Atomos_get_proof(self):
        return self.proof

    def Atomos_get_Hh(self):
        h = strcat(self.datahash, self.sessionid, self.timestamp)
        return bytes_to_int(self.H(h)) % (self.p - 1)
