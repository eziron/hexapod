from mpu6050 import mpu6050
from time import sleep
from math import atan2, degrees


sensor = mpu6050(0x68)
sensor.set_accel_range(sensor.ACCEL_RANGE_2G)
sensor.set_filter_range(sensor.FILTER_BW_10)

s_ref = mpu6050(0x69)
s_ref.set_accel_range(s_ref.ACCEL_RANGE_2G)
s_ref.set_filter_range(s_ref.FILTER_BW_10)

acc_acum = [[0.0,0.0,0.0],[0.0,0.0,0.0]]
acc_vals = [[0.0,0.0,0.0],[0.0,0.0,0.0]]

ang = [[0.0,0.0],[0.0,0.0]]

dic_tag = ["x","y","z"]

n_samps = 25

#for j in range(50):
while(True):
    for n in range(n_samps):
        acc_ref = s_ref.get_accel_data(True)
        acc = sensor.get_accel_data(True)

        for i in range(3):
            acc_acum[0][i] = acc_acum[0][i] + acc_ref[dic_tag[i]]/n_samps
            acc_acum[1][i] = acc_acum[1][i] + acc[dic_tag[i]]/n_samps
    
    for i in range(3):
        acc_vals[0][i] = acc_acum[0][i]
        acc_acum[0][i] = 0.0

        acc_vals[1][i] = acc_acum[1][i]
        acc_acum[1][i] = 0.0
    

    ang[0][0] = degrees(atan2(acc_vals[0][0],acc_vals[0][2]))
    ang[0][1] = degrees(atan2(acc_vals[0][1],acc_vals[0][2]))

    ang[1][0] = -degrees(atan2(acc_vals[1][0],acc_vals[1][2]))
    ang[1][1] = degrees(atan2(acc_vals[1][1],acc_vals[1][2]))


    #print(acc_vals)
    #print(ang)
    print(ang[1][0]-ang[0][0])