from configparser import ConfigParser


def config(section='default'):
    cf = ConfigParser()
    cf.read('config.ini')
    return cf[section]
