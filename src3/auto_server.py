
from multiprocessing import Process
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import connect


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        connect.connection_manager(request)

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


    # def sendHtml(self, html):
    #     """
    #     Send HTML page HTTP response.
    #     """
    #     responseBody = html.encode('utf8')
    #     response = "HTTP/1.1 200 OK\x0d\x0a"
    #     if self.factory.server is not None and self.factory.server != "":
    #         response += "Server: %s\x0d\x0a" % self.factory.server
    #     response += "Content-Type: text/html; charset=UTF-8\x0d\x0a"
    #     response += "Content-Length: %d\x0d\x0a" % len(responseBody)
    #     response += "\x0d\x0a"
    #     self.sendData(response.encode('utf8'))
    #     self.sendData(responseBody)


    def sendServerStatus(self, redirectUrl=None, redirectAfter=0):
        """
        Used to send out server status/version upon receiving a HTTP/GET without
        upgrade to WebSocket header (and option serverStatus is True).
        """
        if redirectUrl:
            redirect = """<meta http-equiv="refresh" content="%d;URL='%s'">""" % (redirectAfter, redirectUrl)
        else:
            redirect = ""
        self.sendHtml("Woops! %s" % (redirect))

import asyncio

@asyncio.coroutine
def keyboard_interrupt_watch():
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    while True:
        yield from asyncio.sleep(1)
        # print("First Worker Executed")


@asyncio.coroutine
def secondWorker():
    while True:
        yield from asyncio.sleep(1)
        print("Second Worker Executed")


def run(port=9000, ip='0.0.0.0', keyboard_watch=True, **kw):
    port = port or 9000
    ip = ip or '0.0.0.0'
    uri = u"ws://{}:{}".format(ip, port)
    print('factory', uri)
    factory = WebSocketServerFactory(uri)
    factory.protocol = kw.get('protocol', MyServerProtocol)

    loop = asyncio.get_event_loop()
    coro_gen = loop.create_server(factory, ip, port)

    print('Run', ip, port)
    server = loop.run_until_complete(coro_gen)
    connect.start()
    if keyboard_watch:
        print('CTRL+C watch')
        asyncio.ensure_future(keyboard_interrupt_watch())

    try:
        print('Step into run run_forever')
        loop.run_forever()
        # CTRL+C works on the next message loop.
        # This is delayed if no messages are given.
    except KeyboardInterrupt as e:
        print('KeyboardInterrupt')
    finally:
        connect.stop()
        server.close()
        print('Final close')
        loop.close()

if __name__ == '__main__':
    run()
