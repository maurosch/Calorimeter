import RPi.GPIO as GPIO
import time

relayNumberIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relayNumberIN, GPIO.OUT)
time.sleep(5)
GPIO.setup(relayNumberIN, GPIO.IN)