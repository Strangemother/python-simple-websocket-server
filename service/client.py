from wlog import plog as log
from websocket import create_connection


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


def connect(ip, port):
    uri = 'ws://{ip}:{port}'.format(ip=ip, port=port)
    log('Client', uri)
    ws = create_connection(uri)
    return ws


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
    # build name
    username = get_username(path, api_key)
    # return config specific to key
    ok, space = get_user_space(username, api_key)
    if ok is False:
        log('-- space failure\n')
        space['fail'] = ok
        return ok, space
    space.uuid = uuid

    # Check path, origin, peer,
    assert path in space.entries
    assert request.host in space.hosts
    assert origin in space.origins

    return ok, space


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

