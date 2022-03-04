import socket
import struct
from time import time
import fcntl, os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0].split(".")
print(local_ip)
local_ip[-1] = str(0)
print(local_ip)
s.close()