# output.py
#
# endlessly taking stuff from queue and passing it to action handling
#

import messagequeue
import actions

STOPMSG='<!>STOP<!>'

def run():
    print "Starting output loop."
    while True:
        m = messagequeue.receive()
        if m == STOPMSG:
            break
        actions.execute(m)

def stop():
    messagequeue.send(STOPMSG)

