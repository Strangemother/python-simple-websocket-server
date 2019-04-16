"""
The handler manages pipe msgs for background handling of a sibling
socket session happening elsewhere.
"""
from multiprocessing import Process, Pipe, Lock
from datetime import datetime
from pydoc import locate
import error

from wlog import color_plog


log = color_plog('magenta').announce(__spec__)


class AUTH:
    # All 'start' requests initially recieve a ZERO, denoting no auth has -
    # First layer auth is basic origin, host.
    ZERO = 0

    # Once an API key has matched a space and passed basic auth assign INIT
    # as the 'first' step without space protocol authentication.
    # All good users should have an INIT state - allowing an open connection.
    INIT = 1

SESSIONS = {}

# A Cache of python discovered routines
ROUTINES = {}

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

    def kill(self):
        log(f'kill {__name__}')
        self.my_pipes[0].close()
        self.my_pipes[1].close()


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
        self.run_routine("connect", session, client_space)

    def run_routine(self, name, session, client_space):
        """Run the procedural steps for the client defined by the given name.
        Acting as middleware the session should perform all required steps
        before the routine is complete.
        """

        def ll(*a):
            if client_space.debug:
                self.to_main_thread(client_space.uuid, *a)
            log(*a)

        self.log = ll
        # ll('run_routine', session, client_space)

        current = self.get_current_routine(name, session, client_space)
        # assert step
        # move pointer or wait for incoming.
        # Close and wait (sleep) for next step action.

    def get_current_routine(self, name, session, client_space):
        """Return the _current_ step the user should exist within, either new
        or existing. The given routine instance should manage the succes of the
        step to allow transition to the next step.
        """
        routines = self.get_routines(name, client_space)
        ## Get alive or new routine.

        # save point
        session_stash = session[name]
        # current position
        index = session_stash['index']
        # Generate expected instance; or find from working session
        _Routine = routines[index]
        ## populate with existing data

        # Provide with the existing session content for the module
        # to utilise as required.
        self.log('Generating current routine instance...')
        instance = _Routine(self, session, client_space, session_stash)

        return instance

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
            self.log('locating', loc)
            items += (locate(loc), )

        self.log(f'Recording new items to ROUTINES[{client_space.uuid}][{name}]')
        ROUTINES[client_space.uuid][name] = items
        self.log("Found:", items)
        return items

    def to_main_thread(self, *a):
        if len(a) == 1:
            a = a[0]
        return self.my_pipes[0].send(a)

    def start(self, uuid, request):
        """Start a new session, receiving a UUID from the main
        websocket client.
        """
        now = datetime.now()
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
