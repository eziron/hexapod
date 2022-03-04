import struct
import socket

#Formato de los paquetes
#byte[0] = primer byte de sincronisacion
#byte[1] = segundo byte de sincronisacion
#byte[2] = Tipo de comando
#byte[3] = formato de los datos
#byte[4] = numero de datos
#byte[5:] = datos

class pro_UDP():
    def __init__(self,s:socket.socket,ip:str,port:int=8888,synq_Byte1 = 254,synq_Byte2 = 252):
        self.s = s
        self.synq_Byte1 = synq_Byte1
        self.synq_Byte2 = synq_Byte2
        self.ip = ip
        self.port = port
        self.s.bind(("0.0.0.0",self.port))
        self.s.setblocking(0)

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
            self.s.sendto(msg_tx,(self.ip,self.port))
            return True
        except:
            return False

        
    def read_command(self):
        try:
            C = self.s.recv(550)
            if(len(C) > 5):
                n= 0
                while(C[n] != self.synq_Byte1 and n<len(C)):
                    n += 1

                if(C[n] == self.synq_Byte1):
                    if(C[n+1] == self.synq_Byte2):
                        buffer_type = chr(C[n+3])*C[n+4]

                        buffer_len = struct.calcsize(">"+buffer_type)

                        if(len(C) == n+buffer_len+5):
                            buffer_values = struct.unpack(">"+buffer_type,C[n+5:])
                            return int(C[n+2]),list(buffer_values)
        except:
            return None, None
            
        return None, None