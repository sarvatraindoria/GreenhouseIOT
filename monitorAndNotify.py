import logging
import json
from sense_hat import SenseHat
import time
import sqlite3 as lite


sense = SenseHat()
sense.clear()

class Humid ():
    def __init__(self, maxHumid, minHumid, notified):
        self.minHumid = minHumid
        self.maxHumid = maxHumid
        self.notified = notified
        
        # logging.debug("humid boundries created: {} (${})".format(self._minHumid, self._maxHumid))
    

    def humidity(self):
        humid = round(sense.get_humidity())
        checker = 0
        try:
            if humid > self.maxHumid:
                checker = 1
                humid = self.maxHumid - humid
                print("humidity greater than Max by: ",humid)
                sense.show_message("humidity greater than Max by:  {0:0.0f}".format(humid))
                return humid,checker
                # logging.debug("humidity greater than Max by {} (${}) ".format(diff))
            elif humid < self.minHumid:
                checker = -1
                humid = self.minHumid - humid
                print("humidity lesser than Min by : ",humid)
                sense.show_message("humidity lesser than Min by : {0:0.0f}".format(humid))
                return humid,checker
                # logging.debug("humidity lesser than Min by {} (${})".format(diff))
            else :
                print("humidity is : ",humid)
                return humid,checker 
                
                # logging.debug("humidity is {} (${})".format(self._humid))

        except:
             print("error")
             sense.show_message("error")

    


