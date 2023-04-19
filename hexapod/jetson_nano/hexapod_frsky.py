from xbox360controller import Xbox360Controller
from math import atan2, sqrt,degrees
from time import time, sleep
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import serial
import json
import os


secuencia = [
    [#secuencia[0] -2 Baile 1
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
    [#secuencia[1] -3 baile 2
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
    [#secuencia[2] -4 golpe base
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
            None, #[10] H 
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
            None, #[10] H 
            0.3,   #[11] step time
            0.0
        ],
        [
            [  0.0, 450.0, 180.0], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.1
        ],
    ],
    [#secuencia[3] -5 golpe base
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
            None, #[10] H 
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
            None, #[10] H 
            0.3,   #[11] step time
            0.0
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None,  None,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None,  None,  None], #[4] pie 5
            [   0.0, 450.0, 180.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.1
        ],
    ],
    [#secuencia[4] -6 golpe 1 2
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
            None, #[10] H 
            0.3,   #[11] step time
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
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  None,  None,  None], #[0] pie 1
            [  None, 100.0,  10.0], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  10.0], #[4] pie 5
            [  None,  None,  None], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  None,  None,  80.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [  None,  None,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.1,   #[11] step time
            0.1
        ],
        [
            [  80.0, 335.0,  80.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [ -80.0, 335.0,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.0
        ],
        [
            [  0.0, 450.0, 100.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [ -80.0, 335.0,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.1
        ],
        [
            [  80.0, 335.0,  80.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [   0.0, 450.0, 100.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.1
        ],
        [
            [  80.0, 335.0,  80.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [ -80.0, 335.0,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.3,   #[11] step time
            0.0
        ],
        [
            [   0.0, 400.0, 100.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [ -80.0, 335.0,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
            0.1,   #[11] step time
            0.0
        ],
        [
            [   0.0, 420.0, 250.0], #[0] pie 1
            [  None, 100.0,  None], #[1] pie 2
            [  None,  None,  None], #[2] pie 3
            [  None,  None,  None], #[3] pie 4
            [  None, 100.0,  None], #[4] pie 5
            [ -80.0, 335.0,  80.0], #[5] pie 6
            [   0.0,   0.0,   0.0], #[6] Rotaciones
            [   0.0,   0.0,   0.0], #[7] punto de rotacion
            [   0.0,   0.0,   0.0], #[8] desplazamiento simple
            [False,False,False,False,False,False],#[9] desplazamientos y rotaciones
            None, #[10] H 
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
            None, #[10] H 
            0.3,   #[11] step time
            0.0
        ],
    ],
    [#secuencia[5] -7 embestida
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
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
            None, #[10] H 
            0.1,   #[11] step time
            0.0
        ],
    ],
]
A = (195/64)
B = -(16575/32)
C = (1440875/64)

limites = [
        [45,135], #desde el centro
        [55,125], #desde rotacion 
        [35,145]  #desde caminata
    ]

pass_n_seq = -1
n_seq = -1
n_step = -1
max_step = 6
h = 100
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

belico = False
trigger = True

but_dic = {
    "button_a":0,
    "button_b":0,
    "button_y":0,
    "button_x":0,

    "button_thumb_l":0,
    "button_thumb_r":0,
    "button_trigger_l":0,
    "button_trigger_r":0,
}

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
    #print('Button {0} was pressed',str(button.name))
    but_dic[button.name] = 1


def on_button_released(button):
    #print('Button {0} was released',str(button.name))
    but_dic[button.name] = 0

def on_back_pressed(button):
    global belico
    belico = not belico

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
    #print(axis.name,axis_dic["Lx"],axis_dic["Ly"],axis_dic["Lm"],axis_dic["La"])

def on_axis_R_moved(axis):
    global axis_dic
    axis_dic["Rx"] = round(dead_val_axis(axis.x,30),5)
    axis_dic["Ry"] = -round(dead_val_axis(axis.y,30),5)

    ang, mod = rec_a_pol(axis_dic["Rx"],axis_dic["Ry"],1)

    axis_dic["Rm"] = mod
    axis_dic["Ra"] = ang
    #print(axis.name,axis_dic["Rx"],axis_dic["Ry"],axis_dic["Rm"],axis_dic["Ra"])

def on_Rt_moved(axis):
    global axis_dic
    axis_dic["Rt"] = round(dead_val_axis(axis.value,30)*50)

def on_Lt_moved(axis):
    global axis_dic
    axis_dic["Lt"] = round(dead_val_axis(axis.value,30)*50)

def a_map(x:float, in_min:float, in_max:float, out_min:float, out_max:float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def set_step_secuencia(n):
    global max_step, n_step
    max_step = len(secuencia[n])

    x = secuencia[n][n_step]
    #print(x)
    for i in range(6):
        hexapod.lineal_set_target_time(i,x[i],x[11],x[9][i])
    
    hexapod.set_param_time(
            time=x[11],
            h=x[10],
            rot=x[6],
            p_rot=x[7],
            desp=x[8]
        )

    sleep(x[12])

json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

baud = conf_hexapod["general"]["baudrate"]

while True:
    try:
        Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)

        serial_com = pro_Serial(Serial)
        hexapod = Hexapod(conf_hexapod)

        while(serial_com.ping() is None):
            print("error al conectar con la RPI pico")
            sleep(0.1)

        serial_com.stop_lidar()
        serial_com.send_duty(hexapod.sv_duty())
        break
    except:
        print("Error al inisiar el serial")
        #os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")

#os.system("""echo 102938 | sudo renice -20 -p $(pgrep "python3")""")


for seg in secuencia:
    for step in seg:
        for index in range(6):
            for art in range(3):
                if(step[index][art] is None):
                    step[index][art] = hexapod.Pierna_param[index][3][art]

control_timer = time()

estado_bucle = True
estado_bucle0 = True
while(estado_bucle):
    try:         
        print("A")
        while(True):
            try:
                estado_g,estado_p,_,_,_,_ =hexapod.actualizar_cord()
                serial_com.send_duty(hexapod.sv_duty())
            except KeyboardInterrupt:
                estado_bucle = False
            except:
                estado_g = False
                estado_p = False

            if(star):
                if(but_dic["button_a"]):
                    n_seq = -2
                elif(but_dic["button_b"]):
                    n_seq = -3
                elif(belico and but_dic["button_y"]):
                    n_seq = -6
                elif(belico and but_dic["button_x"]):
                    n_seq = -7
                elif(belico and but_dic["button_trigger_l"]):
                    n_seq = -5
                elif(belico and but_dic["button_trigger_r"]):
                    n_seq = -4
                elif(axis_dic["Lm"] > 0):
                    cam_speed = axis_dic["Lm"]+30
                    ang_val = axis_dic["La"]
                    ang_abs = abs(ang_val)

                    if(ang_abs > limites[modo_mov][0] and ang_abs < limites[modo_mov][1]):
                        modo_mov = 2
                        caminata_p_rot[0] = 1000000
                        caminata_p_rot[1] = 0

                        if(ang_val > 0):
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

                    #print(ang_abs,n_seq,caminata_p_rot)
                else:
                    n_seq = -1
                    modo_mov = 0
                    cam_speed = 0
                    caminata_p_rot[0] = 0
                    caminata_p_rot[1] = 0

                ang_RX =     -axis_dic["Ry"]*8
                ang_RZ =     -axis_dic["Rx"]*22

                if(n_seq != -1 and n_seq == pass_n_seq):
                    if(estado_g):
                        if(n_seq >= 0):
                            max_step = 6
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
                        elif(n_seq == -2):
                            set_step_secuencia(0)
                        elif(n_seq == -3):
                            set_step_secuencia(1)
                        elif(n_seq == -4):
                            set_step_secuencia(2)
                        elif(n_seq == -5):
                            set_step_secuencia(3)
                        elif(n_seq == -6):
                            set_step_secuencia(4)
                        elif(n_seq == -7):
                            set_step_secuencia(5)

                        n_step += 1
                        if(n_step >= max_step):
                            n_step = 0
                else:
                    pass_n_seq = n_seq
                    n_step = 0
                    for i in range(6):
                        hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],0.1)
                
                if(n_seq >= -1):
                    hexapod.set_param_speed(100,20,h)
                    hexapod.set_param_time(0.1,None,[ang_RX,ang_RY,ang_RZ],[0.0,0.0,0.0],[0.0,0.0,0.0])



            else:
                for i in range(6):
                    hexapod.lineal_set_target_time(i,hexapod.Pierna_param[i][3],1)

                hexapod.set_param_time(1,0,[0,0,0],[0,0,0],[0,0,0])
    except KeyboardInterrupt:
        estado_bucle = False
    except:
        pass
