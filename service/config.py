"""Load config tools
"""
import yaml
from service.wlog import color_plog
log = color_plog('white').announce(__spec__)


def load(filename):
    """
    Load a yaml file and return a tuple for success, content
    """
    with open(filename, 'r') as stream:
        try:
            return True, yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            return False, exc

def get_config(path=None):
    """"
    Load the given filepath expecting a config yaml. If the given path is None,
    return an empty dict.
    """
    conf = {}
    if path is None:
        log('No config path defined')
        return conf
    log('loading config', path)
    ok, conf = config.load(path)
    if ok is False:
        log('config load issue:', conf)
        conf = {}

    return conf

def find_address(conf, ip, port):
    """Extract the ip address and port for the server from the given config
    or arguments. The config takes precedence
    """
    if 'websocket' in conf:
        log('conf has websocket sub')
        conf = conf.get('websocket')
        port = conf.get('port', port) or 9000
        ip = conf.get('address', ip) or '0.0.0.0'
        return ip, port
    port = port or conf.get('port', 9000)
    ip = ip or conf.get('address', '0.0.0.0')
    return ip, port
