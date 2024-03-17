from model.Network.BaseNode import BaseNode
from model.Network.Channel import Channel
from model.Network.NetworkHelper import NetworkHelper
from tools.tools import thread_exec_wait, thread_exec_without_wait


class Network(NetworkHelper):
    instance = None

    def __init__(self, G, ROUTE, PROTOCOL):
        self.nodes = {}
        self.edges = {}
        self.G = G
        self.PROTOCOL = PROTOCOL
        thread_exec_wait(self.set_nodes, self.G.nodes)
        thread_exec_wait(self.set_edges, [(index, edges) for index, edges in enumerate(self.G.edges)])
        self.ROUTE = [[self.nodes[i] for i in path] for path in ROUTE]

    def network_start(self):
        func = lambda x: x.forward()
        return thread_exec_without_wait(func, list(self.nodes.values()))

    def set_nodes(self, index):
        self.nodes[index] = BaseNode(index, self.PROTOCOL)

    def set_edges(self, param):
        index = param[0]
        edge = param[1]
        self.edges[2 * index] = Channel(2 * index, self.nodes[edge[0]], self.nodes[edge[1]])
        self.nodes[edge[0]].add_route(self.nodes[edge[1]], self.edges[2 * index])
        self.edges[2 * index + 1] = Channel(2 * index + 1, self.nodes[edge[1]], self.nodes[edge[0]])
        self.nodes[edge[1]].add_route(self.nodes[edge[0]], self.edges[2 * index + 1])

    def add_node_task(self, task, params):
        thread_exec_wait(task, params)
