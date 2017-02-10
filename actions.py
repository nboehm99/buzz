# actions.py
#
# managing the actions
#

# 
actionMap = {}

# list of all action classes available in config
allActions = []

def execute(actionKey):
    if actionKey in actionMap.keys():
        action = actionMap[actionKey]
        print "Performing action", action
        action.run()
    else:
        print "No action registered for '%s'" % actionKey

def setAction(actionKey, action):
    if actionKey in actionMap.keys():
        print "Warning: action for '%s' registered more than once!" % actionKey
    actionMap[actionKey] = action

def registerActionClass(aClass):
    allActions.append(aClass)
 
