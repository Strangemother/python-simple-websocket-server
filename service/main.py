# qpy:console
"""
This is a sample for qpython webapp
"""
from optparse import OptionParser

from service.wlog import plog as log
from service.exposed.server import run as server_run


parser = OptionParser()
parser.add_option("-f", "--file",
                  dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false",
                  dest="verbose", default=True,
                  help="don't print status messages to stdout")
parser.add_option("-i", "--serve",
                  action="store_true",
                  dest="serve", default=False,
                  help="run the service until system interupt.")
parser.add_option("-c", "--config",
                  dest="config",
                  help="Provide a config path")
parser.add_option("-p", "--port",
                  dest="port", type=int, default=8004,
                  help="Provide a port")
parser.add_option("-a", "--address",
                  dest="ip", type=str, default=None,
                  help="Provide a ip")


parsed = parser.parse_args()


def main(options=None, args=None, **kw):
    if options is None:
      options, args = parsed

    log('Create service')

    kw.update(vars(options))
    kw['name'] = 'Cheese'
    args = ()
    server_run(**kw)


if __name__ == '__main__':
    main(*parsed)
