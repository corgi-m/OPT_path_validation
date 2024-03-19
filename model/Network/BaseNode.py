import logging
import os
import queue
import time

from config.config import Config
from controller.PKI import PKI
from model.Layer.BaseLayer import BaseLayer
from tools.tools import load_obj, strcat


class BaseNode:

    def __init__(self, index, PROTOCOL):
        self.id = index
        self.routing_table = {}  # 路由表
        self.packages = queue.Queue()
        SK, PK = load_obj('record/keys/pk_sk', os.getenv('RandomSeed'), self.id, BaseLayer.ASymKeyGen)
        self.SK = SK.decode()
        self.PK = PK.decode()
        PKI[self.id] = self.PK
        self.Layer = BaseLayer(self)
        self.PROTOCOL = PROTOCOL

    def __repr__(self):
        return strcat("Node ", self.id)

    def receive(self, package):
        PATH = package.PATH
        index = PATH.index(self.id)
        if not self.Layer.receive(self, package, PATH, index, package.PROTOCOL):
            self.drop(package)
        else:
            self.succeed(package) if index == len(PATH) - 1 else self.process(package)

    def forward(self):
        while True:
            if not self.packages.empty():
                package = self.packages.get()
                PATH = package.PATH
                I = PATH.index(self.id)
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
        logging.debug(strcat('succeed '))

    def get_layer(self):
        return self.Layer

    def get_SK(self):
        return self.SK

    def get_PK(self):
        return self.PK

    def get_id(self):
        return self.id

    def add_route(self, destination, channel):
        self.routing_table[destination.id] = channel

    def add_package(self, package):
        Config.add_incomplete()
        self.packages.put(package)
