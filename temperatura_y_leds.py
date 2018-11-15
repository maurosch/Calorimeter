import os.path
import pandas as pd
import datetime
import time
import numpy
import max6675
from random import randint
import RPi.GPIO as GPIO

#------INICIALIZAMOS TERMOMETRO------
cs_pin = 4 #chip select
clock_pin = 24
data_pin = 25
units = "c"
thermocouple = MAX6675(cs_pin, clock_pin, data_pin, units)
GPIO.setmode(GPIO.BCM) 
led_1 = 19
led_2 =
led_3 =
led_4 =
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
GPIO.setup(led_3, GPIO.OUT)
GPIO.setup(led_4, GPIO.OUT)
GPIO.output(led_1, GPIO.HIGH)
GPIO.output(led_2, GPIO.HIGH)
GPIO.output(led_3, GPIO.HIGH)
GPIO.output(led_4, GPIO.HIGH)

while True:
    tc = thermocouple.get()
    file = open("temp_bloque","w")
	file.write(str(tc))
	file.close()        
    time.sleep(0.5)

    GPIO.output(led_1, GPIO.LOW)
    GPIO.output(led_2, GPIO.LOW)
    GPIO.output(led_3, GPIO.LOW)
    GPIO.output(led_4, GPIO.LOW)
    if tc > 20:
        GPIO.output(led_1, GPIO.HIGH)
        if tc > 40:
            GPIO.output(led_2, GPIO.HIGH)
            if tc > 60:
                GPIO.output(led_3, GPIO.HIGH)
                if tc > 80:
                    GPIO.output(led_4, GPIO.HIGH)
thermocouple.cleanup()


    

