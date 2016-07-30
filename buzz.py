#!/usr/bin/python

import argparse
import os
import signal
import sys
import traceback
import threading

import config
import messagequeue
import output
import inputregistry

VERSION="0.90"

def sighandler(signum, frame):
    print "Received SIGHUP. Restarting."
    # close GPIO, etc.
    cleanup()
    # restart
    args=["python"]
    args.extend(sys.argv)
    os.execvp(args[0], args)
    # should be unrechable
    sys.exit(1)


def setup():
    signal.signal(signal.SIGHUP, sighandler)
    for i in inputregistry.getAll():
        it = threading.Thread(target=i.run)
        it.start()
    messagequeue.send('Startup')

def loop(args):
    if args.interactive: 
    # interactive mode - run output in thread and use this for input
        print "Entering interactive mode..."
        ot = threading.Thread(target=output.run)
        ot.start()
        while True:
            s = raw_input('> ')
            messagequeue.send(s)
    else:
        print "(non-interactive)"
        output.run()

def cleanup():
    print "Called cleanup()..."
    for i in inputregistry.getAll():
        i.stop()
    output.stop()



##############################################################################

argp = argparse.ArgumentParser(description='Buzz.')
argp.add_argument('-c', dest='configfile', action='store',
        default='buzz.cfg', help='config file (default: buzz.cfg)')
argp.add_argument('-v', '--version', dest='version', action='store_true',
        default=False, help='Print version and exit.')
argp.add_argument('-i', '--interactive', dest='interactive', action='store_true',
        default=False, help='Interactive mode.')
args = argp.parse_args()

if args.version:
    print "buzz.py, version", VERSION
    sys.exit(0)

config.load(args.configfile)

try:
    setup()
    loop(args)
except:
    traceback.print_exc()

messagequeue.send('Shutdown')
cleanup()

