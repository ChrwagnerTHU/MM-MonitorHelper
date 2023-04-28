import RPi.GPIO as GPIO
import requests
import time
import datetime

def time_in_range(start, end, current):
    return start <= current <= end

PIR_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

url_monitor_dim = 'http://192.168.2.46:8080/remote?action=BRIGHTNESS&value=1'
url_monitor_bright = 'http://192.168.2.46:8080/remote?action=BRIGHTNESS&value=100'
url_monitor_on = 'http://192.168.2.46:8080/remote?action=MONITORON'
url_monitor_off = 'http://192.168.2.46:8080/remote?action=MONITOROFF'
time_monitor_off = datetime.time(23, 45, 0) # turn off monitor at 11:45pm
time_monitor_on = datetime.time(7, 0, 0) # turn on monitor at 7:00am
bright_interval = 60 # brighten the monitor for 1 minute
off_interval = 900 # after 15 minutes of inactivity, turn off monitor
timestamp_dim = datetime.datetime.now()
monitor_on = True


# Initially turn on monitor and dim it
requests.get(url_monitor_dim)
requests.get(url_monitor_on)

# Keep monitor on until 11:45pm
while(time_in_range(time_monitor_on, time_monitor_off, datetime.datetime.now().time())):

    # Wait for motion to be detected with a timeout of 15 seconds
    GPIO.wait_for_edge(PIR_PIN, GPIO.RISING, timeout = 15000)

    # Turn on monitor if motion is detected
    if GPIO.input(PIR_PIN):
        
        # Turn on monitor and brighten it
        requests.get(url_monitor_bright)
        requests.get(url_monitor_on)
        monitor_on = True

        # Keep monitor bright for 1 minute
        time.sleep(bright_interval)

        # Dim monitor after 1 minute
        requests.get(url_monitor_dim)
        timestamp_dim = datetime.datetime.now()

    # Turn off monitor after 15 minutes of inactivity
    if (datetime.datetime.now() - timestamp_dim).seconds > off_interval and monitor_on:
        requests.get(url_monitor_off)
        monitor_on = False

# Turn off monitor at 11:45pm
requests.get(url_monitor_off)