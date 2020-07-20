import logging
import configparser
import os

class configReader():
    '''
    Dedicated class to realize a configReader Singleton class for the webservice so it wont interfere with the tcp-server configReader.
    The webservice is not a module and is meant to stand alone in the future while it still will be startet by the main 'server_start.py' call.
    '''
    config = configparser.ConfigParser()

    def __init__(cls):
        pass

    @classmethod
    def loadConfig(cls, path):
        if os.path.exists(path):
            logging.debug('Config file found!')
            cls.path = path
            cls.config.read(path)
        else:
            logging.warning('Config file not found. Use the TCP server to generate a new config file!')
            return -1

    @classmethod
    def updateConfig(cls, section, key, newValue):
        cls.config[section] = {key : newValue}
        with open(cls.path, 'w') as configFile:
            cls.config.write(configFile)
        return 0

    @classmethod
    def returnEntry(cls, section, key):
        return cls.config[section][key]
