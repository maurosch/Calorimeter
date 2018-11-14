import os.path
import pandas as pd
import datetime
import time
import numpy
import max6675
from random import randint
import RPi.GPIO as GPIO

#https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

'''
def mayorAparicion(arreglo)
    mayor = 0
    for i in range(len(arreglo)):
        if arreglo[i] > mayor:
            mayor = arreglo[i]
    contArreglo = [0]*(mayor+1)
    for i in range(len(arreglo)):
        contArreglo[arreglo] += 1

    mayorAparicionesCant = -1
    mayorAparicionesIndex = -1
    for i in range(len(contArreglo)):
        if mayorAparicionesCant < contArreglo[i]:
            mayorAparicionesCant = contArreglo[i]
            mayorAparicionesIndex = i
    
    return mayorAparicionesIndex
'''

def obtenerTemp()
    file = open('temp_term','r')
    temp_str = file.read()
    file.close()
    return temp_str

if os.path.exists("lock") == False:
    #----------------EMPEZAMOS EL EXPERIMENTO----------------
    f = open("lock","w")
    f.close

    #---PRENDEMOS LUZ DE FUNCIONAMIENTO---
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)

    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    temp_inicial_material = configCalorimetro['DEFAULT']['temp_inicial_material']
    temp_ambiente = configCalorimetro['DEFAULT']['temp_ambiente']
    
    #------INICIALIZAMOS TERMOMETRO------
    #cs_pin = 4 #chip select
    #clock_pin = 24
    #data_pin = 25
    #units = "c"
    #thermocouple = MAX6675(cs_pin, clock_pin, data_pin, units)
    #------------------------------------

    #----------CALENTAMOS PIEZA----------
    #tc = thermocouple.get()
    file = open('temp_term','r')
    temp_str = file.read()
    file.close() 
    while int(temp_str) < temp_inicial_material and int(temp_str) < 200 and os.path.exists("terminar") == False:
        #tc = thermocouple.get()
        #guardoTemp(tc)
        temp_str = obtenerTemp()
        time.sleep(0.5)
    #------------------------------------

    #---EMPEZAMOS EXPERIMENTO---
    tiempoInicio = time.time()
    #temp_ambiente = []
    temp_material = []
    while os.path.exists("terminar") == False: 
        temp_str = obtenerTemp()
        temp_material.append(int(temp_str))
        ejeTiempo.append(time.time()-tiempoInicio)
        time.sleep(0.5)

    tiempoTranscurrido = time.time() - tiempoInicio
    coefEnfriamiento = np.log(temp_inicial-temp_ambiente) / tiempoTranscurrido

    #GUARDAMOS DATOS
    df = pd.DataFrame({'Temperatura Material':temp_material}, ejeTiempo)
    nombre = datetime.datetime.now().strftime ("%Y-%m-%d %H-%M")
    df.to_csv('static/plots_csv/enfriamiento/'+nombre+".csv")
    plot = df.plot(style="*-")
    #plot.annotate('Calor Especifico', xy=(-12, -12), xycoords='axes points', size=14, ha='right', va='top', bbox=dict(boxstyle='round', fc='w'))
    plot.get_figure().savefig('static/plots_pdf/enfriamiento/'+nombre+'.pdf', format='pdf')
    #----------------TERMINAMOS EL EXPERIMENTO----------------
    
    #thermocouple.cleanup()
    os.remove("lock")

#CALCULAMOS COEFICIENTE ENFRIAMENTO NEWTON
    #T(t)=Tamb+(Ti-Tamb)*e^(-r*t) 
    #(T-Tamb)/(Ti-Tamb)=e^(-r*t)