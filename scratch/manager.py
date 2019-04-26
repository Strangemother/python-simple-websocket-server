from multiprocessing.managers import BaseManager
from queue import Queue
from service.wlog import color_plog

log = color_plog('yellow').announce(__spec__)


class MathsClass:
    def add(self, x, y):
        print('Performing add')
        return x + y

    def mul(self, x, y):
        return x * y


queue = Queue()

class MyManager(BaseManager):

    # Not registered = runs local.
    def example(self):
        print('Example called')
        return self.hello_back()

def get_queue():
    #log('Returning queue')
    return queue

MyManager.register('get_queue', callable=get_queue)
MyManager.register('Maths', MathsClass)

def hb():
    m.client_hello(1)
MyManager.register('hello_back', hb)


PORT = 9018
ADDRESS = '127.0.0.1'
AUTH = b'84ytnp9qyn8p3tu8qcp394tpmj'

def hello():
    print('Someone said hello to the server')
    return 'Return value'


def answer(func):
    print('Answer the client client_hello')
    m.example()
    return 'Return value'


def server(reg=None):
    global m

    reg = reg or ['oak']
    m = MyManager(address=(ADDRESS, PORT), authkey=AUTH)
    s = m.get_server()
    m.register('hello', hello)
    m.register('answer', answer)
    m.register('client_hello')
    for r in reg:
        m.register(r)
    s.serve_forever()


def c_hello(v=None):
    print('call client_hello', v)
    return 'Return client value'


def client(cname='client_hello', other='oak'):
    global m
    global s

    m = MyManager(address=(ADDRESS, PORT), authkey=AUTH)
    print(ADDRESS, PORT)
    m.register('hello')
    m.register('answer')
    m.register(other)
    m.register(cname, c_hello)
    s = m.connect()

    return m, s
