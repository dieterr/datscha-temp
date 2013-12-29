import os
import glob
import time
import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
#device_folder1 = glob.glob(base_dir + '10-000802b54*')[0]
#device_folder2 = glob.glob(base_dir + '10-000802b58*')[0]
device_folder = glob.glob('/sys/bus/w1/devices/10*')
device_file = [device_folder[0] + '/w1_slave', device_folder[1] + '/w1_slave']


def read_temp_raw():
    f1 = open(device_file[0], 'r')
    lines1 = f1.readlines()
    f1.close()
    f2 = open(device_file[1], 'r')
    lines2 = f2.readlines()
    f2.close()
    return lines1 + lines2

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES' or lines[2].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t='), lines[3].find('t=')
    temp1 = float(lines[1][equals_pos[0]+2:])/1000
    temp2 = float(lines[3][equals_pos[1]+2:])/1000
    timestamp = time.strftime("%y-%m-%d %H:%M:%S")
    return timestamp, temp1, temp2
    
#print read_temp()
#time.sleep(60)
#time.sleep(900)

fobj = open("/home/pi/temp/temp-datscha2S.txt", "a")
fobj.write(str(read_temp()[0]) + ";" + str(read_temp()[1]) + ";" + str(read_temp()[2]) + '\n')
fobj.close()


##original
#while True:
#    #print read_temp()
#    fobj = open("/tmp/temp-datscha.txt", "a")
#    fobj.write(str(read_temp()[0]) + ";" + str(read_temp()[1]) + ";" + str(read_temp()[2]) + ";" + '\n')
#    fobj.close()
#    #time.sleep(60)
#    #time.sleep(900)#
