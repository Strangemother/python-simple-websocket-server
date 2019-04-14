import logging


logging.basicConfig(level=logging.DEBUG)

def log(*a, prefix=''):
    logging.info("{}{}".format(prefix, ' '.join(map(str, a))))

warn = logging.warn

def plog(*a, prefix='  -- '):
    return log(*a, prefix=prefix)
