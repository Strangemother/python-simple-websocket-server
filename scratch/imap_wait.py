import asyncio
from aioimaplib import aioimaplib

EMAIL_HOST = 'mail.strangemother.org'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'webmaster@strangemother.org'
EMAIL_HOST_PASSWORD = 'FHoCLIlke)Ft'
EMAIL_USE_TLS = True
STOP_WAIT_SERVER_PUSH = 'stop_wait_server_push'


@asyncio.coroutine
def wait_for_new_message(host, user, password):
    imap_client = aioimaplib.IMAP4_SSL(host=host)
    print('wait hello')
    yield from imap_client.wait_hello_from_server()
    print('login')

    yield from imap_client.login(user, password)
    yield from imap_client.select()
    print('wait')
    idle = yield from imap_client.idle_start(timeout=30)
    while imap_client.has_pending_idle():
        msg = yield from imap_client.wait_server_push()
        print(msg)
        if msg == STOP_WAIT_SERVER_PUSH:
            imap_client.idle_done()
            yield from asyncio.wait_for(idle, 1)

    print('logout:', imap_client.has_pending_idle())
    yield from imap_client.logout()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_new_message(EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD))
