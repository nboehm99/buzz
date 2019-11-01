#
# samplelib - Sample playing using mpd
#

import mpd
import os
import random

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
            
        mpc.single(1)
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


class RandomSample:
    def __init__(self):
        pass

    def __repr__(self):
        return "RandomSample()"

    def run(self):
        s = random.choice(registered_samples)
        s.run()


class SampleList:
    def __init__(self, filelist, order='linear'):
        self.samples = []
        self.filelist = filelist
        self.order = order
        if order == 'random':
            self.next = self.__next_random
        else:
            if order != 'linear':
                print "Warning: unsupported sample list ordering '%s'. Using 'linear' instead." % order
            self.next = self.__next_linear

        for f in filelist:
            self.samples.append(Sample(f))

        self.num = len(self.samples)
        self.last = -1


    def __repr__(self):
        return "SampleList(%s, %s)" % (self.filelist, self.order)


    def __next_random(self):
        return random.choice(self.samples)


    def __next_linear(self):
        self.last = (self.last+1) % self.num
        return self.samples[self.last]


    def run(self):
        s = self.next()
        s.run()



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
actions.registerActionClass(RandomSample)
actions.registerActionClass(SampleList)
actions.registerActionClass(Volume)

