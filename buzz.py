#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os

#LED=11
Buttons=[12, 16, 18]

def setup():
    GPIO.setmode(GPIO.BOARD)
    for btn in Buttons:
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    pressed = 0
    nochange = 0
    while True:
        b = 0
        m = 1

        # scan for pressed buttons
        for i in range(0,3):
            if GPIO.input(Buttons[i]) == 1:
                b = b | m
            m = m << 1

        # check for change
        if b != pressed:
            print "Button change! old: %d\tnew: %d\tnot changed for: %d" % (pressed, b, nochange)
            pressed = b
            nochange = 0
        else:
            nochange = nochange + 1
       
        # if buttons are stable for one tick: play sound
        if (nochange == 1) and (pressed != 0):
            os.system('mpc play %d' % (pressed))

        # tick
        time.sleep(0.05)

setup()
try:
    loop()
except:
    pass
GPIO.cleanup()


