import socket
from time import sleep, time
from protocolo_udp import pro_UDP

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hexapod = pro_UDP(s,"hexapod.local")
print(s.getsockname())


count = 0
t_samp = 25
time_ref = time()
while time()-time_ref < t_samp:
    estado = hexapod.send_command(25,"h",[1676,255])
    if(estado):
        cmd,buff = hexapod.read_command()
        if(not cmd is None):
            count += 1

print(count)
print(count/t_samp)
