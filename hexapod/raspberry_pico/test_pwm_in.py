from machine import Pin
from time import sleep_ms, ticks_us


pwm0= Pin(11,Pin.IN)
pwm1= Pin(12,Pin.IN)
pwm2= Pin(13,Pin.IN)

duty_in = [0,0,0]
ms_ref = [0,0,0]

def a_map(x,in_min,in_max,out_min,out_max): 
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def truncar(x,min_val, max_val):
    if(x < min_val):
        return min_val
    elif(x > max_val):
        return max_val
    else:
        return x

def joystick(val:int,min_val:int,max_val:int,cent_val:int,tol:int):
    val = truncar(val,min_val,max_val)
    if(val <= cent_val+tol and val >= cent_val-tol):
        return cent_val
    else:
        if(val > cent_val+tol):
            return round(a_map(val,cent_val+tol,max_val,1500,2000))
        else:
            return round(a_map(val,min_val,cent_val-tol,1000,1500))


def pwm0_duty(p):
    if(pwm0.value()):
        ms_ref[0] = ticks_us()
        pwm0.irq(trigger=Pin.IRQ_FALLING , handler=pwm0_duty)
    else:
        duty_in[0] = round((duty_in[0]*(4/5))+((ticks_us()-ms_ref[0])/5))
        pwm0.irq(trigger=Pin.IRQ_RISING , handler=pwm0_duty)

def pwm1_duty(p):
    if(pwm1.value()):
        ms_ref[1] = ticks_us()
        pwm1.irq(trigger=Pin.IRQ_FALLING , handler=pwm1_duty)
    else:
        duty_in[1] = round((duty_in[1]*(4/5))+((ticks_us()-ms_ref[1])/5))
        pwm1.irq(trigger=Pin.IRQ_RISING , handler=pwm1_duty)

def pwm2_duty(p):
    if(pwm2.value()):
        ms_ref[2] = ticks_us()
        pwm2.irq(trigger=Pin.IRQ_FALLING , handler=pwm2_duty)
    else:
        duty_in[2] = round((duty_in[2]*(4/5))+((ticks_us()-ms_ref[2])/5))
        pwm2.irq(trigger=Pin.IRQ_RISING , handler=pwm2_duty)

pwm0.irq(trigger=Pin.IRQ_RISING , handler=pwm0_duty)
pwm1.irq(trigger=Pin.IRQ_RISING , handler=pwm1_duty)
pwm2.irq(trigger=Pin.IRQ_RISING , handler=pwm2_duty)



while True:
    print(duty_in[0],joystick(duty_in[1],1050,2150,1500,60),joystick(duty_in[2],960,2100,1500,60))

    sleep_ms(10)