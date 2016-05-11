# config.py
#
# method to read the configuration.
# also contains/imports the classes to be used in configuration files
#

import handlers
from buzzgroup import BuzzerGroup, Sample

# Options with their default - can be oerwritten by config file
Options = { 'TickTime': 0.02 }

# Optimistic load function. If anything goes wrong, the exception rushes through to the caller
def load(filename='buzz.cfg'):
    # set up some shortcuts for use in configuration files
    loc = {'basic':handlers.BasicHandler, 
           'double':handlers.DoubleHandler,
           'multi':handlers.MultiHandler}
    execfile(filename, globals(), loc)

    # get buzzer groups
    groups = []
    for i in loc:
        if isinstance(loc[i], BuzzerGroup):
            groups.append(loc[i])
    groups.sort(key=lambda x: x.prio)

    return groups
