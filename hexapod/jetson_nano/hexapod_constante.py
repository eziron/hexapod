import os
import serial
import struct

try:
    Serial = serial.Serial("/dev/ttyTHS1",115200,timeout=0.1)
except:
    os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
    Serial = serial.Serial("/dev/ttyTHS1",115200,timeout=0.1)

def actualizar_duty(duty_vals):
    msg_tx = struct.pack("<"+"H"*18,*duty_vals)
    Serial.write(msg_tx)
    msg_rx = Serial.readline()
    if(msg_rx is None):
        print("raspberry pi pico no responde")

duty = [
    2130, #[0]  - N    P6 sv2
    1520, #[1]  - N    P6 sv0
    1990, #[2]  - inv  P5 sv1
    2170, #[3]  - N    P5 sv2
    1540, #[4]  - N    P5 sv0
    2070, #[5]  - inv  P4 sv1
    2200, #[6]  - N    P4 sv2
    1540, #[7]  - N    P4 sv0
    1510, #[8]  - inv  P3 sv0
    720 , #[9]  - inv  P3 sv2
    930 , #[10] - N    P3 sv1
    1450, #[11] - inv  P2 sv0
    750 , #[12] - inv  P2 sv2
    1020, #[13] - N    P2 sv1
    1550, #[14] - inv  P1 sv0
    850 , #[15] - inv  P1 sv2
    1930, #[16] - inv  P6 sv1
    1000  #[17] - N    P1 sv1
    ]
actualizar_duty(duty)


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
        actualizar_duty(duty)
    else:
        if(duty_val == 5):
            n_sv = int(input("ingrese n_servo: "))
            if(n_sv <= 17 and n_sv >= 0):
                print("valor actual del servo", n_sv, "es:",duty[n_sv])
            else:
                estado = False
        else:
            estado = False

