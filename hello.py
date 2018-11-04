from flask import Flask
from flask import render_template
from flask import request
import configparser
import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen
import subprocess
import socket
#from gpiozero import LED, Button

app = Flask(__name__)

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

@app.route('/')
def inicio():
    return render_template('index.html', ip_addr=get_ip())

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
    mypath = 'static/plots_pdf/calor_especifico'
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


# --------------------------ENFRIAMIENTO--------------------------

@app.route('/enfriamiento')
def index_enfriamiento():
    return render_template('index_enfriamiento.html', ip_addr=get_ip())

@app.route('/enfriamiento/start')
def enfriamiento_start():
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    return render_template('graficoNewton.html', configCalorimetro=configCalorimetro)
#    if os.path.exists("lock") == False:
#        p = subprocess.Popen(["python", 'coefNewton.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    else:
#        file = open("lock", "r")
#        text_file = file.read()
#        if text_file == "COEFICIENTE_CALORICO":
#            return redirect(url_for('start'))
#        if text_file == "COEFICIENTE_NEWTON":
#            return render_template('graficoNewton.html', configCalorimetro=configCalorimetro)
#        return render_template('error.html')

@app.route('/enfriamiento/resultados')
def enfriamiento_resultados():
    mypath = 'static/plots_pdf/enfriamiento'
    experimentos_pasados = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range(len(experimentos_pasados)):
        experimentos_pasados[i] = experimentos_pasados[i].split('.', 1)[0]
    return render_template('resultados.html', experimentos_pasados=experimentos_pasados)

@app.route('/enfriamiento/config', methods=['POST', 'GET'])
def enfriamiento_config():
    text = ""
    if request.method == 'POST':
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'masa_agua': request.form['masa_agua'], 'masa_material': request.form['masa_material'], 'calor_especifico_agua': 4.186, 'temp_inicial_agua': request.form['temp_inicial_agua'], 'temp_inicial_material': request.form['temp_inicial_material']}
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
        text = "CONFIGURACIÓN GUARDADA"
    
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')

    return render_template('config.html', text=text, configCalorimetro=configCalorimetro)

@app.route('/shutdown')
def shutdown():
    return "APAGADO"
