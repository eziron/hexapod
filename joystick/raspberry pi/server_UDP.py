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


ns_dt = (1/5)*1000000
ns_ref = time_ns()
while(True):
    if(time_ns()-ns_ref >= ns_dt):
        ns_ref = time_ns()
        val = joystick.read_arduino()
        if(not val is None):
            print(val)
            s.send(struct.pack("<"+"l"*len(val),*val))
