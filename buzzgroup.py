# buzzgroup.py
#
# defines the BuzzerGroup class

import handlers
import samplelib

import RPi.GPIO as GPIO

# This is basically the workhorse
class BuzzerGroup:
    def __init__(self, name, buttons, prio = 1, pushed_level = 0, handler = handlers.BasicHandler, handler_opts = {} ):
        self.name = name
        self.buttons = buttons
        self.num_buttons = len(buttons)
        self.pushed_level = pushed_level
        self.handler = handler(name, self.num_buttons, **handler_opts)
        self.offset = 0
        self.prio = prio
        self.samples = ()

    def set_samples(self, *samples):
        self.samples = samples

    # assumes that GPIO.setmode(GPIO.BOARD) has been done previously
    def setup(self, pin_offset):
        self.offset = pin_offset
        for btn in self.buttons:
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # register samples
        num_actions = self.handler.get_num_actions()
        for s in self.samples:
            action = s.setup(self.offset, self.handler)
            if action > num_actions:
                print "Warning: Id %s out of range (1..%d). Ignored." % (id, num_actions)
            else:
                samplelib.register(s)
        return num_actions

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
        action = 0
        b = self.get_buttons()
        bcode = self.handler.parse(b)
        if bcode != 0:
            action = bcode + self.offset
        return action


class Sample:
    base_dir = ''
    def __init__(self, buttons, filename, loop=False):
        self.buttons = buttons
        self.action = 0
        self.filename = filename
        if Sample.base_dir:
            self.path=Sample.base_dir + '/' + filename
        else:
            self.path = filename
        self.loop = loop

    def setup(self, offset, handler):
        a = handler.get_sample_index(self.buttons)
        if a > 0:
            self.action = a + offset
        return a

    def get_action(self):
        return self.action

    def get_path(self):
        return self.path

    def is_loop(self):
        return self.loop

