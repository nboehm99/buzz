#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import traceback
import config
import buzzlib
import argparse

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

argp = argparse.ArgumentParser(description='Buzz.')
argp.add_argument('-c', dest='configfile', action='store',
        default='buzz.cfg', help='config file (default: buzz.cfg)')
args = argp.parse_args()

groups = config.load(args.configfile)
setup(groups)

try:
    loop(groups)
except:
    traceback.print_exc()

GPIO.cleanup()


