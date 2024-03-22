import logging
import os
import pickle
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import networkx as nx
from matplotlib import pyplot as plt


def to_bytes(obj):
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, int):
        return str(obj).encode('utf-8')
    return obj.encode('utf-8')


def str_to_list(obj):
    pattern = r'"(.*?)"|\'(.*?)\''
    l = []
    for match in re.finditer(pattern, obj):
        l.append(match.groups(1)[1].encode('utf-8'))
    return l


def bytes_to_int(obj):
    if not isinstance(obj, bytes):
        raise 'not bytes'
    return int.from_bytes(obj)

def strcat(*args):
    result = ""
    for i in args:
        result += str(i)
    return result


def stroutput(*args):
    result = []
    for i in args:
        result.append(type(i))
        result.append(i)
    print(result)


def bytescat(*args):
    result = b""
    for i in args:
        if not isinstance(i, bytes):
            result += i.encode()
        else:
            result += i
    return result


def get_timestamp():
    return str(round(time.time() * 1000))


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


def load_obj(path, seed, filename, gen_obj, stop=False, **kwargs):
    dir = strcat(path, '/', seed)
    os.makedirs(dir, exist_ok=True)
    path = strcat(dir, '/', filename)
    if not os.path.exists(path) or os.getenv('Cache') != 'True' or stop is True:
        obj = gen_obj(*kwargs.values())
        save_obj(path, obj)
    else:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
    return obj


def thread_exec_wait(func, iters):
    with ThreadPoolExecutor(max_workers=len(iters)) as executor:
        results = executor.map(func, iters)
        try:
            for result in results:
                ...
        except Exception as e:
            logging.exception(e)
    return results


def thread_exec_without_wait(func, iters):
    try:
        threads = []
        for i in iters:
            thread = threading.Thread(target=func, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        return threads
    except Exception as e:
        logging.exception(e)


def check_probability(true_probability=0.7):
    return random.choices([True, False], weights=[true_probability, 1 - true_probability])[0]
