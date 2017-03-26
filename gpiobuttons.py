# gpiobuttons.py
#
# Input handler using push-buttons on GPIO pins
#

import RPi.GPIO as GPIO

import messagequeue
import inputregistry
import time


class RPiGpioInput:
    def __init__(self, buttons, btnchrs, pushed_level = 0, tick_time=0.02, debounce=1, longpress=35,
                 doubletimeout=10):
        self.buttons = buttons
        self.btnchrs = btnchrs
        self.pushed_level = pushed_level
        self.tick_time = tick_time
        self.debounce = debounce
        self.longpress = longpress
        self.doubletimeout = doubletimeout
        # internal state
        self.state=self.stateA # initial state
        self.pressed = set()
        self.prev = set()
        self.hold = 0
        # configure gpio pins as input
        GPIO.setmode(GPIO.BOARD)
        for btn in self.buttons:
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            while True:
                btns = self.get_buttons()
                self.handle(btns)
                time.sleep(tick_time)
        except:
            print "GPIO input loop killed or crashed. Bye!"

    def stop(self):
        GPIO.cleanup()

    def get_buttons(self):
        btns = set()
        # scan for pressed buttons
        for btn in self.buttons:
            if GPIO.input(btn) == self.pushed_level:
                btns.add(btn)
        return btns

    def handle(self, btns)
        # count same cycles (used in several states)
        if self.prev == btns:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        # call state machine
        self.state(btns)

        self.prev = btns
        return

    def stateA(self, btns):
        # print "state A - nothing pressed so far"
        if len(btns) != 0:
            self.pressed.update(btns)
            # go to state B
            self.state = self.stateB
        return

    def stateB(self, btns):
        # print "state B - first press"
        if len(btns) == 0:
            # released - go to state D
            self.state = self.stateD
        elif self.hold == self.debounce:
            # update buttons
            self.pressed.update(btns)
        elif self.hold == self.longpress:
            # long press - perform action and go to state C
            self.state = self.stateC
            self.action( pressedLong=True )
        return 
    
    def stateC(self, btns):
        # print "state C - long pressed; waiting for release"
        if len(btns) == 0:
            # go to state A
            self.state = self.stateA
        return

    def stateD(self, btns):
        # print "state D - released; waiting for double"
        if len(btns) != 0:  
            # double click - go to state E
            self.pressed.update(btns)
            self.state = self.stateE
        elif self.hold == self.doubletimeout:
            # time out - perform (single-click) action and go to state A
            self.state = self.stateA
            self.action()
        return

    def stateE(self, btns):
        # print "state E - double click; waiting for release"
        if len(btns) == 0:
            # release - perform action and go to state A
            self.state = self.stateA
            self.action( doubleClick=True )
        elif self.hold == self.debounce:
            # update buttons
            self.pressed.update(btns)
        return

    def action(self, pressedLong=False, doubleClick=False):
        # create string from buttons
        a = ''
        for i in range(0, len(self.buttons)):
            if self.buttons[i] in self.pressed:
                a = a + self.btnchrs[i]
        if pressedLong:
            a = a + '-'
        if doubleClick:
            a = a + '+'
        print "[action] pressed = %s, pressedLong = %s, doubleClick = %s --> action = %s" % (self.pressed, 
                                                            pressedLong, doubleClick, a)
        messagequeue.send(a)
        self.pressed = set()
        return


inputregistry.registerClass(RPiGpioInput)

