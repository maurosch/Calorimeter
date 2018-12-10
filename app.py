from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import configparser
import os
from os import listdir
from os.path import isfile, join, splitext
from subprocess import Popen
import subprocess
import socket
from multiprocessing import Process, Event
import temperatura_y_leds
import coefNewton
#from gpiozero import LED, Button

# Inicio de experimento. Liberarlo implica que corre el experimento
start_event = Event()

# Fin del experimento. Liberarlo, luego de iniciar el experimento termina el experimento
end_event = Event()

# Subprocesos. Usando multiprocessing son procesos python separados que pueden ser sincronizados
temp_process = Process(target=temperatura_y_leds.main)
coef_exp_process = Process(target=coefNewton.main,
                              args=(start_event, end_event))

# Antes de iniciar todo, levanto los procesos
temp_process.start()
coef_exp_process.start()

app = Flask(__name__)

#---------------FUNCION PARA OBTENER LA IP LOCAL---------------
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
#--------------------------------------------------------------

@app.route('/')
def inicio():
    return redirect(url_for('index_enfriamiento'))

@app.route('/shutdown')
def shutdown():
    temp_process.join()
    coef_exp_process.join()
    os.system("sudo shutdown -h now")
    return "APAGADO"

@app.route('/temp_term')
def temp_term():
    file = open('temp_term','r')
    temp_str = file.read()
    file.close() 
    return temp_str

# --------------------------ENFRIAMIENTO--------------------------

@app.route('/enfriamiento')
def index_enfriamiento():
    return render_template('index_enfriamiento.html', ip_addr=get_ip())

@app.route('/enfriamiento/start')
def enfriamiento_start():
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    start_event.set()
    #p = subprocess.Popen(["python", 'coefNewton.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return render_template('grafico.html', configCalorimetro=configCalorimetro, ip_addr=get_ip())

@app.route('/enfriamiento/resultados')
def enfriamiento_resultados():
    mypath = 'static/plots'
    experimentos_pasados = set([splitext(f)[0] for f in listdir(mypath) if isfile(join(mypath, f))])
    return render_template('resultados.html', experimentos_pasados=experimentos_pasados)

@app.route('/enfriamiento/config', methods=['POST', 'GET'])
def enfriamiento_config():
    text = ""
    errorText = ""
    if request.method == 'POST':
        if request.form['temp_inicial_material'] > request.form['temp_ambiente']:            
            config = configparser.ConfigParser() 
            config['DEFAULT'] = {'temp_inicial_material': request.form['temp_inicial_material'], 'temp_ambiente':request.form['temp_ambiente']}
            with open('config.txt', 'w') as configfile:
                config.write(configfile)
            return redirect(url_for('enfriamiento_start'))
        errorText = "La temperatura ambiente no puede ser mayor que la deseada del material"
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    return render_template('config.html', text=text, configCalorimetro=configCalorimetro, errorText=errorText)

@app.route('/terminarExperimento')
def terminarExperimento():
    end_event.set()
    start_event.clear()
    #open('terminar','a').close()
    return render_template('analizar.html')

@app.route('/enfriamiento/resultados/verPDF')
def verPDF():
    experimento = request.args.get('file')
    return render_template('verPDF.html', experimento=experimento)

#--------------------PAGINAS CALORIMETRO (NO LAS USAMOS)--------------------
'''
@app.route('/calor_especifico')
def index_calentamiento():
    return render_template('index_calor_especifico.html', ip_addr=get_ip())

@app.route('/calor_especifico/start')
def calor_especifico_start():
    if os.path.exists("lock") == False:
        p = subprocess.Popen(["python", 'calentar.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    return render_template('grafico.html', configCalorimetro=configCalorimetro)

@app.route('/calor_especifico/resultados')
def calor_especifico_resultados():
    mypath = 'static/plots'
    experimentos_pasados = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range(len(experimentos_pasados)):
        experimentos_pasados[i] = experimentos_pasados[i].split('.', 1)[0]
    return render_template('resultados.html', experimentos_pasados=experimentos_pasados)

@app.route('/calor_especifico/config', methods=['POST', 'GET'])
def calor_especifico_config():
    text = ""
    if request.method == 'POST':
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'masa_agua': request.form['masa_agua'], 'masa_material': request.form['masa_material'], 'calor_especifico_agua': 4.186, 'temp_inicial_agua': request.form['temp_inicial_agua'], 'temp_inicial_material': request.form['temp_inicial_material']}
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
        text = "CONFIGURACIÓN GUARDADA"
    return render_template('config.html', text=text)
'''
#---------------------------------------------------------------------------

if __name__ == "__main__":
   app.run(host="0.0.0.0")
