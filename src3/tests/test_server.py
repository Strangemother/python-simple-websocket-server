import unittest
import auto_server

from multiprocessing import Process, Lock, Manager, Queue
import client

import time

port = 8004
ip = '127.0.0.1'

client_actions = {}

class DemoTestServerProtocol(auto_server.MyServerProtocol):

    def __init__(self, dback, *a, **kw):
        self.dback = dback
        super().__init__(*a, **kw)

    def onConnect(self, request):
        self.lock_write('onConnect', True)

    def lock_write(self, name, value):
        self.dback[name] = value
        print(name, value)

    def onOpen(self):
        self.lock_write('onOpen', True)

from functools import partial

def run_server(cond):
    pproc = partial(DemoTestServerProtocol, cond)
    auto_server.run(port, ip, protocol=pproc)


def run_client():
    c = client.get_client(ip,port)
    print(c.status)
    v = c.send('Apples')
    c.close()


class TestServer(unittest.TestCase):

    def setUp(self):
        self.lock = Lock()
        self.manager = Manager()
        self.cond = self.manager.dict()
        proc = Process(target=run_server, args=(self.cond,))
        proc.start()
        self.server = proc

    def tearDown(self):
        self.server.terminate()

    def test_run(self):
        print('Test Run')
        run_client()
        time.sleep(1)
        self.lock.acquire()
        print('RES', self.cond)
        self.lock.release()

        #proc = Process(target=run_client)
        #proc.start()


