# gpiobuttons.py
#
# Input handler using push-buttons on GPIO pins
#

import RPi.GPIO as GPIO

import messagequeue
import inputregistry
import time

import traceback

DOUBLE  = '+'
LONG    = '-'
REPEAT  = '='
RELEASE = '$'

class RPiGpioInput:
    def __init__(self, buttons, btnchrs, pushed_level = 0, tick_time=0.02, debounce=1, longpress=35,
                 longrepeat=25, doubletimeout=10):
        self.buttons = buttons
        self.btnchrs = btnchrs
        self.pushed_level = pushed_level
        self.tick_time = tick_time
        self.debounce = debounce
        self.longpress = longpress
        self.longrepeat = longrepeat
        self.doubletimeout = doubletimeout
        # internal state
        self.state=self.stateIdle # initial state
        self.pressed = set()
        self.prev = set()
        self.hold = 0
        self.longhold = 0
        self.STOP = False
        # configure gpio pins as input
        GPIO.setmode(GPIO.BOARD)
        for btn in self.buttons:
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            while not self.STOP:
                btns = self.get_buttons()
                self.handle(btns)
                time.sleep(self.tick_time)
        except:
            print "GPIO input loop killed or crashed. Bye!"
            traceback.print_exc()

    def stop(self):
        self.STOP = True
        time.sleep(2 * self.tick_time)
        GPIO.cleanup()

    def get_buttons(self):
        btns = set()
        # scan for pressed buttons
        for btn in self.buttons:
            if GPIO.input(btn) == self.pushed_level:
                btns.add(btn)
        return btns

    def handle(self, btns):
        # count same cycles (used in several states)
        if self.prev == btns:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        # call state machine
        self.state(btns)

        self.prev = btns
        return

    def stateIdle(self, btns):
        # print "state Idle - nothing pressed so far"
        if len(btns) != 0:
            self.pressed.update(btns)
            # go to state Single
            self.state = self.stateSingle
        return

    def stateSingle(self, btns):
        # print "state Single - single push detected"
        if len(btns) == 0:
            # released - go to state DoubleWait
            self.state = self.stateDoubleWait
        elif self.hold == self.debounce:
            # update buttons
            self.pressed.update(btns)
        elif self.hold == self.longpress:
            # long press - perform action and go to state Long
            self.longhold = 0
            self.state = self.stateLong
            self.action(eventType=LONG, clear=False)
        return 
    
    def stateLong(self, btns):
        # print "state Long - long push detected; waiting for release"
        self.longhold = self.longhold + 1
        if len(btns) == 0:
            # perform release action and go to state Idle
            self.action(eventType=RELEASE)
            self.state = self.stateIdle
        elif self.longhold == self.longrepeat:
            # perform repeat action
            self.action(eventType=REPEAT, clear=False)
            self.longhold = 0
        return

    def stateDoubleWait(self, btns):
        # print "state DoubleWait - first push released; waiting for double"
        if len(btns) != 0:  
            # double push - go to state Double
            self.pressed.update(btns)
            self.state = self.stateDouble
        elif self.hold == self.doubletimeout:
            # time out - perform (single-push) action and go to state Idle
            self.state = self.stateIdle
            self.action()
        return

    def stateDouble(self, btns):
        # print "state Double - double push; waiting for release"
        if len(btns) == 0:
            # release - perform action and go to state Idle
            self.state = self.stateIdle
            self.action(eventType=DOUBLE)
        elif self.hold == self.debounce:
            # update buttons
            self.pressed.update(btns)
        return

    def action(self, eventType='', clear=True):
        # create string from buttons
        a = ''
        for i in range(0, len(self.buttons)):
            if self.buttons[i] in self.pressed:
                a = a + self.btnchrs[i]
        a = a + eventType
        print "[action] pressed = %s, eventType = %s --> action = %s" % (self.pressed, eventType, a)
        messagequeue.main.send(a)
        if clear:
            self.pressed = set()
        return


inputregistry.registerClass(RPiGpioInput)

