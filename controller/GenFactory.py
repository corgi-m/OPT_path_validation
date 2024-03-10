import random

import networkx as nx
from Crypto.PublicKey import RSA

from model.Package import OPTPackage


class GenFactory:
    @staticmethod
    def gen_package(PK, PATH, Ki):
        package = OPTPackage()
        size = random.randint(1, 65535)
        payload = random.randbytes(size)
        package.initialization(PK=PK, Ki=Ki, PATH=PATH, payload=payload)
        return package

    @staticmethod
    def gen_route(G, num_paths_to_select=30):
        paths_selected = 0
        paths = []
        while paths_selected < num_paths_to_select:
            # 随机选择起始和结束节点
            start_node = random.choice(list(G.nodes))
            end_node = random.choice(list(G.nodes))

            if start_node == end_node:
                continue
            if not nx.has_path(G, start_node, end_node):
                continue

            # 找到路径
            path = nx.shortest_path(G, start_node, end_node)

            paths_selected += 1
            paths.append(path)

        return paths

    @staticmethod
    def gen_topology(num_node=400):
        # 创建图
        G = nx.Graph()

        # 添加自治域节点
        num_autonomous_systems = num_node
        autonomous_systems = range(1, num_autonomous_systems + 1)
        G.add_nodes_from(autonomous_systems)

        # 添加自治域间连接
        for i in range(1, num_autonomous_systems):
            # 随机选择一个节点进行连接
            connected_node = random.randint(1, num_autonomous_systems)
            if i == connected_node:
                continue
            G.add_edge(i, connected_node)

        return G

    @staticmethod
    def gen_payload(size=1):
        size = random.randint(1, 65535) if size is None else size
        payload = random.randbytes(size)
        return payload

    @staticmethod
    def gen_Ki(package, source, destination, PATH):
        Ki = []
        for _ in PATH:
            key = random.randbytes(32)
            Ki.append(key)  # aes = AES.new(key[:16], AES.MODE_EAX, nonce=key[16:])
        for i in range(1, len(Ki)):
            source.add_Ki(package, PATH[i], Ki[i])
            destination.add_Ki(package, PATH[i], Ki[i])
            PATH[i].add_Ki(package, source, Ki[i])
        return Ki

    @staticmethod
    def gen_SK_PK():
        key = RSA.generate(1024, random.randbytes)
        SK = key.export_key()
        PK = key.publickey().export_key()
        return SK, PK
