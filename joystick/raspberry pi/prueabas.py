import spidev
from time import time_ns
import struct

spi_bus = 1
spi_device = 2

spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

tx_bytes = bytearray(304)

#count = 0
#t_sap = 10
#t_sap_ns = t_sap*(10**9)
#ns_ref = time_ns()
#while(time_ns()-ns_ref < t_sap_ns):
tx_bytes[2] = 64

rx_byte = spi.xfer2(tx_bytes)
if(rx_byte[0] == 200 and rx_byte[1] == 127):
    #print(struct.calcsize("l"*18))
    #print(len(rcv_byte))
    #print(type(rcv_byte))
    #print(rcv_byte)
    #print(bytes(rcv_byte))
    print(struct.unpack(">"+"l"*18,bytes(rx_byte[2:74])))
    #count += 1
else:
    print("error")
    print(rx_byte[0:74])

#print(count)
#print(count/t_sap)
#print((t_sap*1000)/count)