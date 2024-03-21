import random

from model.Package.BasePackage import BasePackage
from task.ABCTask import ABCTask
from tools.tools import strcat, get_timestamp


class OPTTask(ABCTask):
    # net.add_node_task(OPTTask.opt_test, OPTTask.abc_params(net.ROUTE))
    @staticmethod
    def preset_Ki_by_global(PATH):
        SLayer = PATH[0].Layer
        DLayer = PATH[-1].Layer
        session = SLayer.H(strcat(SLayer.get_PK(), [i.id for i in PATH], get_timestamp()))
        for i in PATH[1:]:
            RLayer = i.Layer
            Ki = RLayer.MAC(RLayer.LK, session)
            SLayer.DRKey_set_Ki_by_session_id(Ki, session, RLayer.get_id())
            RLayer.DRKey_set_Ki_by_session_id(Ki, session, SLayer.get_id())
            DLayer.DRKey_set_Ki_by_session_id(Ki, session, RLayer.get_id())
        return session

    @classmethod
    def opt_test(cls, args):
        node, PATH = args
        cls.preset_KSD(PATH[0], PATH[-1])
        layer = node.Layer
        # session = cls.preset_Ki_by_DRKey(node, PATH)
        session = cls.preset_Ki_by_global(PATH)
        PATH = [i.id for i in PATH]
        stream = [BasePackage(PATH) for _ in range(random.randint(1, 30))]
        for p in stream:
            p.OPT_init(layer, session)
            node.add_package(p)
