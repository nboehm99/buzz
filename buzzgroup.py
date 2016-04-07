# buzzgroup.py
#
# defines the BuzzerGroup class

import handlers
import RPi.GPIO as GPIO

# This is basically the workhorse
class BuzzerGroup:
    def __init__(self, buttons, pushed_level = 0, handler = handlers.BasicHandler, prio = 1 ):
        self.buttons = buttons
        self.num_buttons = len(buttons)
        self.pushed_level = pushed_level
        self.handler = handler(self.num_buttons)
        self.offset = 0
        self.prio = prio

    # assumes that GPIO.setmode(GPIO.BOARD) has been done previously
    def setup_pins(self, offset):
        self.offset = offset
        for btn in self.buttons:
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return self.handler.get_num_actions()


    def get_buttons(self):
        btns = 0
        mask = 1
        # scan for pressed buttons
        for i in range(0, self.num_buttons):
            if GPIO.input(self.buttons[i]) == self.pushed_level:
                btns = btns | mask
            mask = mask << 1
        return btns

    def get_action(self):
        b = self.get_buttons()
        return self.handler.parse(b) + self.offset

