import logging
import configparser
import os

class configReader():
    config = configparser.ConfigParser()

    def __init__(self):
        pass

    @classmethod
    def loadConfig(cls, path):
        if os.path.exists(path):
            logging.info('Config file found!')
            cls.config.read(path)
        else:
            logging.warning('Config file not found. A new config file will be generated..')
            cls.createConfigFile(path)

    @classmethod
    def createConfigFile(cls, path):
        try:
            with open(path, 'w') as configFile:
                cls.config.write(configFile)
                cls.config.read(path)
                logging.info('Config file created and loaded')
        except Exception as e:
            logging.warning(str(e))
        return 0

    @classmethod
    def updateConfig(cls, section, key, newValue):
        cls.config[section] = {key : newValue}
        with open(self.path, 'w') as configFile:
            cls.config.write(configFile)
        return 0

    @classmethod
    def returnEntry(cls, section, key):
        return cls.config[section][key]
