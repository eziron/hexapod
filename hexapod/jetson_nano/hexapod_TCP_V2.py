from hexapod_util import dead_val_axis,rec_a_pol
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial

from time import time, sleep
from struct import unpack
import multiprocessing as mp
import numpy as np
import serial
import json
import socket
import os



def servo_serial_task(Hexapod_dutys,serial_com:pro_Serial):
    Hexapod_dutys.acquire()
    serial_com.send_duty(Hexapod_dutys)
    Hexapod_dutys.release()
    
def TCP_task(Hexapod_dic):
    global server_address,joystick_vals
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)

        try:
            while True:
                data = connection.recv(21)
                if(data):
                    joystick_vals = unpack(">BhhhhhhhHHH",data)
                    connection.sendall(bytes([0,127,255,55]))

                    Hexapod_dic.acquire()
                    Hexapod_dic["ON"] = joystick_vals[0]
                    Hexapod_dic["X"] = dead_val_axis(joystick_vals[1]/1000.0,5)
                    Hexapod_dic["Y"] = dead_val_axis(joystick_vals[2]/1000.0,5)
                    Hexapod_dic["RX"] = joystick_vals[3]/100.0
                    Hexapod_dic["RY"] = joystick_vals[4]/100.0
                    Hexapod_dic["RZ"] = joystick_vals[5]/100.0
                    Hexapod_dic["DX"] = joystick_vals[6]/10.0
                    Hexapod_dic["DY"] = joystick_vals[7]/10.0
                    Hexapod_dic["H"] = joystick_vals[8]/10.0
                    Hexapod_dic["Z"] = joystick_vals[9]/10.0
                    Hexapod_dic["arco"] = joystick_vals[10]/10.0
                    Hexapod_dic.release()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

        finally:
            # Clean up the connection
            connection.close()

server_address = ('0.0.0.0', 10000)

PATH = os.getcwd()
#json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
#json_PATH = "/home/pi/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
json_PATH = PATH+"/hexapod/jetson_nano/ajustes_hexapod.json"

#RPI_port = "/dev/ttyTHS1" #GPIO UART Jetson nano
#RPI_port = "/dev/ttyS0"   #GPIO UART Raspberry pi
RPI_port = "/dev/ttyACM0"

limites = [
        [45,135], #desde el centro
        [55,125], #desde rotacion 
        [35,145]  #desde caminata
    ]

pass_n_seq = -1
n_seq = -1
n_step = -1
cam_speed = 0
max_speed = 500
caminata_p_rot = [1000000,0]

modo_mov = -1
estado_p = True
estado_g = True

trigger_on = True
estado_bucle = True
send_redy = False
voltaje = 0.0
corriente = 0.0

joystick_vals = list([0,0,0,0,0,0,0,0,1200,700,700])
with mp.Manager() as manager:
    Hexapod_dic = manager.dict({"ON":0,"X":0,"Y":0,"RX":0,"RY":0,"RZ":0,"DX":0,"DY":0,"H":0,"Z":0,"arco":0})
    Hexapod_dutys = manager.list(np.zeros(18))

with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

hexapod = Hexapod(conf_hexapod)

baud = conf_hexapod["general"]["baudrate"]
Serial = serial.Serial(RPI_port,baud,timeout=0.05)
serial_com = pro_Serial(Serial)

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    sleep(0.1)

serial_com.stop_lidar()

hexapod.set_param_time(0.1,0,[0,0,0],[0,0,0],[0,0,0])
for i in range(6):
    hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)

sleep(1)
hexapod.actualizar_cord()
serial_com.send_duty(hexapod.sv_duty())

sleep(1)
corriente, voltaje,_,_ = serial_com.read_ina_vals()
print(corriente,voltaje)

p1 = mp.Process(target=servo_serial_task, args=(Hexapod_dutys,serial_com))
p2 = mp.Process(target=TCP_task, args=(Hexapod_dic,))

p2.start()

timer_ref = time()
control_timer = time()
INA_timer = time()
while estado_bucle:
    try:
        timer_ref = time()
        if(timer_ref-control_timer >= 0.003):
            control_timer = timer_ref
            #actualizacion de servos

            p1.start()
            estado_g,estado_p,_,_,_,_ =hexapod.actualizar_cord()
            p1.join()
            
            dutys = Hexapod.sv_duty()
            for i in range(18):
                Hexapod_dutys[i] = dutys[i]
        
    except KeyboardInterrupt:
        estado_bucle = False
        break
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        estado_g = False
        estado_p = False

    if(Hexapod_dic["ON"]):
        trigger_on = True

        ang, mod = rec_a_pol(Hexapod_dic["X"],Hexapod_dic["Y"],1)
        if(mod > 0.0):
            cam_speed = (mod*max_speed)+30
            ang_abs = abs(ang)

            if(ang_abs > limites[modo_mov][0] and ang_abs < limites[modo_mov][1]):
                modo_mov = 2
                caminata_p_rot[0] = 1000000
                caminata_p_rot[1] = 0

                if(ang > 0):
                    n_seq = 0
                else:
                    n_seq = 1

            else:
                modo_mov = 1
                caminata_p_rot[0] = 0
                caminata_p_rot[1] = 0

                if(ang_abs < 90):
                    n_seq = 3
                else:
                    n_seq = 2
        else:
            n_seq = -1
            modo_mov = 0
            cam_speed = 0
            caminata_p_rot[0] = 0
            caminata_p_rot[1] = 0

        if(n_seq != -1 and n_seq == pass_n_seq):
            if(estado_g):
                if(n_seq >= 0):
                    hexapod.polar_set_step_caminata(
                            n_sec=n_seq,
                            n_step=n_step,
                            dis_arco=Hexapod_dic["arco"],
                            z=Hexapod_dic["Z"],
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
            pass_n_seq = n_seq
            n_step = 0
            for i in range(6):
                hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)
        
        if(n_seq >= -1):
            hexapod.set_param_speed(100,20,Hexapod_dic["H"],None,None,
                [
                    Hexapod_dic["DX"],
                    Hexapod_dic["DY"],
                    0.0
                ])
            hexapod.set_param_time(0.1,None,
                [
                    Hexapod_dic["RX"],
                    Hexapod_dic["RY"],
                    Hexapod_dic["RZ"],
                ],[0.0,0.0,0.0],
                )
    else:
        if(trigger_on):
            trigger_on = False
            for i in range(6):
                hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)

            hexapod.set_param_time(1,0,[0,0,0],[0,0,0],[0,0,0])


