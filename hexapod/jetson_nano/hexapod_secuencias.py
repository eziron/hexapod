import json
import os
import serial
from time import sleep, time
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import math
import numpy as np
#import open3d as o3d
from datetime import datetime

#pip install pyserial

secuencia = [
    [#secuencia[0] Baile 1
        [
            [ 100.0, 350.0, 100.0], #[0] pie 1
            [ 250.0, 100.0,   0.0], #[1] pie 2
            [ 210.0,-285.0,   0.0], #[2] pie 3
            [-210.0,-285.0,   0.0], #[3] pie 4y 
            [-250.0, 100.0,   0.0], #[4] pie 5
            [-100.0, 350.0, 100.0], #[5] pie 6
            [   0.0,   0.0,  -5.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [  20.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.25,   #[11] step time
            0.0
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
            0.3,   #[11] step time
            0.0
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
            0.25,   #[11] step time
            0.0
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
            0.3,   #[11] step time
            0.0
        ]
    ],
    [#secuencia[1] baile 2
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,  -7.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [  30.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            70.0, #[10] H 
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
            [   0.0,   0.0, -30.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            70.0, #[10] H 
            0.3,   #[11] step time
            0.0
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   7.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [ -30.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            70.0, #[10] H 
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
            [   0.0,   0.0, -30.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            70.0, #[10] H 
            0.3,   #[11] step time
            0.0
        ]
    ],
    [#secuencia[2] vigilancia / movimiento random
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0,   #[11] step time
            1.0
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [ -10.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0,   #[11] step time
            1.0
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [ -10.0,   0.0,  15.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            1.0,   #[11] step time
            1.0
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [ -10.0,   0.0, -15.0], #[6] Rotaciones
            [   0.0,-120.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            2.0,   #[11] step time
            1.0
        ]
        
    ],
    [#secuencia[3] salto simple
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0, -10.0,   0.0], #[6] Rotaciones
            [  50.0,   0.0,   0.0], #[7] punto de rotacion
            [  50.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            100.0, #[10] H 
            0.8,   #[11] step time
            0.0
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,  10.0,   0.0], #[6] Rotaciones
            [ -50.0,   0.0,   0.0], #[7] punto de rotacion
            [ -50.0,   0.0,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            100.0, #[10] H 
            0.8,   #[11] step time
            0.0
        ]
    ],
    [#secuencia[4] salto PRO
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
    ],
    [#secuencia[5] Prueba de carga
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [   0.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            50.0, #[10] H 
            1.0, #[11] step time
            1.0  #[12] time sleep
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [   0.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            210.0, #[10] H 
            5.0, #[11] step time
            2.0  #[12] time sleep
        ],[
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [   0.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            0.0, #[10] H 
            5.0, #[11] step time
            1.0  #[12] time sleep
        ],
    ],
    [#secuencia[6] baile lateral
        [
            [ 300.0 , 165.0 ,   0.0], #[0] pie 1
            [ 350.0 ,   0.0 ,   0.0], #[1] pie 2
            [ 300.0 ,-165.0 ,   0.0], #[2] pie 3
            [-300.0 ,-165.0 ,   0.0], #[3] pie 4
            [-350.0 ,   0.0 ,   0.0], #[4] pie 5
            [-300.0 , 165.0 ,   0.0], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [   0.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            90.0, #[10] H 
            1.0, #[11] step time
            5.0  #[12] time sleep
        ],[
            [ 300.0 , 165.0 ,   0.0], #[0] pie 1
            [ 350.0 ,   0.0 ,   0.0], #[1] pie 2
            [ 300.0 ,-165.0 ,   0.0], #[2] pie 3
            [-300.0 ,-165.0 ,   0.0], #[3] pie 4
            [-350.0 ,   0.0 ,   0.0], #[4] pie 5
            [-300.0 , 165.0 ,   0.0], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [ 80.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            90.0, #[10] H 
            1.0, #[11] step time
            0.0  #[12] time sleep
        ],[
            [ 300.0 , 165.0 ,   0.0], #[0] pie 1
            [ 350.0 ,   0.0 ,   0.0], #[1] pie 2
            [ 300.0 ,-165.0 ,   0.0], #[2] pie 3
            [-300.0 ,-165.0 ,   0.0], #[3] pie 4
            [-350.0 ,   0.0 ,   0.0], #[4] pie 5
            [-300.0 , 165.0 ,   0.0], #[5] pie 6
            [   0.0 ,   0.0 ,   0.0], #[6] Rotaciones
            [   0.0 ,   0.0 ,   0.0], #[7] punto de rotacion
            [-80.0 ,   0.0 ,   0.0], #[8] desplazamiento simple
            [True,True,True,True,True,True],#[9] desplazamientos y rotaciones
            90.0, #[10] H 
            1.0, #[11] step time
            0.0  #[12] time sleep
        ],
    ],
    [#secuencia[7] golpe base
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
    [#secuencia[8] golpe base
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
    [#secuencia[9] golpe 1 2
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
    [#secuencia[10] embestida
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
            0.1,   #[11] step time
            0.0
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  10.0], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  10.0], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None, 120.0,  10.0], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 120.0,  10.0], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None, 120.0,  None], #[1] pie 2
            [  None,  None,  10.0], #[2] pie 3
            [  None,  None,  10.0], #[3] pie 4
            [  None, 120.0,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None, 120.0,  None], #[1] pie 2
            [  None,-150.0,  10.0], #[2] pie 3
            [  None,-150.0,  10.0], #[3] pie 4
            [  None, 120.0,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  10.0, None,  70.0], #[0] pie 1
            [  None, 120.0,  None], #[1] pie 2
            [  None,-150.0,  None], #[2] pie 3
            [  None,-150.0,  None], #[3] pie 4
            [  None, 120.0,  None], #[4] pie 5
            [ -10.0, None,  70.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.1,   #[11] step time
            0.2
        ],
        [
            [  10.0, None,  70.0], #[0] pie 1
            [  None, 120.0,  None], #[1] pie 2
            [  None,-150.0,  None], #[2] pie 3
            [  None,-150.0,  None], #[3] pie 4
            [  None, 120.0,  None], #[4] pie 5
            [ -10.0, None,  70.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,-250.0,   0.0], #[8] desplazamiento simple
            [False,True,True,True,True,False],#[9] desplazamientos y rotaciones
            80.0, #[10] H 
            0.4,   #[11] step time
            0.2
        ],
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
            0.1,   #[11] step time
            0.0
        ],
    ],
]


h = 120
z = 70
arco = 70
n_rep = 2
low_speed = 300
high_speed = 800
caminata_p_rot = [1000000,0]
caminata_giro_izq = [500,0]
caminata_giro_der = [-500,0]
giro_des_frontal = [0,500]
giro_des_trasero = [0,-500]

samp_PATH = "/home/rodrigo/hexapod/PC/samples/"
#samp_PATH = "/home/pi/hexapod/PC/samples/"
#json_PATH = '/home/rodrigo/hexapod/jetson_nano/ajustes_hexapod.json'
json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
#json_PATH = "/home/pi/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

#port = "/dev/ttyTHS1" #GPIO UART Jetson nano
#port = "/dev/ttyS0"   #GPIO UART Raspberry pi
port = "/dev/ttyACM0"  #USB

baud = conf_hexapod["general"]["baudrate"]

while True:
    try:
        print("Iniciando Serial")
        #Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
        Serial = serial.Serial(port,baud,timeout=0.05)
        os.system("""echo 102938 | sudo renice -20 -p $(pgrep "python3")""")

        print("Serial Iniciado")
        break
    except:
        print("Error al inisiar el serial")
        #os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
        os.system("echo 102938 | sudo -S chmod 666 /dev/ttyS0")

    

serial_com = pro_Serial(Serial)

hexapod = Hexapod(conf_hexapod)

for seg in secuencia:
    for step in seg:
        for index in range(6):
            for art in range(3):
                if(step[index][art] is None):
                    step[index][art] = hexapod.Pierna_param[index][3][art]

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
        hexapod.lineal_set_target_time(i,secuencia[n_seq][0][i],1,False)
    bucle_movimiento()

    hexapod.set_param_time(1,h=secuencia[n_seq][0][10])
    bucle_movimiento()

    hexapod.reset_dt()
    for n in range(rep):
        for x in secuencia[n_seq]:
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

def ejecutar_caminata(n_seqf,n_repf=5,speedf=300,hf=80,zf=50,arcof=70,cent_rotf = [0,0]):
    hexapod.reset_dt()

    hexapod.set_param_time(0.5,h=hf)
    bucle_movimiento()

    for n in range(n_repf):
        for n_step in range(6):
            hexapod.polar_set_step_caminata(
                n_sec=n_seqf,
                n_step=n_step,
                dis_arco=arcof,
                z=zf,
                lineal_speed=speedf,
                cord_r=cent_rotf,
                doble_cent_r=False,
                r_por_pie=True,
                estado=True
            )
            bucle_movimiento()
"""
def get_lidar_sample(mode,sample_time,speed1,speed2):
    serial_com.stop_lidar()
    sleep(0.5)
    if(Serial.in_waiting > 0):
        C = Serial.read(Serial.in_waiting)
    
    if(mode > 0):
        if(mode == 1):
            max_rate = 2000
        elif(mode == 2):
            max_rate = 4000
        else:
            max_rate = 8000

        samp_array = np.zeros((round(max_rate*sample_time),3),dtype=np.float64)
        n_samp = 0
        if(serial_com.star_lidar(mode,speed1,speed2)):
            time_ref = time()
            while (time() - time_ref < sample_time):
                samp = serial_com.read_lidar()
                if(not (samp is None)):
                    samp_array[n_samp][0] = samp[0]
                    samp_array[n_samp][1] = samp[1]
                    samp_array[n_samp][2] = samp[2]
                    n_samp+=1

                    if(n_samp%1000 == 0):
                        print(time() - time_ref,n_samp)
            
            print(samp_array[:n_samp])
            print(n_samp)
            print(n_samp/sample_time)

            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(samp_array[:n_samp])

            dt_string = datetime.now().strftime("lidar_sample-%d%m%Y-%H%M%S.ply")
            o3d.io.write_point_cloud(samp_PATH+dt_string, pcd)
        else:
            print("ERROR al inciar el lidar")
    

        serial_com.stop_lidar()
"""

print("Prueba de PING")
while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    #Serial.close()
    #sleep(1)
    #Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
    #serial_com = pro_Serial(Serial)
    sleep(1)
print("Prueba pasada")
hexapod.reset_dt()
serial_com.stop_lidar()



estado = True
while estado:
    print("acciones posibles:")
    print("0) cerrar codigo")
    print("--------")
    print("8) caminata hacia adelante")
    print("2) caminata hacia atras")
    print("88) caminata rapida hacia adelante")
    print("22) caminata rapida hacia atras")
    print("888) caminata larga hacia adelante")
    print("222) caminata larga hacia atras")
    print("--------")
    print("4) giro hacia la izquierda")
    print("6) giro hacia la derecha")
    print("44) giro rapido hacia la izquierda")
    print("66) giro rapido hacia la derecha")
    print("--------")
    print("9) caminata hacia adelante con giro a la izquierda")
    print("7) caminata hacia adelante con giro a la derecha")
    print("3) caminata hacia atras con giro a la izquierda")
    print("1) caminata hacia atras con giro a la derecha")
    print("--------")
    print("99) giro descentralizado, frontal derecha")
    print("77) giro descentralizado, frontal izquierda")
    print("33) giro descentralizado, tracera derecha")
    print("11) giro descentralizado, tracera izquierda")
    print("--------")
    print("10) baile 1")
    print("12) baile 2")
    print("13) oversacion")
    print("14) patada derecha")
    print("15) patada izquierda")
    print("17) embestida")
    print("16) 1 2 upper")
    print("18) rotacion")
    #print("19) salto")
    #print("20) test de carga")
    #print("21) baile lateral")
    

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

    #8) caminata hacia adelante")
    elif(accion == 8):
        ejecutar_caminata(0,n_rep,low_speed,h,z,arco,caminata_p_rot)

    #2) caminata hacia atras")
    elif(accion == 2):
        ejecutar_caminata(1,n_rep,low_speed,h,z,arco,caminata_p_rot)

    #88) caminata rapida hacia adelante")
    elif(accion == 88):
        ejecutar_caminata(0,n_rep*2,high_speed,h,z,arco,caminata_p_rot)

    #22) caminata rapida hacia atras")
    elif(accion == 22):
        ejecutar_caminata(1,n_rep*2,high_speed,h,z,arco,caminata_p_rot)

    #888) caminata larga hacia adelante")
    elif(accion == 888):
        ejecutar_caminata(0,n_rep*4,low_speed,h,z,arco,caminata_p_rot)

    #222) caminata larga hacia atras")
    elif(accion == 222):
        ejecutar_caminata(1,n_rep*4,low_speed,h,z,arco,caminata_p_rot)
    
    #4) giro hacia la izquierda")
    elif(accion == 4):
        ejecutar_caminata(2,n_rep,low_speed,h,z,arco,[0,0])
    #6) giro hacia la derecha")
    elif(accion == 6):
        ejecutar_caminata(3,n_rep,low_speed,h,z,arco,[0,0])
    #44) giro rapido hacia la izquierda")
    elif(accion == 44):
        ejecutar_caminata(2,n_rep,high_speed,h,z,arco,[0,0])
    #66) giro rapido hacia la derecha")
    elif(accion == 66):
        ejecutar_caminata(3,n_rep,high_speed,h,z,arco,[0,0])
    
    #9) caminata hacia adelante con giro a la izquierda")
    elif(accion == 9):
        ejecutar_caminata(0,n_rep,low_speed,h,z,arco,caminata_giro_izq)

    #7) caminata hacia adelante con giro a la derecha")
    elif(accion == 7):
        ejecutar_caminata(0,n_rep,low_speed,h,z,arco,caminata_giro_der)

    #3) caminata hacia atras con giro a la izquierda")
    elif(accion == 3):
        ejecutar_caminata(1,n_rep,low_speed,h,z,arco,caminata_giro_izq)

    #1) caminata hacia atras con giro a la derecha")
    elif(accion == 1):
        ejecutar_caminata(1,n_rep,low_speed,h,z,arco,caminata_giro_der)

    #99) giro descentralizado, frontal derecha")
    elif(accion == 99):
        ejecutar_caminata(2,n_rep,low_speed,h,z,arco,giro_des_frontal)

    #77) giro descentralizado, frontal izquierda")
    elif(accion == 77):
        ejecutar_caminata(3,n_rep,low_speed,h,z,arco,giro_des_frontal)

    #33) giro descentralizado, tracera derecha")
    elif(accion == 33):
        ejecutar_caminata(3,n_rep,low_speed,h,z,arco,giro_des_trasero)

    #11) giro descentralizado, tracera izquierda")
    elif(accion == 11):
        ejecutar_caminata(2,n_rep,low_speed,h,z,arco,giro_des_trasero)


    #baile 1
    if(accion == 10):
        ejecutar_secuencia(0,10)

    #baile 2
    elif(accion == 12):
        ejecutar_secuencia(1,10)

    #movimiento random
    elif(accion == 13):
        ejecutar_secuencia(2,1)

    #ataque simple derecha
    elif(accion == 14):
        ejecutar_secuencia(7,1)

    #ataque simple izquierda
    elif(accion == 15):
        ejecutar_secuencia(8,1)

    #ataque 1 2
    elif(accion == 16):
        ejecutar_secuencia(9,1)

    #embestida
    elif(accion == 17):
        ejecutar_secuencia(10,1)


    #Rotacion
    elif(accion == 18):
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

            hexapod.actualizar_cord()
            serial_com.send_duty(hexapod.sv_duty())

        hexapod.set_param_time(1,rot=[math.sin(ang)*max_ang,math.cos(ang)*max_ang,0])
        bucle_movimiento()

    #salto
    #elif(accion == 19):
    #    ejecutar_secuencia(3,1)

    #prueba de carga
    #elif(accion == 20):
    #    ejecutar_secuencia(5,1)

    #baile lateral
    #elif(accion == 21):
    #    ejecutar_secuencia(6,2)

    elif(accion == 5):
        hexapod.reset_dt()
        hexapod.set_param_time(1,h=0,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
        for i in range(6):
            hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)
        bucle_movimiento()
    """
    elif(accion == 55):
        get_lidar_sample(1,15,50,200)
    
    elif(accion == 555):
        get_lidar_sample(2,15,50,200)
    
    elif(accion == 5555):
        get_lidar_sample(3,15,50,200)
"""
    if(accion != 0 and accion != 5):
        hexapod.set_param_time(0.1,h=h,rot=[0,0,0],p_rot=[0,0,0],desp=[0,0,0])
        for i in range(6):
            hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)
        bucle_movimiento()
