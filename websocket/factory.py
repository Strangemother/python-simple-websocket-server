from autobahn.asyncio.websocket import WebSocketServerFactory
from wlog import plog as log


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url):
        super().__init__(url)
        self.clients = []
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

