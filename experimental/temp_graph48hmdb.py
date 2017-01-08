#!/usr/bin/python
# -*- coding: utf-8 -*-



#import os
#import glob
#import time
import datetime
import psycopg2
import netrc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def db_connect():
    ##connecting to database
    HOST = '192.168.0.14psql'
    secrets = netrc.netrc('/home/dieter/.netrc')
    username, account, password = secrets.authenticators( HOST )

    try:
        conn = psycopg2.connect("dbname='temp' user="+username+" host='localhost' password="+password)
        print "connected to database temp!"
    except:
        print "I am unable to connect to the database"

    #cur = conn.cursor()
    return conn

# ##connecting to database
# HOST = '192.168.0.20psql'
# secrets = netrc.netrc()
# username, account, password = secrets.authenticators( HOST )

# try:
#     conn = psycopg2.connect("dbname='temp' user="+username+" host='localhost' password="+password)
#     print "connected to database temp!"
# except:
#     print "I am unable to connect to the database"

# cur = conn.cursor()

# last48h = {}


def read_db_last48h(conn = db_connect()):
    #print conn
    df = pd.read_sql_query('SELECT * from temp_1170 ORDER BY timestamp DESC LIMIT 4*48;',con=conn)
    return df


##print results
data = read_db_last48h()
#print data[:]
#plt.figure()
data.plot(x='timestamp', y='temp_wozi')
#plt.plot([1,2,3])
plt.xlabel('Zeit')
plt.ylabel('Temperatur')
plt.show()


##close cursor and dbconnection
##cur.close() #no cursor anymore
#conn.close()


## maybe a cursor?
# cur.execute("SELECT * FROM temp_1170 ORDER BY timestamp DESC LIMIT 4;")
# rows = cur.fetchall()

# print "\nShow me the rows:\n"
# n = 1
# for row in read_db_last48h():
#     #print n, row[0], row[1]
#     print row[0], row[1]
#     n += 1

