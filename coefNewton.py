import os.path
import pandas as pd
import datetime
import time
import numpy
import max6675
from random import randint
import RPi.GPIO as GPIO

def guardoTemp(a):
    file = open("temp_bloque","w")
	file.write(str(a))
	file.close()

if os.path.exists("lock") == False:
    #----------------EMPEZAMOS EL EXPERIMENTO----------------
    f = open("lock","w+")
    f.write("COEFICIENTE_ENFRIAMENTO")
    f.close

    #---PRENDEMOS LUZ DE FUNCIONAMIENTO---
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)

    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    temp_inicial_material = configCalorimetro['DEFAULT']['temp_inicial_material']
    
    #------INICIALIZAMOS TERMOMETRO------
    cs_pin = 4
    clock_pin = 24
    data_pin = 25
    units = "c"
    thermocouple = MAX6675(cs_pin, clock_pin, data_pin, units)
    #------------------------------------

    #----------CALENTAMOS PIEZA----------
    tc = thermocouple.get()
    while tc < temp_inicial_material and tc < 200 and os.path.exists("terminar") == False:
        tc = thermocouple.get()
        guardoTemp(tc)
        time.sleep(0.5)
    #------------------------------------

    #---EMPEZAMOS EXPERIMENTO---
    start = time.time()
    #temp_ambiente = []
    temp_material = []
    while os.path.exists("terminar") == False: 
        tc = thermocouple.get()
        guardoTemp(tc)
        time.sleep(0.5)
        temp_material.append(tc)

    #GPIO.output(19, GPIO.LOW)

    #CALCULAMOS COEFICIENTE NEWTON
    #coefNewton = np.log(Tinicial-Tamb)/t
    coefEnfriamiento = np.log(temp_inicial_material-temp_material[])/t

    #GUARDAMOS DATOS
    df = pd.DataFrame({'Temperatura Material':temp_material})
    nombre = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M")
    df.to_csv('static/plots_csv/enfriamiento/'+nombre+".csv")
    plot = df.plot(style="*-")
    #plot.annotate('Calor Especifico', xy=(-12, -12), xycoords='axes points', size=14, ha='right', va='top', bbox=dict(boxstyle='round', fc='w'))
    plot.get_figure().savefig('static/plots_pdf/enfriamiento/'+nombre+'.pdf', format='pdf')
    #----------------TERMINAMOS EL EXPERIMENTO----------------
    
    thermocouple.cleanup()
    os.remove("lock")

#CALCULAMOS COEFICIENTE ENFRIAMENTO NEWTON
    #T(t)=Tamb+(Ti-Tamb)*e^(-r*t) 
    #(T-Tamb)/(Ti-Tamb)=e^(-r*t)