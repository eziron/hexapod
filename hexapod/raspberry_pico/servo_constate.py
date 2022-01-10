from utime import sleep
from machine import Pin, PWM, I2C
from time import sleep_ms
from PCA9685 import pca9685

SDA = Pin(2)
SCL = Pin(3)
i2c = I2C(1,sda=SDA,scl=SCL,freq=1000000)

sleep_ms(100)

print(i2c.scan())

pca = pca9685(i2c=i2c,address=127,freq_refr=333)

#fb_pin = Pin(16,Pin.IN)
#pca.auto_calibration(fb_pin,14,1,True)


sv16 = PWM(Pin(22,Pin.OUT))
sv16.freq(333)


sv17 = PWM(Pin(21,Pin.OUT))
sv17.freq(333)

#pierna 6
pca.set_duty_us(1,1560)  #sv0 = 1
sv16.duty_ns(1930000)    #sv1 = 16
#sv16.duty_ns(1000000)    #sv1 = 16
pca.set_duty_us(0,2130)  #sv2 = 0


#pierna 5
pca.set_duty_us(4,1580)  #sv0 = 4
#pca.set_duty_us(2,1990)  #sv1 = 2
pca.set_duty_us(2,1000)  #sv1 = 2
pca.set_duty_us(3,2100)  #sv2 = 3


#pierna 4
pca.set_duty_us(7,1540)  #sv0 = 7
#pca.set_duty_us(5,2070)  #sv1 = 5
pca.set_duty_us(5,1000)  #sv1 = 5
pca.set_duty_us(6,2200)  #sv2 = 6



#pierna 3
pca.set_duty_us(8,1570)  #sv0 = 8
#pca.set_duty_us(10,930)  #sv1 = 10
pca.set_duty_us(10,2000)  #sv1 = 10
pca.set_duty_us(9,770)  #sv2 = 9



#pierna 2
pca.set_duty_us(11,1500) #sv0 = 11
#pca.set_duty_us(13,1020) #sv1 = 13
pca.set_duty_us(13,2000) #sv1 = 13
pca.set_duty_us(12,750) #sv2 = 12



#pierna 1
pca.set_duty_us(14,1500) #sv0 = 14
sv17.duty_ns(1000000)    #sv1 = 17
#sv17.duty_ns(2000000)    #sv1 = 17
pca.set_duty_us(15,800) #sv2 = 15


