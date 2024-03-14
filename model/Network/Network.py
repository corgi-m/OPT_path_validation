from model.Network.BaseNode import BaseNode
from model.Network.Channel import Channel
from model.Package.BasePackage import BasePackage
from model.Package.OPTPackage import OPTPackage
from tools.tools import thread_exec_wait, thread_exec_without_wait


class Network:
    instance = None

    def __init__(self, G, ROUTE, PROTOCOL):
        self.nodes = {}
        self.edges = {}
        self.G = G
        self.ROUTE = ROUTE
        self.PROTOCOL = PROTOCOL
        thread_exec_wait(self.set_nodes, self.G.nodes)
        thread_exec_wait(self.set_edges, [(index, edges) for index, edges in enumerate(self.G.edges)])

    def network_start(self):
        func = lambda x: x.forward()
        thread_exec_without_wait(func, list(self.nodes.values()))
        thread_exec_wait(self.source_add_package(OPTPackage), self.ROUTE)

    def source_add_package(self, Package):
        def func(route):
            PATH = [self.nodes[i] for i in route]
            package = BasePackage(PATH)
            package.add_package(PATH[0].get_layer(Package.get_layer()), Package)
            PATH[0].add_package(package)
            return package
        return func

    def set_nodes(self, index):
        self.nodes[index] = BaseNode(index, self.PROTOCOL)

    def set_edges(self, param):
        index = param[0]
        edge = param[1]
        self.edges[2 * index] = Channel(2 * index, self.nodes[edge[0]], self.nodes[edge[1]])
        self.nodes[edge[0]].add_route(self.nodes[edge[1]], self.edges[2 * index])
        self.edges[2 * index + 1] = Channel(2 * index + 1, self.nodes[edge[1]], self.nodes[edge[0]])
        self.nodes[edge[1]].add_route(self.nodes[edge[0]], self.edges[2 * index + 1])
