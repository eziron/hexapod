from time import time, sleep
from math import atan2, sqrt,degrees
from xbox360controller import Xbox360Controller



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
h = 80
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
    print('Button {0} was pressed',str(button.name))
    but_dic[button.name] = 1


def on_button_released(button):
    print('Button {0} was released',str(button.name))
    but_dic[button.name] = 0

def on_back_pressed(button):
    global belico
    belico = not belico
    print("beloco =",belico)

def on_star_pressed(button):
    global star
    star = not star
    print("star =",star)

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



control_timer = time()

estado_bucle = True
estado_bucle0 = True
while(estado_bucle):
    try:
        with Xbox360Controller(0, axis_threshold=0) as controller:
            controller.button_start.when_pressed = on_star_pressed
            controller.button_select.when_pressed = on_back_pressed
            controller.axis_l.when_moved = on_axis_L_moved
            controller.axis_r.when_moved = on_axis_R_moved
            controller.trigger_l.when_moved = on_Lt_moved
            controller.trigger_r.when_moved = on_Rt_moved

            controller.button_a.when_pressed = on_button_pressed
            controller.button_b.when_pressed = on_button_pressed
            controller.button_y.when_pressed = on_button_pressed
            controller.button_x.when_pressed = on_button_pressed
            controller.button_thumb_l.when_pressed = on_button_pressed
            controller.button_thumb_r.when_pressed = on_button_pressed
            controller.button_trigger_l.when_pressed = on_button_pressed
            controller.button_trigger_r.when_pressed = on_button_pressed

            controller.button_a.when_released = on_button_released
            controller.button_b.when_released = on_button_released
            controller.button_y.when_released = on_button_released
            controller.button_x.when_released = on_button_released
            controller.button_thumb_l.when_released = on_button_released
            controller.button_thumb_r.when_released = on_button_released
            controller.button_trigger_l.when_released = on_button_released
            controller.button_trigger_r.when_released = on_button_released
            
            while(estado_bucle):

                print(but_dic,star,n_seq,n_step)

                if(star):
                    print(but_dic["button_a"],but_dic["button_a"]==1)
                    if(but_dic["button_a"]==1):
                        n_seq = -2
                    elif(but_dic["button_b"]):
                        n_seq = -3
                    elif(belico and but_dic["button_y"]):
                        n_seq = -6
                    elif(belico and but_dic["button_x"]):
                        n_seq = -7
                    elif(belico and but_dic["button_trigger_l"]):
                        n_seq = -3
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
                        if(n_seq >= 0):
                            print("caminata, n_tep=",n_step,max_step)
                        elif(n_seq == -2):
                            print("secuencia baile 1, n_tep=",n_step,max_step)
                        elif(n_seq == -3):
                            print("secuencia baile 2, n_tep=",n_step,max_step)
                        elif(n_seq == -4):
                            print("secuencia ataque derecha, n_tep=",n_step,max_step)
                        elif(n_seq == -5):
                            print("secuencia ataque izquierda, n_tep=",n_step,max_step)
                        elif(n_seq == -6):
                            print("secuencia ataque 1 2, n_tep=",n_step,max_step)
                        elif(n_seq == -7):
                            print("secuencia embestida, n_tep=",n_step,max_step)

                        n_step += 1
                        if(n_step >= max_step):
                            n_step = 0
                    else:
                        pass_n_seq = n_seq
                        n_step = 0
                        print("cambio de secuencia")
                        sleep(1)

                else:
                    print("hedapod desactivado")
                    sleep(1)
    except:
        pass