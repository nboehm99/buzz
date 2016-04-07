#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import traceback
import config
import buzzlib

def setup(groups):
    GPIO.setmode(GPIO.BOARD)
    offset = 0
    for g in groups:
        offset = offset + g.setup_pins(offset)


def loop(groups):
    # top level loop
    while True:
        action = 0
        for g  in groups:
            action = g.get_action()
            if action != 0: break
       
        if action != 0:
            buzzlib.play(action)

        # tick
        time.sleep(0.05)


groups = config.load()
setup(groups)
try:
    loop(groups)
except:
    traceback.print_exc()

GPIO.cleanup()


