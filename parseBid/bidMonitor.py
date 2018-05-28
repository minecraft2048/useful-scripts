#!/usr/bin/env python
import sqlite3
import notify2
from parseBid import parseBid

DB_PATH =  '/home/feanor/Development/Cosplay_RD/warcraft'
tableList = []
display = []

notify2.init("BidMonitor")



conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('select TableName from Main')
for tableName in c:
    tableList.append(tableName[0])

#print(tableList)
#Update prices in each subtables
for tableName in tableList:
    c.execute('select ID,URL,Name,Cost from "{}"'.format(tableName))
    URLlist = c.fetchall()
    for tup in URLlist:
        #print(tup[1])
        n = parseBid(tup[1])
        if n[1] != tup[3]:
            app = (tup[2],tup[0],tup[3],n[1])
            display.append(app)
        param = (n[0],n[1],tup[0])     
        c.execute('update "{}" set Name=?,Cost=? where ID=?'.format(tableName),param)
    #Sync to Main table
    #TODO: DANGER! SQL INJECTION LIKELY
    #print(tableName)
    try:
        c.execute('drop table min_price')
    except sqlite3.OperationalError:
        pass
    c.execute('create temporary table min_price (Name text, Cost integer)')
    c.execute('insert into min_price(Name,Cost) select Name,min(Cost) from "{}" group by Name having count(*) > 1'.format(tableName))
    c.execute('insert into min_price(Name,Cost) select Name,Cost from "{}" group by Name having count(*) = 1'.format(tableName))
    c.execute('select sum(Cost) from min_price')
    c.execute('update Main set Cost=(select sum(Cost) from min_price) where TableName="{}"'.format(tableName))    
    
conn.commit()

notifstr = ''

#print(tup)

if display:
    for tup1 in display:
        notifstr += "{} (ID {}) {}→{}\n".format(tup1[0],tup1[1],tup1[2],tup1[3])

    notify = notify2.Notification("BidMonitor",notifstr)
   # notify.set_timeout(EXPIRES_NEVER)
    notify.show()
    print(notifstr)
