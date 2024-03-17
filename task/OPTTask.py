import random
from time import sleep

from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage


class OPTTask:
    @staticmethod
    def preset_KSD(SNode, DNode):
        SLayer = SNode.Layer
        DLayer = DNode.Layer
        Sid = SNode.id
        Did = DNode.id
        if Sid not in DLayer.KSD and Did not in SLayer.KSD:
            key = ABCLayer.SymKeyGen()
            SLayer.set_KSD(Did, key)
            DLayer.set_KSD(Sid, key)

    @staticmethod
    def opt_params(ROUTE):
        return [(PATH[0], PATH) for PATH in ROUTE]

    @classmethod
    def opt_test(cls, args):
        node, PATH = args
        cls.preset_KSD(PATH[0], PATH[-1])
        PATH = [i.id for i in PATH]
        layer = node.Layer
        package = BasePackage(PATH)
        package.DRKey_init(layer)
        node.add_package(package)
        session = package.sessionid
        while session not in layer.Ki:
            sleep(0)

        stream = [BasePackage(PATH) for _ in range(random.randint(1, 30))]
        for p in stream:
            p.OPT_init(layer, session)
            node.add_package(p)
