import sqlite3
import csv
import pandas as pd
import os
import json


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


class ReadFile_CheckLimit():

    def readJson(self):
        osp = os.path.realpath(__file__)
        bsp = os.path.basename(__file__)
        relPath = osp.replace(bsp, "")
        with open(relPath+'config.json') as json_file:
            data = json.load(json_file)
            return data

    def checkLimit(self, val, lowerLim, upperLim):
        if(val < lowerLim):
            return -1, lowerLim - val
        elif(val > upperLim):
            return 1, val - upperLim
        else:
            return 0, 0


class createReport():
    def exportCSV(self):
        dataStoreList = {}
        csvData = [['Date', 'Status']]
        myDB = Dbcon()
        cur, con = myDB.createCon()
        df = pd.read_sql_query("""
                                select date,min(temp),
                                max(temp),min(humid),max(humid)
                                from pidata group by date""", con)

        for row in range(0, len(df)):
            dataStoreList.update({df['date'][row]: DataStoreT(df['min(temp)'][row], df['max(temp)'][row], df['min(humid)'][row], df['max(humid)'][row])})

        tmin = ReadFile_CheckLimit().readJson()['min_temprature']
        tmax = ReadFile_CheckLimit().readJson()['max_temprature']
        hmin = ReadFile_CheckLimit().readJson()['min_humidity']
        hmax = ReadFile_CheckLimit().readJson()['max_humidity']
        for i in dataStoreList:
            status = "OK"
            cmnt = ""
            print(i)
            tresp0, tresp1 = ReadFile_CheckLimit().checkLimit(dataStoreList.get(i).minTmp, tmin, tmax)

            if tresp0 == -1:
                tCmnt = str(tresp1)+" degrees below minimum temprature"
                status = "BAD"

            tresp0, tresp1 = ReadFile_CheckLimit().checkLimit(dataStoreList.get(i).maxTmp, tmin, tmax)

            if tresp0 == 1:
                tCmnt = str(tresp1)+" degrees above maximum temprature"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD"

            tresp0, tresp1 = ReadFile_CheckLimit().checkLimit(dataStoreList.get(i).minHumid, hmin, hmax)

            if tresp0 == -1:
                tCmnt = str(tresp1)+"% below minimum humidity"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD"

            tresp0, tresp1 = ReadFile_CheckLimit().checkLimit(dataStoreList.get(i).maxHumid, hmin, hmax)

            if tresp0 == 1:
                tCmnt = str(tresp1)+"% above maximum humidity"
                if len(cmnt) == 0:
                    cmnt = tCmnt
                else:
                    cmnt = cmnt + " ; " + tCmnt
                status = "BAD"

            csvData.append([i, cmnt])

        print(csvData)

myReport = createReport()
myReport.exportCSV()
