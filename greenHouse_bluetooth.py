import bluetooth
import os
import time
import subprocess
from pushbullet.pushbullet import PushBullet

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
    # def __init__(self, botList, iP):
    #     self.botList = botList
    #     self.iP = iP

        
    def detect(self):
        while True:
            print("Scanning...")
            nearbyDevices = bluetooth.discover_devices(lookup_names=True)

            for  name in nearbyDevices:
                print("Found device with mac-address: ", name)
                
                return name




    def connect(self):

        apiKey = "o.UPscOoahFXH2SOglsP5MICsJSywOOlqr"
        p = PushBullet(apiKey)
        # Get a list of devices
        devices = p.getDevices()
        botList=self.detect()

        devices = p.getDevices()

        if devices[0].get("nickname") in botList:
            p.pushNote(devices[0]["iden"], 'Raspberry-Pi-Notification','hello')
           
         

class main():

    def run(self):

       Blconnect().connect()

       print("success")


    
   
obj= main()

obj.run()


    
   
