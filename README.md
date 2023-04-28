# MotionDetector

This repository contains a script to control the monitor on which the MagicMirror runs. 

## Prerequisites
- A RaspberryPi which runs [MagicMirror2](https://github.com/MichMich/MagicMirror/tree/develop)
- [MMM-Remote-Control](https://github.com/Jopyth/MMM-Remote-Control) installed
- PIR Motion Detector connected to one of the RaspberryPis Pins 

## Installation
```
cd AnyDirectoryYouWant
```
```
git clone https://github.com/ChrwagnerTHU/MM-MonitorHelper-PIR-MotionDetector
```
To run the script automatically add a cronjob
```
crontab -e
```
add the following line with the minute, hour, day, month, day-of-week you want to run the script
Example:
```
01 07 * * * python3 /usr/dirToScript/motiondetector.py
````

### Config
Costomize the config.json to control the behavor of the monitor
|Option|Default|Description|
|---|---|---|
|`PIR_PIN`|18|The Pin the motion controller is attached|
|`url_monitor_dim`|'http://xxx.xxx.xxx.xxx:xxxx/remote?action=BRIGHTNESS&value=1'|The URL to set the brightnes to 1|
|`url_monitor_bright`|'http://xxx.xxx.xxx.xxx:xxxx/remote?action=BRIGHTNESS&value=100'|The URL to set the brightnes to 100|
|`url_monitor_on`|'http://xxx.xxx.xxx.xxx:xxxx/remote?action=MONITORON'|The URL to turn on the monitor|
|`url_monitor_off`|'http://xxx.xxx.xxx.xxx:xxxx/remote?action=MONITOROFF'|The URL to turn off the monitor|
|`bright_interval`|60|Time the monitor shall remain bright after motion detected (in s)|
|`off_interval`|900|Time the monitor shall ramin dimmed until turned off (in s)|

Don't forget to change these values to the IP adress and port your MagicMirror runs on 

The control of the times between which the monitor should be completely on and off is in the script. Adjust the following variables to change the behaviour
|Option|Default|Description|
|---|---|---|
|`time_monitor_off`|datetime.time(23, 45, 0)|The when the monitor shall be completely turned off|
|`time_monitor_on`|datetime.time(7, 0, 0)|The when the monitor shall be turned on|
