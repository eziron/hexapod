import struct
from serial import Serial
from time import time

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