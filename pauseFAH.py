#!/usr/bin/env python
#SPDX-License-Identifier: MIT
from telnetlib import Telnet
from subprocess import check_output,CalledProcessError

PROCLIST = ['dota2'] #List of programs that will pause FAHClient if its running
BATTERY_THRESHOLD = 88 #When FAHClient will pause

program_running = False

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

