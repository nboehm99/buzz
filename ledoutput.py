# ledoutput.py
#
# coordinates LED output

import threading
import time
import RPi.GPIO as GPIO

import messagequeue

allLedClasses = []
configuredLedOutputs = []

STOPMSG='<!>STOP<!>'

def _compilePattern(patternStr):
    """
    Compiles a simple language to a blink pattern that is parsed in the output thread.

    There are probably a thousand ways to break this.
    """
    pattern = []
    for l in patternStr.split('\n'):
        line = l.strip()
        if line.startswith('On'):
            pattern.append(True)
        elif line.startswith('Off'):
            pattern.append(False)
        elif line.startswith('Wait'):
            pattern.append(float(line[4:]))
        elif line.startswith('BackTo'):
            pattern.append(int(line[6:]-len(pattern)))
        else:
            # ignore
            pass
    return pattern

defaultPattern = _compilePattern("""
On
Wait 1
Off
""")

suffixPatterns = {
'-': _compilePattern("""
     On
     Wait 2.2
     Off"""),
'+': _compilePattern("""
     On
     Wait 0.5
     Off
     Wait 0.5
     On
     Wait 0.5
     Off""")
}

def addLedOutput(outputInstance):
    configuredLedOutputs.append(outputInstance)

def setLedPattern(suffix, patternStr):
    pattern = _compilePattern(patternStr)
    if suffix == None:
        defaultPattern = pattern
    else:
        suffixPatterns[suffix] = pattern

class Leds74HC595:

    def __init__(self, SER, SRCLK, RCLK, chrs):
        """
        Use LEDs driven by a 74HC595-style shift register.

        Assumes that OE and SRCLR are handled externally.

        :param SER: pin number of the serial input pin (SER)
        :param SRCLK: pin number of the shift register clock pin (SRCLK)
        :param RCLK: pin number of the storate register clock pin (RCLK)
        :param chrs: Action characters to map to the LEDs, LSB first. Length of this defines the number
                     of shifts before the storage is triggered.
        """
        self.SER = SER
        self.SRCLK = SRCLK
        self.RCLK = RCLK
        self.chrs = chrs[::-1] # reverse, because MSB needs to be pushed first

    def setup(self):
        """Configure GPIO pins."""
        for pin in (self.SER, self.SRCLK, self.RCLK):
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        self.state = {}
        for c in self.chrs:
            self.state[c] = False

    def output(self, chrs, on):
        # update state
        for c in chrs:
            if c in self.state.keys():
                self.state[c] = on
        # now push to shift register
        for c in self.chrs:
            GPIO.output(self.SER, self.state[c])
            GPIO.output(self.SRCLK, GPIO.HIGH)
            GPIO.output(self.SRCLK, GPIO.LOW)
        # commit
        GPIO.output(self.RCLK, GPIO.HIGH)
        GPIO.output(self.RCLK, GPIO.LOW)


def _ledOutputThread():
    print "Starting 'LED output loop."
    msg = messagequeue.leds.receive()
    while msg != STOPMSG:
        pattern = defaultPattern
        suffix = msg[-1]
        if suffix in suffixPatterns.keys():
            pattern = suffixPatterns[suffix]
        newMsg = None
        l = len(pattern)
        c = 0
        # now for the magic: the blink pattern parsing
        # blink patterns may consist one of three possible actions, as described below
        while c < l:
            step = pattern[c]
            if type(step) == bool:
                # 1st: A bool value. Means turning the LEDs on or off
                for i in configuredLedOutputs:
                    i.output(msg, step)
            elif step < 0:
                # 2nd: A negative integer. Rewinds the pattern, to be used for endless patterns.
                c = c + step
            else:
                # 3rd: A positive number. Determines the amount of time to wait until the next action.
                newMsg = messagequeue.leds.waitForMessage(step)
                if newMsg != None:
                    break
            c = c + 1
        if newMsg != None:
            for i in configuredLedOutputs:
                i.output(msg, False)
            msg = newMsg
        else:
            msg = messagequeue.leds.receive()

def setup():
    if len(configuredLedOutputs) > 0:
        GPIO.setmode(GPIO.BOARD)
        for i in configuredLedOutputs:
            i.setup()
    ledthread = threading.Thread(target=_ledOutputThread)
    ledthread.start()

def stop():
    messagequeue.leds.send(STOPMSG)

def getConfigSymbols():
    m = {'addLedOutput': addLedOutput}
    for i in allLedClasses:
        m[i.__name__] = i
    return m

allLedClasses.append(Leds74HC595)


