from multiprocessing import Process, Pipe, Lock

from wlog import plog as log

DUP_CLIENT = 'dup_client', "Duplicate Client or client already exists in session"
CLIENT_FAILURE = 'client_failure', "A client failure given through the remote pipe"


def message_handler(pipe, lock):

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


pipe = None
process = None
lock = None

# A Persistent location of cached UUIDs.
MEM = {}

USERNAMES = {
    'api_key_1': ('test1', '/')
}

# Persistend records...
CLIENTS = {
    'test': {
        'api_key_1': dict(
                origins=('https://', 'https://', 'file://', 'ws://'),
                entries=('/', '/0ASD9F0AIF_my_special_app_key',),
                hosts=('192.168.1.104', 'localhost', '*'),
            )
    }
}


"""
The handler manages pipe msgs for background handling of a siling
socket session happening elsewhere.
"""
SESSIONS = {
}

class Handler(object):

    def __init__(self, pipe, lock):
        self.pipe = pipe
        self.lock = lock

    def init_response(self):
        return [42, True, 'Howdy']

    def recv(self, msg):
        name, uuid, *args = msg
        method = f"msg_{name}"
        log('Handler:', uuid, method)
        if hasattr(self, method):
            result = getattr(self, method)(uuid, *args)

    def msg_init(self, uuid, request):

        if uuid in SESSIONS:
            return self.pickup(uuid, request)

        return self.start(uuid, request)

    def pickup(self, uuid, request):
        """A Session reinitiated from a pipe 'init'.
        continue the session or perform a refuse
        """
        session = SESSIONS.get(uuid)
        log('pickup session', uuid)

    def msg_client_failure(self, uuid, reason):
        """A client_failure message
        """
        self.fail_client(uuid, CLIENT_FAILURE, reason=reason)

    def start(self, uuid, request):
        """Start a new session, receiving a UUID from the main
        websocket client.
        """
        now = datetime.now()
        session = dict(uuid=uuid, request=request, start_time=now)
        # Begin modules as per client authing.
        log('new user', uuid, '- wait for client', session['start_time'])

    def msg_client(self, uuid, client):
        session = SESSIONS.get(uuid)
        if 'client' in session:
            log('Wooh. This client should not exist.')
            return self.fail_client(uuid, DUP_CLIENT,
                                    client=client, session=session)

        log('Recv client', uuid, client)



    def fail_client(self, uuid, error_id, **kw):
        """Capture a client failure with the given uuid and error constant
        givden.
        """
        log('CLIENT FAIL', uuid, error_id, kw)


    def kill():
        log('kill')


from datetime import datetime

def start():
    """Called by an external process to initial the internal machinery of pipe
    communication and thread.
    """
    global pipe
    global process
    global lock

    parent_conn, child_conn = Pipe()
    pipe = parent_conn
    lock = Lock()
    process = Process(target=message_handler, args=(child_conn, lock))
    process.start()
    log(pipe.recv())   # prints "[42, None, 'hello']"


def stop():
    try:
        pipe.send('close')
    except BrokenPipeError:
        log('connect::pipe is already closed')
    process.join()


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


def get_client(uuid, request):
    """Return a tuple of success and client data

        request:  '_is_public', 'extensions', 'headers', 'host', 'origin',
                'params', 'path', 'peer', 'protocols', 'version'
        path:           '/'
        peer:           'tcp:192.168.1.104:54454'
        protocols:       []
        host:           '192.168.1.104'
        version:         13
        headers:        {'host': '192.168.1.104:8004', 'connection': 'Upgrade',
                         'pragma': 'no-cache', 'cache-control': 'no-cache',
                         'upgrade': 'websocket', 'origin': 'file://',
                         'sec-websocket-version': '13', 'user-agent':
                         'Mozi ... 6 Safari/537.36',
                         'accept-encoding': 'gzip, deflate',
                         'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                          'cookie': 'mainServerInstance=',
                          'sec-websocket-key': 'bF1BACwsnSbWc60tgzqxjw==',
                          'sec-websocket-extensions': 'permessage-deflate;
                                client_max_window_bits'}
        origin:         'file://'
        params:
    """


    # sign up public owner key.
    api_key = request.headers.get('api_key', None)
    # Remove the first, and replace all / with -
    path = '-'.join(request.path.split('/')[1:])
    request_username = request.headers.get('username')
    # build name
    username = get_username(path, api_key)
    # return config specific to key
    ok, space = get_user_space(username, api_key)
    if ok is False:
        log('-- space failure\n')
        space['fail'] = True
        return False, space
    space.uuid = uuid

    # Check path, origin, peer,
    assert path in space.entries
    assert request.host in space.hosts
    assert origin in space.origins

    return True, space


def get_username(path, api_key):
    """Return a username for the given api key - only if the 'path' mathes the
    stored path in USERNAMES
    """
    udata = USERNAMES.get(api_key, None)
    if udata is None:
        log('bad api_key')
        return

    username, allowed_path = udata
    if allowed_path == path:
        return username
    log('Will not return username, given path does not match allowed path')


def get_user_space(username, api_key):
    """Return a persistent record of the user configuration relative to the given
    username and API key.
    """
    client = CLIENTS.get(username)
    if client is None:
        log('Username does not exist:', username)
        return False, Struct({
                "reason": f"username does not exist {username}",
                "username": username
            })
    space = client[api_key]
    res = Struct(space)
    return True, res


class Struct(object):
    entries = None
    hosts = None
    origins = None

    def __init__(self, o):
        self.__dict__.update(o)

    def __setitem__(self, k, v):
        self.__dict__[k] = v

