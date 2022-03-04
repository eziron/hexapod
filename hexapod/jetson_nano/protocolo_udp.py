import struct
import socket
import fcntl, os

#Formato de los paquetes
#byte[0] = primer byte de sincronisacion
#byte[1] = segundo byte de sincronisacion
#byte[2] = Tipo de comando
#byte[3] = formato de los datos
#byte[4] = numero de datos
#byte[5:] = datos

class pro_Serial():
    def __init__(self,s:socket.socket,synq_Byte1 = 254,synq_Byte2 = 252):
        fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        self.s = s
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
            self.s.send(msg_tx)
            return True
        except:
            return False

        
    def read_command(self):
        try:
            C = self.s.recv(1)
            if(len(C) == 1):
                if(C[0] == self.synq_Byte1):
                    C = self.s.recv(1)
                    if(C[0] == self.synq_Byte2):
                        info_bytes = self.s.recv(3)
                        if(len(info_bytes) == 3):
                            buffer_type = chr(info_bytes[1])*info_bytes[2]

                            buffer_len = struct.calcsize(">"+buffer_type)
                            buffer_bytes = self.s.recv(buffer_len)

                            if(len(buffer_bytes) == buffer_len):
                                buffer_values = struct.unpack(">"+buffer_type,buffer_bytes)
                                return int(info_bytes[0]),list(buffer_values)
        except:
            return None, None
            
        return None, None