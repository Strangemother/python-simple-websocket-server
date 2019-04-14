import asyncio
from multiprocessing import Process, Pipe, Lock

from session import SessionManager
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
    global proc_pipes
    global process
    global lock

    pipe, child_conn = Pipe()
    lock = Lock()
    log('connect::start Process(message_handler)')
    process = Process(target=message_handler, args=(child_conn, lock))
    process.start()


    #loop = asyncio.get_event_loop()

    log('... Waiting for first response pipes')
    proc_pipes = pipe.recv()   # prints "[42, None, 'hello']"
    log('Recieved. Creating asyncio pipe_monitor')
    asyncio.ensure_future(pipe_monitor(pipe, proc_pipes))
    log('.Done. continue start.')


@asyncio.coroutine
def pipe_monitor(sender_pipe, proc_pipes):
    """Bridge the connection between the sesssion handler within the Process
    (message_handler) and this process.

    The initial response from the message_handler start recv() was a set of
    pipes generated within the session.SessionManager.
    Loop the child pipe of the proc_pipes pair. Wait for a recv() message
    from the session manager. Utilise the MEM of persistent 'connected'
    client caches.
    """

    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    log('Monitoring session pipe')
    p1 = proc_pipes[1]
    while True:
        try:
            if p1.poll():
                msg = p1.recv()
                #yield from asyncio.wait_for(p1.recv(), 1)
                result = recv_session_message(msg)
                if result is not None:
                    sender_pipe.send(result)
            else:
                yield from asyncio.sleep(.1)
        except (asyncio.TimeoutError):
            log('Pass.')
        except (KeyboardInterrupt, EOFError) as e:
            log('Kill pipe:', e)
            break
        #yield from asyncio.sleep(1)
    log("death of pipe monitor")


def recv_session_message(msg):
    """Receive a message from the session manager pipe.
    Return a value to send back to the session manager.
    """
    log('connect start while loop received a message from message_handler')
    log(msg)
    return None


def message_handler(pipe, lock):
    """A Process task handler performing a loop on pipe.recv()
    Pass any messages to the session.SessionManager
    """
    log('-- Starting connect handler\n')
    handler = SessionManager(pipe, lock)
    # send back into the start method -
    pipe.send(handler.init_response())
    while True:
        try:
            msg = pipe.recv()
            if msg == 'close':
                log('connect.message_handler received message from session pipe')
                log(message)
                break
                handler.kill()
            handler.recv(msg)
        except (EOFError, KeyboardInterrupt):
            break
    pipe.close()


def pipe_send(*a, _pipe=None):
    """
    Send a message to the waiting session.Handler. If more
    than one item is given as an argument, a tuple is sent.
    """
    if len(a) > 1:
        a= (a,)
    (_pipe or pipe).send(*a)


def connection_manager(uuid, request):
    """Accept a new request from a unique ID from the protocol.
    Send a remote signal followed by a get_client.
    Return a tuple of success, client dict.

    """
    # Send off....
    pipe_send("init", uuid, request)
    # get_client
    ok, client = get_client(uuid, request)

    if ok is False:
        print("Client failure", uuid)
        pipe_send("client_failure", uuid, vars(client))
        return False, client

    cache = MEM.get(uuid, None)
    if cache is None:
        log('New uuid', uuid)
        cache = {}
    else:
        cache['cache_load'] = True

    cache['entry_client'] = client
    pipe_send("client", uuid, client)
    MEM[uuid] = client
    return True, client


def stop():
    try:
        pipe_send('close')
    except BrokenPipeError:
        log('connect::pipe is already closed')
    process.join()
