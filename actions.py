# actions.py
#
# managing the actions
#
import messagequeue

# 
actionMap = {} # map of (action, led:bool)-tuples

# list of all action classes available in config
allActions = []

def execute(actionKey):
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
 
