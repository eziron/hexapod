from joystick import control_joystick
from time import sleep, time
import spidev
import os

os.system("""echo raspberry | sudo renice -20 -p $(pgrep "python")""")

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.mode = 0b00
spi.max_speed_hz = 800000
#spi.max_speed_hz = 50000

joystick = control_joystick(spi)
joystick.write_arduino()
count = 0
loss_count = 0
t_sap = 5*60
time_ref = time()
dt = time_ref
while(time()-time_ref < t_sap):
    if(joystick.read_arduino()):
        val = joystick.arduino_value
        if(time()-dt > 0.02):
            print(round((time()-dt)*1000000),count,val["x_izq"],val["y_izq"],val["x_der"],val["y_der"])

        if(count % 1000 == 0 and count > 0):
            print(count,(time()-time_ref)*1000/count)

        dt = time()
        count += 1
    else:
        loss_count += 1
        print("------  LOSS ------")


print(count)
print(count/t_sap)
print((t_sap*1000)/count)
print(loss_count)
print(loss_count/t_sap)


