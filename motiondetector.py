#! /usr/bin/python3

import json
import os
import RPi.GPIO as GPIO
import requests
import time
import datetime

def time_in_range(start, end, current):
    return start <= current <= end


time_monitor_off = datetime.time(23, 55, 0) # turn off monitor at 11:45pm
time_monitor_on = datetime.time(7, 0, 0) # turn on monitor at 7:00am

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    PIR_PIN = data['MOTION']['PIR_PIN']
    url_monitor_on = data['MOTION']['url_monitor_on']
    url_monitor_off = data['MOTION']['url_monitor_off']
    url_monitor_dim = data['MOTION']['url_monitor_dim']
    url_monitor_bright = data['MOTION']['url_monitor_bright']
    bright_interval = data['MOTION']['bright_interval']
    off_interval = data['MOTION']['off_interval']


# Set GPIO pin for PIR sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
timestamp_dim = datetime.datetime.now()

try:
    # Initially turn on monitor and dim it
    requests.get(url_monitor_dim)
    requests.get(url_monitor_on)
    timestamp_dim = datetime.datetime.now()
except: 
    pass

# Keep monitor on until 11:45pm
while(time_in_range(time_monitor_on, time_monitor_off, datetime.datetime.now().time())):

    # Wait for motion to be detected with a timeout of 15 seconds
    GPIO.wait_for_edge(PIR_PIN, GPIO.RISING, timeout = 15000)

    # Turn on monitor if motion is detected
    if GPIO.input(PIR_PIN):
        try:
            # Turn on monitor and brighten it
            requests.get(url_monitor_bright)
            requests.get(url_monitor_on)
            monitor_on = True

            # Keep monitor bright for 1 minute
            time.sleep(bright_interval)

            # Dim monitor after 1 minute
            requests.get(url_monitor_dim)
            timestamp_dim = datetime.datetime.now()
        except:
            print("Error: Unable to connect to MagicMirror server")
            continue

    # Turn off monitor after 15 minutes of inactivity
    if (datetime.datetime.now() - timestamp_dim).seconds > off_interval and monitor_on:
        requests.get(url_monitor_off)
        monitor_on = False

# Turn off monitor at 11:45pm
requests.get(url_monitor_off)