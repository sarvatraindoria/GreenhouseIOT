import os
import time
import sqlite3
from sense_hat import SenseHat
sense = SenseHat()

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