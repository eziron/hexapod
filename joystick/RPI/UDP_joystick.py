import socket
from time import sleep, time
from protocolo_udp import pro_UDP
import joystick as jk
import spidev
import os
import math

os.system("""echo raspberry | sudo renice -20 -p $(pgrep "python")""")

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

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hexapod = pro_UDP(s,"hexapod.local")
print(s.getsockname())



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
t_sap = 300
time_ref = time()
dt = time_ref
while(time()-time_ref < t_sap):
    if(time()-dt > 0.05):
        dt = time()

        if(joystick.read_arduino()):
            val_dic = joystick.arduino_value
            val = list(val_dic.values())
            ang,mod = rec_to_pol(val_dic["x_izq"],val_dic["y_izq"])
            mod = Aconstrain(mod,0,800)

            

            buff = [
                round(mod),              #velocidad lineal de la caminata
                round(ang*64),          #angulo de giro del hexapod
                val_dic["but_analog_izq"],   #modo de movimientos, caminata/giro
                val_dic["cruz_der_h"],       #Z
                val_dic["cruz_der_v"],       #arco
                val_dic["cruz_izq_h"],       #H  
                val_dic["y_der"],            #RX
                0,                           #RY
                val_dic["x_der"],            #RZ
            ]

            print("SEND")
            estado = hexapod.send_command(25,"h",buff)
            if(estado):
                cmd,buff_rex = hexapod.read_command()
                if(not cmd is None):
                    count += 1
            else:
                print("----------------SEND ERROR----------------")

            
            print(count,buff)
            count += 1
                
            
        else:
            loss_count += 1
            print("------  LOSS ------")
    else:
        sleep(0.001)
    
#/usr/bin/python /home/pi/Desktop/hexapod/joystick/RPI/UDP_joystick.py

print(count)
print(count/t_sap)
print((t_sap*1000)/count)
print(loss_count)
print(loss_count/t_sap)


    
