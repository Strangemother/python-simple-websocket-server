
print('sms view connecting to session remote manager')
#from multiprocessing.managers import BaseManager
import server


def manager_connect(address_pair=None, authkey=b'84ytnp9qyn8p3tu8qcp394tpmj', register=None):
    register = register or ('post', )
    address = address_pair or ('127.0.0.1', 9018)
    man = server.MainManager(address=address, authkey=authkey)

    for name in register:
        # register accepted functions
        man.register(name)
    man.register('hello')

    man.connect()
    man.hello()

    print(f"interface.sms.view connected to manager {address}")
    return man


def send_event(name, *args, **kwargs):
    man = manager_connect()
    func = getattr(man, name, None)
    if func is None:
        man.register(name)
        func = getattr(man, name)

    if func is None:
        print(f'Cannot find or register "{name}"')
    print(f'Calling {name}; {func}')
    func(*args, **kwargs)



