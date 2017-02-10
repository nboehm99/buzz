# messagequeue.py
#
# small wrappers for python Queue
#

import Queue

_myQueue = Queue.Queue(5) # 5 is probably 4 too many

def send(msg):
    _myQueue.put(msg, block=True)

def receive():
    return _myQueue.get(block=True)

