from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from wlog import color_plog
log = color_plog('cyan').announce(__spec__)


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        log("Server connected: {0}".format(response.peer))

    def onOpen(self):
        log("WebSocket connection open.")

        def hello():
            self.sendMessage(u"Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.factory.loop.call_later(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            log("Binary message received: {0} bytes".format(len(payload)))
        else:
            log("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        log("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
