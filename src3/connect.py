from multiprocessing import Process, Pipe, Lock


def message_handler(pipe, lock):
    pipe.send([42, None, 'hello'])
    while True:
        try:
            msg = pipe.recv()
            if msg == 'close':
                break


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
    print(pipe.recv())   # prints "[42, None, 'hello']"


def stop():
    try:
        pipe.send('close')
    except BrokenPipeError:
        print('connect::pipe is already closed')
    process.join()


def connection_manager(uuid, request):
    """Accept a new request from a unique ID
    """
    # Send off....
    pipe.send((uuid, request,))
    # get_client
    ok, client = get_client(uuid, request)

    if ok is False:
        return False, client

    cache = MEM.get(uuid, None)
    if cache is None:
        print('New uuid', uuid)
        cache = {}

    cache['entry_client'] = client
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
    space = get_user_space(username, api_key)
    if space is None:
        print('\nspace failure\n')
        space = Struct({ 'fail': True })
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
        print('bad api_key')
        return

    username, allowed_path = udata
    if allowed_path == path:
        return username
    print('Will not return username, given path does not match allowed path')


def get_user_space(username, api_key):
    """Return a persistent record of the user configuration relative to the given
    username and API key.
    """
    client = CLIENTS.get(username)
    if client is None:
        return
    space = client[api_key]
    res = Struct(space)
    return res


class Struct(object):
    entries = None
    hosts = None
    origins = None

    def __init__(self, o):
        self.__dict__.update(o)
