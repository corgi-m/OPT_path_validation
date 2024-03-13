import logging
import os
import queue
import time

from config.config import Config
from model.Layer.ABCLayer import ABCLayer
from tools.tools import load_obj, strcat


class BaseNode:

    def __init__(self, index, PROTOCOL):
        self.__id = index
        self.__routing_table = {}  # 路由表
        self.packages = queue.Queue()
        self.SK, self.PK = load_obj('record/keys/pk_sk', os.getenv('RandomSeed'), self.__id, ABCLayer.ASymKeyGen)
        self.SK = self.SK.decode()
        self.PK = self.PK.decode()
        self.protocol = {Layer.get_name(): Layer(self) for Layer in PROTOCOL}

    def __repr__(self):
        return strcat("Node ", self.__id)

    def __eq__(self, other):
        return self.__id == other.get_id()

    def __hash__(self):
        return hash(self.__id)

    def receive(self, package):
        PATH = package.get_path()
        index = PATH.index(self)
        for name, layer in self.protocol.items():
            if not layer.receive(self, package.get_package(layer.name), PATH, index):
                self.drop(package)
                break
        else:
            if index == len(PATH) - 1:
                self.succeed(package)
            else:
                self.process(package)

    def forward(self):
        while True:
            if not self.packages.empty():
                package = self.packages.get()
                PATH = package.get_path()
                I = PATH.index(self)
                R_next = PATH[I + 1]
                Channel = self.__routing_table[R_next]
                Channel.transfer(package)
            if Config.is_complete():
                break
            time.sleep(0)

    def drop(self, package):
        leave = Config.complete()
        logging.error(strcat('drop ', 'Network leave:', leave))

    def process(self, package):
        # logging.info(strcat('process '))
        self.packages.put(package)

    def succeed(self, package):
        leave = Config.complete()
        if leave != 0:
            logging.info(strcat('succeed ', 'Network leave:', leave))
        else:
            logging.info(strcat('succeed ', 'finish!'))

    def get_id(self):
        return self.__id

    def get_layer(self, layer_name):
        return self.protocol[layer_name]

    def add_route(self, destination, channel):
        self.__routing_table[destination] = channel

    def add_package(self, package):
        self.packages.put(package)
