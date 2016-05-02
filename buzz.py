#!/usr/bin/python

import argparse
import os
import signal
import sys
import time
import traceback

import samplelib
import buzzwsd
import config

import RPi.GPIO as GPIO

VERSION="0.7"

SystemSounds = ['Startup', 'Shutdown']
SystemOffset = 0

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

def play_system(name):
    if name in SystemSounds:
        samplelib.play(SystemOffset + SystemSounds.index(name) + 1)

def setup(groups):
    global SystemOffset
    signal.signal(signal.SIGHUP, sighandler)
    buzzwsd.start_daemon()
    GPIO.setmode(GPIO.BOARD)
    offset = 0
    for g in groups:
        offset = offset + g.setup(offset)
    # register system sounds
    SystemOffset = offset
    for k in config.System.keys():
        if k in SystemSounds:
            s = config.System[k]
            if s:
                s.setup(SystemOffset, index=(SystemSounds.index(k)+1))
                samplelib.register(s)
    # Done
    play_system('Startup')


def loop(groups):
    # top level loop
    tick = config.Options['TickTime']
    while True:
        action = 0
        for g  in groups:
            action = g.get_action()
            if action != 0: break
       
        if action != 0:
            samplelib.play(action)

        # tick
        time.sleep(tick)

def cleanup():
    print "Called cleanup()..."
    GPIO.cleanup()
    buzzwsd.stop_daemon()

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

try:
    setup(groups)
    loop(groups)
except:
    traceback.print_exc()

cleanup()

try:
    play_system('Shutdown')
except:
    pass


