import logging
import os
import queue
import time

from config.config import Config
from model.Layer.ABCLayer import ABCLayer
from tools.tools import load_obj, strcat


class BaseNode:

    def __init__(self, index, PROTOCOL):
        self.id = index
        self.routing_table = {}  # 路由表
        self.packages = queue.Queue()
        SK, PK = load_obj('record/keys/pk_sk', os.getenv('RandomSeed'), self.id, ABCLayer.ASymKeyGen)
        self.SK = SK.decode()
        self.PK = PK.decode()
        self.PROTOCOL = PROTOCOL
        for Layer in PROTOCOL:
            if not hasattr(self, Layer.get_name()):
                setattr(self, Layer.get_name(), Layer(self))

    def __repr__(self):
        return strcat("Node ", self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def receive(self, basepackage):
        PATH = basepackage.get_path()
        index = PATH.index(self)
        for layer, package in basepackage.packages.items():
            if not self.__getattribute__(layer).receive(self, package, PATH, index):
                self.drop(basepackage)
                break
        else:
            self.succeed(basepackage) if index == len(PATH) - 1 else self.process(basepackage)

    def forward(self):
        while True:
            if not self.packages.empty():
                package = self.packages.get()
                PATH = package.get_path()
                I = PATH.index(self)
                R_next = PATH[I + 1]
                Channel = self.routing_table[R_next]
                Channel.transfer(package)
            if Config.is_complete():
                ...  # break
            time.sleep(0)

    def drop(self, package):
        leave = Config.complete()
        logging.error(strcat('drop '))

    def process(self, package):
        # logging.info(strcat('process '))
        self.packages.put(package)

    def succeed(self, package):
        leave = Config.complete()
        logging.info(strcat('succeed '))

    def get_layer(self, layer_name):
        return self.__getattribute__(layer_name)

    def add_route(self, destination, channel):
        self.routing_table[destination] = channel

    def add_package(self, package):
        Config.add_incomplete()
        self.packages.put(package)
