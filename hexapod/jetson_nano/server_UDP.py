import struct
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('0.0.0.0', 8888))

while True:
    data = s.recv(72)
    if not data:
        break
    print(struct.unpack("<"+"l"*18,data))
    