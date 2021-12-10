import struct
from joystick import control_joystick
import spidev
from socket import *
from time import sleep
from time import time_ns

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

joystick = control_joystick(spi)
joystick.write_arduino()

sleep(2)

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('192.168.1.106', 8888))


ns_ref = time_ns()
count = 0

t_sap = 20
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):
    val = joystick.read_arduino()
    if(not val is None):
        print(len(val),val)
        s.send(struct.pack("<"+"l"*len(val),*val))
        count += 1

print(count)
print(count/t_sap)
print((t_sap*1000)/count)