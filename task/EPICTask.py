import random
from time import sleep

from model.Layer.ABCLayer import ABCLayer
from model.Package.BasePackage import BasePackage


class EPICTask:
    # net.add_node_task(EPICTask.EPIC_test, EPICTask.EPIC_params(net.ROUTE))
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
    def preset_Ki_by_global(SLayer, PATH):
        for i in PATH:
            RLayer = i.Layer
            Ki = SLayer.SymKeyGen()
            SLayer.EPIC_set_Ki_by_id(Ki, RLayer.get_id())
            RLayer.EPIC_set_Ki_by_id(Ki, SLayer.get_id())

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
    def EPIC_params(ROUTE):
        return [(PATH[0], PATH) for PATH in ROUTE]

    @classmethod
    def EPIC_test(cls, args):
        node, PATH = args
        cls.preset_KSD(PATH[0], PATH[-1])
        layer = node.Layer
        cls.preset_Ki_by_global(PATH[0].Layer, PATH)
        cls.preset_Ki_by_global(PATH[-1].Layer, PATH)

        PATH = [i.id for i in PATH]
        stream = [BasePackage(PATH) for _ in range(random.randint(1, 30))]
        for p in stream:
            p.EPIC_init(layer)
            if not layer.receive(node, p, PATH, 0, p.PROTOCOL):
                print('ok')
                exit(0)
            node.add_package(p)
