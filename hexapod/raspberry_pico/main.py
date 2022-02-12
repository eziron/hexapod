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

Serial = UART(0, 1500000,tx=Pin(12),rx=Pin(13)) 
#print("Iniciado")

pass_duty = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]


def send_command(tipo,buffer) -> bool:
    if(isinstance(buffer,list)):
        len_msg = len(buffer)
        if(len_msg == 0):
            return(False)
    else:
        len_msg = 1
        buffer = [buffer]

    if(tipo == 0):
        #tipo ping pong, la RPI pico responde con los mismo bytes +1
        buffer_type = "B"
    else:
        return False
    
    try:
        msg_tx = ustruct.pack(">HBB"+buffer_type,65276,tipo,len_msg,*buffer)
        Serial.write(msg_tx)
        return True
    except:
        return False

    
def read_command():
    C = Serial.read()
    if(not (C is None) and (C[0] == 254)):
        C = Serial.read()
        if(not (C is None) and (C[0] == 252)):
            info_bytes = Serial.read(2)
            if(info_bytes is None):
                return None
            elif(info_bytes[0] == 0):
                buffer_type = "B"*info_bytes[1]
            else:
                return [None, None]

            buffer_len = ustruct.calcsize(">"+buffer_type)
            buffer_bytes = Serial.read(buffer_len)

            if(buffer_bytes is None):
                return [None, None]
            else:
                buffer_values = ustruct.unpack(">"+buffer_type,buffer_bytes)
                return [info_bytes[0],buffer_values]

    return [None, None]

estado = True
while estado:
    if(Serial.any()>0):
        msg = Serial.read(36)
        if(not msg is None):
            try:
                Serial.write(b"Hola Mundo\n")
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
