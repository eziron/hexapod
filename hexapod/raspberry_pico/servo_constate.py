from machine import Pin, PWM

sv16 = PWM(Pin(22,Pin.OUT))
sv16.freq(333)

#duty perfecto
#para sv2 N   - 2322 = 164gr
#para sv2 INV - 678  = 164gr

#para sv1 N   - 1056 = 130gr
#para sv1 INV - 1944  = 130gr

#para sv0 N   - 1500 = 0gr
#para sv0 INV - 1500  = 0gr

while(True):
    duty = int(input("ingerse duty: "))
    sv16.duty_ns(duty*1000)


