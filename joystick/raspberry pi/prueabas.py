import spidev
from time import time_ns
import struct

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

send_byte = bytearray(73)

ns_ref = time_ns()
count = 0
t_sap = 1
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):
    rcv_byte = spi.readbytes(73)
    #rcv_values = struct.unpack("<"+"l"*17,send_byte[1:73])
    print("___",count, len(rcv_byte),type(rcv_byte),"_",rcv_byte,"---")
    count += 1
    
print(count)
print(count/t_sap)
print((t_sap*1000)/count)