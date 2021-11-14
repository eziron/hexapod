from socket import *
import spidev
from time import sleep, time_ns
import json

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('192.168.1.106', 8888))

spi_bus = 1
spi_device = 0

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

send_byte = bytearray(400)

ns_ref = time_ns()
count = 0
t_sap = 1
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):
    spi.xfer([0xFA,0xFA],1000000,1000,8)
    rcv_byte = bytearray(spi.xfer2(send_byte,1000000,0,8)).decode("UTF-8",'ignore')
    print("___",count, len(rcv_byte),len(send_byte),rcv_byte[0],rcv_byte[-1],"_",rcv_byte,"---")
    #arduino_json = json.loads(rcv_byte)
    #s.send(str(arduino_json).encode("UTF-8"))
    count += 1
    


print(count)
print(count/t_sap)
print((t_sap*1000)/count)