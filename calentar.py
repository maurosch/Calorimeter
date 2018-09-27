import os.path
import pandas as pd
import datetime
import time
from random import randint
import RPi.GPIO as GPIO

if os.path.exists("lock") == False:
    
    #----------------EMPEZAMOS EL EXPERIMENTO----------------
    f = open("lock","w+")
    f.write("ARCHIVO PARA INDICAR SI ESTA CALENTANDO")
    f.close

    #---PRENDEMOS LUZ DE CALIENTE---
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, GPIO.HIGH)

    #---CALENTAMOS AGUA Y PIEZA---


    #---EMPEZAMOS EXPERIMENTO---
    start = time.time()
    temp_agua = []
    temp_material = []
    while time.time()-start < 10:
        time.sleep(0.5)
        temp_agua.append(randint(0, 9))
        temp_material.append(randint(0, 9))

   
    GPIO.output(19, GPIO.LOW)

    #CALCULAMOS CALOR ESPECIFICO


    #GUARDAMOS DATOS
    df = pd.DataFrame({'Temperatura Agua':temp_agua, 'Temperatura Material':temp_material})
    nombre = datetime.datetime.now().strftime ("%Y-%m-%d %H:%M")
    df.to_csv('static/plots_csv/'+nombre+".csv")
    plot = df.plot(style="*-")
    #plot.annotate('Calor Especifico', xy=(-12, -12), xycoords='axes points', size=14, ha='right', va='top', bbox=dict(boxstyle='round', fc='w'))
    plot.get_figure().savefig('static/plots_pdf/'+nombre+'.pdf', format='pdf')
    #----------------TERMINAMOS EL EXPERIMENTO----------------
    
    os.remove("lock")