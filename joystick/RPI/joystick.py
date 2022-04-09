from array import array
import math
import struct
import json
import time
import numpy as np

class control_joystick:
    modos = json.loads("{}")
    device_conf = json.loads("{}")
    device_value = json.loads("{}")

    arduino_conf = json.loads("{}")
    arduino_value = json.loads("{}")
    device = "hexapod"

    modo_values = {
        "normal":0,
        "mantenido":1,
        "incremental":1,
        "circular":2,
        "RAW":3
    }

    time_ref = 0

    def __init__(self,spi,device="hexapod"):

        self.device = device
        self.spi = spi

        file = open("/home/pi/Desktop/hexapod/joystick/RPI/modos.json","r")
        self.modos = json.loads(file.read())
        file.close()

        file = open("/home/pi/Desktop/hexapod/joystick/RPI/device_config.json","r")
        self.device_conf = json.loads(file.read())
        file.close()

        file = open("/home/pi/Desktop/hexapod/joystick/RPI/arduino_config.json")
        self.arduino_conf = json.loads(file.read())
        file.close()

        index = list(self.arduino_conf)
        for x in index:
            self.arduino_value[x] = self.arduino_conf[x]["value"]

        index = list(self.device_conf)
        for x in index:
            self.device_value[x] = {}

        index = list(self.device_conf[device])
        for x in index:
            self.device_value[device][x] = self.device_conf[device][x]["value"]

        self.zero_buffer = list(np.zeros(74,int))
        for n in range(len(self.zero_buffer)):
            self.zero_buffer[n] = 0

        self.time_ref = time.time()

    def write_arduino(self):
        tx_value = []
        tx_value.append(self.arduino_conf["x_izq"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["x_izq"]["modo"]])
        tx_value.append(self.arduino_conf["x_izq"]["min"])
        tx_value.append(self.arduino_conf["x_izq"]["max"])
        tx_value.append(self.arduino_conf["x_izq"]["PPS"])
        tx_value.append(self.arduino_conf["x_izq"]["centro"])

        tx_value.append(self.arduino_conf["y_izq"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["y_izq"]["modo"]])
        tx_value.append(self.arduino_conf["y_izq"]["min"])
        tx_value.append(self.arduino_conf["y_izq"]["max"])
        tx_value.append(self.arduino_conf["y_izq"]["PPS"])
        tx_value.append(self.arduino_conf["y_izq"]["centro"])

        tx_value.append(self.arduino_conf["x_der"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["x_der"]["modo"]])
        tx_value.append(self.arduino_conf["x_der"]["min"])
        tx_value.append(self.arduino_conf["x_der"]["max"])
        tx_value.append(self.arduino_conf["x_der"]["PPS"])
        tx_value.append(self.arduino_conf["x_der"]["centro"])

        tx_value.append(self.arduino_conf["y_der"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["y_der"]["modo"]])
        tx_value.append(self.arduino_conf["y_der"]["min"])
        tx_value.append(self.arduino_conf["y_der"]["max"])
        tx_value.append(self.arduino_conf["y_der"]["PPS"])
        tx_value.append(self.arduino_conf["y_der"]["centro"])

        tx_value.append(self.arduino_conf["cruz_izq_h"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["cruz_izq_h"]["modo"]])
        tx_value.append(self.arduino_conf["cruz_izq_h"]["continuo"])
        tx_value.append(self.arduino_conf["cruz_izq_h"]["min"])
        tx_value.append(self.arduino_conf["cruz_izq_h"]["max"])
        tx_value.append(self.arduino_conf["cruz_izq_h"]["PPS"])

        tx_value.append(self.arduino_conf["cruz_izq_v"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["cruz_izq_v"]["modo"]])
        tx_value.append(self.arduino_conf["cruz_izq_v"]["continuo"])
        tx_value.append(self.arduino_conf["cruz_izq_v"]["min"])
        tx_value.append(self.arduino_conf["cruz_izq_v"]["max"])
        tx_value.append(self.arduino_conf["cruz_izq_v"]["PPS"])

        tx_value.append(self.arduino_conf["cruz_der_h"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["cruz_der_h"]["modo"]])
        tx_value.append(self.arduino_conf["cruz_der_h"]["continuo"])
        tx_value.append(self.arduino_conf["cruz_der_h"]["min"])
        tx_value.append(self.arduino_conf["cruz_der_h"]["max"])
        tx_value.append(self.arduino_conf["cruz_der_h"]["PPS"])

        tx_value.append(self.arduino_conf["cruz_der_v"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["cruz_der_v"]["modo"]])
        tx_value.append(self.arduino_conf["cruz_der_v"]["continuo"])
        tx_value.append(self.arduino_conf["cruz_der_v"]["min"])
        tx_value.append(self.arduino_conf["cruz_der_v"]["max"])
        tx_value.append(self.arduino_conf["cruz_der_v"]["PPS"])

        tx_value.append(self.arduino_conf["but_analog_izq"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_analog_izq"]["modo"]])
        tx_value.append(self.arduino_conf["but_analog_izq"]["min"])
        tx_value.append(self.arduino_conf["but_analog_izq"]["max"])

        tx_value.append(self.arduino_conf["but_analog_der"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_analog_der"]["modo"]])
        tx_value.append(self.arduino_conf["but_analog_der"]["min"])
        tx_value.append(self.arduino_conf["but_analog_der"]["max"])

        tx_value.append(self.arduino_conf["but_der_a"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_der_a"]["modo"]])
        tx_value.append(self.arduino_conf["but_der_a"]["min"])
        tx_value.append(self.arduino_conf["but_der_a"]["max"])

        tx_value.append(self.arduino_conf["but_der_b"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_der_b"]["modo"]])
        tx_value.append(self.arduino_conf["but_der_b"]["min"])
        tx_value.append(self.arduino_conf["but_der_b"]["max"])

        tx_value.append(self.arduino_conf["but_der_c"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_der_c"]["modo"]])
        tx_value.append(self.arduino_conf["but_der_c"]["min"])
        tx_value.append(self.arduino_conf["but_der_c"]["max"])

        tx_value.append(self.arduino_conf["but_cruz_der"]["value"])
        tx_value.append(self.modo_values[self.arduino_conf["but_cruz_der"]["modo"]])
        tx_value.append(self.arduino_conf["but_cruz_der"]["min"])
        tx_value.append(self.arduino_conf["but_cruz_der"]["max"])

        tx_value.append(self.arduino_conf["analog_A"]["min"])
        tx_value.append(self.arduino_conf["analog_A"]["max"])

        tx_value.append(self.arduino_conf["analog_B"]["min"])
        tx_value.append(self.arduino_conf["analog_B"]["max"])

        tx_bytes = struct.pack(">"+"l"*len(tx_value),*tx_value)
        self.spi.writebytes(tx_bytes)
        self.time_ref = time.time()

    def read_arduino(self):
        while(time.time()-self.time_ref<0.0005):
            time.sleep(0.000001)

        rx_byte = self.spi.readbytes(74)
        self.time_ref = time.time()
        if(rx_byte[0] == 200 and rx_byte[1] == 127):
            rx_values = struct.unpack(">"+"l"*18,bytes(rx_byte[2:]))

            self.arduino_value["x_izq"]=rx_values[0]
            self.arduino_value["y_izq"]=rx_values[1]
            self.arduino_value["x_der"]=rx_values[2]
            self.arduino_value["y_der"]=rx_values[3]
            self.arduino_value["cruz_izq_h"]=rx_values[4]
            self.arduino_value["cruz_izq_v"]=rx_values[5]
            self.arduino_value["cruz_der_h"]=rx_values[6]
            self.arduino_value["cruz_der_v"]=rx_values[7]
            self.arduino_value["but_analog_izq"]=rx_values[8]
            self.arduino_value["but_analog_der"]=rx_values[9]
            self.arduino_value["but_der_a"]=rx_values[10]
            self.arduino_value["but_der_b"]=rx_values[11]
            self.arduino_value["but_der_c"]=rx_values[12]
            self.arduino_value["but_cruz_der"]=rx_values[13]
            self.arduino_value["cruz_izq"]=rx_values[14]
            self.arduino_value["cruz_der"]=rx_values[15]
            self.arduino_value["analog_A"]=rx_values[16]
            self.arduino_value["analog_B"]=rx_values[17]

            return True
        
        return False

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
            