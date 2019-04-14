import asyncio
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
from multiprocessing import Process

import connect
from protocol import MyServerProtocol
from factory import BroadcastServerFactory
import config
from wlog import plog as log

@asyncio.coroutine
def keyboard_interrupt_watch():
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    while True:
        yield from asyncio.sleep(1)
        # log("First Worker Executed")


# @asyncio.coroutine
# def secondWorker():
#     while True:
#         yield from asyncio.sleep(1)
#         log("Second Worker Executed")

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



def run(port=None, ip=None, keyboard_watch=True, **kw):
    """Run the server, using the given ip,port or extracting from the config.
    if the ip,port are given - and found within the config, the config arguments
    are chosen.
    """
    cpath = kw.get('config', None)
    conf = get_config(cpath)
    ip, port = find_address(conf, ip, port)
    uri = u"ws://{}:{}".format(ip, port)

    log('factory', uri)
    factory = kw.get('factory', BroadcastServerFactory(uri))
    factory.protocol = kw.get('protocol', MyServerProtocol)
    start_loop(factory, ip, port, keyboard_watch)


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


def start_loop(factory, ip, port, keyboard_watch=True):
    log('Run', ip, port)

    loop = asyncio.get_event_loop()
    coro_gen = loop.create_server(factory, ip, port)
    server = loop.run_until_complete(coro_gen)

    connect.start()

    if keyboard_watch:
        log('CTRL+C watch')
        asyncio.ensure_future(keyboard_interrupt_watch())

    try:
        log('Step into run run_forever')
        loop.run_forever()
        # CTRL+C works on the next message loop.
        # This is delayed if no messages are given.
    except KeyboardInterrupt as e:
        log('Server::KeyboardInterrupt')
    finally:
        connect.stop()
        server.close()
        log('Final close')
        loop.close()

if __name__ == '__main__':
    run()
