from wlog import color_plog

log = color_plog('yellow').announce(__spec__)



class SessionCallable(object):

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
        self.log(f'{self.__class__.__name__} init::{client_space.uuid}')

    def recv_session(self, session, session_stash):
        self.session = session
        self.data = session_stash
        self.log(f'module index {session_stash["index"]}')


    def recv_msg(self, data, binary=False):
        pass

    def assert_valid(self):
        """Provide a signal to the system or the connected session manager
        presenting the flow as successful.
        """

        self.log('Valid')
        self.manager.present_valid(self)

    def assert_fail(self):
        """Provide a signal to the system or the connected session manager
        presenting the flow as successful.
        """

        self.log('Fail')
        self.manager.present_fail(self)
