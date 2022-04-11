import socket
from protocolo_udp import pro_UDP
from time import time

A = (195/64)
B = -(16575/32)
C = (1440875/64)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
joystick = pro_UDP(s,"joystick.local")

while True:
    cmd, buffer = joystick.read_command()
    if(not ((cmd is None) or (buffer is None))):
        joystick.send_command(cmd,"h",[5,5])

        if(cmd == 25):
            ang_abs = abs(buffer[1]/64)
            if(ang_abs > 90):
                ang_abs = 180-ang_abs

            if(ang_abs <= 5):
                rad = 100000
            elif(ang_abs >= 85):
                rad = 500
            else:
                rad = A*(ang_abs**2)+B*ang_abs+C

            if(buffer[1] < 0):
                rad = -rad

            rad = round(rad)
        print(rad,buffer)

