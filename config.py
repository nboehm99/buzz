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

configSymbols = {}

def addConfigSymbols(symbolMap):
    configSymbols.update(symbolMap)

# Optimistic load function. If anything goes wrong, the exception rushes through to the caller
def load(filename='buzz.cfg'):
    execfile(filename, globals(), configSymbols)

