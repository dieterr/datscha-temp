#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
sensor_dir = "/sys/bus/w1/devices/10*"
sensor_list = glob.glob(sensor_dir)
print sensor_list
# for device in device_list:
#     #print device
#     #print len(device)
trim_letter = sensor_dir.find("10")
#     device_list[device] = device[trim_letter:]

sensor_list = [sensor[trim_letter:] for sensor in sensor_list]
print sensor_list

for sensor in sensor_list:
    print len(sensor)
