import bluetooth
import os
import time
import subprocess
from pushbullet.pushbullet import PushBullet
import monitorAndNotify as util

from sense_hat import SenseHat
# apiKey = "o.UPscOoahFXH2SOglsP5MICsJSywOOlqr"


class Blconnect():
      
    def detect(self):
        while True:
            print("Scanning...")
            nearbyDevices = bluetooth.discover_devices(lookup_names=True)
            
            for name in nearbyDevices:
                print(name)
                return name


    def blueMsg(self):
        data = util.maindriver().collectStoreNotify(True)
        tmin = util.maindriver().readJson()['min_temprature']
        tmax = util.maindriver().readJson()['max_temprature']
        hmin = util.maindriver().readJson()['min_humidity']
        hmax = util.maindriver().readJson()['max_humidity']

        currentTemp, _, _ = util.monitorTemp(tmax, tmin, 0).checkTemp()
        
        currentHumid, _, _ = util.Humid(hmax, hmin, 0).humidity()
        
        print(data)
        return data,currentTemp,currentHumid
    


    def connect(self):

        apiKey = "o.UPscOoahFXH2SOglsP5MICsJSywOOlqr"
        p = PushBullet(apiKey)
        # Get a list of devices
        devices = p.getDevices()
        
        msg, ct, ch = self.blueMsg()

        
        while True:
            botList=self.detect()
            print(botList)
            if devices[0].get("nickname") in botList:
                
                print("Found device with names: ", botList)
                p.pushNote(devices[0]["iden"], 'Raspberry-Pi-Notification','Current Temperature is :'+str(ct)+'Degrees'+'\nCurrentHumid :'+str(ch)+'%'+'\n'+ msg)
                break
            
           
         

class main():

    def run(self):

       Blconnect().connect()

       print("success")


    
   
obj= main()

obj.run()


    
   
