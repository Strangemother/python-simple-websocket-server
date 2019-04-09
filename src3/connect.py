from multiprocessing import Process, Pipe

pipe = None
process = None

def f(conn):
    conn.send([42, None, 'hello'])
    while True:
        try:
            msg = conn.recv()
            if msg == 'close':
                break
        except (EOFError, KeyboardInterrupt):
            break
    conn.close()


def start():
    global pipe
    global process

    parent_conn, child_conn = Pipe()
    pipe = parent_conn
    process = Process(target=f, args=(child_conn,))
    process.start()


def stop():
    try:
        pipe.send('close')
    except BrokenPipeError:
        print('connect::pipe is already closed')
    process.join()


def connection_manager(content):
    print(pipe.recv())   # prints "[42, None, 'hello']"
    print('Sending content')
    pipe.send(content)
