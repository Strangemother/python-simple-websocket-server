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
    ref = partial(plog, color=color)
    setattr(ref, 'announce', partial(announce, ref))
    return ref


Spaces = {
    'NAME_MIN_WIDTH': 8,
    'COLOR_MIN_WIDTH': 8,
}

def announce(_log, spec):
    # log.announce(__spec__)
    name = spec.name
    file = spec.origin
    if file in Spaces:
        _log('.. skipping re-announce of', name)
        return
    color = "%s:" % _log.keywords.get('color', '').upper()
    Spaces[file] = color
    Spaces['NAME_MIN_WIDTH'] = max(Spaces['NAME_MIN_WIDTH'], len(name)+2)
    Spaces['COLOR_MIN_WIDTH'] = max(Spaces['COLOR_MIN_WIDTH'], len(name)+2)
    _log(f"!{color:<{Spaces['COLOR_MIN_WIDTH']}} {name:<{Spaces['NAME_MIN_WIDTH']}} {file}")

