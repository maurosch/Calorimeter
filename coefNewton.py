import os
import pandas as pd
import datetime
import time
import numpy
from math import log
import max6675
from random import randint
import RPi.GPIO as GPIO
import configparser
import signal

#https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

def obtenerTemp():
    file = open('temp_term','r')
    temp_str = file.read()
    file.close()
    return float(temp_str)

def end_thread(sig_num, stack):
    raise Exception("Finalizando...")

def main(start_event, end_event):
    signal.signal(signal.SIGTERM, end_thread)
    while True:
        start_event.wait()

        #----------------EMPEZAMOS EL EXPERIMENTO----------------
        with open('numExp.txt','r+') as f:
            numExp = f.read()
            numExp = int(numExp)
            f.seek(0)
            f.write(str(numExp+1))

        configCalorimetro = configparser.ConfigParser()
        configCalorimetro.read('config.txt')
        temp_inicial_material = configCalorimetro['DEFAULT']['temp_inicial_material']
        temp_inicial_material = float(temp_inicial_material)
        temp_ambiente = configCalorimetro['DEFAULT']['temp_ambiente']
        temp_ambiente = float(temp_ambiente)

        temp_material = []
        ejeTiempo = []
        tiempoInicio = time.time()

        temp_material.append(temp_ambiente)
        ejeTiempo.append(0)

        temp_str = obtenerTemp()

        relayNumberIN = 18
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(relayNumberIN, GPIO.OUT)

        if temp_str < temp_inicial_material:
            GPIO.output(relayNumberIN, GPIO.LOW)


        while temp_str+5 < temp_inicial_material and temp_str < 200 and not end_event.is_set():
            temp_str = obtenerTemp()
            time.sleep(0.5)
            temp_material.append(float(temp_str))
            ejeTiempo.append(time.time()-tiempoInicio)

        GPIO.setup(relayNumberIN, GPIO.IN)
          
        while not end_event.is_set(): 
            temp_str = obtenerTemp()
            temp_material.append(float(temp_str))
            ejeTiempo.append(time.time()-tiempoInicio)
            time.sleep(0.5)
            
            
        tiempoTranscurrido = time.time() - tiempoInicio
        if temp_inicial_material > temp_ambiente:
            coefEnfriamiento = log(temp_inicial_material-temp_ambiente) / tiempoTranscurrido 

        #GUARDAMOS DATOS
        df = pd.DataFrame({'Temperatura Material':temp_material}, ejeTiempo)
        df.to_csv('/home/pi/calorimetro/static/plots/Exp_'+str(numExp)+".csv")
        plot = df.plot(style="*-", ylim={0,200})
        plot.get_figure().savefig('/home/pi/calorimetro/static/plots/Exp_'+str(numExp)+'.pdf', format='pdf')
