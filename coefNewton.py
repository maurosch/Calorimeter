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

#https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

def obtenerTemp():
    file = open('temp_term','r')
    temp_str = file.read()
    file.close()
    return float(temp_str)


if os.path.exists("lock") == False:
    #----------------EMPEZAMOS EL EXPERIMENTO----------------
    f = open("lock","w")
    f.close

    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    temp_inicial_material = configCalorimetro['DEFAULT']['temp_inicial_material']
    temp_inicial_material = float(temp_inicial_material)
    temp_ambiente = configCalorimetro['DEFAULT']['temp_ambiente']
    temp_ambiente = float(temp_ambiente)
    
    temp_material = []  
    ejeTiempo = []
    tiempoInicio = time.time()

    temp_str = obtenerTemp()

    relayNumberIN = 18
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relayNumberIN, GPIO.OUT)

    if temp_str < temp_inicial_material:
        GPIO.output(relayNumberIN, GPIO.LOW)

    while temp_str < temp_inicial_material and temp_str < 200 and os.path.exists("terminar") == False:
        temp_str = obtenerTemp()
        time.sleep(0.5)
        temp_material.append(float(temp_str))
        ejeTiempo.append(time.time()-tiempoInicio)

    GPIO.setup(relayNumberIN, GPIO.IN)
      
    while os.path.exists("terminar") == False: 
        temp_str = obtenerTemp()
        temp_material.append(float(temp_str))
        ejeTiempo.append(time.time()-tiempoInicio)
        time.sleep(0.5)
        
    os.remove("lock")
    os.remove("terminar")

    tiempoTranscurrido = time.time() - tiempoInicio
    if temp_inicial_material > temp_ambiente:
        coefEnfriamiento = log(temp_inicial_material-temp_ambiente) / tiempoTranscurrido 

    #GUARDAMOS DATOS
    df = pd.DataFrame({'Temperatura Material':temp_material}, ejeTiempo)
    nombre = datetime.datetime.now().strftime ("%Y-%m-%d %H-%M")
    df.to_csv('static/plots_csv/enfriamiento/'+nombre+".csv")
    plot = df.plot(style="*-", ylim={0,200})
    #plot.annotate('Calor Especifico', xy=(-12, -12), xycoords='axes points', size=14, ha='right', va='top', bbox=dict(boxstyle='round', fc='w'))
    plot.get_figure().savefig('static/plots_pdf/enfriamiento/'+nombre+'.pdf', format='pdf')
