from joystick import control_joystick
from time import time_ns
import spidev

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

joystick = control_joystick(spi)
joystick.write_arduino()
ns_ref = time_ns()
count = 0
t_sap = 20
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):
    joystick.read_arduino()
    print(joystick.arduino_value)
    count += 1


print(count)
print(count/t_sap)
print((t_sap*1000)/count)


