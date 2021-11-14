from socket import *
import serial
from time import sleep
from time import time_ns

arduino = serial.Serial("/dev/ttyS0",250000)
arduino.timeout = 0.01
arduino.reset_input_buffer()
arduino.reset_output_buffer()
sleep(2)

s = socket(AF_INET, SOCK_DGRAM)
s.connect(('192.168.1.106', 8888))


ns_ref = time_ns()
count = 0

t_sap = 20
t_sap_ns = t_sap*(10**9)
while(time_ns()-ns_ref < t_sap_ns):

    arduino.write(b"Z")
    s.send(arduino.readline())
    count += 1

print(count)
print(count/t_sap)
print((t_sap*1000)/count)