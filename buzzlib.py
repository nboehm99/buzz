#
# buzzlib - common stuff used by different buzzer thingies.
#
import os

def play(idx):
    os.system('mpc play %d' % (idx))

