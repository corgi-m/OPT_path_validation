import random

from model.Package.BasePackage import BasePackage
from task.ABCTask import ABCTask
from tools.tools import strcat


class PPVTask(ABCTask):
    # net.add_node_task(PPVTask.ppv_test, PPVTask.abc_params(net.ROUTE))

    @staticmethod
    def preset_Ki_by_global(PATH):
        SLayer = PATH[0].Layer
        DLayer = PATH[-1].Layer
        PATH_id = [i.id for i in PATH]
        src = PATH_id[0]
        srcp = PATH_id[0]
        dst = PATH_id[-1]
        dstp = PATH_id[-1]
        prtl = 'PPV'
        KSD = SLayer.PPV_get_KSD(PATH_id[-1])
        hsd = SLayer.H(strcat(KSD))
        flowid = SLayer.H(strcat(src, srcp, dst, dstp, prtl, hsd))
        for i in PATH[1:]:
            RLayer = i.Layer
            Ki = RLayer.MAC(RLayer.LK, flowid)
            RLayer.DRKey_set_Ki_by_session_id(Ki, flowid, DLayer.get_id())
            DLayer.DRKey_set_Ki_by_session_id(Ki, flowid, RLayer.get_id())
        return flowid

    @classmethod
    def ppv_test(cls, args):
        node, PATH = args
        cls.preset_KSD(PATH[0], PATH[-1])
        layer = node.Layer
        # session = cls.preset_Ki_by_DRKey(node, PATH)
        flowid = cls.preset_Ki_by_global(PATH)
        PATH = [i.id for i in PATH]
        stream = [BasePackage(PATH) for _ in range(random.randint(1, 30))]
        for p in stream:
            p.PPV_init(layer, flowid)
            node.add_package(p)
