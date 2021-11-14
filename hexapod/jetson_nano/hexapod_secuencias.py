import serial
import struct
from time import sleep
from servo_carteciano import Hexapod


secuencia = [
    [
        [ 100.0, 350.0, 100.0], #[0] pie 1
        [ 250.0, 100.0,   0.0], #[1] pie 2
        [ 210.0,-285.0,   0.0], #[2] pie 3
        [-210.0,-285.0,   0.0], #[3] pie 4
        [-250.0, 100.0,   0.0], #[4] pie 5
        [-100.0, 350.0, 100.0], #[5] pie 6
        [   0.0,   0.0,  -5.0], #[6] Rotaciones
        [   0.0,   0.0,   0.0], #[7] punto de rotacion
        [  20.0,   0.0,   0.0], #[8] desplazamiento simple
        [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
        80.0, #[10] H 
        0.25   #[11] step time
    ],[
        [ 100.0, 350.0, 100.0], #[0] pie 1
        [ 250.0, 100.0,   0.0], #[1] pie 2
        [ 210.0,-285.0,   0.0], #[2] pie 3
        [-210.0,-285.0,   0.0], #[3] pie 4
        [-250.0, 100.0,   0.0], #[4] pie 5
        [-100.0, 350.0, 100.0], #[5] pie 6
        [   0.0,   0.0,   0.0], #[6] Rotaciones
        [   0.0,   0.0,   0.0], #[7] punto de rotacion
        [   0.0,   0.0,  20.0], #[8] desplazamiento simple
        [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
        80.0, #[10] H 
        0.3   #[11] step time
    ],[
        [ 100.0, 350.0, 100.0], #[0] pie 1
        [ 250.0, 100.0,   0.0], #[1] pie 2
        [ 210.0,-285.0,   0.0], #[2] pie 3
        [-210.0,-285.0,   0.0], #[3] pie 4
        [-250.0, 100.0,   0.0], #[4] pie 5
        [-100.0, 350.0, 100.0], #[5] pie 6
        [   0.0,   0.0,   5.0], #[6] Rotaciones
        [   0.0,   0.0,   0.0], #[7] punto de rotacion
        [ -20.0,   0.0,   0.0], #[8] desplazamiento simple
        [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
        80.0, #[10] H 
        0.25   #[11] step time
    ],[
        [ 100.0, 350.0, 100.0], #[0] pie 1
        [ 250.0, 100.0,   0.0], #[1] pie 2
        [ 210.0,-285.0,   0.0], #[2] pie 3
        [-210.0,-285.0,   0.0], #[3] pie 4
        [-250.0, 100.0,   0.0], #[4] pie 5
        [-100.0, 350.0, 100.0], #[5] pie 6
        [   0.0,   0.0,   0.0], #[6] Rotaciones
        [   0.0,   0.0,   0.0], #[7] punto de rotacion
        [   0.0,   0.0,  20.0], #[8] desplazamiento simple
        [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
        80.0, #[10] H 
        0.3   #[11] step time
    ]
]

Serial = serial.Serial("/dev/ttyTHS1",1000000,timeout=0.1)
sleep(1)
hexapod = Hexapod()

def bucle_movimiento():
    estado = False
    while(not estado):
        estado,_,_,_,_,_ =hexapod.actualizar_cord()
        duty_vals = hexapod.sv_duty()
        msg_tx = struct.pack("<"+"H"*18,*duty_vals)
        Serial.write(msg_tx)
        msg_rx = Serial.readline()
        if(msg_rx is None):
            print("raspberry pi pico no responde")

hexapod.reset_dt()

for i in range(6):
    hexapod.lineal_set_target_time(i,secuencia[0][i],1,False)
bucle_movimiento()

hexapod.set_param_time(1,h=secuencia[0][10])
bucle_movimiento()

for n in range(30):
    for x in secuencia:
        for i in range(6):
            hexapod.lineal_set_target_time(i,x[i],x[11],x[9][i])
        
        hexapod.set_param_time(
                time=x[11],
                h=x[10],
                rot=x[6],
                p_rot=x[7],
                desp=x[8]
            )
        
        bucle_movimiento()


"""for n in range(10):
    for n_step in range(6):
        #n_step = int(input("n_step:"))
        hexapod.polar_set_step_caminata(
            n_sec=1,
            n_step=n_step,
            dis_arco=70,
            z=30,
            lineal_speed=300,
            cord_r=[0,0],
            doble_cent_r=False,
            r_por_pie=True,
            estado=True
        )
        bucle_movimiento()
"""

hexapod.set_param_time(2,h=0)
bucle_movimiento()