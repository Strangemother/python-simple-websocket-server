from wlog import color_plog

log = color_plog('yellow').announce(__spec__)


class Authed(object):
    """assert the socket user has authorized with the connected
    site.
    """
    def __init__(self, manager, session, client_space, session_stash):
        """
            Session: The users connected session information
            client_space: the persistent definition created by the owner
            session_stash: transient data kept in session outside this instance for
                           cross request persistence.
        """
        log(f'Authed init::{client_space.uuid}')
        self.session = session
        self.manager = manager
        self.client_space = client_space
        self.session_stash = session_stash

        self.manager.to_main_thread(client_space.uuid, f'Auth module index {session_stash["index"]}')

