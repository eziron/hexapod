from time import sleep, time
from serial import Serial
import time
from protocolo_serial import pro_Serial
import math
import numpy as np
import open3d as o3d



while True:
    try:
        RPI_serial = Serial("COM6",2000000,timeout=0.5)
        break
    except:
        sleep(0.01)
serial_com = pro_Serial(RPI_serial)

ang1 = 0
ang2 = 0
dist = 0


samp = np.asarray([[0,0,0]])

time_ref = time.time()
while (time.time() - time_ref < 25):
    _,sample = serial_com.read_command()

    if(not sample is None):
        ang1 = math.radians(sample[0]/64)
        ang2 = math.radians(sample[1]/64)
        dist = sample[2]/4

        x = math.sin(ang2)*dist
        z = math.cos(ang2)*dist

        hipo = abs(x)
        ang = math.atan2(0,x)+(ang1-90)

        X = math.sin(ang)*hipo
        Y = math.cos(ang)*hipo

        samp = np.append(samp,[[X,Y,z]],0)

        print(ang1,ang2,dist,X,Y,z)

print(samp)
print(len(samp))
print(len(samp)/25)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(samp)
o3d.visualization.draw_geometries([pcd])