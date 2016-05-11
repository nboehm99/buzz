#
# samplelib - common stuff used by different buzzer thingies.
#
import mpd
import os

registered_samples = []

def _connect():
    mpc = mpd.MPDClient()
    mpc.connect("/var/run/mpd/socket", 0)
    return mpc

def _disconnect(mpc):
    mpc.close()
    mpc.disconnect()

def register(sample):
    global registered_samples

    mpc = _connect()
    if len(registered_samples) == 0:
        mpc.clear()
    path = sample.get_path()
    idx = -1
    if os.path.isfile(path):
        print "Adding %s" % ('file://' + path)
        mpc.add('file://' + path)
        registered_samples.append(sample)
        idx = len(registered_samples)
    else:
        print "Warning: invalid sample path '%s'. Ignored." % path
    _disconnect(mpc)
    return idx


def play(idx, loop=False):
    if idx >= 0:
        aidx = idx - 1
        print "Buzzing sound", registered_samples[aidx].get_path()
        mpc = _connect()
        if registered_samples[aidx].is_loop():
            mpc.repeat(1)
        else:
            mpc.repeat(0)
        mpc.play(aidx)
        _disconnect(mpc)

