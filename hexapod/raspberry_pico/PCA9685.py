import ustruct
from time import sleep, sleep_us
from utime import sleep_ms, ticks_us
from machine import Pin, I2C
class pca9685:
    A=1.09971
    freq_clk = 25123059.74960
    i2c: I2C
    def __init__(self, i2c: I2C, address:int=0x40, freq_refr:int=50, freq_clk=None, A=None):
        
        self.i2c = i2c 
        self.address = address
        self.reset()
        self.set_freq(freq_refr,freq_clk,A)

    def _write(self, address, value):
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self._write(0x00, 0x00) # Mode1
        sleep(0.1)

    def set_freq(self, freq_refr:int, freq_clk=None,A=None):
        if(not freq_clk is None):
            self.freq_clk = freq_clk
        if(not A is None):
            self.A=A

        prescale = self._contrain(round(self.freq_clk/(4096.0*freq_refr) - self.A),0,255)
        self.freq_refr = self.freq_clk/((prescale+self.A)*4096.0)
        self.set_prescale(prescale)
        
    def set_prescale(self,prescale:int):
        prescale = self._contrain(round(prescale),0,255)
        old_mode = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        sleep_us(500)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on
        sleep_ms(1)

    def pwm(self, index:int, on=None, off=None):
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index,  data)

    def massive_pwm(self, array_vals:list=[]):
        # array format
        # [
        #   [on,off], values for servo 0
        #   [on,off], values for servo 1
        #   [on,off], values for servo 2
        #   [on,off], values for servo 3
        #   ...
        #   [on,off]  values for servo 15
        # ]

        if(len(array_vals) == 16):
            one_list = []
            for x in array_vals:
                one_list.append(x[0])
                one_list.append(x[1])
            data = ustruct.pack('<'+'H'*16*2, *one_list)
            self.i2c.writeto_mem(self.address, 0x06,  data)
        else:
            data = self.i2c.readfrom_mem(self.address, 0x06, 64)
            return ustruct.unpack('<'+'H'*16*2, data)
    
    def _contrain(self,value,min_val,max_val):
        if(value > max_val):
            return max_val
        if(value < min_val):
            return min_val
        return value

    def set_duty_us(self,index:int ,duty_us:int):
        count_val = round((duty_us*self.freq_refr*4096)/1000000)
        self.pwm(index,0,self._contrain(count_val,0,4096))

    def set_massive_us(self,duty_us_array=[]):
        # array format
        # [duty_0, duty_1, duty_2...duty_15]

        if(len(duty_us_array) == 16):
            duty_count_array = []
            for n in range(16):
                count_val = round((duty_us_array[n]*self.freq_refr*4096)/1000000)
                duty_count_array.append([0,self._contrain(count_val,0,4096)])
            
            self.massive_pwm(duty_count_array)
    
    def disable_servo(self):
        self.massive_pwm([
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0]
        ])

    def auto_calibration(self,feedback_pin:Pin,feedback_port:int,sample_time:float=1.0,print_samp:bool = False):
        samples = []
        sample_time = sample_time*1000000
        for prescale in range(3,256,1):
            self.set_prescale(prescale)
            self.pwm(feedback_port,0,2048)
            sleep_ms(100)
            frec_prom = 0.0
            samples_count = 0.0
            estado = 0
            sample_us_ref = ticks_us()
            freq_us_ref = 0
            while(ticks_us()-sample_us_ref < sample_time):
                if(feedback_pin.value() and not estado):
                    s = ticks_us()
                    if(freq_us_ref != 0):
                        frec_prom += 1000000.0/(s-freq_us_ref)
                        samples_count += 1.0
                    freq_us_ref = s
                    estado = 1

                elif(not feedback_pin.value() and estado):
                    estado = 0
            if(samples_count > 0):
                frec_prom = frec_prom/samples_count
                samples.append([prescale,frec_prom])
                if(print_samp):
                    print("sample_value: ",prescale,samples_count,frec_prom)
        L_samp = len(samples)
        A = 0.0
        A_prom = 0.0
        clk = 0.0
        clk_prom = 0.0
        samples_count = 0
        
        for n in range(L_samp-1):
            for nn in range(n+1,L_samp,1):
                A = ((samples[n][0]*samples[n][1])-(samples[nn][0]*samples[nn][1]))/(samples[n+1][1]-samples[n][1])
                clk = 4096.0*(samples[n][0]+A)*samples[n][1]
                if(A >= 0 and A <= 2):
                    samples_count += 1
                    A_prom += A
                    clk_prom += clk
        
        A_prom = A_prom/samples_count
        clk_prom = clk_prom/samples_count
        self.A = A_prom
        self.freq_clk = clk_prom
        print("final values: A=","{:.5f}".format(round(A_prom,5))," / freq_clk=","{:.5f}".format(round(clk_prom,5)))
