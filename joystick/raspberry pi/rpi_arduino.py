from joystick import control_joystick
from time import time_ns
from socket import *



s = socket(AF_INET, SOCK_DGRAM)
s.connect(('192.168.1.106', 8888))

joystick = control_joystick("skeleton")

ns_ref = time_ns()
count = 0
t_sap = 20
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):
    joystick.read_arduino()
    s.send(str(joystick.arduino_value).encode('utf-8'))
    count += 1


print(count)
print(count/t_sap)
print((t_sap*1000)/count)


