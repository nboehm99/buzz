# actions.py
#
# managing the actions
#
import messagequeue

# 
actionMap = {} # map of (action, led:bool)-tuples

# list of all action classes available in config
allActions = []

# Action prefix, aka bank selection
_prefix = None

class ActionList:

    def __init__(self, *args):
        self.actions = args

    def __repr__(self):
        return "ActionList(%s)" % ", ".join(map(str,self.actions))

    def run(self):
        for a in self.actions:
            a.run()


class SetPrefix:

    def __init__(self, prefix):
        self.prefix = prefix

    def __repr__(self):
        return "SetPrefix(%s)" % self.prefix

    def run(self):
        global _prefix
        _prefix = self.prefix


def execute(rawActionKey):
    actionKey = rawActionKey
    if _prefix != None:
        actionKey = "%s:%s" % (_prefix, rawActionKey)
    if actionKey in actionMap.keys():
        action, led = actionMap[actionKey]
        print "Performing action", action
        if led:
            messagequeue.leds.send(actionKey)
        action.run()
    else:
        print "No action registered for '%s'" % actionKey

def setAction(actionKey, action, led=False):
    if actionKey in actionMap.keys():
        print "Warning: action for '%s' registered more than once!" % actionKey
    actionMap[actionKey] = (action, led)

def setLedAction(actionKey, action):
    setAction(actionKey, action, True)

def registerActionClass(aClass):
    allActions.append(aClass)


registerActionClass(ActionList)
registerActionClass(SetPrefix)

