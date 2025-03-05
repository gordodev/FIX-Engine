#!/usr/bin/env python2.7
  
import socket
import sys

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    
    print 'Server started, waiting for connections...'
    conn, addr = s.accept()
    print 'Connection address:', addr
    
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print "received data:", data
        conn.send(data)  # echo
    
    conn.close()
    
except socket.error as e:
    print "Socket error:", e
    sys.exit(1)
except KeyboardInterrupt:
    print "Server stopped by user"
    if 'conn' in locals():
        conn.close()
    sys.exit(0)
