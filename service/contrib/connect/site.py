from contrib.base import SessionCallable


class Authed(SessionCallable):
    """assert the socket user has authorized with the connected
    site.

    Upon validation, check the database for a validate login.
    If false, wait for X and check again.
              wait for an event from the socket for valid or invalid
    If true, tell the manager 'valid'.
    """

    def recv_msg(self, payload, binary=False):
        """When _in-process_ the Auth instance captures messages directly from
        the client socket.
        """
        res = payload == b'secret'
        self.log(f'Auth module received message: {payload} == {res} Binary: {binary}')

        if res:
            return self.assert_valid()
        self.assert_fail()
