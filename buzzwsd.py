# buzzwsd - buzzer websocket daemon
#
# Implementation of RBTP (remote buzzer triggering protocol) over websocket
#

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import re
import buzzlib

rbtp_ws_port = 8055
rbtp_parser = re.compile("^buzz ([0-9]+)$")

class SimpleEcho(WebSocket):

    def handleMessage(self):
        msg = self.data[0:15] # 10 billion sounds should be enough for everyone
        print "command:", msg
        mo = rbtp_parser.match(msg)
        if mo:
#            print "mpd play", int(mo.groups()[0])
            buzzlib.play(int(mo.groups()[0]))

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

print "Starting server on localhost:%d" % rbtp_ws_port
server = SimpleWebSocketServer('', rbtp_ws_port, SimpleEcho)
server.serveforever()

