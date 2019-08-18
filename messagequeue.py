# messagequeue.py
#
# small wrappers for python Queue
#

import Queue

class _qWrapper:
    
    def __init__(self, size):
        self._q = Queue.Queue(size)

    def send(self, msg):
        self._q.put(msg, block=True)

    def receive(self):
        return self._q.get(block=True)

main = _qWrapper(5) # 5 is probably 4 too many
leds = _qWrapper(5) # same here

