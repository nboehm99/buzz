#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import traceback
import config
import buzzlib
import argparse
import sys

VERSION="0.4"

def setup(groups):
    GPIO.setmode(GPIO.BOARD)
    offset = 0
    for g in groups:
        offset = offset + g.setup_pins(offset)


def loop(groups):
    # top level loop
    tick = config.Options['TickTime']
    while True:
        action = 0
        for g  in groups:
            action = g.get_action()
            if action != 0: break
       
        if action != 0:
            buzzlib.play(action)

        # tick
        time.sleep(tick)

def cleanup():
    GPIO.cleanup()

##############################################################################

argp = argparse.ArgumentParser(description='Buzz.')
argp.add_argument('-c', dest='configfile', action='store',
        default='buzz.cfg', help='config file (default: buzz.cfg)')
argp.add_argument('-v', '--version', dest='version', action='store_true',
        default=False, help='Print version and exit.')
args = argp.parse_args()

if args.version:
    print "buzz.py, version", VERSION
    sys.exit(0)

groups = config.load(args.configfile)
setup(groups)

try:
    loop(groups)
except:
    traceback.print_exc()

cleanup()


