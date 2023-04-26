from math import atan2, sqrt,degrees

def scal(x:float, in_min:float, in_max:float, out_min:float, out_max:float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def rec_a_pol(x:float,y:float,max_mod:float):
    mod = min(sqrt((x**2)+(y**2)),max_mod)
    ang = degrees(atan2(y,x))

    return ang,mod

def dead_val_axis(axis_val:float,dead_val:float,rangue=1.0):
    dead_min = -(dead_val/100)*rangue
    dead_max =  (dead_val/100)*rangue

    if(axis_val >= dead_min and axis_val <= dead_max):
        return 0.0
    elif(axis_val > dead_max):
        return scal(axis_val,dead_max,rangue,0,rangue)
    elif(axis_val < dead_min):
        return scal(axis_val,-rangue,dead_min,-rangue,0)
    else:
        return 0.0