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

    def __call__(self):
        for a in self.actions:
            a()


class SetPrefix:

    def __init__(self, prefix):
        self.prefix = prefix

    def __repr__(self):
        return "SetPrefix(%s)" % self.prefix

    def __call__(self):
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
            print "With led:", actionKey
            messagequeue.leds.send(actionKey)
        action()
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

def setInitialPrefix(prefix):
    global _prefix
    _prefix = prefix

def getConfigSymbols():
    m = {'setAction': setAction,
         'setLedAction': setLedAction,
         'setInitialPrefix': setInitialPrefix}
    for a in allActions:
        m[a.__name__] = a
    return m

registerActionClass(ActionList)
registerActionClass(SetPrefix)

