#!/usr/bin/python
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
import time
import socket
import threading


class mysocket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        MSGLEN=len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        msg = ''
        MSGLEN=120
        while len(msg) < MSGLEN:
            chunk = self.sock.recv(MSGLEN-len(msg))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            msg = msg + chunk
        return msg
    def myclose(self):
        self.sock.close()


class SimpleEcho(WebSocket):
    def SockFun(self):
        try:
            ms=mysocket()
            ms.connect("127.0.0.1",7778)
            self.FlagDict["sockexists"]=1
            while (1):
                print "inside  ",self.FlagDict
                if ( self.FlagDict["Data"] ):
                    time.sleep(1)
                    msg=str(self.FlagDict["Data"])
                    #self.FlagDict["Data"]=''
                    ms.mysend(msg)
                else:
                    time.sleep(10)
                a=ms.myreceive()
                self.sendMessage(a)

            self.FlagDict["sockexists"]=0
            self.FlagDict["threadexists"]=0
            ms.myclose()
        except Exception as a:
            self.FlagDict["sockexists"]=0
            self.FlagDict["threadexists"]=0
            ms.myclose()
            print "error in SockFun",a


    def handleMessage(self):
        if self.data is None:
            self.data = ''
        else:
            self.CheckThread()

    def handleConnected(self):
        print self.address, 'connected'
        try:
            self.FlagDict={}
            self.FlagDict["sockexists"]=0
            self.FlagDict["threadexists"]=0
            self.FlagDict["Data"]=self.data
        except:
            print "error in handle connect"

    def handleClose(self):
        print self.address, 'closed'



server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()
