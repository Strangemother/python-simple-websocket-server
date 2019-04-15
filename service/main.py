# qpy:console
"""
This is a sample for qpython webapp
"""
from wlog import plog as log

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
parser.add_option("-i", "--serve",
                  action="store_true", dest="serve", default=False,
                  help="run the service until system interupt.")
parser.add_option("-c", "--config", dest="config",
                  help="Provide a config path")
parser.add_option("-p", "--port", dest="port", type=int, default=8004,
                  help="Provide a port")
parser.add_option("-a", "--address", dest="ip", type=str, default=None,
                  help="Provide a ip")

parsed = parser.parse_args()

from auto_server import run

def process_run(options=None, *args, **kw):
    kw.update(vars(options))
    kw['name'] = 'Cheese'
    args = ()
    run(**kw)

def main(options, args):
    log('Create service')
    global pr
    pr = process_run(options)


if __name__ == '__main__':
    main(*parsed)
