from multiprocessing import Process, Pipe, Lock

from session import Handler
from client import get_client
from wlog import color_plog


log = color_plog('cyan').announce(__spec__)

pipe = None
process = None
lock = None


# A Persistent location of cached UUIDs.
MEM = {}


def start():
    """Called by an external process to initial the internal machinery of pipe
    communication and thread.
    """
    global pipe
    global process
    global lock

    pipe, child_conn = Pipe()
    lock = Lock()

    process = Process(target=message_handler, args=(child_conn, lock))
    process.start()
    log(pipe.recv())   # prints "[42, None, 'hello']"


def message_handler(pipe, lock):
    """A Process task handler performing a loop on pipe.recv()
    Pass any messages to the session.Handler
    """
    log('-- Starting connect handler\n')
    handler = Handler(pipe, lock)
    pipe.send(handler.init_response())
    while True:
        try:
            msg = pipe.recv()
            if msg == 'close':
                break
                handler.kill()
            handler.recv(msg)
        except (EOFError, KeyboardInterrupt):
            break
    pipe.close()


def connection_manager(uuid, request):
    """Accept a new request from a unique ID
    """
    # Send off....
    pipe.send(("init", uuid, request,))
    # get_client
    ok, client = get_client(uuid, request)

    if ok is False:
        print("Client failure", uuid)
        pipe.send(("client_failure", uuid, vars(client),))
        return False, client

    cache = MEM.get(uuid, None)
    if cache is None:
        log('New uuid', uuid)
        cache = {}
    else:
        cache['cache_load'] = True

    cache['entry_client'] = client
    pipe.send(("client", uuid, client,))
    return True, client

def stop():
    try:
        pipe.send('close')
    except BrokenPipeError:
        log('connect::pipe is already closed')
    process.join()
