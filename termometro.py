import spidev
import max6675
from time import sleep
while True:
    sensor_0_0 = max6675.MAX6675(7, 18, 22, "c")
    print sensor_0_0.get()
    sleep(2)
