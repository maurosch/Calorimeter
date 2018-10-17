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

@app.route('/modos')
def modos():
    return render_template('modos.html')

@app.route('/start')
def start():
    if os.path.exists("lock") == False:
        p = subprocess.Popen(["python", 'calentar.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    configCalorimetro = configparser.ConfigParser()
    configCalorimetro.read('config.txt')
    return render_template('grafico.html', configCalorimetro=configCalorimetro)

@app.route('/startNewton')
def startNewton():
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
                    
@app.route('/data')
def data():
    file = open("temp_bloque", "r")
    text_file = file.read()
    file.close()
    return render_template('data.html', data=text_file)
    
    
@app.route('/datos')
def datos():
    mypath = 'static/plots_pdf/'
    experimentos_pasados = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range(len(experimentos_pasados)):
        experimentos_pasados[i] = experimentos_pasados[i].split('.', 1)[0]

    return render_template('datos.html', experimentos_pasados=experimentos_pasados)

@app.route('/config', methods=['POST', 'GET'])
def config():
    text = ""
    if request.method == 'POST':
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'masa_agua': request.form['masa_agua'], 'masa_material': request.form['masa_material'], 'calor_especifico_agua': 4.186, 'temp_inicial_agua': request.form['temp_inicial_agua'], 'temp_inicial_material': request.form['temp_inicial_material']}
        with open('config.txt', 'w') as configfile:
            config.write(configfile)
        text = "CONFIGURACIÓN GUARDADA"
    return render_template('config.html', text=text)

@app.route('/shutdown')
def shutdown():
    return "APAGADO"

'''
https://www.raspberrypi.org/documentation/usage/gpio/python/README.md
led = LED(17)
button = Button(2)

@app.route('/start')
def start():
    led.on()
    sleep(1)
    led.off()

    if button.is_pressed:
        print("Pressed")
    else:
        print("Released")

    return "START"
'''
    
