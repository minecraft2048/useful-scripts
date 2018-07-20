#!/usr/bin/env python
#SPDX-License-Identifier: MIT

#Pauses Folding@Home if running on battery power, or battery is below a certain percentage,
#or a program is running

#Supports only Linux for now
#Run this script periodically for automation, for example using systemd user timers

from telnetlib import Telnet
from subprocess import check_output,CalledProcessError

PROCLIST = ['dota2','NSUNS4.exe','NSUNS.exe'] #List of programs that will pause FAHClient if its running
BATTERY_THRESHOLD = 88 #Battery percentage that FAHClient will pause

program_running = False
on_ac_power = False

for proc in PROCLIST:
    interm = 0
    try:
        interm = check_output(["pidof",proc]) 
    except CalledProcessError:
        pass
    if interm:
        program_running = True
        print(f"{proc} is running")
        break

#Change BAT1 and ADP1 to your actual device name
#You can find those by running ls /sys/class/power_supply
#BAT* is battery while ADP* is AC power

with open('/sys/class/power_supply/BAT1/capacity','r') as bat:
    battery_level = int(bat.readline())

with open('/sys/class/power_supply/ADP1/online','r') as ac:
    on_ac_power = int(ac.readline())

with Telnet('localhost',36330) as tn:
    if battery_level >= BATTERY_THRESHOLD and on_ac_power and not program_running:
        print("Starting FAH")
        tn.write(b'unpause')
    else:
        print("Pausing FAH")
        tn.write(b'pause')
