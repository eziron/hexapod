import struct
from socket import *
import json
import os
import serial
from time import sleep, time
from servo_carteciano import Hexapod
from protocolo_serial import pro_Serial
import math

json_PATH = "/home/rodrigo/hexapod/hexapod/jetson_nano/ajustes_hexapod.json"
with open(json_PATH) as json_file:
    conf_hexapod = json.load(json_file)

baud = conf_hexapod["general"]["baudrate"]

while True:
    try:
        Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
        os.system("""sudo renice -20 -p $(pgrep "python3")""")
        break
    except:
        print("Error al inisiar el serial")
        os.system("echo 102938 | sudo -S chmod 666 /dev/ttyTHS1")
        Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)

serial_com = pro_Serial(Serial)
hexapod = Hexapod(conf_hexapod)

while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    Serial.close()
    sleep(1)
    Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
    serial_com = pro_Serial(Serial)
    sleep(1)

hexapod.reset_dt()

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('0.0.0.0', 8888))

def contrain_circular(val,min_val,max_val):
    if(val < min_val):
        return max_val
    if(val > max_val):
        return min_val

    return val

estado = True
n_step = 0

hexapod.reset_dt()
while True:
    data = s.recv(72)
    if not data is None:
        vals = struct.unpack("<"+"l"*18,data)
    