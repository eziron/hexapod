import socket
from protocolo_udp import pro_UDP
from time import time, sleep
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import serial
import json
import os

A = (195/64)
B = -(16575/32)
C = (1440875/64)

n_seq = -1
n_step = -1
h = 0
z = 50
arco = 50
speed = 300
cam_speed = 300
caminata_p_rot = [1000000,0]
ang_RX = 0.0
ang_RY = 0.0
ang_RZ = 0.0

modo_mov = -1
estado_p = True
estado_g = True

json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

baud = conf_hexapod["general"]["baudrate"]

while True:
    try:
        Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
        os.system("""echo 102938 | sudo renice -20 -p $(pgrep "python3")""")
        break
    except:
        print("Error al inisiar el serial")
        os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")

serial_com = pro_Serial(Serial)
hexapod = Hexapod(conf_hexapod)
joystick = pro_UDP()

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    sleep(0.2)

serial_com.stop_lidar()
serial_com.send_duty(hexapod.sv_duty())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("0.0.0.0", 8888))
    print("Servidor activado")
    s.listen()
    conn, addr = s.accept()
    conn.setblocking(0)
    hexapod.reset_dt()
    
    with conn:
        print(f"Connected by {addr}")
        while True:
            cmd, buffer = joystick.read_command(conn)
            if(not ((cmd is None) or (buffer is None))):
                joystick.send_command(conn,cmd,"h",[5,5])
                #print(buffer[0],buffer[1]/64,buffer[3],buffer[4],buffer[5],buffer[6]/64,buffer[7]/64,buffer[8]/64)
                if(cmd == 25):
                    if(buffer[0] > 10):
                        ang_val = buffer[1]/64
                        ang_abs = abs(ang_val)

                        if(ang_abs > 45 and ang_abs < 135):
                            if(modo_mov == -1):
                                modo_mov = 0
                                
                        else:
                            if(modo_mov == -1):
                                modo_mov = 1

                        if(modo_mov == 0):
                            caminata_p_rot[0] = 0
                            caminata_p_rot[1] = 0

                            if(buffer[1] < 0):
                                n_seq = 3
                            else:
                                n_seq = 2
                        elif(modo_mov == 1):
                            caminata_p_rot[0] = 1000000
                            caminata_p_rot[1] = 0

                            if(ang_abs > 90):
                                n_seq = 0
                            else:
                                n_seq = 1
                        #print(ang_abs,n_seq,caminata_p_rot)

                        cam_speed = buffer[0]
                        z      = abs(buffer[3])
                        arco   = abs(buffer[4])

                    else:
                        modo_mov = -1
                        n_step = 0
                        n_seq = -1
                    
                    h      = abs(buffer[5])
                    ang_RX =     buffer[6]/64
                    ang_RY =     buffer[7]/64
                    ang_RZ =     buffer[8]/64

            try:
                estado_g,estado_p,_,_,_,_ =hexapod.actualizar_cord()
                serial_com.send_duty(hexapod.sv_duty())
            except:
                pass

            if(n_seq >= 0):
                if(estado_p):
                    hexapod.polar_set_step_caminata(
                            n_sec=n_seq,
                            n_step=n_step,
                            dis_arco=arco,
                            z=z,
                            lineal_speed=cam_speed,
                            cord_r=caminata_p_rot,
                            doble_cent_r=False,
                            r_por_pie=True,
                            estado=estado_p
                        )

                    n_step += 1
                    if(n_step >= 6):
                        n_step = 0
            else:
                for i in range(6):
                    hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)
                
            hexapod.set_param_speed(100,20,h)
            hexapod.set_param_time(0.1,None,[ang_RX,ang_RY,ang_RZ])
