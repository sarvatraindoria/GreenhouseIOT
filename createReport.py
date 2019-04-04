import sqlite3
import csv
import pandas as pd
import os
import json
import collections
import monitorAndNotify


class DataStoreT():
    def __init__(self, minTmp, maxTmp, minHumid, maxHumid):
        self.minHumid = minHumid
        self.maxHumid = maxHumid
        self.minTmp = minTmp
        self.maxTmp = maxTmp


class readCheck():
    # check limit and return checker (-1, 0, 1)
    def chkLt(self, val, lowerLim, upperLim):
        if(val < lowerLim):
            return -1, lowerLim - val
        elif(val > upperLim):
            return 1, val - upperLim
        else:
            return 0, 0


class createReport():
    # dump data to csv
    def exportCSV(self):
        dsl = {}
        dsl = collections.OrderedDict(dsl)
        csvData = []
        myDB = monitorAndNotify.Dbcon()
        cur, con = myDB.createCon()
        # getting values from db
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
            tmin = monitorAndNotify.maindriver().readJson()['min_temprature']
            tmax = monitorAndNotify.maindriver().readJson()['max_temprature']
            hmin = monitorAndNotify.maindriver().readJson()['min_humidity']
            hmax = monitorAndNotify.maindriver().readJson()['max_humidity']
        # checking db values with config
        # string formating for dynamic comment
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
        # csv dump
        df = pd.DataFrame(csvData, columns=['Date', 'Status'])
        df.to_csv("report.csv", sep=',', index=False)

myReport = createReport()
myReport.exportCSV()
