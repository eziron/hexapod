import socket
from time import sleep, time

from numpy import true_divide
from protocolo_udp import pro_UDP


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip_array = s.getsockname()[0].split(".")
s.close()

print(local_ip_array)

hexapod_ip = ""
for n in range(3):
    hexapod_ip += local_ip_array[n] + "."
hexapod_ip += "208"

print(hexapod_ip)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hexapod = pro_UDP(s,hexapod_ip)

while True:
    estado = hexapod.send_command(25,"H",[1676,255])
    print(estado)
    sleep(0.1)
    print(hexapod.read_command())
    sleep(1)
