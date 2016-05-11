# buzzwsd - buzzer websocket daemon
#
# Implementation of RBTP (remote buzzer triggering protocol) over websocket
#

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import re
import threading

import samplelib

rbtp_ws_port = 8055
rbtp_parser = re.compile("^buzz ([0-9]+)$")

wsd_thread = None
wsd_server = None

class SimpleEcho(WebSocket):

    def handleMessage(self):
        msg = self.data[0:15] # 10 billion sounds should be enough for everyone
        print "command:", msg
        mo = rbtp_parser.match(msg)
        if mo:
#            print "mpd play", int(mo.groups()[0])
            samplelib.play(int(mo.groups()[0]))

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

def buzzwsd():
    print "Starting server on localhost:%d" % rbtp_ws_port
    try:
        wsd_server.serveforever()
    except:
        print "Buzzws server killed or crashed. Bye!"

def start_daemon():
    global wsd_server, wsd_thread
    wsd_server = SimpleWebSocketServer('', rbtp_ws_port, SimpleEcho)
    wsd_thread = threading.Thread(target=buzzwsd)
    wsd_thread.start()

def stop_daemon():
    wsd_server.close()

