import json, os, serial
import time
from time import sleep
from protocolo_serial import pro_Serial
import math
import numpy as np
import open3d as o3d
from datetime import datetime

samp_PATH = "/home/rodrigo/hexapod/PC/samples/"
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

"""while(serial_com.ping() is None):
    print("error al conectar con la RPI pico")
    Serial.close()
    sleep(1)
    Serial = serial.Serial("/dev/ttyTHS1",baud,timeout=0.05)
    serial_com = pro_Serial(Serial)
    sleep(1)"""

serial_com.star_lidar(0,255,255)
sleep(1)
if(Serial.in_waiting > 0):
    C = Serial.read(Serial.in_waiting)

samp_array = np.zeros((500000,3),dtype=np.float64)
n_samp = 0
t_samp = 10



if(serial_com.star_lidar(3,0,0)):
    time_ref = time.time()
    while (time.time() - time_ref < t_samp):
        samp = serial_com.read_lidar()
        if(not (samp is None)):
            samp_array[n_samp][0] = samp[0]
            samp_array[n_samp][1] = samp[1]
            samp_array[n_samp][2] = samp[2]
            n_samp+=1

            if(n_samp%1000 == 0):
                print(time.time() - time_ref,n_samp)
    
    print(samp_array[:n_samp])
    print(n_samp)
    print(n_samp/t_samp)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(samp_array[:n_samp])

    dt_string = datetime.now().strftime("lidar_sample-%d%m%Y-%H%M%S.ply")
    o3d.io.write_point_cloud(samp_PATH+dt_string, pcd)
else:
    print("ERROR al inciar el lidar")

serial_com.stop_lidar()