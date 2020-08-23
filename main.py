import machine
#from datetime import datetime as dt
from time import sleep
import utime as dt 
from random import choice 

r = machine.Pin(2,machine.Pin.OUT)

def controleLed(status):
    now = dt.time()
    tm = dt.localtime(now)
    if status ==1:
        print(str(tm),"STATUS: LED ON")
        r.value(status)
    else:
        print(str(tm),"STATUS: LED OFF")
        r.value(status)

while True:
     status = choice([1,0])
     controleLed(status)
     sleep(1)


