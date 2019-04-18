from wlog import color_plog

log = color_plog('yellow').announce(__spec__)



class SessionCallable(object):

    def __init__(self, manager, client_space, init_session_stash):
        """
            Session: The users connected session information
            client_space: the persistent definition created by the owner
            session_stash: transient data kept in session outside this instance for
                           cross request persistence.
        """
        self.manager = manager
        self.client_space = client_space
        self.data = init_session_stash
        def ll(*a):
            if client_space.debug:
                self.manager.to_main_thread(client_space.uuid, *a)
            log(*a)

        self.log = ll
        self.log(f'{self.__class__.__name__} init::{client_space.uuid}')

    def recv_session(self, session, session_stash):
        self.session = session
        self.data.update(session_stash)
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

    def created(self, index):
        """Called bt the session manager when a new instance of this class is
        generated for tracking a users flow.
        """
        self.log(f'Created {self.__class__.__name__} at position {index}')

    def close(self):
        """Called by the session manager if the instance is alive and will be
        killed.
        """
        if self.data['valid'] is True:
            self.log("I'm closing well!")
        else:
            self.log("Closing whilst invalid")

