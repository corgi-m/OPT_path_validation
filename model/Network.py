import logging
import time
from concurrent.futures import ThreadPoolExecutor

from controller.GenFactory import GenFactory
from model.Channel import Channel
from model.Node import Node
from model.Package import OPTPackage
from tools.opt_debug import check_Ki
from tools.tools import get_time_take


class Network:
    instance = None
    incomplete = 0

    def __init__(self, G, ROUTE):
        self.__nodes = {}
        self.__edges = {}
        self.G = G
        self.ROUTE = ROUTE
        self.set_incomplete(len(ROUTE))
        logging.info(get_time_take())
        self.init_network()
        logging.info(get_time_take())
        self.init_package()
        logging.info(get_time_take())

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def set_nodes(self, index):
        self.__nodes[index] = Node(index)
        time.sleep(0)

    def set_edges(self, param):
        index = param[0]
        edge = param[1]
        self.__edges[2 * index] = (Channel(2 * index, self.__nodes[edge[0]], self.__nodes[edge[1]]))
        self.__nodes[edge[0]].add_route(self.__nodes[edge[1]], self.__edges[2 * index])
        self.__edges[2 * index + 1] = Channel(2 * index + 1, self.__nodes[edge[1]], self.__nodes[edge[0]])
        self.__nodes[edge[1]].add_route(self.__nodes[edge[0]], self.__edges[2 * index + 1])

    def init_network(self):
        with ThreadPoolExecutor(max_workers=len(self.G.nodes)) as executor:
            results = executor.map(self.set_nodes, self.G.nodes)
            try:
                for result in results:
                    ...
            except Exception as e:
                logging.exception(e)

        with ThreadPoolExecutor(max_workers=len(self.G.edges)) as executor:
            results = executor.map(self.set_edges, enumerate(self.G.edges))
            try:
                for result in results:
                    ...
            except Exception as e:
                logging.exception(e)

    def source_add_package(self, route):
        source = self.get_node(route[0])
        destination = self.get_node(route[-1])
        PATH = [self.get_node(i) for i in route]
        package = OPTPackage()
        payload = GenFactory.gen_payload()
        Ki = GenFactory.gen_Ki(package, source, destination, PATH)  # 包含S、D
        package.initialization(PK=source.PK, Ki=Ki, PATH=PATH, payload=payload)
        source.add_package(package)
        return package

    def init_package(self):
        with ThreadPoolExecutor(max_workers=len(self.ROUTE)) as executor:
            results = executor.map(self.source_add_package, self.ROUTE)
            try:
                for result in results:
                    check_Ki(result)
            except Exception as e:
                logging.exception(e)
        executor.shutdown(wait=True)

    def network_start(self):
        forward_start = lambda x: x.forward()
        with ThreadPoolExecutor(max_workers=len(self.__nodes)) as executor:
            results = executor.map(forward_start, list(self.__nodes.values()))
            try:
                for result in results:
                    ...
            except Exception as e:
                logging.exception(e)
        executor.shutdown(wait=True)

    @classmethod
    def set_incomplete(cls, param):
        cls.incomplete = param

    @classmethod
    def complete(cls):
        cls.incomplete -= 1
        return cls.incomplete

    @classmethod
    def is_complete(cls):
        if cls.incomplete == 0:
            return True
        else:
            return False

    def get_nodes(self):
        return self.__nodes

    def get_node(self, id):
        return self.__nodes[id]

    def get_edges(self):
        return self.__edges

    def get_edge(self, id):
        return self.__edges[id]
