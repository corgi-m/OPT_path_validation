from model.Network.BaseNode import BaseNode
from model.Network.Channel import Channel
from model.Package.BasePackage import BasePackage
from tools.tools import thread_exec


class Network:
    instance = None

    def __init__(self, G, ROUTE, PROTOCOL):
        self.__nodes = {}
        self.__edges = {}
        self.G = G
        self.ROUTE = ROUTE
        self.PROTOCOL = PROTOCOL
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
        for protocol in self.PROTOCOL:
            thread_exec(self.source_add_package(protocol.package), self.ROUTE)

    def network_start(self):
        func = lambda x: x.forward()
        thread_exec(func, list(self.__nodes.values()))

    def source_add_package(self, Package):
        def func(route):
            PATH = [self.get_node(i) for i in route]
            package = BasePackage(path=PATH)
            package.add_package(PATH[0].get_layer(Package.get_layer()), Package)
            PATH[0].add_package(package)

            return package

        return func

    def set_nodes(self, index):
        self.__nodes[index] = BaseNode(index, self.PROTOCOL)

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
