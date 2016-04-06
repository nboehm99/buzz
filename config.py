# config.py
#
# method to read the configuration.
# also contains/imports the classes to be used in configuration files
#

import handlers
from buzzgroup import BuzzerGroup


# Optimistic load function. If anything goes wrong, the exception rushes through to the caller
def load(filename='buzz.cfg'):
    loc = {'basic':handlers.BasicHandler, 'multi':handlers.MultiHandler}
    execfile(filename, globals(), loc)

    groups = []
    for i in loc:
        if isinstance(loc[i], BuzzerGroup):
            groups.append(loc[i])
    groups.sort(key=lambda x: x.prio)

    return groups
