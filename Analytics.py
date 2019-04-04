from importFix import fixImport
import os
import sqlite3
import seaborn as sns
import pandas as pd
import pygal
import cairosvg
import monitorAndNotify

# Import fix for matplotlib
plot = fixImport().getPLT()

# Bar graph generator Class with a single function


class CreateAnalyticsBar():
    def generateBar(self):
        conn = monitorAndNotify.Dbcon().createCon()[1]

        data = pd.read_sql_query(
            '''SELECT date, MIN(temp), MAX(temp), MIN(humid),
                MAX(humid) FROM pidata GROUP BY date''', conn)
        conn.close()
        data["date"] = data["date"].str.slice(5, 10)
        data = pd.melt(
            data,
            id_vars="date",
            var_name="Attributes",
            value_name="Value")
        cmnt = "and temprature by date"
        ax = sns.catplot(
            x='date',
            y='Value',
            hue='Attributes',
            data=data,
            kind='bar')
        ax.fig.suptitle('       minimum and maximum humidity ' + cmnt)
        plot.savefig('bar.png')

CreateAnalyticsBar().generateBar()
