import asyncio
from service.wlog import plog as log

def ensure_keyboard_interrupt_watch():
    log('CTRL+C watch')
    asyncio.ensure_future(keyboard_interrupt_watch())



@asyncio.coroutine
def keyboard_interrupt_watch():
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    while True:
        yield from asyncio.sleep(1)
        # log("First Worker Executed")
