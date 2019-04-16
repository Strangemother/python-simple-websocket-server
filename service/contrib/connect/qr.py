"""Validate a session with a QR client response.
"""

from wlog import color_plog

log = color_plog('yellow').announce(__spec__)


class Authed(object):
    """assert the socket user has authorized with the connected
    site.

    Upon validation, check the database for a validate login.
    If false, wait for X and check again.
              wait for an event from the socket for valid or invalid
    If true, tell the manager 'valid'.
    """
    def __init__(self, manager, client_space):
        """
            Session: The users connected session information
            client_space: the persistent definition created by the owner
            session_stash: transient data kept in session outside this instance for
                           cross request persistence.
        """
        self.manager = manager
        self.client_space = client_space
        def ll(*a):
            if client_space.debug:
                self.manager.to_main_thread(client_space.uuid, *a)
            log(*a)

        self.log = ll
        self.log(f'Authed init::{client_space.uuid}')

    def recv_session(self, session, session_stash):
        self.session = session
        self.session_stash = session_stash
        self.log(f'Auth module index {session_stash["index"]}')

    def recv_msg(self, data, binary=False):
        """When _in-process_ the Auth instance captures messages directly from
        the client socket.
        """
