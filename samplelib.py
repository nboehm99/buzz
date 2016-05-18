#
# samplelib - common stuff used by different buzzer thingies.
#
import mpd
import os

registered_samples = []
sample_map = {}

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
    if os.path.isfile(path):
        print "Adding %s" % ('file://' + path)
        mpc.add('file://' + path)
        registered_samples.append(sample)
        idx = len(registered_samples)
        sample_map[sample.get_action()] = idx-1
    else:
        print "Warning: invalid sample path '%s'. Ignored." % path
    _disconnect(mpc)


def play(action, loop=False):
    idx = -1
    try:
        idx = sample_map[action]
    except KeyError:
        pass
    if idx >= 0:
        mpc = _connect()
        print "Buzzing sound", registered_samples[idx].get_path() ,
        if registered_samples[idx].is_loop():
            mpc.repeat(1)
            print "(looping)"
        else:
            mpc.repeat(0)
            print
        mpc.play(idx)
        _disconnect(mpc)

