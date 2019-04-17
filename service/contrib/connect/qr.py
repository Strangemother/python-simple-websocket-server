"""Validate a session with a QR client response.
"""
from contrib.base import SessionCallable

import sys

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
        token = payload.decode('utf')
        is_valid = au.validate_time_auth(token, self.data['secret'])
        if is_valid:
            return self.assert_valid()
        self.assert_fail()


    def created(self, index):
        self.log(f'QR created at index {index}')
