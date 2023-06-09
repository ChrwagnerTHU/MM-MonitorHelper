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
init = False

__location__ = os.path.dirname(os.path.abspath(__file__))
with open (__location__ + "/config.json", "r") as f:
    data = json.load(f)
    PIR_PIN = data['MOTION']['PIR_PIN']
    LED_PIN_1 = data['MOTION']['LED_PIN_1']
    LED_PIN_2 = data['MOTION']['LED_PIN_2']
    url_monitor_on = data['MOTION']['url_monitor_on']
    url_monitor_off = data['MOTION']['url_monitor_off']
    url_monitor_dim = data['MOTION']['url_monitor_dim']
    url_monitor_bright = data['MOTION']['url_monitor_bright']
    bright_interval = data['MOTION']['bright_interval']
    off_interval = data['MOTION']['off_interval']

while not init:
    try:
        # Set GPIO pin for PIR sensor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.setup(LED_PIN_1, GPIO.OUT)
        GPIO.setup(LED_PIN_2, GPIO.OUT)
      
        # Initially turn on monitor and dim it
        requests.get(url_monitor_dim)
        requests.get(url_monitor_on)
        GPIO.output(LED_PIN_1, GPIO.LOW)
        GPIO.output(LED_PIN_2, GPIO.LOW)
        timestamp_dim = datetime.datetime.now()
        init = True
    except:
        print("Error while initializing script")
        pass

# Keep monitor on until 11:45pm
while(time_in_range(time_monitor_on, time_monitor_off, datetime.datetime.now().time())):

    try:
        # Wait for motion to be detected with a timeout of 15 seconds
        GPIO.wait_for_edge(PIR_PIN, GPIO.RISING, timeout = 15000)
        # Turn on monitor if motion is detected
        if GPIO.input(PIR_PIN):
            try:
                # Turn on monitor and brighten it
                requests.get(url_monitor_bright)
                requests.get(url_monitor_on)
                GPIO.output(LED_PIN_1, GPIO.HIGH)
                GPIO.output(LED_PIN_2, GPIO.HIGH)
                monitor_on = True

                # Keep monitor bright for 1 minute
                time.sleep(bright_interval)

                # Dim monitor after 1 minute
                requests.get(url_monitor_dim)
                GPIO.output(LED_PIN_1, GPIO.LOW)
                GPIO.output(LED_PIN_2, GPIO.LOW)
                timestamp_dim = datetime.datetime.now()
            except:
                print("Error: Unable to connect to MagicMirror server")
                continue

        # Turn off monitor after 15 minutes of inactivity
        if (datetime.datetime.now() - timestamp_dim).seconds > off_interval and monitor_on:
            requests.get(url_monitor_off)
            GPIO.output(LED_PIN_1, GPIO.LOW)
            GPIO.output(LED_PIN_2, GPIO.LOW)
            monitor_on = False
    except:
        print("Error: While handling GPIO state")

# Turn off monitor at 11:45pm
requests.get(url_monitor_off)
GPIO.output(LED_PIN_1, GPIO.LOW)
GPIO.output(LED_PIN_2, GPIO.LOW)
GPIO.cleanup()