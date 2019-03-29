import bluetooth
import os
import time
import subprocess
from pushbullet.pushbullet import PushBullet
import monitorAndNotify as util

from sense_hat import SenseHat
# apiKey = "o.UPscOoahFXH2SOglsP5MICsJSywOOlqr"
# p = PushBullet(apiKey)
# # Get a list of devices
# devices = p.getDevices()

# # Get a list of contacts
# contacts = p.getContacts()

# # Send a note
# p.pushNote(devices[0]["iden"], 'Hello world', 'Test body')

# # Send a map location
# p.pushAddress(devices[0]["iden"], "Eiffel tower", "Eeiffel tower, france")

# # Send a list
# p.pushList(devices[0]["iden"], "Groceries", ["Apples", "Bread", "Milk"])

# # Send a link
# p.pushLink(devices[0]["iden"], "Google", "http://www.google.com")

# # Send a file
# p.pushFile(devices[0]["iden"], "file.txt", "This is a text file", open("file.txt", "rb"))

# # Send a note to a channel
# p.pushNote('channel_tag', 'Hello world', 'Test body', recipient_type='channel_tag')

# # Send a note to an email
# p.pushNote('myemail@domain.com', 'Hello world', 'Test body', recipient_type='email')



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
            # else :
            #     print("Device not found")
                
            #     print (i," Loop cycle out of 9 ")
            #     i +=1
           
         

class main():

    def run(self):

       Blconnect().connect()

       print("success")


    
   
obj= main()

obj.run()


    
   
