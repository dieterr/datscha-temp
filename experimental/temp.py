h#!/usr/bin/python
# -*- coding: utf-8 -*-

## this scrpit is based on http://pastebin.com/aBjEPPq0

import os
import glob
import time
import datetime
import psycopg2
import netrc

## starting the kernel-modules
## added this to /etc/modules, so most likely not necessary here
## testing this next time
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

## setting the correct files of the sensors
#device_folder = glob.glob('/sys/bus/w1/devices/10*')[0]
#device_file = [device_folder + '/w1_slave']#, device_folder[1] + '/w1_slave'
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'


##connecting to database
HOST = '192.168.1.2psql'
secrets = netrc.netrc()
username, account, password = secrets.authenticators( HOST )

try:
    conn = psycopg2.connect("dbname='temp' user="+username+" host='localhost' password="+password)
    print "connected to database temp!"
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

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
        timestamp = time.strftime("%y-%m-%d %H:%M:%S")
        #timestamp = datetime.datetime.now()
        cur.execute("INSERT INTO temp_1170 (timestamp, temp_wozi) VALUES (%s, %s)", (datetime.datetime.now(), temp_c))
        conn.commit()
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
print read_temp()

##close cursor and dbconnection
cur.close()
conn.close()
