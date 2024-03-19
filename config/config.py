import configparser
import logging
import os
import random
import time

from tools.tools import strcat


class Config:
    time0 = time.time()
    incomplete = 0
    lseg = 3
    lval = 2

    def __init__(self, ininame='config/config.ini'):
        self.ininame = ininame
        config = configparser.ConfigParser()
        config.read(ininame)
        for i in config.sections():
            for k, v in config[i].items():
                os.environ[k] = str(v)
        random.seed(int(os.getenv('RandomSeed')))

    @classmethod
    def add_incomplete(cls):
        cls.incomplete += 1
        logging.debug(strcat('Network leave:', cls.incomplete))

    @classmethod
    def complete(cls):
        cls.incomplete -= 1
        logging.info(strcat('Network leave:', cls.incomplete))
        return cls.incomplete

    @classmethod
    def is_complete(cls):
        if cls.incomplete == 0:
            return True
        else:
            return False

    @classmethod
    def get_time_take(cls):
        return time.time() - cls.time0
