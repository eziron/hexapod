
import serial
import struct
from time import sleep, time
from servo_carteciano import Hexapod


secuencia = [
    [
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
            [   0.0,   0.0, -20.0], #[8] desplazamiento simple
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
            [   0.0,   0.0, -20.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.3   #[11] step time
        ]
    ],[
        [
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [   0.0,   0.0,  -5.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [  20.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.3   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0, -20.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.3   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   5.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [ -20.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.3   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0, -20.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.3   #[11] step time
        ]
    ],[
        [
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [ -10.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [ -10.0,   0.0,  15.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0   #[11] step time
        ],[
            [ 210.0, 285.0,   0.0], #[0] pie 1
            [ 300.0,   0.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4
            [-300.0,   0.0,   0.0], #[4] pie 5
            [-210.0, 285.0,   0.0], #[5] pie 6
            [ -10.0,   0.0, -15.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            2.0   #[11] step time
        ]
        
    ]
]
seq = 2

Serial = serial.Serial("/dev/ttyTHS1",1000000,timeout=0.1)
print("iniciado")
sleep(1)
hexapod = Hexapod()

def actualizar_duty():
    duty_vals = hexapod.sv_duty()
    msg_tx = struct.pack("<"+"H"*18,*duty_vals)
    Serial.write(msg_tx)
    msg_rx = Serial.readline()
    if(msg_rx is None):
        print("raspberry pi pico no responde")

def bucle_movimiento():
    estado = False
    while(not estado):
        estado,_,_,_,_,_ =hexapod.actualizar_cord()
        actualizar_duty()

hexapod.reset_dt()


#secuencias
"""for i in range(6):
    hexapod.lineal_set_target_time(i,secuencia[seq][0][i],1,False)
bucle_movimiento()

hexapod.set_param_time(1,h=secuencia[seq][0][10])
bucle_movimiento()

for n in range(2):
    for x in secuencia[seq]:
        sleep(1)
        hexapod.reset_dt()
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
"""
#caminatas rotacion
hexapod.set_param_time(2,h=80)
bucle_movimiento()

for n in range(10):
    for n_step in range(6):
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

#caminatas lineal
"""hexapod.set_param_time(2,h=80)
bucle_movimiento()

for n in range(10):
    for n_step in range(6):
        hexapod.polar_set_step_caminata(
            n_sec=0,
            n_step=n_step,
            dis_arco=70,
            z=30,
            lineal_speed=300,
            cord_r=[10000,0],
            doble_cent_r=False,
            r_por_pie=True,
            estado=True
        )
        bucle_movimiento()"""


#rotacion
"""
hexapod.set_param_time(2,h=80)
bucle_movimiento()

ang_speed = 3.0
ang = 0.0
max_ang = 10.0

hexapod.set_param_time(1,rot=[0,max_ang,0])
bucle_movimiento()

ms = time()
ms2 = time()
while (time()-ms < 60):
    ang += ang_speed*(time()-ms2)
    ms2 = time()
    hexapod.rotacion[0][0] = math.sin(ang)*max_ang
    hexapod.rotacion[0][1] = math.cos(ang)*max_ang

    hexapod.rotacion[1][0] = hexapod.rotacion[0][0]
    hexapod.rotacion[1][1] = hexapod.rotacion[0][1]

    hexapod.actualizar_rot_desp()
    actualizar_duty()

hexapod.set_param_time(1,rot=[math.sin(ang)*max_ang,math.cos(ang)*max_ang,0])
bucle_movimiento()
"""






hexapod.set_param_time(2,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
for i in range(6):
    hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],2)
bucle_movimiento()