#
# samplelib - common stuff used by different buzzer thingies.
#
import mpd

def _mpc():
    mpc = mpd.MPDClient()
    mpc.connect("localhost", 6600)
    return mpc


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

