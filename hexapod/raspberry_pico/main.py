from machine import Pin, PWM, I2C, UART
from time import sleep_ms
from PCA9685 import pca9685
import ustruct

SDA = Pin(2)
SCL = Pin(3)
i2c = I2C(1,sda=SDA,scl=SCL,freq=1000000)

sleep_ms(100)

#print(i2c.scan())

#if not 0x40 in i2c.scan():
#    print("El Driver PWM PCA9685 no esta conectado")
#sleep_ms(100)

pca = pca9685(i2c=i2c,address=127,freq_refr=333)

sv16 = PWM(Pin(22,Pin.OUT))
sv16.freq(333)

sv17 = PWM(Pin(21,Pin.OUT))
sv17.freq(333)

serial = UART(0, 115200,tx=Pin(12),rx=Pin(13)) 
#print("Iniciado")

pass_duty = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]


estado = True
while estado:
    if(serial.any()>0):
        msg = serial.read(36)
        if(not msg is None):
            try:
                serial.write(b"Hola Mundo\n")
                msg_array = ustruct.unpack("<"+"H"*18,msg)
                #print(msg_array)

                pca.set_massive_us(msg_array[0:16])
                sv16.duty_ns(msg_array[16]*1000)
                sv17.duty_ns(msg_array[17]*1000)

                pass_duty = msg_array
            except:
                pca.set_massive_us(pass_duty[0:16])
                sv16.duty_ns(pass_duty[16]*1000)
                sv17.duty_ns(pass_duty[17]*1000)
