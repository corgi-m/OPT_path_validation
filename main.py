import logging
import os

from config.config import Config
from model.Layer.OPTLayer import OPTLayer
from model.Network.Network import Network
from model.Network.NetworkHelper import NetworkHelper
from task.AtomosTask import AtomosTask
from task.EPICTask import EPICTask
from task.OPTTask import OPTTask
from task.PPVTask import PPVTask
from tools.tools import strcat, load_obj

if __name__ == "__main__":
    Config('config/config.ini')
    logging.basicConfig(level=logging.INFO)

    logging.info(strcat('gen_G start ', Config.get_time_take()))
    G = load_obj('record/graph', os.getenv('RandomSeed'), 'graph', NetworkHelper.gen_topology)

    logging.info(strcat('gen_ROUTE start ', Config.get_time_take()))
    ROUTE = load_obj('record/route', os.getenv('RandomSeed'), 'route', NetworkHelper.gen_route, True, G=G,
                     num_paths_to_select=int(os.getenv('RouteNum')))

    logging.info(strcat('network initial start ', Config.get_time_take()))
    PROTOCOL = [OPTLayer]
    net = Network(G, ROUTE, PROTOCOL)

    logging.info(strcat('network start ', Config.get_time_take()))
    deamons = net.network_start()

    logging.info(strcat('network end ', Config.get_time_take()))
    AtomosTask.preset_Ki_by_global(net.nodes.values())

    # net.add_node_task(OPTTask.opt_test, OPTTask.abc_params(net.ROUTE))
    # net.add_node_task(EPICTask.EPIC_test, EPICTask.abc_params(net.ROUTE))
    # net.add_node_task(PPVTask.ppv_test, PPVTask.abc_params(net.ROUTE))
    net.add_node_task(AtomosTask.atomos_test, PPVTask.abc_params(net.ROUTE))


    for i in deamons:
        i.join()
