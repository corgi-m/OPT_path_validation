import logging
import os
from time import sleep

from config.config import Config
from controller.GenFactory import GenFactory
from model.Layer.OPTLayer import OPTLayer
from model.Network.Network import Network
from tools.tools import strcat, load_obj

if __name__ == "__main__":
    Config('config/config.ini')
    logging.basicConfig(level=logging.DEBUG)

    logging.info(strcat('gen_G start ', Config.get_time_take()))
    G = load_obj('record/graph', os.getenv('RandomSeed'), 'graph', GenFactory.gen_topology)

    logging.info(strcat('gen_ROUTE start ', Config.get_time_take()))
    ROUTE = load_obj('record/route', os.getenv('RandomSeed'), 'route', GenFactory.gen_route, True, G=G,
                     num_paths_to_select=int(os.getenv('RouteNum')))

    logging.info(strcat('network initial start ', Config.get_time_take()))
    PROTOCOL = [OPTLayer]
    net = Network(G, ROUTE, PROTOCOL)

    logging.info(strcat('network start ', Config.get_time_take()))
    net.network_start()

    logging.info(strcat('network end ', Config.get_time_take()))
