from websocket import create_connection

from service.wlog import color_plog
log = color_plog('red').announce(__spec__)

# A record of users associated with an API key.
USERNAMES = {
    'api_key_1': ('test1', ('entries_url_0ASD9F0AIF', '',) ),
    'api_key_2': ('test1', 'key123'),
}

PUBLIC = {
    'daves-endpoint': ('test1', 'api_key_1', 'entries_url_0ASD9F0AIF'),
    'txt': ('test1', 'api_key_1', 'entries_url_0ASD9F0AIF'),
}

# Persistent records...
CLIENTS = {
    'test2': {},
    'test1': {
        # A single socket system.
        'api_key_1': dict(
                # Flag for more output and freedom
                debug=True,
                # Accessible openers
                origins=('https://', 'https://', 'file://', 'ws://'),
                # API key URL or param key
                entries=('', 'entries_url_0ASD9F0AIF',),
                # Allowed incoming host
                hosts=('127.0.0.1', '192.168.1.104', 'localhost', '*'),
                # modules for authenticating the onConnect; AUTH 0.
                connect=(
                        ('service.contrib.connect.email.Announce', {},),
                        ('service.contrib.connect.auth.Password',{ 'password': b'secret'}),
                        ('service.contrib.connect.totp.Authed', { "secret": 'gegoyuja4liponix' }, ),
                        ('service.contrib.connect.sms.TextLocal',
                            {
                                'apikey': '/TCFoNjKR6I-RdT4GsnSVj9oEjzuRfU08UZ1lYBYrH',
                                # The user must reply on text.
                                #'sms_confirm': True,
                                'ask_random': True,
                                # catch-all endpoint for receipts
                                'receipt_url': 'http://one.briansdojo.co.uk:8000/sms/receipt/',
                                #'debug': True,
                            },),
                    )
            ),
        'api_key_2': dict(
                debug=True,
                origins=('file://', 'ws://'),
                entries=('key123',),
                hosts=('127.0.0.1',),
                connect=(
                        ('service.contrib.connect.auth.Password', { 'password': b'secret'}),
                    )
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
    if api_key is None:
        # HEaders not available; use params
        api_key = request.params.get('api_key', None)
        if api_key is not None:
            api_key = api_key[0]
        else:
            log('get_client api_key failure')

    # Remove the first, and replace all / with -

    path = '-'.join(request.path.split('/')[1:])
    # build name
    username, user_pointer = get_username_pointer(path, api_key)
    # return config specific to key
    ok, space = get_user_space(username, user_pointer)

    if ok is False:
        log('-- space failure\n')
        space['fail'] = ok
        return ok, space

    space.user_pointer = user_pointer
    space.uuid = uuid

    # Check the basic path, origin, peer - this should move...
    if (user_pointer.path in space.entries) is False:
        log(f'Bad path: "{path}" is not in {space.entries}')
        return False, space
    assert request.host in space.hosts
    assert request.origin in space.origins

    return ok, space


def get_username_pointer(path, api_key):
    """Return a username for the given api key - only if the 'path' mathes the
    stored path in USERNAMES
    """
    log(f'get_username({path}, {api_key})')
    udata = USERNAMES.get(api_key, None)
    allowed_paths = ''
    if udata is None:
        resource = PUBLIC.get(path, None)
        if resource:
            # found a pointer to private content
            log(f'Found public URL "{path}" for api_key: {api_key}: {resource}')
            real_user = api_key
            public_path = path
            username, api_key, path = resource
            log(f'Connecting user "{real_user}" to "{username}::{api_key}" through "{path}"')
            return real_user, UserPointer(username, api_key, path, public_path)
        else:
            log(f'bad api_key: "{api_key}" is not a client.USERNAMES through {path}')
    else:
        username, allowed_paths = udata
        if path in allowed_paths:
            return username, UserPointer(username, api_key, path, path)
    log(f'Will not return username, given path "{path}" does not match allowed path "{allowed_paths}"')

    return (None, None, )


class UserPointer(object):

    def __init__(self, username, api_key, path, public_path):
        self.username = username
        self.api_key = api_key
        self.path = path
        self.public_path = public_path


def get_user_space(username, user_pointer):
    """Return a persistent record of the user configuration relative to the given
    username and API key.
    """
    if user_pointer is None:
        log('UserPointer is None for', username)
        return False, Struct({})
    api_key = user_pointer.api_key

    client = CLIENTS.get(user_pointer.username)
    if client is None:
        log('Username does not exist:', username)
        return False, Struct({
                "reason": f"username does not exist {username}",
                "username": username
            })
    space = client.get(api_key, None)
    if space is None:
        log(f'client space "{api_key}" for "{username}" does not exist - ')
        return False, Struct({
                "reason": f'Client space "{api_key}" does not exist for {username}',
                "username": username

            })

    space['entry_username'] = username
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

    def __getitem__(self, k):
        return self.__dict__[k]

    def __repr__(self):
        keys = dir(self)
        return f"<client.Struct {keys}>"
