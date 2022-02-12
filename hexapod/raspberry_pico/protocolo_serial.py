import ustruct as struct
from machine import UART as serial

class pro_Serial():
    def __init__(self,Serial:serial,synq_Byte1 = 254,synq_Byte2 = 252):
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
        if(not (C is None) and (C[0] == self.synq_Byte1)):
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

        return None,None