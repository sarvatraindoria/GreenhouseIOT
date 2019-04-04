from importFix import fixImport
import os
import sqlite3
import seaborn as sns
import pandas as pd
import pygal
import cairosvg
import monitorAndNotify

plot = fixImport().getPLT()


class CreateAnalyticsScatter():
        def geberateScatter():
                # DB connection and data retrival
                conn = monitorAndNotify.Dbcon().createCon()[1]
                que = 'select time,temp,humid from pidata'
                data = pd.read_sql_query(que, conn)
                time = data['time']

                # data cleaning and formatting
                range1 = (time >= "12") & (time < "14")
                df1 = data[range1]
                df1 = df1.assign(range="12-14")
                range2 = (time >= "14") & (time < "16")
                df2 = data[range2]
                df2 = df2.assign(range="14-16")
                range3 = (time >= "16") & (time < "18")
                df3 = data[range3]
                df3 = df3.assign(range="16-18")
                range4 = (time >= "18") & (time < "20")
                df4 = data[range4]
                df4 = df4.assign(range="18-20")

                r1 = []
                r2 = []
                r3 = []
                r4 = []

                # Data sets creation

                for index, row in df1.iterrows():
                        r1.append((row['temp'], row['humid']))

                for index, row in df2.iterrows():
                        r2.append((row['temp'], row['humid']))

                for index, row in df3.iterrows():
                        r3.append((row['temp'], row['humid']))

                for index, row in df4.iterrows():
                        r4.append((row['temp'], row['humid']))

                # Chart config

                xy_chart = pygal.XY(stroke=False)
                xy_chart.title = 'Correlation'
                xy_chart.add('12-14', r1)
                xy_chart.add('14-16', r2)
                xy_chart.add('16-18', r3)
                xy_chart.add('18-20', r4)
                xy_chart.show_legend = True
                xy_chart.render_to_png('scatter.png')

CreateAnalyticsScatter().geberateScatter()
