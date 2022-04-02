from time import sleep, time
from serial import Serial
import time
from protocolo_serial import pro_Serial
import math
import numpy as np
import open3d as o3d



while True:
    try:
        RPI_serial = Serial("COM7",1500000,timeout=0.5)
        break
    except:
        sleep(0.01)
serial_com = pro_Serial(RPI_serial)

ang1 = 0
ang2 = 0
dist = 0


#samp = np.asarray([[0,0,0]])
samp = np.zeros((500000,3),dtype=np.float64)
n_samp = 0
t_samp = 60
time_ref = time.time()
while (time.time() - time_ref < t_samp):
    _,sample = serial_com.read_command()
    
    if(not sample is None):
        try:
            ang2 = math.radians(sample[0]/64)
            ang1 = math.radians(sample[1]/64)
            dist = sample[2]/4

            if(dist > 0 and dist < 8000):
                x = math.sin(ang2)*dist
                z = math.cos(ang2)*dist

                hipo = abs(x)
                ang = math.atan2(0,x)+(ang1-math.pi/2)

                X = math.sin(ang)*hipo
                Y = math.cos(ang)*hipo

                #samp = np.append(samp,[[X,Y,z]],0)
                samp[n_samp][0] = X
                samp[n_samp][1] = Y
                samp[n_samp][2] = z
                n_samp+=1

                #print(round(sample[0]/64,2),round(sample[1]/64,2),dist,X,Y,z)
                #if(len(samp)%1000 == 0):
                #    print(time.time() - time_ref,len(samp),ang1,ang2)

                if(n_samp%1000 == 0):
                    print(time.time() - time_ref,n_samp,ang1,ang2)
        except:
            print("ERROR... en algo")
#print(samp)
#print(len(samp))
#print(len(samp)/t_samp)

print(samp)
print(n_samp)
print(n_samp/t_samp)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(samp)

o3d.io.write_point_cloud("sync.ply", pcd)
o3d.visualization.draw_geometries([pcd])