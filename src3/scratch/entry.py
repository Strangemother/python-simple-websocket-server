"""Base entry unit to accept websockets and send them to the correct procedures.
"""
import asyncio
import json
import logging
import websockets

logging.basicConfig()

STATE = {'value': 0}
IP = 'localhost'
PORT = 8004
USERS = set()


class SocketClient(object):

    def __init__(self, websocket, path=None, **kwargs):
        self.ws = websocket
        self.path = path
        self.kw = kwargs

    def send(self, *a, **kw):
        self.ws.send(*a, **kw)


def state_event():
    return json.dumps({'type': 'state', **STATE})

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def send_all(data):
    if USERS:       # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(data) for user in USERS])

async def register(websocket, path):
    """Register an incoming user to the system. Upon failure, the user will not
    access the socker"""

    client = SocketClient(websocket)
    USERS.add(client)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def entry_point(websocket, path):
    """The first method accepting a websocket from serve.
    """
    await register(websocket, path)
    print('Register', websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            print('Message', message)
            data  = message
            # If await is not here; this function doesn't call.
            await send_all(data)
    finally:
        await unregister(websocket)

logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

logging.info('Serving', IP, PORT)
serve = websockets.serve(entry_point, IP, PORT)
try:
    asyncio.get_event_loop().run_until_complete(serve)
    print('Run forever', IP, PORT)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logging.info('User cancelled loop')
