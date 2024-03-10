import logging
from concurrent.futures import ThreadPoolExecutor

from controller.GenFactory import GenFactory
from model.Channel import Channel
from model.Node import Node
from tools.opt_debug import check_Ki
from tools.tools import check_thread_err, thread_exec


class Network:
    instance = None
    incomplete = 0

    def __init__(self, G, ROUTE):
        self.__nodes = {}
        self.__edges = {}
        self.G = G
        self.ROUTE = ROUTE
        self.set_incomplete(len(ROUTE))
        self.init_network()
        self.init_package()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init_network(self):
        thread_exec(self.set_nodes, self.G.nodes)
        thread_exec(self.set_edges, [(index, edges) for index, edges in enumerate(self.G.edges)])

    def init_package(self):
        results = thread_exec(self.source_add_package, self.ROUTE)
        for result in results:
            check_Ki(result)

    def network_start(self):
        thread_exec(lambda x: x.forward(), list(self.__nodes.values()))


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

    def source_add_package(self, route):
        PATH = [self.get_node(i) for i in route]
        package = GenFactory.gen_package(PATH)
        PATH[0].add_package(package)
        return package

    def set_nodes(self, index):
        self.__nodes[index] = Node(index)

    def set_edges(self, param):
        index = param[0]
        edge = param[1]
        self.__edges[2 * index] = Channel(2 * index, self.__nodes[edge[0]], self.__nodes[edge[1]])
        self.__nodes[edge[0]].add_route(self.__nodes[edge[1]], self.__edges[2 * index])
        self.__edges[2 * index + 1] = Channel(2 * index + 1, self.__nodes[edge[1]], self.__nodes[edge[0]])
        self.__nodes[edge[1]].add_route(self.__nodes[edge[0]], self.__edges[2 * index + 1])

    def get_nodes(self):
        return self.__nodes

    def get_node(self, id):
        return self.__nodes[id]

    def get_edges(self):
        return self.__edges

    def get_edge(self, id):
        return self.__edges[id]
