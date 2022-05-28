import json
import os
import serial
from time import sleep, time
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import math
import numpy as np


secuencia = [
    [#secuencia[0] baile 2
        "baile",
        [
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,  -5.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [  20.0,   0.0,   0.0], #[8] desplazamiento simple
                [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],[
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0, -20.0], #[8] desplazamiento simple
                [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],[
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   5.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [ -20.0,   0.0,   0.0], #[8] desplazamiento simple
                [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],[
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0, -20.0], #[8] desplazamiento simple
                [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ]
        ]
    ],

    [#secuencia[1] golpe base
        "golpe derecha base",
        [
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  80.0, 335.0,  80.0], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  80.0, 450.0, 180.0], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.1
            ],
        ],
    ],
    [#secuencia[1] golpe base
        "golpe izquierda base",
        [
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [ -80.0, 450.0, 180.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.1
            ],
        ],
    ],
    [#secuencia[2] golpe 1 2
        "golpe 1 2",
        [
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  80.0, 335.0,  80.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  80.0, 450.0, 100.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.1
            ],
            [
                [  80.0, 335.0,  80.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 450.0, 100.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.1
            ],
            [
                [  80.0, 335.0,  80.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
            [
                [  80.0, 400.0, 100.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.1,   #[11] step time
                0.0
            ],
            [
                [  80.0, 420.0, 250.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 335.0,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.1
            ],
            [
                [  None,  None,  80.0], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  80.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                0.0
            ],
        ],
    ],
    [#secuencia[3] embestida
        "embestida",
        [
            [
                [  None,  None,  None], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  None], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                1.0
            ],
            [
                [  80.0, 300.0,  70.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 300.0,  70.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                1.0
            ],
            [
                [  80.0, 300.0,  70.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 300.0,  70.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0, 50.0,   0.0], #[8] desplazamiento simple
                [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.5,   #[11] step time
                1.2
            ],
            [
                [  80.0, 300.0,  70.0], #[0] pie 1
                [  None,  50.0,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  50.0,  None], #[4] pie 5
                [ -80.0, 300.0,  70.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0, 50.0,   0.0], #[8] desplazamiento simple
                [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.5,   #[11] step time
                1.2
            ],
            [
                [  None,  None,  70.0], #[0] pie 1
                [  None,  None,  None], #[1] pie 2
                [  None,  None,  None], #[2] pie 3
                [  None,  None,  None], #[3] pie 4
                [  None,  None,  None], #[4] pie 5
                [  None,  None,  70.0], #[5] pie 6
                [   0.0,   0.0,   0.0], #[6] Rotaciones
                [   0.0,   0.0,   0.0], #[7] punto de rotacion
                [   0.0,   0.0,   0.0], #[8] desplazamiento simple
                [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
                80.0, #[10] H 
                0.3,   #[11] step time
                1.0
            ],
        ],
    ]
]

h = 80
z = 50
arco = 70
n_rep = 2
low_speed = 300
high_speed = 800
caminata_p_rot = [1000000,0]
caminata_giro_izq = [500,0]
caminata_giro_der = [-500,0]
giro_des_frontal = [0,500]
giro_des_trasero = [0,-500]

#json_PATH = '/home/rodrigo/hexapod/jetson_nano/ajustes_hexapod.json'
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

print("iniciado")
sleep(1)

def truncar(val, val_min, val_max):
    if(val < val_min):
        return val_min
    elif(val > val_max):
        return val_max
    elif(val is None):
        return val_min

    return val


def bucle_movimiento():
    estado = False
    while(not estado):
        estado,_,_,_,_,_ =hexapod.actualizar_cord()
        serial_com.send_duty(hexapod.sv_duty())

def ejecutar_secuencia(n_seq:int,rep:int):
    hexapod.reset_dt()

    for i in range(6):
        hexapod.lineal_set_target_time(i,secuencia[n_seq][1][0][i],1,False)
    bucle_movimiento()

    hexapod.set_param_time(1,h=secuencia[n_seq][1][0][10])
    bucle_movimiento()

    hexapod.reset_dt()
    for n in range(rep):
        for x in secuencia[n_seq][1]:
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


while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    sleep(0.1)

for seg in secuencia:
    for step in seg[1]:
        for index in range(6):
            for art in range(3):
                if(step[index][art] is None):
                    step[index][art] = hexapod.Pierna_param[index][3][art]

hexapod.reset_dt()

estado = True
while estado:
    print("acciones posibles:")
    print("0) cerrar codigo")
    print("5) home ")
    print("--------")
    
    print("--------")
    print("10) baile ")
    
    try:
        accion = int(input("ingrese el numero de accion: "))

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
            ejecutar_secuencia(0,10)

        #golpe base
        if(accion == 2):
            ejecutar_secuencia(1,1)
        
        if(accion == 3):
            ejecutar_secuencia(2,1)
        
        if(accion == 4):
            ejecutar_secuencia(3,1)
        
        if(accion == 6):
            ejecutar_secuencia(4,1)

        elif(accion == 5):
            hexapod.reset_dt()
            hexapod.set_param_time(1,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
            for i in range(6):
                hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)
            bucle_movimiento()

        if(accion != 0 and accion != 5):
            hexapod.set_param_time(0.1,h=h,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
            for i in range(6):
                hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)
            bucle_movimiento()
    except:
        hexapod.reset_dt()
        hexapod.set_param_time(1,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
        for i in range(6):
            hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)
        bucle_movimiento()
