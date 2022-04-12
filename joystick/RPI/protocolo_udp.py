import struct
import socket
import time

#Formato de los paquetes
#byte[0] = primer byte de sincronisacion
#byte[1] = segundo byte de sincronisacion
#byte[2] = Tipo de comando
#byte[3] = formato de los datos
#byte[4] = numero de datos
#byte[5:] = datos

class pro_UDP():
    def __init__(self,synq_Byte1 = 254,synq_Byte2 = 252):
        self.synq_Byte1 = synq_Byte1
        self.synq_Byte2 = synq_Byte2

    def send_command(self,conn:socket.socket,tipo_command:int,tipo_dato:str,buffer) -> bool:
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
            #R = self.s.sendto(msg_tx,(self.ip,self.port))
            #if(R == len(msg_tx)):
            #    return True
            #else:
            #    return False

            conn.sendall(msg_tx)
            return True
        except:
            return False

        
    def read_command(self,conn:socket.socket,time_out = 0.02):
        time_ref = time.time()
        while (time.time()-time_ref < time_out):
            try:
                #C = self.s.recv(4096)
                C = conn.recv(550)
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
                pass

        return None, None
