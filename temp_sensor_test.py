import csv
import os
import time
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, False)

folder = '/sys/bus/w1/devices/'
temp_sensors = ['28-00000c36f9a3','28-00000c36fab6']

def sleep_step(mins):
    time_now = time.time()
    return (mins * 60) - time.gmtime(time_now).tm_sec - (time_now - int(time_now))

def temp_raw(sensor_path):
    f = open(sensor_path,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    temp_c = [time.time()]
    for i in temp_sensors:
        sensor_path = folder + i + '/w1_slave'
        lines = temp_raw(sensor_path)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = temp_raw()
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c.append(float(temp_string) / 1000.0)
    return temp_c

def write_line(output_file,line):
    with open(output_file, 'a') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(line)

# Run the loop
for i in range(10):
    # time.sleep(sleep_step(1))
    time.sleep(1)
    output = read_temp()
    print(output)
    if output[1] >= 25.0:
        GPIO.output(17, True)
    else:
        GPIO.output(17, False)
    # write_line('output.csv',output)

GPIO.output(17, False)