#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
import traceback

#LED=11
num_Buttons = 3
pressed_level = 0
Buttons = [12, 16, 18]

def setup():
    GPIO.setmode(GPIO.BOARD)
    for btn in Buttons:
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_buttons():
    b = 0
    m = 1
    # scan for pressed buttons
    for i in range(0,num_Buttons):
        if GPIO.input(Buttons[i]) == pressed_level:
            b = b | m
        m = m << 1
    return b


class SimpleHandler:
    def __init__(self):
        self.prev = 0
        self.hold = 0

    def parse(self, btn):
        # count same cycles (for de-bouncing)
        if self.prev == btn:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        r = 0
        if self.hold == 0:
            r = btn

        self.prev = btn
        return r


class MultiHandler:
    def __init__(self):
        self.pressed1 = 0
        self.pressed2 = 0
        self.prev = 0
        self.hold = 0
        self.pressedLong = 0
        self.bstates = (1 << num_Buttons)-1 
    
    def action(self):
        a = 0
        if self.pressed2 == 0:
            a = self.pressed1
            if self.pressedLong:
                a = a + self.bstates**2 + self.bstates
        else:
            a = (self.bstates * self.pressed2) + self.pressed1
        print "pressed1 = %d, pressed2 = %d, pressedLong = %s --> action = %d" % (self.pressed1, self.pressed2, self.pressedLong, a)
        self.pressed1 = 0
        self.pressed2 = 0
        return a


    def parse(self, btn):
        # count same cycles (for de-bouncing)
        if self.prev == btn:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        if self.pressedLong:
            # print "state C - long pressed; waiting for release"
            if btn == 0:
                self.pressedLong = False
        elif self.pressed1 == 0:
            # print "state A - nothing pressed so far"
            if self.hold == 1:
                # trans to B
                self.pressed1 = btn
        elif self.pressed2 != 0:
            # print "state E - double click; waiting for release"
            if btn == 0:
                return self.action()
            if self.hold == 1:
                # update buttons
                self.pressed2 = btn
        else:
            if self.prev == 0:
                # print "state D - released; waiting for double"
                if self.hold == 3:
                    return self.action()
                elif btn != 0:  
                    # trans to E
                    self.pressed2 = btn
            else:
                # print "state B - first press"
                if btn != 0 and self.hold == 1:
                    # update buttons
                    self.pressed1 = btn
                if self.hold == 20:
                    # trans to C
                    self.pressedLong = True
                    return self.action()

        self.prev = btn
        return 0


def loop():
    # top level loop
    #handler = SimpleHandler()
    handler = MultiHandler()
    while True:
        b = get_buttons()
        action = handler.parse(b)
       
        if action != 0:
            os.system('mpc play %d' % (action))

        # tick
        time.sleep(0.05)

setup()
try:
    loop()
except:
    traceback.print_exc()
GPIO.cleanup()


