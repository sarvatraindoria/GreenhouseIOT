import logging
import json
from sense_hat import SenseHat
logging.basicConfig(level = logging.DEBUG)


senseHum = SenseHat()

#humid = senseHum.get_humidity()
class Humid ():
    def __init__(self, Humid,  maxHumid, minHumid, Date):
        self._minHumid = minHumid
        self._maxHumid = maxHumid
        self._humid = Humid
        self._date = Date
        logging.debug("humid boundries created: {} (${})".format(self._minHumid, self._maxHumid))


    def gethumidity(self, self._humid, self._maxHumid, self._minHumid ):
        self._maxHumid = 60
        self._minHumid = 50
        
        try:
            if self._humid > self._macHumid
            logging.debug("humidity greater than ")


