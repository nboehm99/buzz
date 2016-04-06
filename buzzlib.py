#
# buzzlib - common stuff used by different buzzer thingies.
#

def play(idx):
    os.system('mpc play %d' % (idx))

