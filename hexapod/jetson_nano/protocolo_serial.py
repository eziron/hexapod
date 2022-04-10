import struct
from serial import Serial
from time import time
import math

#Formato de los paquetes
#byte[0] = primer byte de sincronisacion
#byte[1] = segundo byte de sincronisacion
#byte[2] = Tipo de comando
#byte[3] = formato de los datos
#byte[4] = numero de datos
#byte[5:] = datos

class pro_Serial():
    def __init__(self,Serial:Serial,synq_Byte1 = 254,synq_Byte2 = 252):
        self.Serial = Serial
        self.synq_Byte1 = synq_Byte1
        self.synq_Byte2 = synq_Byte2

    def send_command(self,tipo_command:int,tipo_dato:str,buffer) -> bool:
        try:
            if(isinstance(buffer,list)):
                len_msg = len(buffer)
                if(len_msg == 0):
                    return(False)
            else:
                len_msg = 1
                buffer = [buffer]
        
        
            msg_tx = struct.pack(
                ">BBBsB"+(tipo_dato*len_msg),
                self.synq_Byte1,#B
                self.synq_Byte2,#B
                tipo_command,#B
                tipo_dato.encode("ascii"),#c
                len_msg,#B
                *buffer
                )
            self.Serial.write(msg_tx)
            return True
        except:
            return False

        
    def read_command(self):
        C = self.Serial.read(1)
        if(not (C is None)):
            if(len(C) == 1):
                if(C[0] == self.synq_Byte1):
                    C = self.Serial.read(1)
                    if(not (C is None) and (C[0] == self.synq_Byte2)):
                        info_bytes = self.Serial.read(3)
                        if(not info_bytes is None):
                            buffer_type = chr(info_bytes[1])*info_bytes[2]

                            buffer_len = struct.calcsize(">"+buffer_type)
                            buffer_bytes = self.Serial.read(buffer_len)

                            if(not buffer_bytes is None):
                                buffer_values = struct.unpack(">"+buffer_type,buffer_bytes)
                                return int(info_bytes[0]),list(buffer_values)

        return None, None
    
    def send_duty(self,duty_vals:list):
        if(len(duty_vals) == 18):
            self.send_command(1,"H",duty_vals)

            tipo,buffer = self.read_command()
            if(not (tipo is None or buffer is None)):
                if(tipo == 1 and len(buffer) == 2 and buffer[0] == 5 and buffer[1] == 5):
                    return True
        
        return False

    def ping(self,buff=[1,2,3]):
        time_ref = time()
        self.send_command(0,"B",buff)
        tipo_resp,buff_resp = self.read_command()
        if(not (tipo_resp is None or buff_resp is None) and (tipo_resp == 0) and (len(buff_resp) == len(buff))):
            for i in range(len(buff)):
                if(buff[i]+1 != buff_resp[i]):
                    return None

            return (time()-time_ref)
        
        return None

    def star_lidar(self,mode:int,speed1:int,speed2:int):
        self.send_command(3,"B",[mode,speed1,speed2])

        while(True):
            tipo,buffer = self.read_command()
            if(not (tipo is None or buffer is None)):
                if(tipo == 3 and len(buffer) == 2 and buffer[0] == 5 and buffer[1] == 5):
                    print("LIDAR STAR: INICIADO")
                    return True
                elif (tipo == 3 and len(buffer) == 2 and buffer[0] == 0 and buffer[1] == 0):
                    print("LIDAR STAR: error al inicial")
                    return False
            else:
                print("LIDAR STAR: time out")
                return False
    
    def stop_lidar(self):
        self.send_command(3,"B",[0,0,0])

        while(True):
            tipo,buffer = self.read_command()
            if(not (tipo is None or buffer is None)):
                if(tipo == 3 and len(buffer) == 2 and buffer[0] == 5 and buffer[1] == 5):
                    print("LIDAR STOP: error al detener")
                    return None
                elif (tipo == 3 and len(buffer) == 2 and buffer[0] == 0 and buffer[1] == 0):
                    print("LIDAR STOP: Detenido")
                    return None
            else:
                print("LIDAR STOP: time out")
                return None

    def read_lidar(self):
        if(self.Serial.in_waiting):
            tipo,sample = self.read_command()
            if(not (tipo is None or sample is None)):
                if(tipo == 127 and len(sample) == 5):
                    dist = sample[0]/4
                    ang1 = math.radians(sample[1]/64)
                    ang2 = math.radians((sample[2]/64)-45)
                    

                    if(dist > 0 and dist < 8000):
                        x = math.sin(ang1)*dist
                        z = math.cos(ang1)*dist

                        hipo = abs(x)
                        ang = math.atan2(0,x)+(ang2-math.pi/2)

                        X = math.sin(ang)*hipo
                        Y = math.cos(ang)*hipo 

                        return [X,Y,z]
        return None