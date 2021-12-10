import struct
from socket import *
import serial
from servo_carteciano import Hexapod
from time import sleep, time

Serial = serial.Serial("/dev/ttyTHS1",1000000,timeout=0.1)
sleep(1)
hexapod = Hexapod()
sleep(0.1)

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('0.0.0.0', 8888))

def actualizar_duty():
    duty_vals = hexapod.sv_duty()
    msg_tx = struct.pack("<"+"H"*18,*duty_vals)
    Serial.write(msg_tx)
    msg_rx = Serial.readline()
    if(msg_rx is None):
        print("raspberry pi pico no responde")

def contrain_circular(val,min_val,max_val):
    if(val < min_val):
        return max_val
    if(val > max_val):
        return min_val

    return val
trig_stop = False
trig_step = True
estado = True
n_step = 0

vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hexapod.reset_dt()
while True:
    data = s.recv(72)
    if not data is None:
        vals = struct.unpack("<"+"l"*18,data)


    if(vals[14] == 0):
        if(not trig_stop):
            for n in range(6):
                hexapod.lineal_set_target_speed(n,hexapod.Pierna_param[n[3]],1000)

            trig_stop = True

    elif(vals[14] == 1):
        if(trig_stop):
            trig_stop = False
            trig_step = False
            n_step = 0
        else:
            if(trig_step and estado):
                n_step = contrain_circular(n_step+1,0,6)
                trig_step = False
            elif((not trig_step) and (not estado)):
                trig_step = True
                
        hexapod.polar_set_step_caminata(
            n_sec=0,
            n_step=n_step,
            dis_arco=70,
            z=30,
            lineal_speed=vals[16],
            cord_r=[10000,0],
            doble_cent_r=False,
            r_por_pie=True,
            estado=estado
        )

    hexapod.set_param_speed(lineal_seed=vals[16],h=vals[17])
    try:
        estado,_,_,_,_,_ =hexapod.actualizar_cord()
    except:
        print("error de calculo en las cordenadas")
    actualizar_duty()


    