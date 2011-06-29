#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from meinheld import server
from wsgi     import application
from optparse import OptionParser

getopt = OptionParser()
getopt.add_option('-p', '--port',   dest='port',    type='int',    default=5000, help='Listen Port')
getopt.add_option('-a', '--address', dest='address', type='string', default='0.0.0.0', help='Listen address')
getopt.add_option('-d', '--debug',   dest='debug',  action='store_true', default=False )

def main ():
    opts, args = getopt.parse_args()

    if opts.debug:
        application.debug = True

    print "Server listen: http://%s:%s/" % ( opts.address, opts.port  )  
    server.listen( ( opts.address, opts.port ) )
    server.run( application )

if __name__ == '__main__':
    main()
