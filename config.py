# config.py
#
# method to read the configuration.
# also contains/imports the classes to be used in configuration files
#

#import handlers
#from buzzgroup import BuzzerGroup, Sample

# Options with their default - can be oerwritten by config file
# Options = { 'TickTime': 0.02 }

import buzzwsd
import samplelib

import actions
import inputregistry

# Optimistic load function. If anything goes wrong, the exception rushes through to the caller
def load(filename='buzz.cfg'):
    # add action classes to config file namespace
    loc = {'setAction':actions.setAction,
           'addInput':inputregistry.addInput}
    for c in actions.allActions:
        loc[c.__name__] = c
    for c in inputregistry.allInputClasses:
        loc[c.__name__] = c
    execfile(filename, globals(), loc)

