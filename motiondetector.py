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
monitor_off = datetime.time(23, 55, 0)
monitor_on = datetime.time(7, 0, 0)	

# Initially turn off monitor
requests.get(url_monitor_dim)

while(True):
    if not time_in_range(monitor_on, monitor_off, datetime.datetime.now().time()):
        break
    if GPIO.input(PIR_PIN):
        requests.get(url_monitor_bright)
        time.sleep(10)
        requests.get(url_monitor_dim)





