import joystick as jk
from time import sleep, time
import spidev
import os
import socket
from protocolo_udp import pro_UDP
os.system("""echo raspberry | sudo renice -20 -p $(pgrep "python")""")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hexapod = pro_UDP(s,"hexapod.local")

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.mode = 0b00
spi.max_speed_hz = 800000
#spi.max_speed_hz = 50000

joystick = jk.control_joystick(spi)
joystick.write_arduino()
count = 0
loss_count = 0
t_sap = 5
time_ref = time()
dt = time_ref
while(time()-time_ref < t_sap):
    if(joystick.read_arduino()):
        val = joystick.arduino_value
        estado = hexapod.send_command(25,"h",list(val.values()))
        
        if(estado):
            cmd,buff = hexapod.read_command()
            if(not cmd is None):
                count += 1
                print(count,estado,list(val.values()))
    else:
        loss_count += 1
        print("------  LOSS ------")


print(count)
print(count/t_sap)
print((t_sap*1000)/count)
print(loss_count)
print(loss_count/t_sap)


