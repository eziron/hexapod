import struct
from joystick import control_joystick
import spidev
from socket import *
from time import sleep, time

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000
sleep(0.1)

joystick = control_joystick(spi)
joystick.write_arduino()
sleep(1)

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('192.168.1.106', 8888))
sleep(0.1)

dt = 1/60
time_ref = time()
while(True):
    if(time()-time_ref >= dt):
        time_ref = time()
        val = joystick.read_arduino()
        if(not val is None):
            print(val)
            s.send(struct.pack("<"+"l"*len(val),*val))
