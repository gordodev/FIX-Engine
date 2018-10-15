#!/usr/bin/env python2.7

import socket
   
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "35=D,55=AAPL,38=10000,54=2,44=1,49=MYFIRM,56=FIXHUB,128=AESDESK"
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
 
print "received data:", data
