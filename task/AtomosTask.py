import os
import random

from controller.PKI import AtomosPKI
from model.Layer.AtomosLayer import AtomosLayer
from model.Package.AtomosPackage import AtomosPackage
from model.Package.BasePackage import BasePackage
from model.Protocol.AtomosHelper import AtomosHelper
from task.ABCTask import ABCTask
from tools.tools import load_obj, thread_exec_wait


class AtomosTask(ABCTask, AtomosHelper):

    @classmethod
    def set_PK_SK(cls, node):
        layer = node.get_layer()
        id = node.get_id()
        sk, pk = load_obj('record/Atomos/keys/sk_pk', os.getenv('RandomSeed'), id, cls.SPPrimeGen, g=cls.g, p=cls.p)
        layer.set_SK(sk)
        layer.set_PK(pk)
        AtomosPKI[id] = pk

    @classmethod
    def preset_Ki_by_global(cls, nodes):
        cls.q, cls.p = load_obj('record/Atomos/q_p', os.getenv('RandomSeed'), 'q_p', cls.PQPrimeGen)
        cls.g = load_obj('record/Atomos/g', os.getenv('RandomSeed'), 'g', cls.GGen, p=cls.p, q=cls.q)
        AtomosPackage.q = AtomosLayer.q = cls.q
        AtomosPackage.p = AtomosLayer.p = cls.p
        AtomosPackage.g = AtomosLayer.g = cls.g
        thread_exec_wait(cls.set_PK_SK, nodes)

    @classmethod
    def atomos_test(cls, args):
        node, PATH = args
        layer = node.get_layer()
        PATH = [i.id for i in PATH]
        stream = [BasePackage(PATH) for _ in range(random.randint(1, 30))]
        for p in stream:
            p.Atomos_init(layer)
            node.add_package(p)
