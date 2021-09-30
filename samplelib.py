#
# samplelib - Sample playing using mpd
#

import mpd
import os
import random

import actions

registered_samples = []
basedir = ''
maxvolume = 100

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
        self.valid = False

        if os.path.isfile(fullpath):
            self.valid = True
            registered_samples.append(self)
        else:
            print "Warning: invalid sample path '%s'. Ignored." % path
            
        print "A glorious instance of the Sample-class was created (%s)" % path


    def __repr__(self):
        return "Sample('%s', loop=%s)" % (self.path, self.loop)


    def __call__(self):
        if self.valid:
            mpc = _connect()
            print "Running sample %s" % self
            mpc.clear()
            mpc.add('file://' + self.fullpath)
            if self.loop:
                mpc.repeat(1)
            else:
                mpc.repeat(0)
            mpc.play()
            _disconnect(mpc)


class RandomSample:
    def __init__(self):
        pass

    def __repr__(self):
        return "RandomSample()"

    def __call__(self):
        s = random.choice(registered_samples)
        s()


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


    def __call__(self):
        s = self.next()
        s()



class Volume:
    def __init__(self, vol, absolute=False):
        self.vol = vol
        self.absolute = absolute

    def __repr__(self):
        return "Volume(%d, %s)" % (self.vol, self.absolute)

    def __call__(self):
        mpc = _connect()
        global maxvolume
        oldvol = 0
        if not self.absolute:
            s = mpc.status()
            oldvol = int(s['volume'])
        newvol = oldvol + self.vol
        if newvol < 0: newvol = 0
        if newvol > maxvolume: newvol = maxvolume
        print "Setting volume to %s" % newvol
        mpc.setvol(newvol)
        _disconnect(mpc)


class MpdPlayPause:
    def __init__(self):
        pass

    def __repr__(self):
        return "MpdPlayPause()"

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['state'] in ('play','pause'):
            mpc.pause()
        else:
            mpc.play()
        _disconnect(mpc)


class MpdToggleRepeat:
    def __init__(self):
        pass

    def __repr__(self):
        return "MpdToggleRepeat()"

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['repeat'] is '0':
            mpc.repeat(1)
        else:
            mpc.repeat(0)
        _disconnect(mpc)


class MpdToggleSingle:
    def __init__(self):
        pass

    def __repr__(self):
        return "MpdToggleSingle()"

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['single'] is '0':
            mpc.single(1)
            mpc.repeat(1)
        else:
            mpc.single(0)
            mpc.repeat(0)
        _disconnect(mpc)


class MpdToggleRandom:
    def __init__(self):
        pass

    def __repr__(self):
        return "MpdToggleRandom()"

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['random'] is '0':
            mpc.random(1)
        else:
            mpc.random(0)
        _disconnect(mpc)


# mpd module's seekcur doesn't seem to work properly with negative offsets
# so we use a manual workaround
class MpdSeekBwd:
    def __init__(self, offset):
        self.offset = float(offset)

    def __repr__(self):
        return "MpdSeekBwd(%d)" % self.offset

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['state'] == 'play':
            now = float(s['time'].split(':')[0])
            then = now - self.offset
            if then < 0:
                then = 0
            mpc.seekcur('%.2f' % then)
        _disconnect(mpc)


class MpdCommand:
    def __init__(self, mname, *args):
        self.mname = mname
        self.args = args

    def __repr__(self):
        if len(self.args) > 0:
            return "MpdCommand('%s', %s)" % (self.mname, ','.join(map(str, self.args)))
        else:
            return "MpdCommand('%s')" % (self.mname)

    def __call__(self):
        mpc = _connect()
        s = mpc.status()
        if s['state'] == 'play':
            func = getattr(mpc, self.mname)
            func(*self.args)
        _disconnect(mpc)


actions.registerActionClass(Sample)
actions.registerActionClass(RandomSample)
actions.registerActionClass(SampleList)
actions.registerActionClass(Volume)

def getConfigSymbols():
    m = {'MpdNext': MpdCommand('next'),
         'MpdPrev': MpdCommand('previous'),
         'MpdSeekFwd': MpdCommand('seekcur','+5'),
         'MpdSeekBwd': MpdSeekBwd(5),
         'MpdPlayPause': MpdPlayPause(),
         'MpdToggleSingle': MpdToggleSingle(),
         'MpdToggleRepeat': MpdToggleRepeat(),
         'MpdToggleRandom': MpdToggleRandom()}
    return m

