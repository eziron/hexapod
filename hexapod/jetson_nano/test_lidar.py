from time import sleep
from rplidar_copy import RPLidar
lidar = RPLidar('/dev/ttyUSB0',timeout=5)

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

sleep(10)

lidar.set_pwm(1023)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    for j in scan:
        print(j)
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()