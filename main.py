import machine
from dht import DHT11
from time import sleep
import utime as dt 
from random import choice 
import network
import urequests
import ujson


endpoint_thingspeak = "https://api.thingspeak.com/update?api_key=EKX911IZ10C56N5V&field1={}&field2={}"

class IoT(object):
    
    @staticmethod
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
    
    @staticmethod
    def SensorAmbiente():
        for p in range(1,5):
          sleep(1)
        d.measure()
        umidade = d.humidity()
        temperatura = d.temperature()   
        return [umidade,temperatura]
    
    @staticmethod
    def connect_wifi(ssid, password):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid,password)
        for tentativa in range(50):
            if station.isconnected():
                break
            sleep(0.1)
        return station    

class ThingsSpeak(object):
  
  @staticmethod 
  def send(data):
      response = None
      try:
        response = urequests.get(endpoint_thingspeak.format(
                  data['temperatura'],
                  data['umidade'])).json()
      except:
        response = 0  
      return response
       
      
def main():
      station = IoT.connect_wifi("Juan_Oesteline","naomelembro")
      while station.isconnected():
         umidade, temperatura = IoT.SensorAmbiente()
         
         status = None
         if temperatura > 31 and umidade > 70:
             status = 0
         else:    
             status = 1
             
         value = {"umidade":str(umidade),
                  "temperatura":str(temperatura),
                  "relay_flag":str(status)}
         
         result = ThingsSpeak.send(value)
         
         print("result: ","FALHA NO ENDPOINT" if result == 0 else result)
         print("Umidade: {}\tTemperatura: {} \tSTATUS_LED: {}".format(umidade,
                                                                      temperatura,
                                                                      IoT.controleLed(status)))
         sleep(1)
         
          
if __name__== "__main__":   
    r = machine.Pin(33,machine.Pin.OUT)
    d = DHT11(machine.Pin(32))
    main()
