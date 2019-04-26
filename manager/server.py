"""Maintain an authorative connection to the factory, [session] pipes and a thread
manager for third party attachment.
"""
from multiprocessing.managers import BaseManager
from multiprocessing import Process

import asyncio


PORT = 9018
ADDRESS = '127.0.0.1'
AUTH = b'84ytnp9qyn8p3tu8qcp394tpmj'

from service import wlog
log = wlog.color_plog('white')#.announce(__spec__)


class MainManager(BaseManager):
    """Existing within a unique process the manager serves functions
    across many clients.
    """


from queue import Queue

queue = Queue()

def get_queue():
    #log('Returning queue')
    return queue


def hello():
    log('Someone said hello to the server')
    return 'Return value'

def post(event_type, entity):
    uuid = entity.get('custom')
    log('Manager received post', event_type, uuid)
    m.pipes[0].send([uuid, event_type, entity])

def session_pipes(entity):
    m.pipes = entity
    log('Manager received session_pipes', m.pipes)


MainManager.register('get_queue', callable=get_queue)
MainManager.register('hello', hello)
MainManager.register('post', post)
MainManager.register('session_pipes', session_pipes)

def register(name, func):
    MainManager.register(name, func)


@asyncio.coroutine
def manager_loop_client(factory, session_pipes):
    """
    Utility to start the main procedures from the main thread; pushed into
    an asyncio ensures_futures
    """
    log('starting manager_loop_client')
    # yield from asyncio.sleep(2)
    m = MainManager(address=(ADDRESS, PORT), authkey=AUTH)
    m.register('hello')
    # factory.manager = m
    log('Connecting manager_loop', (ADDRESS, PORT))
    m.connect()
    log('Connected. Saying Hello.')
    m.hello()
    log('Stepping into loop.')
    m.session_pipes(session_pipes)
    while True:
        yield from asyncio.sleep(5)
        # clients = factory.clients
        #for cl in clients:
            #cl.send_text('Manager said hello')
            #print(cl.factory == factory)
        # log("First Worker Executed")from multiprocessing.managers import BaseManager


async def manager_server(factory, pipes):
    global m
    log('Starting manager_server', ADDRESS, PORT)
    m = MainManager(address=(ADDRESS, PORT), authkey=AUTH)
    m.factory = factory
    m.pipes = pipes
    s = m.get_server()
    s.serve_forever()
    return 0
    # while True:
    #     try:
    #         print('.s')
    #         s.serve_forever()
    #         yield from asyncio.sleep(.1)
    #     except (asyncio.TimeoutError):
    #         log('Pass.')
    #     except (KeyboardInterrupt, EOFError) as e:
    #         log('Kill pipe:', e)
    #         break
    #     except SystemExit:
    #         log('!! SystemExit exit')
    #     print('Started')
        #yield from asyncio.sle


async def main(factory, pipes):
    await manager_server(factory, pipes)

if __name__ == '__main__':
    asyncio.run(main(None, None))
