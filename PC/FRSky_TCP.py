from sbus_receiver_pi import SBUSReceiver
import socket
from struct import pack

def boton_3p(val:int,out_min,out_med,out_max,lim_min=582,lim_max=1401):
    if(val > lim_min and val < lim_max):
        return out_med
    elif(val > lim_max):
        return out_max
    elif(val < lim_min):
        return out_min
    else:
        return out_med
    
#sbus_port = "COM7"
#Hexapod_ip = "rpi0.local"

sbus_port = "/dev/ttyUSB0"
Hexapod_ip = "localhost"

Hexapod_port = 10000

sbus = SBUSReceiver(sbus_port) 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (Hexapod_ip, Hexapod_port)

Hexapod_vals = list([0,0,0,0,0,0,0,0,1200,700,700])
message = pack(">BhhhhhhhHHH",*Hexapod_vals)

estado = True
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
try:    
    while(estado):
        if(sbus.update()):
            if(sbus.failSafeStatus == sbus.SBUS_SIGNAL_OK):
                Hexapod_vals[0] = sbus.boton_norm(sbus.sbusChannels[4]) > 0 #ON
                Hexapod_vals[9] = boton_3p(sbus.sbusChannels[5],400,600,1000) #Z
                Hexapod_vals[10] = boton_3p(sbus.sbusChannels[6],200,400,600) #arco
                Hexapod_vals[8] = round(sbus.scal(sbus.sbusChannels[7],172,1811,900,2000)) #H

                modo = sbus.boton_norm(sbus.sbusChannels[8])
                if(modo == -1):
                    Hexapod_vals[1] = round(sbus.scal(sbus.sbusChannels[1],172,1811,1000,-1000))
                    Hexapod_vals[2] = round(sbus.scal(sbus.sbusChannels[2],172,1811,-1000,1000))

                    Hexapod_vals[6] = 0
                    Hexapod_vals[7] = 0

                    Hexapod_vals[3] = 0
                    Hexapod_vals[4] = 0
                    Hexapod_vals[5] = 0
                elif(modo == 0):
                    Hexapod_vals[1] = round(sbus.scal(sbus.sbusChannels[1],172,1811,1000,-1000))
                    Hexapod_vals[2] = round(sbus.scal(sbus.sbusChannels[2],172,1811,-1000,1000))

                    Hexapod_vals[6] = 0
                    Hexapod_vals[7] = 0

                    Hexapod_vals[3] = round(sbus.scal(sbus.sbusChannels[0],172,1811,1500,-1500))
                    Hexapod_vals[4] = 0
                    Hexapod_vals[5] = round(sbus.scal(sbus.sbusChannels[3],172,1811,2500,-2500))
                elif(modo == 1):
                    Hexapod_vals[1] = 0
                    Hexapod_vals[2] = 0

                    Hexapod_vals[6] = round(sbus.scal(sbus.sbusChannels[1],172,1811,-800,800))
                    Hexapod_vals[7] = round(sbus.scal(sbus.sbusChannels[2],172,1811,800,-800))

                    Hexapod_vals[3] = round(sbus.scal(sbus.sbusChannels[0],172,1811,1500,-1500))
                    Hexapod_vals[4] = 0
                    Hexapod_vals[5] = round(sbus.scal(sbus.sbusChannels[3],172,1811,2500,-2500))
                else:
                    Hexapod_vals[1] = 0
                    Hexapod_vals[2] = 0
                    
                    Hexapod_vals[6] = 0
                    Hexapod_vals[7] = 0

                    Hexapod_vals[3] = 0
                    Hexapod_vals[4] = 0
                    Hexapod_vals[5] = 0
                
                #if(len(Hexapod_vals) == 11):
                message = pack(">BhhhhhhhHHH",*Hexapod_vals)

                sock.sendall(message)
                Respuesta = sock.recv(4)

finally:
    print('closing socket')
    sock.close()

    


"""
Variables Hexapod
ON/OFF
Movimiento X,Y
Rotacion X,Y,Z
cuerpo H, DX,DY
Pie Z, arco

ON,X,Y,RX,RY,XZ,H,DX,DY,Z,arco,speed

Variable, formato, escala,descripcion
0 : ON: b , 1:1 , ON/OFF del robot
1 : X : h , 1:1 , Direccional en X
2 : Y : h , 1:1 , Direccional en Y
3 : RX: h , 1:1000 , Rotacion X en rad
4 : RY: h , 1:1000 , Rotacion Y en rad
5 : XZ: h , 1:1000 , Rotacion Z en rad
6 : DX: h , 1:10 , Desplazamiento X, en mm
7 : DY: h , 1:10 , Desplazamiento Y, en mm
8 : H : H , 1:10 , altura del cuerpo en mm
9 : Z : H , 1:10 , Altura del pie, en mm
10: arco:  H , 1:10 , desplazamiento del pie, en mm

"""