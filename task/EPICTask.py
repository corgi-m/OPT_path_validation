import random
from time import sleep

from model.Package.BasePackage import BasePackage
from task.ABCTask import ABCTask


class EPICTask(ABCTask):
    # net.add_node_task(EPICTask.EPIC_test, EPICTask.abc_params(net.ROUTE))

    @staticmethod
    def preset_Ki_by_global(SLayer, PATH):
        for i in PATH:
            RLayer = i.Layer
            Ki = SLayer.SymKeyGen()
            SLayer.EPIC_set_Ki_by_id(Ki, RLayer.get_id())
            RLayer.EPIC_set_Ki_by_id(Ki, SLayer.get_id())

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
                exit(0)
            node.add_package(p)
