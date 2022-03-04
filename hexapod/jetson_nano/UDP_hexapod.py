import socket

from click import command
from protocolo_udp import pro_UDP
from time import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
joystick = pro_UDP(s,"192.168.120.207")

while True:
    cmd, buffer = joystick.read_command()
    if(not ((cmd is None) or (buffer is None))):
        print(cmd,buffer)
        print(joystick.send_command(cmd,"H",buffer))