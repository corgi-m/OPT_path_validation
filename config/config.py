import configparser
import os
import random
import time


class Config:
    time0 = time.time()

    def __init__(self, ininame='config/config.ini'):
        self.ininame = ininame
        config = configparser.ConfigParser()
        config.read(ininame)
        for i in config.sections():
            for k, v in config[i].items():
                os.environ[k] = str(v)
        random.seed(int(os.getenv('RandomSeed')))
