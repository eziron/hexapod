import os
from time import sleep
import serial
import struct
from protocolo_serial import pro_Serial

try:
    Serial = serial.Serial("/dev/ttyTHS1",1500000,timeout=0.05)
except:
    os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
    Serial = serial.Serial("/dev/ttyTHS1",1500000,timeout=0.05)

os.system("""sudo renice -20 -p $(pgrep "python3")""")

serial_com = pro_Serial(Serial)

print("iniciado")

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    Serial.close()
    sleep(1)
    Serial = serial.Serial("/dev/ttyTHS1",1500000,timeout=0.05)
    serial_com = pro_Serial(Serial)
    sleep(1)

def actualizar_duty(duty_vals):
    msg_tx = struct.pack("<"+"H"*18,*duty_vals)
    Serial.write(msg_tx)
    msg_rx = Serial.readline()
    print(msg_rx)
    if(msg_rx is None):
        print("raspberry pi pico no responde")
#duty perfecto
#para sv2 N   - 2322 = 164gr
#para sv2 INV - 678  = 164gr

#para sv1 N   - 1056 = 130gr
#para sv1 INV - 1944  = 130gr

#para sv0 N   - 1500 = 0gr
#para sv0 INV - 1500  = 0gr
duty = [
    2322, #[0]  - N    P6 sv2
    1520, #[1]  - N    P6 sv0
    1990, #[2]  - inv  P5 sv1
    2170, #[3]  - N    P5 sv2
    1540, #[4]  - N    P5 sv0
    2070, #[5]  - inv  P4 sv1
    2322, #[6]  - N    P4 sv2
    1540, #[7]  - N    P4 sv0
    1510, #[8]  - inv  P3 sv0
    678 , #[9]  - inv  P3 sv2
    930 , #[10] - N    P3 sv1
    1450, #[11] - inv  P2 sv0
    678 , #[12] - inv  P2 sv2
    1020, #[13] - N    P2 sv1
    1550, #[14] - inv  P1 sv0
    850 , #[15] - inv  P1 sv2
    1930, #[16] - inv  P6 sv1
    1000  #[17] - N    P1 sv1
    ]

#duty = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]

serial_com.send_duty(duty)


duty_val = None
estado = True
n_sv = int(input("ingrese n_servo: "))
if(n_sv <= 17 and n_sv >= 0):
    print("valor actual del servo", n_sv, "es:",duty[n_sv])
else:
    estado = False


while(estado):
    duty_val = int(input("ingrese duty: "))
    if(duty_val >= 500 and duty_val <= 2500):
        duty[n_sv] = duty_val
        serial_com.send_duty(duty)
    else:
        if(duty_val == 5):
            n_sv = int(input("ingrese n_servo: "))
            if(n_sv <= 17 and n_sv >= 0):
                print("valor actual del servo", n_sv, "es:",duty[n_sv])
            else:
                estado = False
        else:
            estado = False

