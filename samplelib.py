#
# samplelib - Sample playing using mpd
#

import mpd
import os
import actions

registered_samples = []
basedir = ''


def _connect():
    mpc = mpd.MPDClient()
    mpc.connect("/var/run/mpd/socket", 0)
    return mpc


def _disconnect(mpc):
    mpc.close()
    mpc.disconnect()


class Sample:
    def __init__(self, path, loop=False):
        global registered_samples
        global basedir
        fullpath = os.path.join(basedir,path)
        self.path = path
        self.fullpath = fullpath
        self.loop = loop
        self.idx = -1

        mpc = _connect()
        if len(registered_samples) == 0:
            mpc.clear()
        
        if os.path.isfile(fullpath):
            mpc.add('file://' + fullpath)
            registered_samples.append(self)
            idx = len(registered_samples)
            self.idx = idx-1
        else:
            print "Warning: invalid sample path '%s'. Ignored." % path
            
        _disconnect(mpc)
        print "A glorious instance of the Sample-class was created (%s)" % path


    def __repr__(self):
        return "Sample('%s', loop=%s)" % (self.path, self.loop)


    def run(self):
        if self.idx >= 0:
            mpc = _connect()
            print "Running sample %s" % self
            if self.loop:
                mpc.repeat(1)
            else:
                mpc.repeat(0)
            mpc.play(self.idx)
            _disconnect(mpc)

class Volume:
    def __init__(self, vol, absolute=False):
        self.vol = vol
        self.absolute = absolute


    def __repr__(self):
        return "Volume(%d)" % (self.vol)


    def run(self):
        mpc = _connect()
        oldvol = 0
        if not self.absolute:
            s = mpc.status()
            oldvol = int(s['volume'])
        newvol = oldvol + self.vol
        if newvol < 0: newvol = 0
        if newvol > 100: newvol = 100
        print "Setting volume to %s" % newvol
        mpc.setvol(newvol)
        _disconnect(mpc)

actions.registerActionClass(Sample)
actions.registerActionClass(Volume)

