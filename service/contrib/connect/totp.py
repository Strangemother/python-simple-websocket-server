"""Use a time based auth token to authenticate an incoming user during a connect
phase.

Presuming the user has previously signed-up and authenticated a google
authenticator, they present a 'token' through the pipe. If the given
token matches the internal generated token (based upon the secret), assert_valid.
"""
import sys


from service.contrib.base import SessionCallable

sys.path.append('C:\\Users\\jay\\Documents\\projects\\websocket\\qr')
import authenticator as au


class Authed(SessionCallable):
    """assert the socket user has authorized with a QR Code previously authenticated
    through a users session.
    The QR code validates only if the message is a valid key.
    """

    def recv_msg(self, payload, binary=False):
        """When _in-process_ the Auth instance captures messages directly from
        the client socket.
        """
        self.log(f'QR Auth module received message, len({len(payload)}) Binary: {binary}')
        if isinstance(payload, str) is False:
            self.log(f'Did not present correct payload: {payload}')
            self.assert_fail()
        token = payload.decode('utf')

        # Debug hotwire.
        if (self.client_space.debug is True) and token == '666':
            self.log('\n\n hotwire allowed - - MARK OF TEH GOATS!! RAAAAN!')
            return self.assert_valid()

        is_valid = au.validate_time_auth(token, self.data['secret'])
        if is_valid:
            return self.assert_valid()
        self.assert_fail()


    def created(self, action, index):
        self.log(f'QR created at index {action}::{index}')
