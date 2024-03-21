from time import sleep

from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage


class ABCTask:

    @staticmethod
    def preset_KSD(SNode, DNode):
        SLayer = SNode.get_layer()
        DLayer = DNode.get_layer()
        Sid = SNode.get_id()
        Did = DNode.get_id()
        if Sid not in DLayer.KSD and Did not in SLayer.KSD:
            key = ABCLayer.SymKeyGen()
            SLayer.DRKey_set_KSD(Did, key)
            DLayer.DRKey_set_KSD(Sid, key)

    @staticmethod
    def preset_Ki_by_DRKey(node, PATH):
        layer = node.Layer
        PATH = [i.id for i in PATH]
        package = BasePackage(PATH)
        package.DRKey_init(layer)
        node.add_package(package)
        session = package.DRKey_get_session()
        while not layer.DRKey_has_Ki_by_session(session):
            sleep(0)
        return session

    @staticmethod
    def abc_params(ROUTE):
        return [(PATH[0], PATH) for PATH in ROUTE]
