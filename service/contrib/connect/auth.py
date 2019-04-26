"""
Basic connection Authentication routines for a connecting socket to a session.
Initially a client must validate the basic protocols of a session; origin, peer (cors).

After AUTH.INIT (0) the welcome routine proceeds with ROUTINES. Basic auth
routines help validate an incoming client before content delivery.

A Basic auth requires no development. An example of a password first input - note
this is a test and an insecure example of password verification:

A session unit can call assert_valid() and assert_fail() for the session manager
to control:


    class Authed(SessionCallable):

        def recv_msg(self, payload, binary=False):
            success = 'valid' if payload == self.data['password'] else 'fail'
            self.log(f'Password authentication: {success}')
            getattr(self, f'assert_{success}')()


It can be applied to to the client API persistent record:

    # Persistent records...
    CLIENTS = {
        'test1': {
            'api_key_1': dict(
                    # modules for authenticating the onConnect; AUTH 0.
                    connect=(
                            ('contrib.connect.auth.Password', { 'password': b'secret'}),
                        )
                )
        }
    }

used by `client.get_client(uuid, request)`

"""
from service.contrib.base import SessionCallable


class Password(SessionCallable):
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
        password = self.data['password']
        res = payload == password
        self.log(f'Auth module received message: {payload} == {password} = {res} Binary: {binary}')

        if res:
            return self.assert_valid()
        self.assert_fail()
