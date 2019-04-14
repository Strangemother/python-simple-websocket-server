"""
The handler manages pipe msgs for background handling of a siling
socket session happening elsewhere.
"""

from datetime import datetime
import error
from wlog import color_plog
log = color_plog('magenta')
log(__name__, __file__)

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
        self.fail_client(uuid, error.CLIENT_FAILURE, reason=reason)

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
            return self.fail_client(uuid, error.DUP_CLIENT,
                                    client=client, session=session)

        log('Recv client', uuid, client)



    def fail_client(self, uuid, error_id, **kw):
        """Capture a client failure with the given uuid and error constant
        givden.
        """
        log('CLIENT FAIL', uuid, error_id, kw)


    def kill():
        log('kill')

