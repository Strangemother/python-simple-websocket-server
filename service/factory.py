from autobahn.asyncio.websocket import WebSocketServerFactory

from wlog import color_plog
log = color_plog('yellow')
log.announce(__spec__)

class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """
    server_version = 'Facor'

    @property
    def server(self):
        return "Strangemother/BroadcastServerFactory::{}/0.01".format(self._server_name)

    @server.setter
    def server(self, name):
        self._server_name = name


    def __init__(self, url, **kw):
        super().__init__(url, **kw)
        self.clients = []
        self._server_name = 'Unnamed.'
        self.tickcount = 0
        self.tick()


    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)

    def register(self, client):
        if client not in self.clients:
            log("registered client {}".format(client.peer))
            self.clients.append(client)
            self.tick()

    def unregister(self, client):
        if client in self.clients:
            log("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        log("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            log("message sent to {}".format(c.peer))

