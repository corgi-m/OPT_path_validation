import logging
import os
import queue
import threading
import time

from controller.GenFactory import GenFactory
from model.Network import Network
from tools.tools import load_obj, strcat


class Node:
    def __init__(self, id):
        self.__id = id
        self.__routing_table = {}  # 路由表
        self.packages = queue.Queue()
        self.Ki = {}
        (self.SK, self.PK) = load_obj('record/keys/pk_sk', os.getenv('RandomSeed'), self.__id, GenFactory.gen_SK_PK)
        self.lock = threading.Lock()

    def __repr__(self):
        return strcat("Node ", self.__id)

    def __eq__(self, other):
        return self.__id == other.get_id()

    def __hash__(self):
        return hash(self.__id)

    def receive(self, package):
        PATH = package.get_path()
        I = PATH.index(self)
        source = PATH[0]
        destination = PATH[-1]
        if I == len(PATH) - 1:
            Ki = [self.Ki[package][i] for i in PATH[1:-1]]
            Kd = self.Ki[package][destination]
            if package.D_validation(Ki, Kd):
                self.succeed(package)
            else:
                self.drop(package)
        else:

            Ki = self.Ki[package][source]
            if package.R_validation(Ki, I):
                self.process(package)
            else:
                self.drop(package)

    def forward(self):
        while True:
            if not self.packages.empty():
                package = self.packages.get()
                PATH = package.get_path()
                I = PATH.index(self)
                R_next = PATH[I + 1]
                Channel = self.__routing_table[R_next]
                Channel.transfer(package)
            if Network.is_complete():
                break
            time.sleep(0)

    def drop(self, package):
        leave = Network.complete()
        logging.error(strcat('drop ', 'Network leave:', leave, package.get_path()))

    def succeed(self, package):
        leave = Network.complete()
        logging.debug(strcat('succeed ', 'Network leave:', leave))

    def process(self, package):
        self.packages.put(package)

    def get_id(self):
        return self.__id

    def get_routing_table(self):
        return self.__routing_table

    def add_route(self, destination, channel):
        self.__routing_table[destination] = channel

    def add_package(self, package):
        self.packages.put(package)

    def add_Ki(self, package, node, Ki):
        # logging.debug(Ki)
        if package not in self.Ki:
            self.Ki[package] = {}
        self.Ki[package][node] = Ki
