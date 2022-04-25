from xbox360controller import Xbox360Controller
from math import atan2, sqrt,degrees
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

star = False
loss_ref = 0

axis_dic = {
    "Lx":0,
    "Ly":0,

    "Lm":0,
    "La":0,

    "Ry":0,
    "Rx":0,

    "Rm":0,
    "Ra":0,

    "Lt":0,
    "Rt":0,
}

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

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))

def on_star_pressed(button):
    global star
    star = not star

def on_axis_L_moved(axis):
    global axis_dic
    axis_dic["Lx"] = round(dead_val_axis(axis.x,30)*800)
    axis_dic["Ly"] = -round(dead_val_axis(axis.y,30)*800)

    ang, mod = rec_a_pol(axis_dic["Lx"],axis_dic["Ly"],800)

    axis_dic["Lm"] = mod
    axis_dic["La"] = ang
    print(axis.name,axis_dic["Lx"],axis_dic["Ly"],axis_dic["Lm"],axis_dic["La"])

def on_axis_R_moved(axis):
    global axis_dic
    axis_dic["Rx"] = round(dead_val_axis(axis.x,30)*10,1)
    axis_dic["Ry"] = -round(dead_val_axis(axis.y,30)*10,1)

    ang, mod = rec_a_pol(axis_dic["Rx"],axis_dic["Ry"],10)

    axis_dic["Rm"] = mod
    axis_dic["Ra"] = ang
    print(axis.name,axis_dic["Rx"],axis_dic["Ry"],axis_dic["Rm"],axis_dic["Ra"])

def on_Rt_moved(axis):
    global axis_dic
    axis_dic["Rt"] = round(dead_val_axis(axis.value,30)*50)

def on_Lt_moved(axis):
    global axis_dic
    axis_dic["Lt"] = round(dead_val_axis(axis.value,30)*50)

def a_map(x:float, in_min:float, in_max:float, out_min:float, out_max:float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

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

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    sleep(0.2)

serial_com.stop_lidar()
serial_com.send_duty(hexapod.sv_duty())

estado_bucle = True
with Xbox360Controller(0, axis_threshold=0) as controller:
    controller.axis_l.when_moved = on_axis_L_moved
    controller.axis_r.when_moved = on_axis_R_moved
    controller.trigger_l.when_moved = on_Lt_moved
    controller.trigger_r.when_moved = on_Rt_moved
    while(estado_bucle):

        try:
            estado_g,estado_p,_,_,_,_ =hexapod.actualizar_cord()
            serial_com.send_duty(hexapod.sv_duty())
        except KeyboardInterrupt:
            estado_bucle = False
        except:
            pass

        if(star):
            if(axis_dic["Lm"] > 10):
                ang_val = axis_dic["La"]
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

                    if(axis_dic["La"] < 0):
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

                cam_speed = axis_dic["Lm"]

            ang_RX =     axis_dic["Rx"]
            ang_RZ =     axis_dic["Ry"]

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
        else:
            for i in range(6):
                hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)

            hexapod.set_param_time(1,0,[0,0,0],[0,0,0],[0,0,0])
