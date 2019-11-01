# inputregistry.py
#
# list of all input classes available in config

allInputClasses = []
allInputs = []

def addInput(inputInstance):
    allInputs.append(inputInstance)

def getAll():
    return allInputs

def registerClass(iClass):
    allInputClasses.append(iClass)
 
def getConfigSymbols():
    m = {'addInput': addInput}
    for i in allInputClasses:
        m[i.__name__] = i
    return m

