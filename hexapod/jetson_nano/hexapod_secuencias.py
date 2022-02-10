import os
import serial
import struct
from time import sleep, time
from servo_carteciano import Hexapod
import math


secuencia = [
    [
        [#secuencia[0]
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
    ],[#secuencia[1]
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
    ],[#secuencia[2]
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
        
    ],[#secuencia[3]
        [
            [ 250.0, 335.0,   0.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 250.0,-335.0,   0.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-350.0,   0.0,   0.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0, -10.0,   0.0], #[6] Rotaciones
            [  50.0,   0.0,   0.0], #[7] punto de rotacion
            [  50.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            100.0, #[10] H 
            0.8   #[11] step time
        ],
        [
            [ 250.0, 335.0,   0.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 250.0,-335.0,   0.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-350.0,   0.0,   0.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0,  10.0,   0.0], #[6] Rotaciones
            [ -50.0,   0.0,   0.0], #[7] punto de rotacion
            [ -50.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            100.0, #[10] H 
            0.8   #[11] step time
        ]
    ],[
        [
            [ 250.0, 335.0,   0.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 250.0,-335.0,   0.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-350.0,   0.0,   0.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            10.0 #[12] time sleep
        ],[
            [ 250.0, 335.0,  30.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 250.0,-335.0,  30.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-350.0,   0.0,  30.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],[
            [ 145.0, 230.0,  10.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 145.0,-230.0,  10.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-222.0,   0.0,  10.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],
        [
            [ 145.0, 230.0,   0.0], #[0] pie 1
            [ 350.0,   0.0,   0.0], #[1] pie 2
            [ 145.0,-230.0,   0.0], #[2] pie 3
            [-250.0,-335.0,   0.0], #[3] pie 4
            [-222.0,   0.0,   0.0], #[4] pie 5
            [-250.0, 335.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],[
            [ 145.0, 230.0,   0.0], #[0] pie 1
            [ 350.0,   0.0,  30.0], #[1] pie 2
            [ 145.0,-230.0,   0.0], #[2] pie 3
            [-250.0,-335.0,  30.0], #[3] pie 4
            [-222.0,   0.0,   0.0], #[4] pie 5
            [-250.0, 335.0,  30.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],[
            [ 145.0, 230.0,   0.0], #[0] pie 1
            [ 222.0,   0.0,  10.0], #[1] pie 2
            [ 145.0,-230.0,   0.0], #[2] pie 3
            [-145.0,-230.0,  10.0], #[3] pie 4
            [-222.0,   0.0,   0.0], #[4] pie 5
            [-145.0, 230.0,  10.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],[
            [ 145.0, 230.0,   0.0], #[0] pie 1
            [ 222.0,   0.0,   0.0], #[1] pie 2
            [ 145.0,-230.0,   0.0], #[2] pie 3
            [-145.0,-230.0,   0.0], #[3] pie 4
            [-222.0,   0.0,   0.0], #[4] pie 5
            [-145.0, 230.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            150.0, #[10] H 
            1.0,   #[11] step time
            0.0 #[12] time sleep
        ],[
            [ 145.0, 230.0,   0.0], #[0] pie 1
            [ 222.0,   0.0,   0.0], #[1] pie 2
            [ 145.0,-230.0,   0.0], #[2] pie 3
            [-145.0,-230.0,   0.0], #[3] pie 4
            [-222.0,   0.0,   0.0], #[4] pie 5
            [-145.0, 230.0,   0.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            280.0, #[10] H 
            1.0,   #[11] step time
            5.0 #[12] time sleep
        ],
    ]
]
seq = 2

h = 80
z = 50
n_rep = 10

try:
    Serial = serial.Serial("/dev/ttyTHS1",115200,timeout=0.1)
except:
    os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
    Serial = serial.Serial("/dev/ttyTHS1",115200,timeout=0.1)

print("iniciado")
sleep(1)
hexapod = Hexapod()

def truncar(val, val_min, val_max):
    if(val < val_min):
        return val_min
    elif(val > val_max):
        return val_max
    elif(val is None):
        return val_min

    return val

def actualizar_duty():
    duty_vals = hexapod.sv_duty()
    #print(duty_vals)
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




estado = True
while estado:
    print("acciones posibles:")
    print("0) cerrar codigo")
    print("1) baile 1")
    print("2) baile 2")
    print("3) movimiento random")
    print("4) rotacion")
    print("5) caminata")
    print("6) caminata rapida")
    print("7) giro")
    print("8) giro rapido")
    print("9) caminata con giro")
    print("10) giro descentralizado")
    print("11) salto")

    accion = int(input("ingrese el numero de accion: "))
    #accion = 11
    #estado = False
    
    #cerrar codigo
    if(accion == 0):
        estado = False

        hexapod.reset_dt()
        hexapod.set_param_time(1,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
        for i in range(6):
            hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)
        bucle_movimiento()
    
    #baile 1
    if(accion == 1):

        hexapod.reset_dt()
        seq = 3
        for i in range(6):
            hexapod.lineal_set_target_time(i,secuencia[seq][0][i],1,False)
        bucle_movimiento()

        hexapod.set_param_time(1,h=secuencia[seq][0][10])
        bucle_movimiento()

        for n in range(n_rep):
            for x in secuencia[seq]:
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

    #baile 2
    elif(accion == 2):
        hexapod.reset_dt()
        seq = 1
        for i in range(6):
            hexapod.lineal_set_target_time(i,secuencia[seq][0][i],1,False)
        bucle_movimiento()

        hexapod.set_param_time(1,h=secuencia[seq][0][10])
        bucle_movimiento()

        for n in range(n_rep):
            for x in secuencia[seq]:
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

    #movimiento random
    elif(accion == 3):
        hexapod.reset_dt()
        seq = 2
        for i in range(6):
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
        sleep(1)
    #Rotacion
    elif(accion == 4):
        hexapod.reset_dt()

        hexapod.set_param_time(2,h=h)
        bucle_movimiento()

        ang_speed = 3.0
        ang = 0.0
        max_ang = 10.0

        hexapod.set_param_time(1,rot=[0,max_ang,0])
        bucle_movimiento()

        ms = time()
        ms2 = time()
        while (time()-ms < 15):
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

    #caminata
    elif(accion == 5 or accion == 6):
        if(accion == 5):
            vel = 300
            n_rep = 5
        else:
            vel = 800
            n_rep = 10

        hexapod.reset_dt()

        hexapod.set_param_time(2,h=h)
        bucle_movimiento()

        for n in range(n_rep):
            for n_step in range(6):
                hexapod.polar_set_step_caminata(
                    n_sec=0,
                    n_step=n_step,
                    dis_arco=70,
                    z=z,
                    lineal_speed=vel,
                    cord_r=[100000,0],
                    doble_cent_r=False,
                    r_por_pie=True,
                    estado=True
                )
                bucle_movimiento()



    #giro
    elif(accion == 7 or accion == 8):
        if(accion == 7):
            vel = 300
            n_rep = 10
        else:
            vel = 800
            n_rep = 20

        hexapod.reset_dt()
        hexapod.set_param_time(2,h=h)
        bucle_movimiento()

        for n in range(n_rep):
            for n_step in range(6):
                hexapod.polar_set_step_caminata(
                    n_sec=1,
                    n_step=n_step,
                    dis_arco=70,
                    z=z,
                    lineal_speed=vel,
                    cord_r=[0,0],
                    doble_cent_r=False,
                    r_por_pie=True,
                    estado=True
                )
                bucle_movimiento()


    #caminata con giro
    elif(accion == 9):
        hexapod.reset_dt()

        hexapod.set_param_time(2,h=h)
        bucle_movimiento()

        for n in range(5):
            for n_step in range(6):
                hexapod.polar_set_step_caminata(
                    n_sec=0,
                    n_step=n_step,
                    dis_arco=70,
                    z=z,
                    lineal_speed=300,
                    cord_r=[500,0],
                    doble_cent_r=False,
                    r_por_pie=True,
                    estado=True
                )
                bucle_movimiento()

    #giro descentralizado
    elif(accion == 10):
        hexapod.reset_dt()
        hexapod.set_param_time(2,h=h)
        bucle_movimiento()

        for n in range(5):
            for n_step in range(6):
                hexapod.polar_set_step_caminata(
                    n_sec=1,
                    n_step=n_step,
                    dis_arco=70,
                    z=z,
                    lineal_speed=300,
                    cord_r=[0,300],
                    doble_cent_r=False,
                    r_por_pie=True,
                    estado=True
                )
                bucle_movimiento()

    #salto
    elif(accion == 11):
        hexapod.reset_dt()
        seq = 4
        for i in range(6):
            hexapod.lineal_set_target_time(i,secuencia[seq][0][i],1,False)
        bucle_movimiento()

        hexapod.set_param_time(1,h=secuencia[seq][0][10])
        bucle_movimiento()

        sleep(2)
        hexapod.reset_dt()

        for x in secuencia[seq]:
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

            sleep(x[12])


    hexapod.set_param_time(1,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
    for i in range(6):
        hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)
    bucle_movimiento()