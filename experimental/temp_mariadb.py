#!/usr/bin/python
# -*- coding: utf-8 -*-

## this scrpit is based on http://pastebin.com/aBjEPPq0

import glob
import time
import datetime
import netrc
import sys
import MySQLdb as mariadb

netrc_name='192.168.0.13tempmariadb'
host='192.168.0.13'

cred = netrc.netrc()

cred_full = cred.authenticators(netrc_name)
##print(cred_full)

mdbcon = mariadb.connect(host, cred_full[0], cred_full[2] , 'tempdb')

# mdbcon.query("SELECT VERSION()")
# ResultVersion = mdbcon.use_result()
# print("Test: %s" % ResultVersion.fetch_row()[0])

# mdbcon.query("SELECT * FROM SensorLocations")
# ResultSensorLocations = mdbcon.use_result()

# print("SensorLocs: %s " % ResultSensorLocations.fetch_row()[0])

#timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

mcursor = mdbcon.cursor()

## setting the correct files of the sensors
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

## reading actuall temperature of two sensors
def read_temp_raw():
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
        temp_c = round(float(temp_string) / 1000.0,1)
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        ##print(timestamp, temp_c)
        mcursor.execute("""INSERT INTO Temp (SensorLocationID_FK, Temp, MeasureTimestamp) VALUES (%s, %s, %s)""", (1, temp_c, timestamp))
        mdbcon.commit()
        return timestamp, temp_c




read_temp()

##close dbconnection
mdbcon.close()

print("Done!")
