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

hexapod = pro_UDP()

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

estado = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("hexapod.local", 8888))
    
    time_ref = time()
    dt = time_ref
    while(estado):
        if(time()-dt > 0.05):
            dt = time()

            if(joystick.read_arduino()):
                val_dic = joystick.arduino_value
                val = list(val_dic.values())
                ang,mod = rec_to_pol(val_dic["x_izq"],val_dic["y_izq"])
                mod = Aconstrain(mod,0,800)

                buff = [
                    round(mod),                  #[0] velocidad lineal de la caminata
                    round(ang*64),               #[1] angulo de giro del hexapod
                    val_dic["but_analog_izq"],   #[2] modo de movimientos, caminata/giro
                    val_dic["cruz_der_h"],       #[3] Z
                    val_dic["cruz_der_v"],       #[4] arco
                    val_dic["cruz_izq_h"],       #[5] H  
                    val_dic["y_der"],            #[6] RX
                    0,                           #[7] RY
                    val_dic["x_der"],            #[8] RZ
                ]

                estado_resp = hexapod.send_command(s,25,"h",buff)
                if(estado_resp):
                    cmd,buff_rex = hexapod.read_command(s)
                    if(not cmd is None):
                        count += 1
                        loss_count = 0
                    else:
                        loss_count += 1
                else:
                    loss_count += 1

                if(loss_count > 50):
                    estado = False
                
                print(count,"speed:",buff[0],"/ Z:",buff[3],"/ arco:",buff[4],"/ H:",buff[5],"/ RX:",round(buff[6]/64,1),"/ RZ:",round(buff[8]/64,1))
    
#/usr/bin/python /home/pi/Desktop/hexapod/joystick/RPI/UDP_joystick.py



    
