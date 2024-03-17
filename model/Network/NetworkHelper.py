import random

import networkx as nx


class NetworkHelper:

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
