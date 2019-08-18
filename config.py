# config.py
#
# method to read the configuration.
# also contains/imports the classes to be used in configuration files
#

import buzzwsd
import gpiobuttons
import samplelib

import actions
import inputregistry
import ledoutput

# Optimistic load function. If anything goes wrong, the exception rushes through to the caller
def load(filename='buzz.cfg'):
    # add action classes to config file namespace
    loc = {'setAction':actions.setAction,
           'setLedAction':actions.setLedAction,
           'addInput':inputregistry.addInput,
           'addLedOutput': ledoutput.addLedOutput}
    for c in actions.allActions:
        loc[c.__name__] = c
    for c in inputregistry.allInputClasses:
        loc[c.__name__] = c
    for c in ledoutput.allLedClasses:
        loc[c.__name__] = c
    execfile(filename, globals(), loc)

