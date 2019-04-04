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
    def generateBar():
        conn = monitorAndNotify.Dbcon().createCon()[1]

        data = pd.read_sql_query(
            '''SELECT date, MIN(temp), MAX(temp), MIN(humid),
                MAX(humid) FROM pidata GROUP BY date''', conn)
        conn.close()
        data = pd.melt(
            data,
            id_vars="date",
            var_name="Attributes",
            value_name="Value")

        sns.catplot(
            x='date',
            y='Value',
            hue='Attributes',
            data=data,
            kind='bar')

        plot.savefig('bar.png')

CreateAnalyticsBar().generateBar()
