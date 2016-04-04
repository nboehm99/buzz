#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os

LED=11
Buttons=[12, 16, 18]
#BasePath='/media/pool'
#ButtonFiles=['BTN01.wav', 'BTN02.wav', 'BTN03.wav']

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.HIGH)
    for btn in Buttons:
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#        GPIO.add_event_detect(btn, GPIO.FALLING, bouncetime=100)

def loop():
    old = [False] * 3
    while True:
        for i in range(0,3):
#            print "Checking button", i,
            # check if button has been pressed
            if GPIO.input(Buttons[i]) == 1:
                if not old[i]:
                    GPIO.output(LED, GPIO.LOW)
#                    os.system('aplay %s' % os.path.join(BasePath, ButtonFiles[i]))
                    os.system('mpc play %d' % (i+1))
                    GPIO.output(LED, GPIO.HIGH)
                old[i] = True
            else:
                old[i] = False
#                print "not pressed."
                GPIO.output(LED, GPIO.HIGH)
#        for i in range(0,3):
#            print "Button", i, ":", GPIO.input(Buttons[i])
        time.sleep(0.08)

setup()
try:
    loop()
except:
    pass
GPIO.output(LED, GPIO.HIGH)
GPIO.cleanup()


