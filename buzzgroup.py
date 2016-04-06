# buzzgroup.py
#
# defines the BuzzerGroup class

import handlers
import samplelib

import RPi.GPIO as GPIO

# This is basically the workhorse
class BuzzerGroup:
    def __init__(self, buttons, prio = 1, pushed_level = 0, handler = handlers.BasicHandler, handler_opts = {} ):
        self.buttons = buttons
        self.num_buttons = len(buttons)
        self.pushed_level = pushed_level
        self.handler = handler(self.num_buttons, **handler_opts)
        self.offset = 0
        self.prio = prio
        self.samples = ()
        self.sampleIds = {}

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
            id = s.get_index()
            if id > num_actions:
                print "Warning: Id %s out of range (1..%d). Ignored." % (id, num_actions)
            elif id in self.sampleIds.keys():
                print "Warning: Id %s used multiple times. Ignored." % id
            else:
                self.sampleIds[id] = samplelib.register(s)

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
        b = self.get_buttons()
        bcode = self.handler.parse(b)
        action = 0
        if bcode != 0:
            try:
                action = self.sampleIds[bcode]
            except KeyError:
                # if bcode is not in list, we'll return the default value (0)
                pass
        return action


class Sample:
    base_dir = ''
    def __init__(self, index, filename, loop=False):
        self.index = index
        self.filename = filename
        if Sample.base_dir:
            self.path=Sample.base_dir + '/' + filename
        else:
            self.path = filename
        self.loop = loop

    def get_index(self):
        return self.index

    def get_path(self):
        return self.path

    def is_loop(self):
        return self.loop
