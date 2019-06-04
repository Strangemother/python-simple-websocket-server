import sys

sys.path.append('C:/Users/jay/Documents/projects/websocket')

from manager.server import register
from mail import send_mail
from manager.client import manager_connect
import imap_wait

def smtp_send(*a, **k):
    print('smtp_send handler received a call...', a, k)

register('smtp_send', smtp_send)
man = manager_connect()
recv, send = man.com_pipes()
# imap_wait.wait()
