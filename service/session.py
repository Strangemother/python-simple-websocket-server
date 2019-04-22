"""
The handler manages pipe msgs for background handling of a sibling
socket session happening elsewhere.

    service.connect.pipe_monitor
"""
from multiprocessing import Process, Pipe, Lock
from datetime import datetime
from pydoc import locate
import error
import asyncio

from wlog import color_plog

MEM = {}

log = color_plog('magenta').announce(__spec__)


def start_process(loop_message_handler=None):
    """Called by an external process to initial the internal machinery of pipe
    communication and thread.
    """
    global pipe
    global proc_pipes
    global process
    global lock

    pipe, child_conn = Pipe()
    lock = Lock()
    _message_handler = loop_message_handler or message_handler
    log(f'connect::start Process({_message_handler})')
    process = Process(target=_message_handler, args=(child_conn, lock))
    process.start()


    #loop = asyncio.get_event_loop()

    log('... Waiting for first response pipes')
    proc_pipes = pipe.recv()   # prints "[42, None, 'hello']"
    log('Recieved. Creating asyncio pipe_monitor')

    asyncio.ensure_future(pipe_monitor(pipe, proc_pipes))
    log('.Done. continue start.')
    return pipe, proc_pipes, process, lock


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
                log(f'connect.message_handler received message from session pipe \n {msg}')
                handler.kill()
                break
            # Handler.recv
            handler.recv(msg)
        except (EOFError, KeyboardInterrupt):
            log('Closing message_handler')
            break
    handler.kill()
    pipe.close()


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
                read_pipe(p1, sender_pipe)
                continue
            yield from asyncio.sleep(.1)
        except (asyncio.TimeoutError):
            log('Pass.')
        except (KeyboardInterrupt, EOFError) as e:
            log('Kill pipe:', e)
            break
        #yield from asyncio.sleep(1)
    log("death of pipe monitor")


def read_pipe(p1, sender_pipe):
    """Called by the pipe_monitor, read the given pipe expecting a recv().
    """
    msg = p1.recv()
    print('session.read_pipe from pipe_monitor pipe 1', msg)
    #yield from asyncio.wait_for(p1.recv(), 1)
    result = recv_session_message(msg)
    if result is not None:
        sender_pipe.send(result)


def recv_session_message(msg):
    """Receive a message from the session manager pipe.
    Return a value to send back to the session manager.
    """
    if len(msg) <= 1:
        log('Badly formatted session manager response:', msg)
        return
    uuid, *args = msg

    ## WARNING!
    # This nasty little hack coverts the string ID from the POST to an
    # int ID stored upon message action.
    # I think is should be just a string - therefore the 'STORE' location
    # should store as a string.
    if uuid is None:
        log(f' !! recv_session_message received an unknown message:\n{msg}')
        return
    uuid = int(uuid)

    log('>', uuid)
    # Locking is not required with a async loop.
    # lock.acquire()

    cache = MEM.get(uuid)
    ret = f'recv_session_message: {args}'
    if cache is None:
        log(f' {uuid} not in MEM: {MEM}')
        log(cache.keys())
        return
    try:
        proto = cache['protocol']
        # protocol.MyServerProtocol.session_message
        proto.session_message(args)
    except TypeError as e:
        # dead protocol.
        log(f'\n\n --- Failed message to {uuid}\n{ret}\n{e}::{MEM.keys()}')
        log(MEM)
    return None




class AUTH:
    # All 'start' requests initially recieve a ZERO, denoting no auth has -
    # First layer auth is basic origin, host.
    ZERO = 0

    # Once an API key has matched a space and passed basic auth assign INIT
    # as the 'first' step without space protocol authentication.
    # All good users should have an INIT state - allowing an open connection.
    INIT = 1

# unique data for a connecting user
USER_DATA = {
    'test2': {
        # settings for each unit.
        'details': {
            'contrib.connect.auth.Password': { 'password': b'horse'},
            'contrib.connect.qr.Authed': { "secret": 'gegoyuja4liponix' },
        }
    },
    'test1': {
        'details': {
            'contrib.connect.auth.Password': { 'password': b'666'},
            'contrib.connect.sms.TextLocalAnnounce': {
                'tel': '447480924803',
                'debug': False,
                #'reply': 'http://3deb9232.ngrok.io'
            }#'debug': False },
        }
    }
}

SESSIONS = {}

# A Cache of python discovered routines
ROUTINES = {}

RAISE = 'raise'
CONTINUE = 'continue'


class Handler(object):

    def __init__(self, pipe, lock):
        self.pipe = pipe
        self.lock = lock
        self.log = log


    def init_response(self):
        self.my_pipes = Pipe()
        return self.my_pipes

    def recv(self, msg):
        """Receive a message from the pipe loop and call
        a method to handle the msg.

        """
        try:
            if isinstance(msg, tuple):
                name, uuid, *args = msg
            else:
                log(f'Handler anonymous message "{msg}"')
                return
        except ValueError as e:
            # not a tuple to unpack
            log('Handled unpackage', msg)
            return

        method = f"msg_{name}"
        log('Handler:', uuid, method)
        if hasattr(self, method):
            result = getattr(self, method)(uuid, *args)
        else:
            self.lost_recv(msg)

    def kill(self):
        log(f'kill {__name__}')
        self.my_pipes[0].close()
        self.my_pipes[1].close()

    def lost_recv(self, msg):
        log(f'!! Lost message to session, {msg}')


class SessionManager(Handler):
    """
        Handle messages given to recv(msg) to call the msg_ methods with the
        arguments. Designed to communicate through pipes within its own process -
        the session_manager is not within the same thread as the connect.* or
        websocket client.

        Content seen within:

            uuid: The unique ID of the connecting socket. Unique for every connection
                  Currently this is a id() hash of the socket client entity - but
                  this may change in the future
            session: The active user session created for the client socket. It's
                     considered fresh and voliatile.
            client_space: the API key content specifying the owners requests for the
                          socket intent. This is a persistent record from the database
                          and should not be used to store content.
    """

    def msg_init(self, uuid, request):

        if uuid in SESSIONS:
            return self.pickup(uuid, request)

        return self.start(uuid, request)

    def msg_client_failure(self, uuid, reason):
        """A client_failure message
        """
        self.fail_client(uuid, error.CLIENT_FAILURE, reason=reason)

    def msg_client(self, uuid, client_space):
        """Called by the pipe immediately after an init, after the remote
        connect manager has resolved the client object.
        If the client did not resolve msg_client_failure is called."""

        session = SESSIONS.get(uuid)
        if session is None:
            log('Client without a session?')

        if 'client' in session:
            log('Wooh. This client should not exist.')
            return self.fail_client(uuid, error.DUP_CLIENT,
                                    client=client_space, session=session)

        self.welcome(session, client_space)

    def get_session(self, uuid):
        return SESSIONS.get(uuid)

    def msg_message(self, uuid, payload, isBinary):
        """Receive a socket message from the procotol through the
        connect.message_manager. Pass the message the an existing routine.
        """
        self.log(f'Received message: len({len(payload)}), Binary: {isBinary}')
        routine = self._get_open_routine(uuid)
        routine.recv_msg(payload, isBinary)

    def msg_open(self, uuid):
        """An 'open' client has successfully authenticated the first stage
        as a good socket. The start() or pickup() method should have been
        called by an 'init' (msg_init(uuid, request)) message.
        """
        #self.log(f'Received open: {uuid}')
        routine = self._get_open_routine(uuid)

    def msg_content(self, uuid, content):
        """data content given from the protocol for the session to digest

            connect.message(uuid, content) -> pipe_send("content", uuid, content)
        """
        log('SESSION RECEIVED CONTENT', uuid, content)
        routine = self._get_open_routine(uuid)
        routine.recv_msg(content)
    def _get_open_routine(self, uuid):
        session = self.get_session(uuid)
        current = None
        if session is not None:
            current = session.get('routine')
        if current is None:
            self.log('No current routine? Did the user Auth correctly?')
            return
        return current
        # continue

    def welcome(self, session, client_space):
        # set the client at auth 1 - the socket is welcome. Next onboard
        # based upon 'space' settings
        session['auth'] = AUTH.INIT
        # client.CLIENT
        uuid = client_space.uuid
        log('Recv client', uuid, client_space)
        b = client_space.entry_username
        s = f'Yey. Client passed basic props. Please welcome - {uuid}:{b}'
        log(s)
        self.to_main_thread(uuid, s)

        # Begin modules as per client authing.
        session['connect'] = { 'index': 0 }
        ROUTINES[uuid] = {}
        # content returned from the on_connect hook.
        on_result = self.run_routine("connect", session, client_space)
        # force stop welcome?

    def run_routine(self, name, session, client_space):
        """Run the procedural steps for the client defined by the given name.
        Acting as middleware the session should perform all required steps
        before the routine is complete.
        """

        def ll(*a, **kw):
            if client_space.debug:
                self.to_main_thread(client_space.uuid, *a)
            log(*a, **kw)

        self.log = ll
        # ll('run_routine', session, client_space)

        current = self.get_current_routine(name, session, client_space)
        session_stash = session[name]
        current.recv_session(session, session_stash)
        # Store the active handler unit
        session['routine'] = current
        # Store the current proc for step actuation.
        session['current'] = name

        # Run the specific hook for the routine name. i.e 'connect'
        result = getattr(current, f"on_{name}")()
        # move pointer or wait for incoming.
        # Close and wait (sleep) for next step action.
        return result

    def get_current_routine(self, name, session, client_space):
        """Return the _current_ step the user should exist within, either new
        or existing. The given routine instance should manage the success of the
        step to allow transition to the next step.
        """
        routines = self.get_routines(name, client_space)
        ## Get alive or new routine.

        # save point
        session_stash = session[name]
        # current position
        index = session_stash['index']
        # Generate expected instance; or find from working session
        _Routine, init_session_stash = routines[index]
        ## populate with existing data
        self.log('Generating new current routine instance...', index, _Routine)

        if ('valid' in init_session_stash) is False:
            self.log('Setting init_session_stash[valid] as False')
            init_session_stash['valid'] = False

        # decorate with user specific init data
        client_data = self.get_client_data(_Routine.pointer, session, client_space)
        init_session_stash.update(client_data or {})
        # Provide with the existing session content for the module
        # to utilise as required.
        # contrib.connect.site.Authed
        instance = _Routine(self, client_space, init_session_stash)
        instance.created(name, index)
        self.log(instance.__module__, instance.__class__.__name__)

        return instance

    def get_client_data(self, loc_string, session, client_space):
        username = client_space.entry_username
        self.log(f'get_client_data {loc_string} {session}, {username}', color='white')
        # user specific record
        data = USER_DATA.get(username)
        if data is None:
            self.log(f'User data does not exist for {username}')
            return
        # fetch the addon data for the given routine - ID'd by its import string
        loc = data.get('details').get(loc_string, None)
        return loc

    def get_routines(self, name, client_space):
        """Given a list of string dotted notations, resolve the pointer
        objects classes or functions and return a tuple.
        If the routines for the client already exist (previously resolved),
        return the cache value.
        """
        locations = client_space[name]
        cache_val = ROUTINES.get(client_space.uuid).get(name, None)
        if cache_val is not None:
            return cache_val

        # resolve classes
        items = ()

        for loc in locations:
            init_session_stash = {}
            self.log('locating', loc)
            if isinstance(loc, (tuple, list,)):
                loc, init_session_stash = loc
            discovered = locate(loc)
            if discovered is None:
                action = self.assert_bad_pointer(loc, name, client_space)
                err = f'Cannot resolve pointer: {name} "{loc}" for {client_space.uuid}'
                if action == RAISE:
                    raise Exception(err)
                if action == CONTINUE:
                    spacer = '\n\n{}\n\n'.format('-' * 40)
                    self.log(f'\n{spacer}CONTINUE - Ignore issue:\n{err}{spacer}\n', color='red')
                    continue

            discovered.pointer = loc

            item = (discovered, init_session_stash,)
            items += (item, )

        self.log(f'Recording new items to ROUTINES[{client_space.uuid}][{name}]')
        ROUTINES[client_space.uuid][name] = items
        self.log("Found:", items)
        return items

    def assert_bad_pointer(self, pointer, name, client_space):
        """The given string pointer from the client_space did not resolve a
        callable entity.
        """
        self.log(f'Bad session routine pointer {name} "{pointer}"')

        return RAISE
        #return CONTINUE

    def to_main_thread(self, *a):
        if len(a) == 1:
            a = a[0]
        return self.my_pipes[0].send(a)

    def start(self, uuid, request):
        """Start a new session, receiving a UUID from the main
        websocket client.
        """
        now = datetime.now()
        # pre test
        session = dict(uuid=uuid, request=request, start_time=now)
        log('new user', uuid, '- wait for client', session['start_time'])
        # Ensure websocket session is ready - load channel specific modules
        session['auth'] = AUTH.ZERO
        SESSIONS[uuid] = session

    def pickup(self, uuid, request):
        """A Session reinitiated from a pipe 'init'.
        continue the session or perform a refuse
        """
        session = SESSIONS.get(uuid)
        log('pickup session', uuid)

    def fail_client(self, uuid, error_id, **kw):
        """Capture a client failure with the given uuid and error constant
        givden.
        """
        log('CLIENT FAIL', uuid, error_id, kw)
        session = SESSIONS.get(uuid, None)
        if session is None:
            return

        log('Deleting session', uuid)
        del SESSIONS[uuid]

        routines = ROUTINES.get(uuid, None)
        if routines is None:
            return

        log('Deleting routines', uuid)
        del ROUTINES[uuid]

    def present_valid(self, unit):
        """Assert the given unit as valid, being asserted by the unit itself.
        """
        self.log('Manager present_valid')
        session = unit.session
        uuid  = unit.client_space.uuid
        self_session = self.get_session(uuid)
        name = self_session['current']
        unit.data['valid'] = True
        self_session[name]['valid'] = True

        if unit == self_session['routine']:
            # The current routine has asserted  itself
            self.log(f'routine validation of {uuid}')
            self.step_session(name, session, unit.client_space, session['routine'])

    def step_session(self, name, session, client_space, current=None):
        """Perform a change to the next session unit index.
        If the session subset is complete the session manager will
        handle the loading of the next substep and validation.

            name: the substep name e.g 'connect'
            session: the active socket session tracking user data
            client_space: API assignment from the owner persistent settings
        """
        uuid = client_space.uuid
        if current is None:
            # resolve client
            self_session = self.get_session(uuid)
            current = self_session['routine']
        # IndexError: tuple index out of range

        session_stash = session[name]
        self.log(f'routine validation of {uuid}', name, session_stash)
        session_stash['index'] += 1
        current.close()
        self.run_routine(name, session, client_space)

    def present_fail(self, unit):
        """Assert the given unit as valid, being asserted by the unit itself.
        """
        self.log('Manager present_fail')
        session = unit.session
        uuid  = unit.client_space.uuid
        self_session = self.get_session(uuid)
        name = self_session['current']
        session[name]['valid'] = False
        self_session[name]['valid'] = False

        if unit == self_session['routine']:
            # The current routine has asserted  itself
            self.log(f'FAIL routine validation of {uuid}')

