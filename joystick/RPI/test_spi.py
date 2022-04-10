import joystick as jk
from time import sleep, time
import spidev
import os
import math

def rec_to_pol(X,Y):
    ang = math.degrees(math.atan2(X,Y))
    mod = math.sqrt((X**2)+(Y**2))
    return ang, mod

def Aconstrain(val,min_val,max_val):
    if(val < min_val):
        return min_val
    elif(val > max_val):
        return max_val
    else:
        return val 

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.mode = 0b00
spi.max_speed_hz = 800000

joystick = jk.control_joystick(spi)
joystick.write_arduino()
count = 0
loss_count = 0
t_sap = 30
time_ref = time()
dt = time_ref
while(time()-time_ref < t_sap):
    if(joystick.read_arduino()):
        val = joystick.arduino_value
        ang,mod = rec_to_pol(val["x_izq"],val["y_izq"])
        mod = Aconstrain(mod,0,2000)
        print(count,ang,mod,list(val.values()))
        count += 1
        sleep(0.08)
    else:
        loss_count += 1
        print("------  LOSS ------")


print(count)
print(count/t_sap)
print((t_sap*1000)/count)
print(loss_count)
print(loss_count/t_sap)