import os, glob, time

# Load drivers
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Find device file
device_folder = glob.glob('/sys/bus/w1/devices/28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    # Check for valid read
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = open(device_file, 'r').readlines()
    # Extract & convert temperature
    t_str = lines[1].find('t=')
    if t_str != -1:
        c = float(lines[1][t_str+2:]) / 1000.0
        return c, (c * 9.0 / 5.0 + 32.0)

while True:
    print("Temp: {:.2f}°C | {:.2f}°F".format(*read_temp()))
    time.sleep(1)
