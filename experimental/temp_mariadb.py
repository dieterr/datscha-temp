#!/usr/bin/python
# -*- coding: utf-8 -*-

## this scrpit is based on http://pastebin.com/aBjEPPq0

#import os
import glob
import time
import datetime
#import psycopg2
import netrc

import sqlite3 as lite
import sys

#import mysql.connector as mariadb
import MySQLdb as mariadb

host='84.115.199.11'

mariadb_connection = mariadb.connect(host, 'tempuser', 'tempuser', 'tempdb')
#timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
mcursor = mariadb_connection.cursor()


## starting the kernel-modules
## added this to /etc/modules, so most likely not necessary here
## testing this next time
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')
# kernel modules already started - throws exception in cron

## setting the correct files of the sensors
#device_folder = glob.glob('/sys/bus/w1/devices/10*')[0]
#device_file = [device_folder + '/w1_slave']#, device_folder[1] + '/w1_slave'
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'


##connecting to database
conn = None

# def db_connect():
#     try:
#         conn = lite.connect('/home/dieter/code/temp/temp.db')
#         print "Connected to sqlite3 & mariadb database temp.db!"

#     except:
#         conn = None
#         #print "I am unable to connect to sqlite3 database temp.db!"

#     return conn

# conn = db_connect()


## reading actuall temperature of two sensors
def read_temp_raw():
    #f1 = open(device_file[0], 'r')
    #lines1 = f1.readlines()
    #f1.close()
    #f2 = open(device_file[1], 'r')
    #lines2 = f2.readlines()
    #f2.close()
    #return lines1 + lines2

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

## extracting needed information
def read_temp():
    lines = read_temp_raw()
    #while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:#lines[1].find('t='), lines[3].find('t=')
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        

        #.isoformat()
        #timestamp = time.strftime("%y-%m-%d %H:%M:%S")
        #timestamp2 = datetime.datetime.now()
        #timestamp3 = datetime.datetime('%Y-%m-%d %H:%M:%S')
        #c = conn.cursor()
        print(timestamp)
        #print(timestamp2)
        #print(timestamp3)
        #mcursor.execute("INSERT INTO 1170_wozi (timestamp, temp) VALUES (?, ?)", (timestamp, temp_c))
        #mcursor.execute("INSERT INTO 1170_wozi (timestamp, temp) VALUES (?, ?)", (timestamp2, temp_c))
        #time.sleep(10)
        mcursor.execute("""INSERT INTO 1170_wozi (timest, temp) VALUES (%s, %s)""", (timestamp, temp_c))
        mariadb_connection.commit()
        return timestamp, temp_c
    #temp1 = float(lines[1][equals_pos[0]+2:])/1000
    #temp2 = float(lines[3][equals_pos[1]+2:])/1000
    #timestamp = time.strftime("%y-%m-%d %H:%M:%S")
    #return timestamp, temp1, temp2

## write results into file
#fobj = open("/home/pi/temp/temp-datscha2S.txt", "a")
#fobj.write(str(read_temp()[0]) + ";" + str(read_temp()[1]) + ";" + str(read_te#mp()[2]) + '\n')
#fobj.close()

##print results
read_temp()

##close cursor and sqlite dbconnection
#conn.close()
