import os
import pickle
import time

import networkx as nx
from matplotlib import pyplot as plt

from config.config import Config


def to_bytes(obj):
    if isinstance(obj, bytes):
        return obj
    return obj.encode('utf-8')


def strcat(*args):
    result = ""
    for i in args:
        result += str(i)
    return result


def get_timestamp():
    return round(time.time() * 1000)


def draw_topology(G, ROUTE):
    # 绘制图形
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, seed=42)  # 使用 spring layout 进行布局
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8)

    # 绘制路径
    for i, path in enumerate(ROUTE):
        edges = [(path[2][j], path[2][j + 1]) for j in range(len(path[2]) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.7, edge_color='r', label=f"Path {i + 1}")

    # 显示图形
    plt.title('Autonomous System Topology with Cross Connections (400 ASes)')
    plt.show()


def save_obj(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def load_obj(path, seed, filename, gen_obj, **kwargs):
    dir = strcat(path, '/', seed)
    os.makedirs(dir, exist_ok=True)
    path = strcat(dir, '/', filename)
    if not os.path.exists(path) or os.getenv('Cache') != 'True':
        obj = gen_obj(*kwargs.values())
        save_obj(path, obj)
    else:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
    return obj


def get_time_take():
    return time.time() - Config.time0
