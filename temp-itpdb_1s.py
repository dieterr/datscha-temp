import os
import glob
import time
import datetime
import psycopg2
import netrc

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

HOST = '192.168.0.20psql'
secrets = netrc.netrc()
username, account, password = secrets.authenticators( HOST )

#print username, password

try:
    conn = psycopg2.connect("dbname='temp' user="+username+" host='localhost' password="+password)
    print "connected to database temp!"
except:
    print "I am unable to connect to the database"


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f
        timestamp = time.strftime("%y-%m-%d %H:%M:%S")
        nowday = str(time.localtime()[0])+str(time.localtime()[1])+str(time.localtime()[2])
        nowtime = str(time.localtime()[3])+":"+str(time.localtime()[4])+":"+str(time.localtime()[5])
        #return nowday, nowtime, temp_c, timestamp
        return timestamp, temp_c

while True:
    print read_temp()
    time.sleep(10)
#time.sleep(900)

##original
#while True:
#    #print read_temp()
#    fobj = open("/tmp/temp-datscha.txt", "a")
#    fobj.write(str(read_temp()[0]) + ";" + str(read_temp()[1]) + ";" + str(read_temp()[2]) + ";" + '\n')
#    fobj.close()
#    #time.sleep(60)
#    #time.sleep(900)#
