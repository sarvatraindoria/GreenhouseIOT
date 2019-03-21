import sqlite3 


class Dbconn ():
    
       

     def createCon(self):
        self.con = sqlite3.connect('iotdb.db')   
        self.cur = self.con.cursor()
        return self.cur,self.con

     def execute(self, q):
        self.cur,self.cuon = self.createCon()
        self.cur.execute(q)
        self.con.commit()

myCon = Dbconn ()

q="insert into data (temp, humidity, time, notified) Values(30, 40, 89, 1);"

myCon.execute(q)



