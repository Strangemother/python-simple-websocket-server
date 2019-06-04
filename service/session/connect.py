import asyncio
from multiprocessing import Process, Pipe, Lock

from service.session.session import SessionManager, start_process, pipe_monitor, MEM
from service.client.client import get_client
from service.wlog import color_plog


log = color_plog('cyan').announce(__spec__)

global_pipe = None
process = None
lock = None


# A Persistent location of cached UUIDs.


def start(ip, port):
    """Called by an external process to initial the internal machinery of pipe
    communication and thread.
    """
    global global_pipe
    global proc_pipes
    global process
    global lock

    global_pipe, proc_pipes, process, lock = start_process()

    return proc_pipes


def pipe_send(*a, _pipe=None):
    """
    Send a message to the waiting session.Handler. If more
    than one item is given as an argument, a tuple is sent.
    """
    if len(a) > 1:
        a = (a,)
    (_pipe or global_pipe).send(*a)


def connection_manager(uuid, request, protocol):
    """Accept a new request from a unique ID from the protocol.
    Send a remote signal followed by a get_client.
    Return a tuple of success, client dict.

    """
    # Send off....
    pipe_send("init", uuid, request)
    # get_client
    ok, client = get_client(uuid, request)

    if ok is False:
        log("Client failure", uuid)
        pipe_send("client_failure", uuid, vars(client))
        return False, client

    cache = MEM.get(uuid, None)
    if cache is None:
        log('New uuid', uuid)
        cache = {}
    else:
        cache['cache_load'] = True

    cache['entry_client'] = client
    cache['protocol'] = protocol

    log(f'!! connection_manager Cache connection: {uuid}')
    pipe_send("client", uuid, client)
    MEM[uuid] = cache
    return True, client


def close_manager(uuid, error, protocol):
    pipe_send("close", uuid, error)
    cache = MEM.get(uuid, None)
    # change this to a Mark and sweep.
    if cache is None:
        return False, None

    del MEM[uuid]
    # close...
    log(f'!! close_manager deleted connection: {uuid}:"{error}"')
    return True, cache


def open_manager(uuid, protocol):
    pipe_send("open", uuid)
    cache = MEM.get(uuid, None)

    log(f'!! open_manager assert connection: {uuid}')
    return True, cache


def message(uuid, content):
    pipe_send("content", uuid, content)
    return True


def message_manager(uuid, payload, isBinary):
    """
    Send the message to the manager. Return any next-step the protcol
    should action - such as 'drop connection'
    """
    pipe_send("message", uuid, payload, isBinary)
    action = {}

    log(f'!! message_manager message: {uuid}')
    # back to protocol.
    return True, action


def stop():
    try:
        pipe_send('close')
    except BrokenPipeError:
        log('connect::pipe is already closed')
    process.join()
