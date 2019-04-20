from multiprocessing.managers import BaseManager

class MathsClass:
    def add(self, x, y):
        return x + y

    def mul(self, x, y):
        return x * y

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)


PORT = 9012
ADDRESS = '127.0.0.1'
AUTH = b'84ytnp9qyn8p3tu8qcp394tpmj'

def hello():
    print('Someone said hello to the server')
    return 'Return value'


def answer(func):
    print('Answer the client chi')
    func()
    return 'Return value'


def server():
    global m
    m = MyManager(address=(ADDRESS, PORT), authkey=AUTH)
    s = m.get_server()
    m.register('hello', hello)
    m.register('answer', answer)
    m.register('chi')
    s.serve_forever()


def c_hello(v=None):
    print('CLIENT hello?', v)
    return 'Return client value'


def client():
    global m
    global s

    m = MyManager(address=(ADDRESS, PORT), authkey=AUTH)
    s = m.connect()
    m.register('hello')
    m.register('answer')
    m.register('chi', c_hello)

    return m, s
