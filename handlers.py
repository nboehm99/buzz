# handlers.py
#
# provides several button handlers to choose from
#

class BasicHandler:
    def __init__(self, num_buttons):
        self.prev = 0
        self.hold = 0
        self.num_actions = (2**num_buttons) - 1

    def get_num_actions(self):
        return self.num_actions

    def parse(self, btn):
        # count same cycles (for de-bouncing)
        if self.prev == btn:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        r = 0
        if self.hold == 1:
            r = btn

        self.prev = btn
        return r


class MultiHandler:
    def __init__(self, num_buttons):
        self.state=self.stateA # initial state
        self.pressed1 = 0
        self.pressed2 = 0
        self.prev = 0
        self.hold = 0
        self.bstates = (2**num_buttons)-1 
        self.num_actions = (2**(2*num_buttons)) - 1

    def get_num_actions(self):
        return self.num_actions
    
    def action(self, pressedLong=False):
        a = 0
        if self.pressed2 == 0:
            a = self.pressed1
            if pressedLong:
                a = a + self.bstates**2 + self.bstates
        else:
            a = (self.bstates * self.pressed2) + self.pressed1
        print "pressed1 = %d, pressed2 = %d, pressedLong = %s --> action = %d" % (self.pressed1,
                                                                                  self.pressed2, pressedLong, a)
        self.pressed1 = 0
        self.pressed2 = 0
        return a

    def stateA(self, btn):
        # print "state A - nothing pressed so far"
        if btn != 0:
            self.pressed1 = btn
            # go to state B
            self.state = self.stateB
        return 0

    def stateB(self, btn):
        # print "state B - first press"
        if btn == 0:
            # released - go to state D
            self.state = self.stateD
        elif self.hold == 1:
            # update buttons
            self.pressed1 = btn
        elif self.hold == 15:
            # long press - perform action and go to state C
            self.state = self.stateC
            return self.action( pressedLong=True )
        return 0
    
    def stateC(self, btn):
        # print "state C - long pressed; waiting for release"
        if btn == 0:
            # go to state A
            self.state = self.stateA
        return 0

    def stateD(self, btn):
        # print "state D - released; waiting for double"
        if btn != 0:  
            # double click - go to state E
            self.pressed2 = btn
            self.state = self.stateE
        elif self.hold == 4:
            # time out - perform (single-click) action and go to state A
            self.state = self.stateA
            return self.action()
        return 0

    def stateE(self, btn):
        # print "state E - double click; waiting for release"
        if btn == 0:
            # release - perform action and go to state A
            self.state = self.stateA
            return self.action()
        elif self.hold == 1:
            # update buttons
            self.pressed2 = btn
        return 0

    def parse(self, btn):
        # count same cycles (used in several states)
        if self.prev == btn:
            self.hold = self.hold + 1
        else:
            self.hold = 0

        # call state machine
        act = self.state(btn)

        self.prev = btn
        return act

