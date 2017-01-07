#!/usr/bin/python
# -*- coding: utf-8 -*-



#import os
#import glob
#import time
# import datetime
#import psycopg2
# import netrc
from pandas import read_sql_query as pdrsq
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

import sqlite3 as lite
# import sys

conn = None

def db_connect():
    try:
        conn = lite.connect('temp.db')
        print "Connected to sqlite3 database temp.db!"

    except:
        print "I am unable to connect to sqlite3 database temp.db!"

    return conn

def read_db_last48h():
    df = pdrsq("SELECT * from temp_1170 ORDER BY timestamp DESC LIMIT 4*48;", conn)
    return df

conn = db_connect()
print(conn)
##print results
data = read_db_last48h()
print data[:]
#plt.figure()
data.plot(x='timestamp', y='temp_wozi')
#plt.plot([1,2,3])
plt.xlabel('Zeit')
plt.ylabel('Temperatur')
plt.show()

