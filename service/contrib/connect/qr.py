"""Validate a session with a QR client response.
"""
from contrib.base import SessionCallable


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
