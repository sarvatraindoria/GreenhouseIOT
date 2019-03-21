import logging
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

class Dbcon():
 
    def createCon(self):
        self.con = sqlite3.connect('a1.db')
        self.cur = self.con.cursor()
        return self.cur,self.con
    
    def executeQuery(self,q):
        self.cur,self.con=self.createCon()
        self.cur.execute(q)
        self.con.commit()
        
class monitorTemp():
    def __init__(self, upperTemp, lowerTemp, notified):
        self.upperTemp=upperTemp
        self.lowerTemp=lowerTemp
        self.notified=notified

    def get_cpu_temprature(self):
        result = os.popen("vcgencmd measure_temp").readline()
        ct = float(result.replace("temp=","").replace("'C\n",""))
        return(ct)

    def checkTemp(self):
        tempTemp = sense.get_temperature_from_humidity()
        temp_cpu = self.get_cpu_temprature()
        temp_corrected = tempTemp - ((temp_cpu-tempTemp)/1.5)
        if self.upperTemp<temp_corrected:
            return temp_corrected,1
        elif temp_corrected<self.lowerTemp:
            return temp_corrected,-1
        else:
            return temp_corrected,0

