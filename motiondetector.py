import json
import os
import RPi.GPIO as GPIO
import requests
import time
import datetime

def time_in_range(start, end, current):
    return start <= current <= end


time_monitor_off = datetime.time(23, 45, 0) # turn off monitor at 11:45pm
time_monitor_on = datetime.time(7, 0, 0) # turn on monitor at 7:00am

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    
    PIR_PIN = data['PIR_PIN']
    url_monitor_on = data['url_monitor_on']
    url_monitor_off = data['url_monitor_off']
    url_monitor_dim = data['url_monitor_dim']
    url_monitor_bright = data['url_monitor_bright']
    bright_interval = data['bright_interval']
    off_interval = data['off_interval']


# Set GPIO pin for PIR sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

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