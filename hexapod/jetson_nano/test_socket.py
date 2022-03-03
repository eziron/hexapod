import socket
import struct
from time import time
import sys
import fcntl, os
import errno

s1, s2 = socket.socketpair()
fcntl.fcntl(s2, fcntl.F_SETFL, os.O_NONBLOCK)

s1.send(struct.pack("BBBBH",0,1,2,3,5000))



print(s2.recv(10))
print(s2.recv(1))