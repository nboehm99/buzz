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
        m = messagequeue.main.receive()
        if m == STOPMSG:
            break
        actions.execute(m)

def stop():
    messagequeue.main.send(STOPMSG)

