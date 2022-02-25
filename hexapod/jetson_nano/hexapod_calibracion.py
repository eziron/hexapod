import os
from time import sleep
import serial
import struct
from protocolo_serial import pro_Serial
import json

json_PATH = 'hexapod/jetson_nano/ajustes_hexapod.json'
with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

baud = conf_hexapod["general"]["baudrate"]

try:
    Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
except:
    os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
    Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)

os.system("""sudo renice -20 -p $(pgrep "python3")""")

serial_com = pro_Serial(Serial)

print("iniciado")

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    Serial.close()
    sleep(1)
    Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
    serial_com = pro_Serial(Serial)
    sleep(1)

def constrain(val, min_val, max_val):
    if(val < min_val):
        return min_val
    elif(val > max_val):
        return max_val
    else:
        return val
#duty perfecto
#para sv2 N   - 2322 = 164gr
#para sv2 INV - 678  = 164gr

#para sv1 N   - 1056 = 130gr
#para sv1 INV - 1944  = 130gr

#para sv0 N   - 1500 = 0gr
#para sv0 INV - 1500  = 0gr
duty = [
        2322, #[0]  - N    P6 sv2
        1944, #[1]  - inv  P6 sv1
        1944, #[2]  - inv  P5 sv1
        2322, #[3]  - N    P5 sv2
        1500, #[4]  - N    P5 sv0
        1944, #[5]  - inv  P4 sv1
        2322, #[6]  - N    P4 sv2
        1500, #[7]  - N    P4 sv0
        1500, #[8]  - inv  P3 sv0
        678 , #[9]  - inv  P3 sv2
        1056, #[10] - N    P3 sv1
        1500, #[11] - inv  P2 sv0
        678 , #[12] - inv  P2 sv2
        1056, #[13] - N    P2 sv1
        1056, #[14] - N    P1 sv1
        678 , #[15] - inv  P1 sv2
        1500, #[16] - N    P6 sv0
        1500  #[17] - inv  P1 sv0
    ]


for P in ["P1","P2","P3","P4","P5","P6"]:
    for sv in ["sv0","sv1","sv2"]:
        duty[conf_hexapod[P][sv]["n_sv"]] = conf_hexapod[P][sv]["duty_base"]
#duty = [869, 1560, 1027, 719, 1580, 1215, 939, 1540, 1570, 2031, 1785, 1500, 2131, 1983, 1500, 2061, 1075, 1855]

serial_com.send_duty(duty)

duty_val = 0
estado = True
estado2 = True

while(estado):
    n_p = int(input("ingrese el numero de pierna [1-6]: "))
    if(1 <= n_p <= 6):
        n_sv = int(input("ingrese el numero del servo [0-2]: "))
        if(0 <= n_sv <= 2):
            estado2 = True
            n_duty = conf_hexapod["P"+str(n_p)]["sv"+str(n_sv)]["n_sv"]
            print("duty actual de P"+str(n_p)+" / sv"+str(n_sv)+" / n_duty=",n_duty," es: ", duty[n_duty])

            while(estado2):
                #duty_val = int(input("ingrese duty [500-2500]: "))
                duty_str = input("ingrese duty [500-2500]: ")
                duty_val = int(duty_str)
                if("+" in duty_str or "-" in duty_str):
                    duty[n_duty] = constrain(duty[n_duty] + duty_val,500,2500)
                    print("nuevo duty = ",duty[n_duty])
                elif(duty_val >= 500 and duty_val <= 2500):
                    duty[n_duty] = duty_val
                elif(duty_val == 9):
                    estado2 = False
                    estado = False
                else:
                    estado2 = False

                serial_com.send_duty(duty)
        elif(n_sv == 9):
            estado = False
    elif(n_p == 9):
        estado = False

print(duty_val)
if(input("Desea guardar los ajustes actuales? [y/n]: ") == "y"):
    for P in ["P1","P2","P3","P4","P5","P6"]:
        for sv in ["sv0","sv1","sv2"]:
            conf_hexapod[P][sv]["duty_base"] = duty[conf_hexapod[P][sv]["n_sv"]]

    with open(json_PATH, 'w') as outfile:
        json.dump(conf_hexapod, outfile, indent=4)