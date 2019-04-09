
from websocket import create_connection
def get_client(ip, port):
    uri = 'ws://{ip}:{port}'.format(ip=ip, port=port)
    print('Client', uri)
    ws = create_connection(uri)
    return ws
