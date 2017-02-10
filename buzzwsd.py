# buzzwsd - buzzer websocket daemon
#
# Implementation of RBTP (remote buzzer triggering protocol) over websocket
#

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import messagequeue
import inputregistry


DEFAULT_PORT = 8055


class BuzzSocket(WebSocket):

    def handleMessage(self):
        print "Received message:", self.data
        if self.data.startswith('buzz '):
            msg = self.data[5:]
            print "command:", msg
            messagequeue.send(msg)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'


class WebSocketInput:
    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.wss  = None

    def run(self):
        print "Starting server on localhost:%d" % self.port
        self.wss = SimpleWebSocketServer('', self.port, BuzzSocket)
        try:
            self.wss.serveforever()
        except:
            print "Buzzws server killed or crashed. Bye!"

    def stop(self):
        self.wss.close()


inputregistry.registerClass(WebSocketInput)
