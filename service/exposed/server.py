import sys
from multiprocessing import Process
import asyncio

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

from service import config
from service.wlog import color_plog

from service.session import connect
from service.exposed import keyboard

from service.exposed.factory import BroadcastServerFactory
from service.server.protocol import MyServerProtocol

sys.path.append('C:/Users/jay/Documents/projects/websocket/manager')

from server import manager_loop_client

session_pipes = None

log = color_plog('white').announce(__spec__)


def run(port=None, ip=None, keyboard_watch=True, **kw):
    """Run the server, using the given ip,port or extracting from the config.
    if the ip,port are given - and found within the config, the config arguments
    are chosen.
    """
    cpath = kw.get('config', None)
    conf = config.get_config(cpath)
    ip, port = config.find_address(conf, ip, port)
    uri = u"ws://{}:{}".format(ip, port)

    log('factory', uri)

    server_kwargs = dict(server=kw.get('name', 'No Name'))
    factory = kw.get('factory', BroadcastServerFactory(uri, **server_kwargs))
    factory.protocol = kw.get('protocol', MyServerProtocol)
    start_loop(factory, ip, port, keyboard_watch)


def start_loop(factory, ip, port, keyboard_watch=True):
    """ Start the server, manager client and run_loop"""
    log('Run', ip, port)

    if keyboard_watch:
        keyboard.ensure_keyboard_interrupt_watch()

    server, loop = create_server(factory, ip, port)
    ensure_manager_client(factory, ip, port)
    run_loop(loop, server)


def run_loop(loop, server):
    """Perform a blocking loop for the ascynio loop. Kill with keyboard interrupt
    """
    try:
        log('Step into run run_forever')
        loop.run_forever()
        # CTRL+C works on the next message loop.
        # This is delayed if no messages are given.
    except KeyboardInterrupt as e:
        log('Server::KeyboardInterrupt')
    finally:
        close(server, loop)


def close(server=None, loop=None):
    """Perform a final close on all open handlers:
    connect, server and loop
    """

    connect.stop()

    if server:
        server.close()

    log('Final close')
    loop = loop or asyncio.get_event_loop()
    loop.close()


def ensure_manager_client(factory, ip, port):
    session_pipes = connect.start(ip, port)
    asyncio.ensure_future(manager_loop_client(factory, session_pipes))
    return session_pipes


def create_server(factory, ip, port):
    loop = asyncio.get_event_loop()
    #https://docs.python.org/3/library/asyncio-eventloop.html#creating-network-servers
    # https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.Server
    # https://docs.python.org/3/library/asyncio-protocol.html#asyncio-protocol
    coro_gen = loop.create_server(factory, ip, port)
    server = loop.run_until_complete(coro_gen)
    return server, loop


if __name__ == '__main__':
    run()
