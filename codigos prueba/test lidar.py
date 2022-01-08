from time import sleep
from rplidar import RPLidar
lidar = RPLidar('COM4')

info = lidar.get_info()
print(info)


health = lidar.get_health()
print(health)

health = lidar.get_health()
print(health)

health = lidar.get_health()
print(health)

sleep(1)
for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()