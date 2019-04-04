from sense_hat import SenseHat
import datetime
import sqlite3
import json
import os
from pushbullet.pushbullet import PushBullet

sense = SenseHat()
sense.clear()


class Humid():
    def __init__(self, maxHumid, minHumid, notified):
        self.minHumid = minHumid
        self.maxHumid = maxHumid
        self.notified = notified

    def humidity(self):
        # Humidity data collection and check
        humid = round(sense.get_humidity())
        if humid <= 0:
            sys.exit() 
        checker = 0
        try:
            if humid > self.maxHumid:
                checker = 1
                originalHumid = humid
                humid = self.maxHumid - humid
                return originalHumid, humid, checker
            elif humid < self.minHumid:
                originalHumid = humid
                checker = -1
                humid = self.minHumid - humid
                return originalHumid, humid, checker
            else:
                originalHumid = humid
                print("humidity is : ", humid)
                return originalHumid, humid, checker

        except BaseException:
            print("error")
            sense.show_message("error")


class Dbcon():

    def createCon(self):
        # DB connection init
        try:
            osp = os.path.realpath(__file__)
            bsp = os.path.basename(__file__)
            relPath = osp.replace(bsp, "")
            self.con = sqlite3.connect(relPath + 'a1.db')
            self.cur = self.con.cursor()
        except FileNotFoundError:
            f = open("ErrorLog.txt", "a")
            errorLog = " : Failed to load database  \n"
            f.write(str(datetime.datetime.now)+errorLog)
            f.close()
            sys.exit(0)
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 'pidata'
        ('temp'	REAL NOT NULL,'humid'
        REAL NOT NULL,'date'
        TEXT NOT NULL,'time'
        TEXT NOT NULL,'notified'
        INTEGER NOT NULL);''')
        return self.cur, self.con

    def executeQuery(self, q, tmp, humid, date, time, notify):
        # DB query execution for non result based queries
        self.cur, self.con = self.createCon()
        self.cur.execute(q, (tmp, humid, date, time, notify))
        self.con.commit()
        self.con.close()

    def updateQuery(self, q, dateNow):
        # DB query execution for update queries
        self.cur, self.con = self.createCon()
        self.cur.execute(q, [dateNow])
        self.con.commit()
        self.con.close()

    def getRes(self, q, param):
        # DB query execution for result based queries
        self.cur, self.con = self.createCon()
        self.cur.execute(q, [param])
        row = self.cur.fetchall()
        self.con.close()
        return row, self.cur


class pushBulletImp():

    def sendNotify(self, msg):
        # pushBullet notify call for registerd devices
        apiKey = "o.2uIo9r0MKCCFX8Mv3uMhp4xOXE9vgBrC"
        p = PushBullet(apiKey)
        devices = p.getDevices()
        p.pushNote(devices[0]["iden"], 'Raspberry-Pi-Notification', msg)


class monitorTemp():
    def __init__(self, upperTemp, lowerTemp, notified):
        self.upperTemp = upperTemp
        self.lowerTemp = lowerTemp
        self.notified = notified

    def get_cpu_temprature(self):
        # temprature correction logic
        result = os.popen("vcgencmd measure_temp").readline()
        ct = float(result.replace("temp=", "").replace("'C\n", ""))
        return(ct)

    def checkTemp(self):
        # temprature get and check
        tempTemp = sense.get_temperature_from_humidity()
        temp_cpu = self.get_cpu_temprature()
        temp_cor = tempTemp - ((temp_cpu - tempTemp) / 1.5)
        if self.upperTemp < temp_cor:
            return round(temp_cor, 1), round(temp_cor-self.upperTemp, 1), 1
        elif temp_cor < self.lowerTemp:
            return round(temp_cor, 1), round(self.lowerTemp-temp_cor, 1), -1
        else:
            return round(temp_cor, 1), 0, 0


class maindriver():

    def readJson(self):
        # read config file
        try:
            osp = os.path.realpath(__file__)
            bsp = os.path.basename(__file__)
            relPath = osp.replace(bsp, "")
            with open(relPath + 'config.json') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            f = open("ErrorLog.txt", "a")
            errorLog = " : Failed to load congif file  \n"
            f.write(str(datetime.datetime.now)+errorLog)
            f.close()
            sys.exit(0)

    def getNotified(self):
        # Check if notification sent
        q = "select * from pidata where date = ? limit 1 ;"
        nowDate = ((str(datetime.datetime.now())).split(" "))[0]
        dbCheckNotify = Dbcon()
        dbRow, rowCur = dbCheckNotify.getRes(q, str(nowDate))
        if dbRow[0][4] == 1:
            return True
        else:
            return False

    def doNotify(self, msg):
        # Send notification to registerd device
        updateDB = Dbcon()
        subQ = "(select ROWID from pidata where date = ? limit 1) ;"
        q = "UPDATE pidata SET notified=1 WHERE ROWID = " + subQ
        nowDate = ((str(datetime.datetime.now())).split(" "))[0]
        updateDB.updateQuery(q, str(nowDate))
        myPB = pushBulletImp()
        myPB.sendNotify(msg)

    def collectStoreNotify(self, flag=False):
        # Function to match values with config
        # run queries
        # populate database
        tmin = self.readJson()['min_temprature']
        tmax = self.readJson()['max_temprature']
        tobj = monitorTemp(tmax, tmin, 0)
        tresp = tobj.checkTemp()
        hmin = self.readJson()['min_humidity']
        hmax = self.readJson()['max_humidity']
        hobj = Humid(hmax, hmin, 0)
        hresp = hobj.humidity()
        date = ((str(datetime.datetime.now())).split(" "))[0]
        time = (((str(datetime.datetime.now())).split(" "))[1]).split(".")[0]
        q = "insert into pidata values (?, ?, ?, ?, ?)"
        tmp = tresp[0]
        humid = hresp[0]
        noti = 0

        # conditions for temprature and humidity according to config.json

        if flag is True:
            cmnt = ""

        if hresp[2] == 1:
            hCmnt = str(hresp[1]) + "% above maximum humidity"
            cmnt = hCmnt
            if flag is False:
                dbx = Dbcon()
                if self.getNotified() is False:
                    self.doNotify(cmnt + " on date:" + date + " time:" + time)

        elif hresp[2] == -1:
            hCmnt = str(hresp[1]) + "% below minimum humidity"
            cmnt = hCmnt
            if flag is False:
                dbx = Dbcon()
                dbx.executeQuery(q, tmp, humid, date, time, noti)
                if self.getNotified() is False:
                    self.doNotify(cmnt + " on date:" + date + " time:" + time)

        elif tresp[2] == 1:
            tCmnt = str(tresp[1]) + " degrees above maximum temprature"
            cmnt = tCmnt
            if flag is False:
                dbx = Dbcon()
                dbx.executeQuery(q, tmp, humid, date, time, noti)
                if self.getNotified() is False:
                    self.doNotify(cmnt + " on date:" + date + " time:" + time)

        elif tresp[2] == -1:
            tCmnt = str(tresp[1]) + " degrees below minimum temprature"
            cmnt = tCmnt
            if flag is False:
                dbx = Dbcon()
                dbx.executeQuery(q, tmp, humid, date, time, noti)
                if self.getNotified() is False:
                    self.doNotify(cmnt + " on date:" + date + " time:" + time)

        else:
            if flag is False:
                dbx = Dbcon()
                dbx.executeQuery(q, tmp, humid, date, time, noti)

        if flag is True:
            return cmnt


p = maindriver()
p.collectStoreNotify()
