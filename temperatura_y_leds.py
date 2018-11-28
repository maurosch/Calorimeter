import datetime
import time
import numpy
from max6675 import MAX6675
import RPi.GPIO as GPIO
import os

os.remove("~/calorimetro/lock")
os.remove("~/calorimetro/terminar")
#------INICIALIZAMOS TERMOMETRO------
cs_pin = 13 #chip select
clock_pin = 11
data_pin = 15
units = "c"
thermocouple = MAX6675(cs_pin, clock_pin, data_pin, units, GPIO.BOARD)

while True:
    try:
        tc = thermocouple.get()
        file = open("temp_term","w+")
        file.write(str(tc))
        file.close()
        #print(str(tc))
    except Exception: 
        pass
    time.sleep(0.5)
thermocouple.cleanup()


    

