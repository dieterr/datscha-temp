# import os
import glob
import time
import datetime

class temperature:
    def __init__(self):
        print("Der Konstruktor")
        # pass

    def list_sensors(self):
        base_dir = '/sys/bus/w1/devices/'
        sensor_list =  glob.glob(base_dir + '10*')
        #print(sensor_list)
        return sensor_list
        #return ''.join(sensor_list)
        

    def read_temp_raw(self):
    
        # os.system('modprobe w1-gpio')
        # os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '10*')[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        # print lines
        f.close()
        print("Test")
        return lines

    def read_temp(self):
        lines = t.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = t.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
        
            timestamp = time.strftime("%y-%m-%d %H:%M:%S")
            return timestamp, temp_c

    def write_temp(self):
        return t.read_temp()
        


t = temperature()
#print t.read_temp_raw
#for i in t.list_sensors:
#    print i
print t.list_sensors()

print t.write_temp()

while True:
    print t.read_temp()
    time.sleep(10)
