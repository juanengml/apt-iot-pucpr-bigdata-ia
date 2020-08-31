import machine
from dht import DHT11
from time import sleep
import utime as dt 
from random import choice 
import network
import urequests
import ujson

def controleLed(status):
    now = dt.time()
    tm = dt.localtime(now)
    msg = None
    if status == 0:
        msg = "STATUS: LED ON"
        r.value(status)
    else:
        msg = "STATUS: LED OFF"
        r.value(status)
    return msg

def SensorAmbiente():
    for p in range(1,3):
      sleep(1)
    d.measure()
    umidade = d.humidity()
    temperatura = d.temperature()   
    return [umidade,temperatura]

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid,password)
    for tentativa in range(50):
        if station.isconnected():
            break
        sleep(0.1)
    return station    

def GenerateID():
  reponse = None
  try:
    response = urequests.get("http://TintedNimbleCompilerbug--five-nine.repl.co/api/iot/v1/GENERATE_ID")
    return response.json()
  except:
    return {"ID":"","dt":""} 

def EnviarDadosSensores(data):
      response = None
      response = urequests.get("http://TintedNimbleCompilerbug--five-nine.repl.co/api/iot/v1/SEND?umidade={}&temperatura={}&relay_flag={}".format(
                  data['umidade'],
                  data['temperatura'],
                  data['relay_flag'])).json()
      return response
       
      
def main():
      station = connect_wifi("USSID","PASSWD")
      response = GenerateID()
      print(response)
      while station.isconnected():
         umidade, temperatura = SensorAmbiente()
         
         status = None
         if temperatura > 31 and umidade > 70:
             status = 0
         else:    
             status = 1
             
         value = {"umidade":str(umidade),"temperatura":str(temperatura),"relay_flag":str(status)}
         #print("value: ", value)
         result = EnviarDadosSensores(value)
         print("result: ",result)
         print("Umidade: {}\tTemperatura: {} \tSTATUS_LED: {}".format(umidade, temperatura,controleLed(status)))
         sleep(1)
         
          
if __name__== "__main__":   
    r = machine.Pin(33,machine.Pin.OUT)
    d = DHT11(machine.Pin(32))
    main()
    


