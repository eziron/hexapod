from math import atan2, sqrt,degrees
from time import time, sleep
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import serial
import json
import socket
from struct import pack,unpack
import asyncio
from time import time
# Create a TCP/IP socket

server_address = ('0.0.0.0', 10000)
json_PATH = "/home/pi/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
RPI_port = "/dev/ttyS0"

limites = [
        [45,135], #desde el centro
        [55,125], #desde rotacion 
        [35,145]  #desde caminata
    ]

pass_n_seq = -1
n_seq = -1
n_step = -1
max_step = 6
h = 120
z = 60
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

star = False
loss_ref = 0

Hexapod_vals = list([0,0,0,0,0,0,0,0,1200,700,700])
Hexapod_dic = {
    "ON":0,
    "X":0,
    "Y":0,
    "RX":0,
    "RY":0,
    "RZ":0,
    "DX":0,
    "DY":0,
    "H":0,
    "Z":0,
    "arco":0
}
def a_map(x:float, in_min:float, in_max:float, out_min:float, out_max:float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def rec_a_pol(x,y,max_mod):
    mod = min(sqrt((x**2)+(y**2)),max_mod)
    ang = degrees(atan2(y,x))

    return ang,mod

def dead_val_axis(axis_val,dead_val):
    dead_min = -(dead_val/100)
    dead_max =  (dead_val/100)

    if(axis_val >= dead_min and axis_val <= dead_max):
        return 0.0
    elif(axis_val > dead_max):
        return a_map(axis_val,dead_max,1,0,1)
    elif(axis_val < dead_min):
        return a_map(axis_val,-1,dead_min,-1,0)
    else:
        return 0.0


#json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"

with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

baud = conf_hexapod["general"]["baudrate"]

Serial = serial.Serial(RPI_port,baud,timeout=0.05)

serial_com = pro_Serial(Serial)
hexapod = Hexapod(conf_hexapod)

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    sleep(0.1)

serial_com.stop_lidar()
serial_com.send_duty(hexapod.sv_duty())

# Bind the socket to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
trigger_on = True
estado_bucle = True
control_timer = time()
while estado_bucle:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            try:
                estado_g,estado_p,_,_,_,_ =hexapod.actualizar_cord()
                serial_com.send_duty(hexapod.sv_duty())
            except KeyboardInterrupt:
                estado_bucle = False
                break
            except:
                estado_g = False
                estado_p = False

            data = connection.recv(21)
            if(data):
                Hexapod_vals = unpack(">BhhhhhhhHHH",data)
                connection.sendall(bytes([0,127,255,55]))

                Hexapod_dic["ON"] = Hexapod_vals[0]
                Hexapod_dic["X"] = dead_val_axis(Hexapod_vals[1]/1000,5)*500
                Hexapod_dic["Y"] = dead_val_axis(Hexapod_vals[2]/1000,5)*500
                Hexapod_dic["RX"] = Hexapod_vals[3]/100
                Hexapod_dic["RY"] = Hexapod_vals[4]/100
                Hexapod_dic["RZ"] = Hexapod_vals[5]/100
                Hexapod_dic["DX"] = Hexapod_vals[6]/10
                Hexapod_dic["DY"] = Hexapod_vals[7]/10
                Hexapod_dic["H"] = Hexapod_vals[8]/10
                Hexapod_dic["Z"] = Hexapod_vals[9]/10
                Hexapod_dic["arco"] = Hexapod_vals[10]/10
                print(Hexapod_dic)
            if(Hexapod_dic["ON"]):
                trigger_on = True

                ang, mod = rec_a_pol(Hexapod_dic["X"],Hexapod_dic["Y"],500)
                if(mod > 0):
                    cam_speed = mod+30
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
                            max_step = 6
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
                        if(n_step >= max_step):
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

    finally:
        # Clean up the connection
        connection.close()