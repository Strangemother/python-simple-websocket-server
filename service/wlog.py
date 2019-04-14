import logging

from colorama import Fore, Back, Style
from colorama import init
init()
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

class Colors:
    black = Fore.BLACK
    red = Fore.RED
    green = Fore.GREEN
    yellow = Fore.YELLOW
    blue = Fore.BLUE
    magenta = Fore.MAGENTA
    cyan = Fore.CYAN
    white = Fore.WHITE
    reset = Fore.RESET

logging.basicConfig(level=logging.DEBUG)

def log(*a, prefix='', color=None):
    if color is None:
        color = ''
    elif hasattr(Colors, color):
        color = getattr(Colors, color)

    if color is not None:
        logging.sys.stdout.write(color)

    logging.info("{}{}".format(prefix, ' '.join(map(str, a))))
    if color:
        logging.sys.stdout.write(Style.RESET_ALL)

warn = logging.warn

def plog(*a, prefix='  -- ', **kw):
    return log(*a, prefix=prefix, **kw)

from functools import partial


def color_plog(color):
    return partial(plog, color=color)
