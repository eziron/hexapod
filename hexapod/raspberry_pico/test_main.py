from machine import Pin, PWM, I2C, UART
from time import sleep_ms
from PCA9685 import pca9685
from protocolo_serial import pro_Serial

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




estado = True
while estado:
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
                serial_com.send_command(1,"B",[5,5])
                val = True
                for x in buffer:
                    if(x < 500 or x > 2500):
                        val = False
                if(val):
                    pca.set_massive_us(buffer[0:16])
                    sv16.duty_ns(buffer[16]*1000)
                    sv17.duty_ns(buffer[17]*1000)

                    pass_duty = buffer
