from wlog import plog as log
from websocket import create_connection


def get_client(ip, port):
    uri = 'ws://{ip}:{port}'.format(ip=ip, port=port)
    log('Client', uri)
    ws = create_connection(uri)
    return ws
