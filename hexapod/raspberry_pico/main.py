from machine import Pin, PWM, I2C, UART, freq
from time import sleep_ms, ticks_us
from PCA9685 import pca9685
from protocolo_serial import pro_Serial

freq(240000000)
#print(freq())

SDA = Pin(2)
SCL = Pin(3)
i2c = I2C(1,sda=SDA,scl=SCL,freq=1000000)

sleep_ms(100)

pca = pca9685(i2c=i2c,address=127,freq_refr=333)

sv16 = PWM(Pin(22,Pin.OUT))
sv16.freq(333)

sv17 = PWM(Pin(21,Pin.OUT))
sv17.freq(333)

sleep_ms(100)

Serial = UART(0, 1500000,tx=Pin(12),rx=Pin(13)) 
serial_com = pro_Serial(Serial)
#print("Iniciado")

pass_duty = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]

pwm0= Pin(11,Pin.IN)
pwm1= Pin(14,Pin.IN)
pwm2= Pin(15,Pin.IN)


duty_in = [0,0,0]
duty_in_map = [0,0,0]
ms_ref = [0,0,0]

#11
#14
#15
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
        duty_in_map[0] = joystick(duty_in[0],1300,1800,1500,60)
        pwm0.irq(trigger=Pin.IRQ_RISING , handler=pwm0_duty)

def pwm1_duty(p):
    if(pwm1.value()):
        ms_ref[1] = ticks_us()
        pwm1.irq(trigger=Pin.IRQ_FALLING , handler=pwm1_duty)
        duty_in_map[1] = joystick(duty_in[1],1050,2150,1500,60)
    else:
        duty_in[1] = round((duty_in[1]*(4/5))+((ticks_us()-ms_ref[1])/5))
        pwm1.irq(trigger=Pin.IRQ_RISING , handler=pwm1_duty)

def pwm2_duty(p):
    if(pwm2.value()):
        ms_ref[2] = ticks_us()
        pwm2.irq(trigger=Pin.IRQ_FALLING , handler=pwm2_duty)
    else:
        duty_in[2] = round((duty_in[2]*(4/5))+((ticks_us()-ms_ref[2])/5))
        duty_in_map[1] = joystick(duty_in[2],960,2100,1500,60)
        pwm2.irq(trigger=Pin.IRQ_RISING , handler=pwm2_duty)

pwm0.irq(trigger=Pin.IRQ_RISING , handler=pwm0_duty)
pwm1.irq(trigger=Pin.IRQ_RISING , handler=pwm1_duty)
pwm2.irq(trigger=Pin.IRQ_RISING , handler=pwm2_duty)

while True:
    if(Serial.any()>0):
        tipo,buffer = serial_com.read_command()
        if(not (tipo is None or buffer is None)):
            if(tipo == 0):
                for i in range(len(buffer)):
                    buffer[i] = buffer[i]+1
                    if(buffer[i] > 255):
                        buffer[i] = 0
                serial_com.send_command(0,"B",buffer)
            elif(tipo == 1 and len(buffer) == 18):
                serial_com.send_command(1,"H",duty_in)
                val = True
                for x in buffer:
                    if(x < 500 or x > 2500):
                        val = False
                if(val):
                    pca.set_massive_us(buffer[0:16])
                    sv16.duty_ns(buffer[16]*1000)
                    sv17.duty_ns(buffer[17]*1000)

                    pass_duty = buffer


