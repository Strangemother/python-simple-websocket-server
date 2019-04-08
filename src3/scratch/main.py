# qpy:console
"""
This is a sample for qpython webapp
"""
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
parser.add_option("-a", "--address", dest="address", type=str, default=None,
                  help="Provide a ip")

parsed = parser.parse_args()


def process_run(options=None, *args, **kw):
    kw['port'] = kw.get('port', options.port)
    kw['ip'] = kw.get('ip', options.address)
    args = ()


def main(options, args):
    print('Create service')
    global pr
    pr = process_run(options)


if __name__ == '__main__':
    main(*parsed)
