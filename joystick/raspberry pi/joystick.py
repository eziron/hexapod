import math

import json
from time import sleep
import serial

class control_joystick:
    modos = json.loads("{}")
    device_conf = json.loads("{}")
    device_value = json.loads("{}")

    arduino_conf = json.loads("{}")
    arduino_value = json.loads("{}")
    device = ""

    W_id = "W"
    R_id = "Z"

    def __init__(self,device):

        self.device = device

        file = open("modos.json","r")
        self.modos = json.loads(file.read())
        file.close()

        file = open("device_config.json","r")
        self.device_conf = json.loads(file.read())
        file.close()

        file = open("arduino_config.json")
        self.arduino_conf = json.loads(file.read())
        file.close()

        index = list(self.arduino_conf["variables"])
        for x in index:
            self.arduino_value[x] = self.arduino_conf["variables"][x]["value"]

        index_device = list(self.device_conf)
        for x in index_device:
            self.device_value[x] = {}

        index = list(self.device_conf[device]["variables"])
        for x in index:
            self.device_value[device][x] = self.device_conf[device]["variables"][x]["value"]

        self.W_id = str(self.arduino_conf["coneccion"]["write_id"])
        self.R_id = str(self.arduino_conf["coneccion"]["read_id"])

        self.arduino = serial.Serial(self.arduino_conf["coneccion"]["port"],self.arduino_conf["coneccion"]["baudrate"])
        self.arduino.timeout = 0.1
        self.arduino.reset_input_buffer()
        self.arduino.reset_output_buffer()
        sleep(2)

        self.write_arduino(self.arduino_conf["variables"])
        sleep(0.1)

        self.write_arduino(self.modos[device]["arduino"])
        sleep(0.1)


    def write_arduino(self,msg):
        msg = str(msg)
        self.arduino.write(str(self.W_id+msg).encode('ascii'))

    def read_arduino(self):
        try:
            self.arduino.flush()
            msg = self.arduino.readline().decode().replace("\'","\"")

            if(msg != ""):
                valores = json.loads(msg)

                index = list(valores)

                for x in index:
                    self.arduino_value[x] = valores[x]
                
                self.recargar_device()
            
            self.arduino.write(self.R_id.encode())
        except:
            print("error lectura arduino")
            self.arduino.reset_input_buffer
            self.arduino.reset_output_buffer

    def recargar_device(self):
        index = list(self.device_value[self.device])
        
        for x in index:
            modo = self.modos[self.device]["salidas"][x]["modo"]
            if(modo == "directo"):
                self.device_value[self.device][x] = self.arduino_value[self.modos[self.device]["salidas"][x]["entrada"]]
            elif(modo == "HSV_to_RGB"):
                h = self.joystick_values(self.modos[self.device]["salidas"][x]["h"])
                s = self.joystick_values(self.modos[self.device]["salidas"][x]["s"])
                v = self.joystick_values(self.modos[self.device]["salidas"][x]["v"])
                self.device_value[self.device][x] = self.HSV_to_RGB(h,s,v)

    def joystick_values(self,variable):
        variables_arduino = list(self.arduino_value)
        if(variable in variables_arduino):
            return(self.arduino_value[variable])
        else:
            return(variable)
    def HSV_to_RGB(self,h, s=1, v=1):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return [r, g, b]
            