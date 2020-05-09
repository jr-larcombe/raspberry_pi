import db_setup
import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

folder = '/sys/bus/w1/devices/'
temp_sensors = ['28-00000c36f9a3','28-00000c36fab6']

# Define function to fetch sensor file
def temp_raw(sensor_path):
    f = open(sensor_path,'r')
    lines = f.readlines()
    f.close()
    return lines

# Define function to fetch all sensor readings 
def read_temp():
    output_data = []
    output_data.append(time.time())
    for i in temp_sensors:
        sensor_path = folder + i + '/w1_slave'
        lines = temp_raw(sensor_path)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = temp_raw(sensor_path)
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            output_data.append([i,float(temp_string) / 1000.0])
    return output_data

# Fetch string with sensor readings
readings = read_temp()
read_time = readings[0]
read_vals = readings[1:]

# Write readings to database
for i in read_vals:
    db_setup.insert_readings(read_time, i[0],'temp', i[1])
