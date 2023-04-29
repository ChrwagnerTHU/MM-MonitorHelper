# MonitorHelper

This repository bundles several helper scripts to control the MagicMirror
Until now, this repository only contains a script to control the monitor.
The repository shall function as a place to bundle every other control script.

## Prerequisites
- A RaspberryPi which runs [MagicMirror2](https://github.com/MichMich/MagicMirror/tree/develop)
- [MMM-Remote-Control](https://github.com/Jopyth/MMM-Remote-Control) installed

## Installation
```
cd AnyDirectoryYouWant
```
```
git clone https://github.com/ChrwagnerTHU/MM-MonitorHelper
```
To run the any script automatically add a cronjob
```
crontab -e
```
add the following line with the minute, hour, day, month, day-of-week you want to run the script
Example:
```
01 07 * * * python3 /usr/home/dirToScript/MM-MonitorHelper/motiondetector.py
````

# MotionDetector

The script `motiondetector.py` controls the screen  depending on the signal of the connected motion detector 

## Prerequisites
- PIR Motion Detector connected to one of the RaspberryPis Pins 

### Config
Costomize the 'MOTION' section in the `config.json` file to control the behavor of the monitor
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
