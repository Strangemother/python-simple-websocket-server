"""
The handler manages pipe msgs for background handling of a sibling
socket session happening elsewhere.
"""

from multiprocessing import Process, Pipe, Lock
from datetime import datetime
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

SESSIONS = {
}


class Handler(object):

    def __init__(self, pipe, lock):
        self.pipe = pipe
        self.lock = lock


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

    def kill():
        log('kill')


class SessionManager(Handler):
    """
    Handle messages given to recv(msg) to call the msg_ methods with the
    arguments. Designed to communicate through pipes within its own process -
    the session_manager is not within the same thread as the connect.* or
    websocket client.
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
        b = client_space.entry_username
        a = client_space.uuid


        if 'client' in session:
            log('Wooh. This client should not exist.')
            return self.fail_client(uuid, error.DUP_CLIENT,
                                    client=client_space, session=session)

        # set the client at auth 1 - the socket is welcome. Next onboard
        # based upon 'space' settings
        session['auth'] = AUTH.INIT
        # client.CLIENT
        log('Recv client', uuid, client_space)
        s = f'Yey. Client passed basic props. Please welcome - {a}:{b}'
        log(s)
        self.to_main_thread(uuid, s)
        # Begin modules as per client authing.

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
