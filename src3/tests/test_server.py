import unittest
from functools import partial
from multiprocessing import Process, Lock, Manager, Queue

import client
import auto_server
import time


port = 8004
ip = '127.0.0.1'


client_actions = {}

class DemoTestServerProtocol(auto_server.MyServerProtocol):
    """A DemoTest runs a protocol to manage the shared
    resource object the original testing unit will read.
    """
    def __init__(self, dback, *a, **kw):
        self.dback = dback
        super().__init__(*a, **kw)

    def onConnect(self, request):
        """Store the message back to the dictionary manager com"""
        self.store('onConnect', True)

    def store(self, name, value):
        self.dback[name] = value

    def onOpen(self):
        """Store the message back to the dictionary manager com"""
        self.store('onOpen', True)

    def onMessage(self, payload, isBinary):
        """Store the message back to the dictionary manager com"""
        self.store('onMessage', (payload, isBinary, ))


def run_server_process(cond):
    """Run the standard server class, providing "DemoTestServerProtocol"
    as the procotol to run - wrapped in a partial() to ensure the firt
    argument is the _test_ write-back dict.
    """
    pproc = partial(DemoTestServerProtocol, cond)
    auto_server.run(port, ip, protocol=pproc)

def run_test_server():
    """Run a server within a new process, sharing a dictionary through
    a multiprocess manager
    """
    manager = Manager()
    cond = manager.dict()
    proc = Process(target=run_server_process, args=(cond,))
    proc.start()
    return manager, cond, proc

def run_bounce_client():
    """Open a client a send a single "Apples" message and close.
    """
    c = client.get_client(ip,port)
    print(c.status)
    v = c.send('Apples')
    c.close()


class TestServer(unittest.TestCase):

    def setUp(self):
        manager, cond, proc = run_test_server()
        self.server = proc
        self.cond = cond

    def tearDown(self):
        self.server.terminate()

    def test_run(self):
        """Ensure the server can turn-on and receive a message"""
        run_bounce_client()
        # print('RES', self.cond)
        expected = {'onConnect': True,
            'onOpen': True,
            'onMessage': (b'Apples', False)}
        message = "Process Manager captured basic communication"
        self.assertDictEqual(dict(self.cond), expected, message)
