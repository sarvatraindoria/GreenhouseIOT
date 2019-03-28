import sqlite3
import csv
import pandas as pd
import os
import json
import collections


class Dbcon():

    def createCon(self):
        self.con = sqlite3.connect('a1.db')
        self.cur = self.con.cursor()
        return self.cur, self.con

    def executeQuery(self, q, tmp, humid, date, time, notify, cmnt, stat):
        self.cur, self.con = self.createCon()
        self.cur.execute(q, (tmp, humid, date, time, notify, cmnt, stat))
        self.con.commit()
        self.con.close()

    def updateQuery(self, q, dateNow):
        self.cur, self.con = self.createCon()
        self.cur.execute(q, [dateNow])
        self.con.commit()
        self.con.close()

    def getRes(self, q):
        self.cur, self.con = self.createCon()
        self.cur.execute(q)
        rows = self.cur.fetchall()
        cols = self.cur.column_names
        self.con.close()
        return rows, cols


class DataStoreT():
    def __init__(self, minTmp, maxTmp, minHumid, maxHumid):
        self.minHumid = minHumid
        self.maxHumid = maxHumid
        self.minTmp = minTmp
        self.maxTmp = maxTmp


class readCheck():

    def readJson(self):
        osp = os.path.realpath(__file__)
        bsp = os.path.basename(__file__)
        relPath = osp.replace(bsp, "")
        with open(relPath+'config.json') as json_file:
            data = json.load(json_file)
            return data

    def chkLt(self, val, lowerLim, upperLim):
        if(val < lowerLim):
            return -1, lowerLim - val
        elif(val > upperLim):
            return 1, val - upperLim
        else:
            return 0, 0


class createReport():
    def exportCSV(self):
        dsl = {}
        dsl = collections.OrderedDict(dsl)
        csvData = []
        myDB = Dbcon()
        cur, con = myDB.createCon()
        df = pd.read_sql_query("""
                                select date,min(temp),
                                max(temp),min(humid),max(humid)
                                from pidata group by date""", con)

        for row in range(0, len(df)):
            mint = df['min(temp)'][row]
            maxt = df['max(temp)'][row]
            minh = df['min(humid)'][row]
            maxh = df['max(humid)'][row]
            dt = df['date'][row]
            dsl.update({dt: DataStoreT(mint, maxt, minh, maxh)})
            print(dt)

        tmin = readCheck().readJson()['min_temprature']
        tmax = readCheck().readJson()['max_temprature']
        hmin = readCheck().readJson()['min_humidity']
        hmax = readCheck().readJson()['max_humidity']
        print("---")
        for i in dsl:
            status = "OK : "
            cmnt = ""
            tresp0, tresp1 = readCheck().chkLt(dsl.get(i).minTmp, tmin, tmax)
            print(i)

            if tresp0 == -1:
                tCmnt = str(tresp1)+" degrees below minimum temprature"
                status = "BAD : "

            tresp0, tresp1 = readCheck().chkLt(dsl.get(i).maxTmp, tmin, tmax)

            if tresp0 == 1:
                tCmnt = str(tresp1)+" degrees above maximum temprature"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD : "

            tresp0, tresp1 = readCheck().chkLt(dsl.get(i).minHumid, hmin, hmax)

            if tresp0 == -1:
                tCmnt = str(tresp1)+"% below minimum humidity"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD : "

            tresp0, tresp1 = readCheck().chkLt(dsl.get(i).maxHumid, hmin, hmax)

            if tresp0 == 1:
                tCmnt = str(tresp1)+"% above maximum humidity"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD : "

            csvData.append([i, status + cmnt])

        df = pd.DataFrame(csvData, columns=['Date', 'Status'])
        df.to_csv("report.csv", sep=',', index=False)

myReport = createReport()
myReport.exportCSV()
