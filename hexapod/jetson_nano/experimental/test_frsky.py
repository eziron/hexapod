import serial


Serial = serial.Serial("/dev/ttyUSB0",100000,timeout=0.05)

estado = True
while(estado):
    try:
        data = Serial.read(23)
        print(data)
    except:
        break

Serial.close()