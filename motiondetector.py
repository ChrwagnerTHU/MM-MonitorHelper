import RPi.GPIO as GPIO
import requests
import time
import datetime
import subprocess

def time_in_range(start, end, current):
    return start <= current <= end

PIR_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

url_monitor_dim = 'http://192.168.2.46:8080/remote?action=BRIGHTNESS&value=1'
url_monitor_bright = 'http://192.168.2.46:8080/remote?action=BRIGHTNESS&value=100'
url_monitor_on = 'http://192.168.2.46:8080/remote?action=MONITORON'
url_monitor_off = 'http://192.168.2.46:8080/remote?action=MONITOROFF'
time_monitor_off = datetime.time(23, 55, 0)
time_monitor_on = datetime.time(7, 0, 0)


# Initially turn off monitor
requests.get(url_monitor_dim)
requests.get(url_monitor_on)

while(time_in_range(time_monitor_on, time_monitor_off, datetime.datetime.now().time())):
    if GPIO.input(PIR_PIN):
        requests.get(url_monitor_bright)
        time.sleep(10)
        requests.get(url_monitor_dim)

requests.get(url_monitor_off)