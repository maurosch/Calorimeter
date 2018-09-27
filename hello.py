from flask import Flask
from flask import render_template
from flask import request
import configparser
import os
from os import listdir
from os.path import isfile, join
from subprocess import Popen
import subprocess
#from gpiozero import LED, Button

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

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
    
