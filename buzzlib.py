#
# buzzlib - common stuff used by different buzzer thingies.
#
import os

def play(idx):
    print "Buzzing sound", idx
    os.system('mpc play %d' % (idx))

