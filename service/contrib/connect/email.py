"""
"""
import sys

from service.contrib.base import SessionCallable

sys.path.append('C:/Users/jay/Documents/projects/websocket')
from manager import client
print('\n\nclient', client)
from manager.client import send_event


class Announce(SessionCallable):
    """assert the socket user has authorized with a QR Code previously authenticated
    through a users session.
    The QR code validates only if the message is a valid key.
    """

    def recv_msg(self, payload, binary=False):
        """When _in-process_ the Auth instance captures messages directly from
        the client socket.
        """
        return self.assert_valid()

    def on_connect(self):
        self.log('email on_connect')
        event = { 'email': self.data.get('email') }
        #send_event('smtp_send', event)
        #self.to_main_thread(self.uuid, 'smtp_send', event)
