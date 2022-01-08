from machine import Pin, PWM, I2C, UART
from time import sleep_ms

SDA = Pin(2)
SCL = Pin(3)
i2c = I2C(1,sda=SDA,scl=SCL,freq=1000000)

sleep_ms(100)

print(i2c.scan())