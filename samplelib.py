#
# samplelib - common stuff used by different buzzer thingies.
#
import mpd

setup_done = False
registered_samples = []

def _mpc():
    mpc = mpd.MPDClient()
    mpc.connect("localhost", 6600)
    return mpc

def register(sample):
    registered_samples.append(sample)

    return 0


def play(idx, loop=False):
    print "Buzzing sound", idx
    mpc = _mpc()
    if loop:
        mpc.repeat(1)
    else:
        mpc.repeat(0)
    mpc.play(idx-1)
    mpc.close()
    mpc.disconnect()

