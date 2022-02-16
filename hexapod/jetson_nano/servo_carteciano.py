import math
from time import sleep, time

from pandas import array

class Hexapod():
    H = [20.0 ,20.0 ,0.0 ]

    delta_time = [0.0,0.0]

    servo_param = [
        #[n][0] = duty_us a 90gr
        #[n][1] = angulo normal = True ; angulo inverso = False
        #[n][2] = angulo de desfase
        #[n][3] = parametros de una ecuacion lineal [m,A] , donde x es el
        #[n][4] = angulos limite, para 500us y 2500us
        [2380,True , -90, [0,0],[0,0]], #[0]  - N    P6 sv2
        [1520,True , 135, [0,0],[0,0]], #[1]  - N    P6 sv0
        [1990,False,   0, [0,0],[0,0]], #[2]  - inv  P5 sv1
        [2170,True , -90, [0,0],[0,0]], #[3]  - N    P5 sv2
        [1540,True ,  90, [0,0],[0,0]], #[4]  - N    P5 sv0
        [2070,False,   0, [0,0],[0,0]], #[5]  - inv  P4 sv1
        [2322,True , -90, [0,0],[0,0]], #[6]  - N    P4 sv2
        [1540,True ,  45, [0,0],[0,0]], #[7]  - N    P4 sv0
        [1510,False,  45, [0,0],[0,0]], #[8]  - inv  P3 sv0
        [678 ,False, -90, [0,0],[0,0]], #[9]  - inv  P3 sv2
        [930 ,True ,   0, [0,0],[0,0]], #[10] - N    P3 sv1
        [1450,False,  90, [0,0],[0,0]], #[11] - inv  P2 sv0
        [678 ,False, -90, [0,0],[0,0]], #[12] - inv  P2 sv2
        [1020,True ,   0, [0,0],[0,0]], #[13] - N    P2 sv1
        [1550,False, 135, [0,0],[0,0]], #[14] - inv  P1 sv0
        [850 ,False, -90, [0,0],[0,0]], #[15] - inv  P1 sv2
        [1930,False,   0, [0,0],[0,0]], #[16] - inv  P6 sv1
        [1000,True ,   0, [0,0],[0,0]], #[17] - N    P1 sv1
    ]

    Pierna_param = [
        #[n][0][0:2] numero del servo en el eje [sv0, sv1, sv2]
        #[n][1][0:1] cordenadas [x,y] del origen de la pierna
        #[n][2] eje X inverso
        #[n][3] cordenadas de origen movimiento
        [[14, 17, 15], [  80.0   , 165.0  ], True  ,[ 250.0, 335.0, 0.0]], #[0]
        [[11, 13, 12], [ 130.0   ,   0.0  ], True  ,[ 350.0,   0.0, 0.0]], #[1]
        [[ 8, 10,  9], [  80.0   ,-165.0  ], True  ,[ 250.0,-335.0, 0.0]], #[2]
        [[ 7,  5,  6], [ -80.0   ,-165.0  ], False ,[-250.0,-335.0, 0.0]], #[3]
        [[ 4,  2,  3], [-130.0   ,   0.0  ], False ,[-350.0,   0.0, 0.0]], #[4]
        [[ 1, 16,  0], [ -80.0   , 165.0  ], False ,[-250.0, 335.0, 0.0]], #[5]
        [71.0, 110.0, 180.0]  #[6] distancias entre ejes, m0, m1, m2
    ]
    #[0][n][xyz] Cordenadas actuales
    #[1][n][xyz] Cordenadas target
    #[2][n][xyz] velocidades
    cord_global = [
                [0.0 ,0.0 ,0.0 ],
                [0.0 ,0.0 ,0.0 ],
                [0.0 ,0.0 ,0.0 ],
                [0.0 ,0.0 ,0.0 ],
                [0.0 ,0.0 ,0.0 ],
                [0.0 ,0.0 ,0.0 ]
            ]
    

    #[n] = True: para movimiento lineal, False: para movimiento circular
    modo_movimiento = [True,True,True,True,True,True]

    #[0][n][xyz] Cordenadas target
    #[1][n][xyz] velocidades
    movimiento_lineal=[
        [
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ]
        ],[
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ],
            [0.0 ,0.0 ,0.0 ]
        ]
    ]

    #movimiento_circular[0][n] angulo actual
    #movimiento_circular[1][n] angulo target
    #movimiento_circular[2][n] velocidad angular
    #movimiento_circular[3][n] radio
    #movimiento_circular[4][n] Z target
    #movimiento_circular[5][n] velocidad lineal Z
    #movimiento_circular[6][n][XY] cordenadas de centro de la circunferencia actual
    #movimiento_circular[6][n][XY] cordenadas de centro de la circunferencia pasado
    movimiento_circular=[
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ],
        [
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ],[
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ]
    ]

    
    estado_rot_desp = [True,True,True,True,True,True]
    rotacion = [
            [0.0,0.0,0.0], #[0] actual
            [0.0,0.0,0.0], #[1] target
            [0.0,0.0,0.0]  #[2] velocidad
        ]
    punto_rotacion = [
            [0.0,0.0,0.0], #[0] actual
            [0.0,0.0,0.0], #[1] target
            [0.0,0.0,0.0]  #[2] velocidad
        ]
    desplazamiento_cuerpo = [
            [0.0,0.0,0.0], #[0] actual
            [0.0,0.0,0.0], #[1] target
            [0.0,0.0,0.0]  #[2] velocidad
        ]

    

    all_duty_us = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]

#secuencias_caminata[n][0] = posicion
#secuencias_caminata[n][1] = altura
    secuencias_caminata = [
        [#secuencia caminata
            [#paso 1
                [  None, None, None, None, None, None], 
                [     0,    1,    0,    1,    0,    1],
            ],[#paso 2
                [    -1,    1,   -1,    1,   -1,    1], 
                [  None, None, None, None, None, None],
            ],[#paso 3
                [  None, None, None, None, None, None], 
                [     0,    0,    0,    0,    0,    0],
            ],[#paso 4
                [  None, None, None, None, None, None], 
                [     1,    0,    1,    0,    1,    0],
            ],[#paso 5
                [     1,   -1,    1,   -1,    1,   -1],
                [  None, None, None, None, None, None],
            ],[#paso 6
                [  None, None, None, None, None, None], 
                [     0,    0,    0,    0,    0,    0],
            ]
        ],[#secuencia giro
            [#paso 1
                [  None, None, None, None, None, None], 
                [     0,    1,    0,    1,    0,    1],
            ],[#paso 2
                [    -1,    1,   -1,   -1,    1,   -1], 
                [  None, None, None, None, None, None],
            ],[#paso 3
                [  None, None, None, None, None, None], 
                [     0,    0,    0,    0,    0,    0],
            ],[#paso 4
                [  None, None, None, None, None, None], 
                [     1,    0,    1,    0,    1,    0],
            ],[#paso 5
                [     1,   -1,    1,    1,   -1,    1], 
                [  None, None, None, None, None, None],
            ],[#paso 0
                [  None, None, None, None, None, None], 
                [     0,    0,    0,    0,    0,    0],
            ]
        ]
    ]


    def __init__(self):
        for n in range(len(self.servo_param)):
            if(self.servo_param[n][1]):
                self.servo_param[n][3][0] = 1000/90
            else:
                self.servo_param[n][3][0] = -1000/90
            
            self.servo_param[n][3][1] = self.servo_param[n][0]-self.servo_param[n][3][0]*90

            self.servo_param[n][4][0] = (500-self.servo_param[n][3][1])/self.servo_param[n][3][0]
            self.servo_param[n][4][1] = (2500-self.servo_param[n][3][1])/self.servo_param[n][3][0]

        for n in range(6):
            self.cord_global[n][0] = self.Pierna_param[n][3][0]
            self.cord_global[n][1] = self.Pierna_param[n][3][1]
            self.cord_global[n][2] = self.Pierna_param[n][3][2]
            self.set_cord(n,self.cord_global[n])

            self.movimiento_circular[0][n] = self.angulo_positivo(math.atan2(self.Pierna_param[n][3][1],self.Pierna_param[n][3][0]))
            self.movimiento_circular[1][n] = self.movimiento_circular[0][n]
            self.movimiento_circular[3][n] = self.dis_PaP_R2([0,0],[self.Pierna_param[n][3][0],self.Pierna_param[n][3][1]]) 

        sleep(1)
    
    def angulo_positivo(self,ang: float,rad: bool =True):
        if(ang < 0):
            if(rad):
                return (2*math.pi) + ang
            else:
                return 360.0 + ang
        else:
            return ang
            

    #convierte cordenadas globales en cordenadas locales para cada pierna
    def global_to_local(self,index: int,cord: list):
        if(self.Pierna_param[index][2]):
            X = cord[0]-self.Pierna_param[index][1][0]
        else:
            X = self.Pierna_param[index][1][0]-cord[0]
        
        Y = cord[1]-self.Pierna_param[index][1][1]
        Z = cord[2]

        return [X,Y,Z]

    #convierte cordenadas locales en cordenadas globales para cada pierna
    def loca_to_global(self,index: int,cord: list):
        if(self.Pierna_param[index][2]):
            X = self.Pierna_param[index][1][0]+cord[0]
        else:
            X = -cord[0]+self.Pierna_param[index][1][0]
        
        Y = self.Pierna_param[index][1][1]+cord[1]
        Z = cord[2]

        return [X,Y,Z]

    #limita un valor en un intervalo
    def contrain(self,value,min_val,max_val):
        if(value > max_val):
            return max_val
        if(value < min_val):
            return min_val
        return value

    #fija el largo de pulso de PWM de una mierna
    def set_duty_pierna(self,index:int,duty_0:int,duty_1:int,duty_2:int):
        self.all_duty_us[self.Pierna_param[index][0][0]] = self.contrain(duty_0,500,2500)
        self.all_duty_us[self.Pierna_param[index][0][1]] = self.contrain(duty_1,500,2500)
        self.all_duty_us[self.Pierna_param[index][0][2]] = self.contrain(duty_2,500,2500)

    #actualiza el largo de pulso PWM de todo el robot
    def sv_duty(self):
        return self.all_duty_us

    #distancia entre dos puntos en R2
    def dis_PaP_R2(self,Pi=[0,0], Pf=[]):
        return math.sqrt(math.pow(Pf[0]-Pi[0],2)+math.pow(Pf[1]-Pi[1],2))

    def hipotenusa_R2(self,X,Y):
        return math.sqrt(math.pow(X,2)+math.pow(Y,2))

    def hipotenusa_R3(self,X,Y,Z):
        return math.sqrt(math.pow(X,2)+math.pow(Y,2)+math.pow(Z,2))

    #convierte el angulo del servo en su equivalente en largo de pulso PWM
    def ang_a_duty(self,index_sv:int,ang:float)->int:
        if(self.servo_param[index_sv][1]):
            ang = self.contrain(ang+self.servo_param[index_sv][2],self.servo_param[index_sv][4][0],self.servo_param[index_sv][4][1])
        else:
            ang = self.contrain(ang+self.servo_param[index_sv][2],self.servo_param[index_sv][4][1],self.servo_param[index_sv][4][0])
        
        duty = self.servo_param[index_sv][3][0]*ang+self.servo_param[index_sv][3][1]
        return round(duty)
    
    #fija y convierte el angulo de una pierna a sus equivalentes en largo de pulso PWM
    def set_ang_pierna(self,index,ang0,ang1,ang2):
        n_sv0 = self.Pierna_param[index][0][0]
        n_sv1 = self.Pierna_param[index][0][1]
        n_sv2 = self.Pierna_param[index][0][2]

        duty_sv0 = self.ang_a_duty(n_sv0,ang0)
        duty_sv1 = self.ang_a_duty(n_sv1,ang1)
        duty_sv2 = self.ang_a_duty(n_sv2,ang2)

        self.set_duty_pierna(index,duty_sv0,duty_sv1,duty_sv2)

    #toma las cordenadas globales de una pierna y calcula los angulos de cada servo
    def set_cord(self,index:int,cord:list):
        P = self.global_to_local(index,cord)
        #P[0] = x
        #P[1] = y
        #P[2] = z

        #angulo del servo 0
        alfa_0 = math.degrees(math.atan2(-P[1],P[0]))
        #print("*** alfa 0 = ", alfa_0)

        #distancia de P0 a P3 en plano x, y (vista superior)
        d_p0p3 = self.dis_PaP_R2(Pf=P[0:2])
        #print("d_p0p3 = ", d_p0p3)

        #distancia P1 a P3 en plano x, y (plano superior)
        d_p1p3 = d_p0p3-self.Pierna_param[6][0]
        #print("d_p1p3 = ", d_p1p3)

        #distancia C = sqrt(DP1P2^2 + (H-Z)^2)
        dis_C = self.dis_PaP_R2(
            [0,P[2]],
            [d_p1p3,self.H[0]])
        #print("dis_C = ", dis_C)
        
        #distancia q = (m2^2 + m1^2 + C^2)/(2C)
        dis_q = (-math.pow(self.Pierna_param[6][2],2) + math.pow(self.Pierna_param[6][1],2) + math.pow(dis_C,2))/(2*dis_C)
        #print("dis_q = ", dis_q)

        #angulo P2 P1 P3 = acos(q/m1)
        ang_p2p1p3 = math.degrees(math.acos(dis_q/self.Pierna_param[6][1]))
        #print("ang_p2p1p3 = ", ang_p2p1p3)

        #angulo P1 P3 P2 = acos((C-q)/m2)
        ang_p1p3p2 = math.degrees(math.acos((dis_C-dis_q)/self.Pierna_param[6][2]))
        #print("ang_p1p3p2 = ", ang_p1p3p2)

        alfa_2 = 180-(ang_p2p1p3+ang_p1p3p2)
        #print("*** alfa 2 = ", alfa_2)

        #angulo P3 P1 vertical = asin(d_p1p3/C)
        #ang_P3P1V = math.degrees(math.asin(d_p1p3/dis_C))
        ang_P3P1V = math.degrees(math.atan((P[2]-self.H[0])/d_p1p3))+90
        #print("ang_P3P1V = ", ang_P3P1V)
        alfa_1 = ang_P3P1V+ang_p2p1p3
        #print("*** alfa 1 = ", alfa_1)

        #print(P,alfa_0,alfa_1,alfa_2)
        self.set_ang_pierna(index,alfa_0,alfa_1,alfa_2)

    #calcula las rotaciones y desplazamientos
    def actualizar_rot_desp(self):
        rot = [0.0,0.0,0.0]
        for i in range(3):
            rot[i] = math.radians(self.rotacion[0][i])
        

        for n in range(6):
            if(self.estado_rot_desp[n]):
                new_cords = [0.0,0.0,0.0]
                for i in range(3):
                    new_cords[i] = self.cord_global[n][i]-self.punto_rotacion[0][i]

                #new_cords[0] = X
                #new_cords[1] = Y
                #new_cords[2] = Z

                #rotacion en X
                if(self.rotacion[0] != 0):
                    #hipotesuna Y,Z
                    hipo = self.hipotenusa_R2(new_cords[1],new_cords[2])
                    if(round(hipo,5) == 0.0):
                        new_cords[1] = 0.0
                        new_cords[2] = 0.0
                    else:
                        angulo = math.atan2(new_cords[2],new_cords[1])+rot[0]
                        new_cords[1] = math.cos(angulo)*hipo
                        new_cords[2] = math.sin(angulo)*hipo
                    
                #rotacion en Y
                if(self.rotacion[1] != 0):
                    #hipotesuna X,Z
                    hipo = self.hipotenusa_R2(new_cords[0],new_cords[2])
                    if(round(hipo,5) == 0.0):
                        new_cords[0] = 0.0
                        new_cords[2] = 0.0
                    else:
                        angulo = math.atan2(new_cords[2],new_cords[0])+rot[1]
                        new_cords[0] = math.cos(angulo)*hipo
                        new_cords[2] = math.sin(angulo)*hipo

                #rotacion en Z
                if(self.rotacion[2] != 0):
                    #hipotesuna Y,X
                    hipo = self.hipotenusa_R2(new_cords[1],new_cords[0])
                    if(round(hipo,5) == 0.0):
                        new_cords[1] = 0.0
                        new_cords[0] = 0.0
                    else:
                        angulo = math.atan2(new_cords[0],new_cords[1])+rot[2]
                        new_cords[1] = math.cos(angulo)*hipo
                        new_cords[0] = math.sin(angulo)*hipo
                
                for i in range(3):
                    new_cords[i]+=self.punto_rotacion[0][i]+self.desplazamiento_cuerpo[0][i]

                self.set_cord(n,new_cords)
            else:
                self.set_cord(n,self.cord_global[n])
    
    #convierte una velocidad vectorial a las velocidades de cada eje
    def vector_seed(self,punto_inicial,punto_final,speed):
        dc = [
                punto_final[0]-punto_inicial[0],
                punto_final[1]-punto_inicial[1],
                punto_final[2]-punto_inicial[2]
            ]

        time = self.hipotenusa_R3(dc[0],dc[1],dc[2])/speed

        return [
                    dc[0]/time,
                    dc[1]/time,
                    dc[2]/time
                ]

    #fija una cordenada objetivo en una pierna
    def lineal_set_target_time(self,index,cord,time,rot_dep=True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = True
        self.movimiento_lineal[0][index] = cord

        for i in range(3):
            self.movimiento_lineal[1][index][i] = (cord[i]-self.cord_global[index][i])/time
    
    #fija una cordenada objetivo en una pierna
    def lineal_set_target_speed(self,index,cord,speed,rot_dep=True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = True
        self.movimiento_lineal[0][index] = cord
        self.movimiento_lineal[1][index] = self.vector_seed(self.cord_global[index],cord,speed)
    

    #movimiento_circular[0][n] angulo actual
    #movimiento_circular[1][n] angulo target
    #movimiento_circular[2][n] velocidad angular
    #movimiento_circular[3][n] radio
    #movimiento_circular[4][n] Z target
    #movimiento_circular[5][n] velocidad lineal Z
    #movimiento_circular[6][n][XY] cordenadas de centro de la circunferencia
    def polar_set_target_time(self,index,ang,z,cord_rot,radio,time,rot_dep=True,rad = True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = False

        if(not rad):
            ang = math.radians(ang)

        self.movimiento_circular[3][index] = radio
        self.movimiento_circular[6][index] = cord_rot

        self.movimiento_circular[1][index] = ang
        self.movimiento_circular[2][index] = (self.movimiento_circular[1][index]-self.movimiento_circular[0][index])/time

        self.movimiento_circular[4][index] = z
        self.movimiento_circular[5][index] = (z-self.cord_global[index][2])/time

    def polar_set_target_speed(self,index,ang,z,cord_rot,radio,ang_speed,z_speed=0,rot_dep=True,rad = True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = False

        if(not rad):
            ang = math.radians(ang)
            ang_speed = math.radians(ang_speed)

        
        if(not ang is None):
            self.movimiento_circular[3][index] = radio
            self.movimiento_circular[6][index] = cord_rot

        
            self.movimiento_circular[1][index] = ang
            if(self.movimiento_circular[0][index] > ang):
                self.movimiento_circular[2][index] = -abs(ang_speed)
            else:
                self.movimiento_circular[2][index] = abs(ang_speed)

        if(not z is None):
            self.movimiento_circular[4][index] = z
            if(self.cord_global[index][2] > z):
                self.movimiento_circular[5][index] = -abs(z_speed)
            else:
                self.movimiento_circular[5][index] = abs(z_speed)


    #fija los parametros de rotacion y desplazamientos en el robot
    def set_param_time(self,time,h=None,rot = None,p_rot=None,desp=None):
        if(not h is None):
            self.H[1] = h
            self.H[2] = (h-self.H[0])/time

        if(not rot is None):
            for i in range(3):
                self.rotacion[1][i] = rot[i]
                self.rotacion[2][i] = (rot[i]-self.rotacion[0][i])/time

        if(not p_rot is None):
            for i in range(3):
                self.punto_rotacion[1][i] = p_rot[i]
                self.punto_rotacion[2][i] = (p_rot[i]-self.punto_rotacion[0][i])/time

        if(not desp is None):
            for i in range(3):
                self.desplazamiento_cuerpo[1][i] = desp[i]
                self.desplazamiento_cuerpo[2][i] = (desp[i]-self.desplazamiento_cuerpo[0][i])/time

    #fija los parametros de rotacion y desplazamientos en el robot
    def set_param_speed(self,lineal_seed=None,angular_speed=None,h=None,rot = None,p_rot=None,desp=None):
        if(not lineal_seed is None):
            if(not h is None):
                self.H[1] = h
                self.H[2] = lineal_seed

            if(not p_rot is None):
                self.punto_rotacion[1] = p_rot
                self.punto_rotacion[2] = self.vector_seed(self.punto_rotacion[0],p_rot,lineal_seed)

            if(not desp is None):
                self.desplazamiento_cuerpo[1] = desp
                self.desplazamiento_cuerpo[2] = self.vector_seed(self.desplazamiento_cuerpo[0],desp,lineal_seed)

        if((not rot is None) and (not angular_speed is None)):
            self.rotacion[1] = rot
            self.rotacion[2] = self.vector_seed(self.rotacion[0],rot,angular_speed)

    #mueve una pierna una cirte distancia respecto al punto actual
    def lineal_move_time(self,index,cord,time,rot_dep=True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = True
        for i in range(3):
            cord[i] += self.cord_global[i]

        self.lineal_set_target_time(index,cord,time)

    #mueve una pierna una cirte distancia respecto al punto actual
    def lineal_move_speed(self,index,cord,speed,rot_dep=True):
        self.estado_rot_desp[index] = rot_dep
        self.modo_movimiento[index] = True
        for i in range(3):
            cord[i] += self.cord_global[i]

        self.lineal_set_target_speed(index,cord,speed)

    #resetea el reloj interno
    def reset_dt(self):
        self.delta_time[0] = 0.0
        self.delta_time[1] = time()

    #calcula los movimientos de las piernas
    def condicion_objetivo(self,index):
        result = True
        pre_result = True
        if(self.modo_movimiento[index]):
            for j in range(3):
                [
                    self.cord_global[index][j],
                    self.movimiento_lineal[0][index][j],
                    self.movimiento_lineal[1][index][j],
                    pre_result
                ] = self.condicion_objetivo_lineal(
                    self.cord_global[index][j],
                    self.movimiento_lineal[0][index][j],
                    self.movimiento_lineal[1][index][j],
                    self.delta_time[0]
                    )
                result = result and pre_result
        else:
            result = self.condicion_objetivo_polar(index)
        return result

    #calcula los movimientos de las piernas cuando estan en modo lineal
    def condicion_objetivo_lineal(self,p_inicial,p_final,vel,dt,lim=3):
        if(abs(vel)>0):
            dif = p_final-p_inicial
            if(((vel > 0) and (dif > lim)) or ((vel < 0) and (dif < -lim))):
                p_inicial = p_inicial+(vel*dt)
                dif = p_final-p_inicial

            if(not(((vel > 0) and (dif > lim)) or ((vel < 0) and (dif < -lim)))):
                return [p_final,p_final,0,True]
        else:
            return [p_inicial,p_inicial,0,True]
        
        return [p_inicial,p_final,vel,False]


    #calcula los movimientos de las piernas cuando estan en modo polar
    def condicion_objetivo_polar(self,index,lim=0):
        result = True
        pre_result = False
        [
            self.movimiento_circular[0][index],
            self.movimiento_circular[1][index],
            self.movimiento_circular[2][index],
            pre_result
        ] = self.condicion_objetivo_lineal(
            self.movimiento_circular[0][index],
            self.movimiento_circular[1][index],
            self.movimiento_circular[2][index],
            self.delta_time[0],
            math.radians(lim)
        )
        result = result and pre_result  
        self.cord_global[index][0] = (math.cos(self.movimiento_circular[0][index])*self.movimiento_circular[3][index])+self.movimiento_circular[6][index][0]
        self.cord_global[index][1] = (math.sin(self.movimiento_circular[0][index])*self.movimiento_circular[3][index])+self.movimiento_circular[6][index][1]

        [
            self.cord_global[index][2],
            self.movimiento_circular[4][index],
            self.movimiento_circular[5][index],
            pre_result
        ] = self.condicion_objetivo_lineal(
            self.cord_global[index][2],
            self.movimiento_circular[4][index],
            self.movimiento_circular[5][index],
            self.delta_time[0]
        )
        result = result and pre_result   
        return result

    #actualiza todos los movimientos, resplazamientos, rotaciones
    def actualizar_cord(self):
        time_ref = time()
        self.delta_time[0] = time_ref - self.delta_time[1]
        self.delta_time[1] = time_ref

        result_por_pierna = [False,False,False,False,False,False]
        result_H = False
        rasult_rot = [True,False]
        rasult_p_rot = [True,False]
        rasult_desp = [True,False]
        result_general = True
        for i in range(6):
            result_por_pierna[i] = self.condicion_objetivo(i)
            result_general = result_general and result_por_pierna[i]
        [
            self.H[0],
            self.H[1],
            self.H[2],
            result_H
        ]=self.condicion_objetivo_lineal(
            self.H[0],
            self.H[1],
            self.H[2],
            self.delta_time[0]
        )
        result_general = result_general and result_H
        for i in range(3):
            [
                self.rotacion[0][i],
                self.rotacion[1][i],
                self.rotacion[2][i],
                rasult_rot[1]
            ]=self.condicion_objetivo_lineal(
                self.rotacion[0][i],
                self.rotacion[1][i],
                self.rotacion[2][i],
                self.delta_time[0],0.5
            )  
            rasult_rot[0] = rasult_rot[0] and rasult_rot[1]

            [
                self.punto_rotacion[0][i],
                self.punto_rotacion[1][i],
                self.punto_rotacion[2][i],
                rasult_p_rot[1]
            ]=self.condicion_objetivo_lineal(
                self.punto_rotacion[0][i],
                self.punto_rotacion[1][i],
                self.punto_rotacion[2][i],
                self.delta_time[0]
            )
            rasult_p_rot[0] = rasult_p_rot[0] and rasult_p_rot[1]

            [
                self.desplazamiento_cuerpo[0][i],
                self.desplazamiento_cuerpo[1][i],
                self.desplazamiento_cuerpo[2][i],
                rasult_desp[1]
            ]=self.condicion_objetivo_lineal(
                self.desplazamiento_cuerpo[0][i],
                self.desplazamiento_cuerpo[1][i],
                self.desplazamiento_cuerpo[2][i],
                self.delta_time[0]
            )
            rasult_desp[0] = rasult_desp[0] and rasult_desp[1]

        result_general = result_general and rasult_rot[0] and rasult_p_rot[0] and rasult_desp[0]
        self.actualizar_rot_desp()
        return(result_general,result_por_pierna,result_H,rasult_rot[0],rasult_p_rot[0],rasult_desp[0])

    def bucle_movimiento(self):
        estado = False
        self.reset_dt()
        while(not estado):
            estado,_,_,_,_,_ = self.actualizar_cord()

    def polar_set_step_caminata(self,n_sec,n_step,dis_arco,z,lineal_speed,cord_r,doble_cent_r,r_por_pie,estado,sep_pie=0):

        rot_time = dis_arco/lineal_speed

        angulos = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #[0][n] = radio
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #[1][n] = angulos base/central
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #[2][n] = posicion -1 es a la derecha y 1 es a la izquierda
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #[3][n] = angulos frontal
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #[4][n] = angulos trasero
        ]

        if(doble_cent_r):
            #modo doble circulo, el segundo circulo es un reflejo del principal
            #los pies 0, 2, 4 estan suquetos al circulo principal
            #los pies 1, 3, 5 estan suquetos al circulo reflejo
            #este modo es para caminata
            sleep(0.00001)
        else:
            #modo circulo cimple, este modo cirve para caminata y rotacion en un punto

            for n in range(6):
                if(self.Pierna_param[n][3][0] < cord_r[0]):
                    angulos[2][n] = -1
                else:
                    angulos[2][n] = 1

            if(r_por_pie):
                for n in range(6):
                    angulos[0][n]=self.dis_PaP_R2(self.Pierna_param[n][3][0:2],cord_r)
                    angulos[1][n] = math.atan2((self.Pierna_param[n][3][1]-cord_r[1]),(self.Pierna_param[n][3][0]-cord_r[0]))
                    angulos[1][n] = self.angulo_positivo(angulos[1][n])

                d_ang = dis_arco/max(angulos[0])
            
            else:
                radio_0 = self.dis_PaP_R2(self.Pierna_param[1][3][0:2],cord_r)
                radio_1 = self.dis_PaP_R2(self.Pierna_param[4][3][0:2],cord_r)

                sep_0 = (sep_pie+70)/radio_0
                sep_1 = (sep_pie+70)/radio_1

                d_ang = dis_arco/max(radio_0,radio_1)
                
                ang_base_0 = math.atan2((self.Pierna_param[1][3][1]-cord_r[1]),(self.Pierna_param[1][3][0]-cord_r[0]))
                ang_base_1 = math.atan2((self.Pierna_param[4][3][1]-cord_r[1]),(self.Pierna_param[4][3][0]-cord_r[0]))

                angulos[1][0] = ang_base_0 + ((2*d_ang+sep_0)*angulos[2][0])
                angulos[1][1] = ang_base_0
                angulos[1][2] = ang_base_0 - ((2*d_ang+sep_0)*angulos[2][2])

                angulos[1][3] = ang_base_1 - ((2*d_ang+sep_1)*angulos[2][3])
                angulos[1][4] = ang_base_1
                angulos[1][5] = ang_base_1 + ((2*d_ang+sep_1)*angulos[2][5])

                angulos[0][0] = radio_0
                angulos[0][1] = radio_0
                angulos[0][2] = radio_0

                angulos[0][3] = radio_1
                angulos[0][4] = radio_1
                angulos[0][5] = radio_1

            ang_speed = d_ang/rot_time
            for n in range(6):
                angulos[1][n] = self.angulo_positivo(angulos[1][n])

                #if(self.movimiento_circular[6][n][0] != cord_r[0] or self.movimiento_circular[6][n][1] != cord_r[1]):
                #    self.movimiento_circular[0][n] = angulos[1][n]

                angulos[3][n] = angulos[1][n] + (d_ang*angulos[2][n])
                angulos[4][n] = angulos[1][n] - (d_ang*angulos[2][n])

                if(estado):
                    if(self.secuencias_caminata[n_sec][n_step][0][n] is None):
                        

                        r_actual=self.dis_PaP_R2(self.cord_global[n][0:2],cord_r)
                        ang_actual = math.atan2((self.cord_global[n][1]-cord_r[1]),(self.cord_global[n][0]-cord_r[0]))

                        if((angulos[3][n] > 0 and angulos[4][n] > 0) or (angulos[3][n] < 0 and angulos[4][n] < 0)):
                            ang_actual = self.angulo_positivo(ang_actual)

                        self.movimiento_circular[0][n] = ang_actual
                        self.movimiento_circular[1][n] = ang_actual
                        self.movimiento_circular[2][n] = 0
                        self.movimiento_circular[3][n] = r_actual
                        self.movimiento_circular[6][n] = cord_r
                        ang = None
                    else:
                        if(self.secuencias_caminata[n_sec][n_step][0][n]==1):
                            ang = angulos[3][n]
                        elif(self.secuencias_caminata[n_sec][n_step][0][n]==-1):
                            ang = angulos[4][n]
                        else:
                            ang = angulos[1][n]
                    
                    if(self.secuencias_caminata[n_sec][n_step][1][n] is None):
                        z_tar = None
                    else:
                        if(self.secuencias_caminata[n_sec][n_step][1][n]==1):
                            z_tar = z
                        else:
                            z_tar = 0
                    

                    self.polar_set_target_speed(
                        n,
                        ang,
                        z_tar,
                        cord_r,
                        angulos[0][n],
                        ang_speed,
                        lineal_speed,
                        False,
                        True
                    )