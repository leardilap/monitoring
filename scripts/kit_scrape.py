#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adapted from apollo_scrape.py for KIT crate by Luis Ardila <luis.ardila@kit.edu>
"""


import time
import re
import pickle
import struct
import socket
from os import popen
from collections import defaultdict

# settable parameters
IPMI_IP = "192.168.10.22"
IPMI_ADDR = [ 
    0x5A, # Fan Tray Lower
    0x5C, # Fan Tray Upper
    0x9A, # slot 01 (9a): Serenity-Z1.0 + OpenIPMC_v1.0(12) + STLINK_v3.0
    #0x96, # slot 02 (96):
    #0x92, # slot 03 (92):
    0x8E, # slot 04 (8e): Pulsar iib (no FPGA) + OpenIPMC_v1.0(14)
    #0x8A, # slot 05 (8a): Pulsar iib (with FPGA) + OpenIPMC_v1.0(07)
    0x86, # slot 06 (86): Pulsar iib (no FPGA) + OpenIPMC_v1.0(05)
    0x82, # slot 07 (82): Vadatech ATC807 ETH SW
    0x84, # slot 08 (84): Pulsar iib (no FPGA) + OpenIPMC_v1.0(15)
    0x88, # slot 09 (88): Pulsar iib (no FPGA) + OpenIPMC_v1.0(08)
    0x8C, # slot 10 (8c): Serenity-Z1.1 + OpenIPMC_v1.0(01) + miniSTLINK_v3.0
    #0x90, # slot 11 (90):
    #0x94, # slot 12 (94):
    0x98, # slot 13 (98): Pulsar iib (no FPGA) + OpenIPMC_v1.0(06) 
    0x9C  # slot 14 (9c): Pulsar iib (no FPGA) + OpenIPMC_v1.0(13)
    ] 
    
IPMI_STR  = [ 
    "FTL.", 
    "FTU.", 
    "Slot01.", 
    #"Slot02.", 
    #"Slot03.", 
    "Slot04.", 
    #"Slot05.", 
    "Slot06.", 
    "Slot07.", 
    "Slot08.", 
    "Slot09.", 
    "Slot10.", 
    #"Slot11.", 
    #"Slot12.", 
    "Slot13.", 
    "Slot14."
    ]
GRAPHITE_IP = '127.0.0.1'
GRAPHITE_PORT = 2004
carbon_directory = "atca.kit."  

#%%
def get_all_sensors(ipmi_ip, ipmi_addr):
    cmd = 'ipmitool -H %s -P "" -t 0x%x sensor ' % (ipmi_ip, ipmi_addr)
    print (cmd)
    output = popen(cmd).read()
    res = []
    for l in output.splitlines():
        s = l.split("|")
        sm = list(map(str.strip,s))
        res.append(sm)
        #print(",".join(sm))
    return res
    #print(s)

#%%
def map_fcn(val):
   if val == 'na' or val is None:
        return ""
   else:
        return str(val)
#%%
sleeptime=60.0


tempstr = re.compile("[Tt]em")
fanstr= re.compile("Tach")
OpenIPMC = re.compile("PIM400")

db = ([])
ii = 0

# set up connection to Graphite database
sock = socket.socket()
sock.connect((GRAPHITE_IP, GRAPHITE_PORT))
starttime = time.time()
#%%
while True:
    sensors = defaultdict(list)
    for i in range(len(IPMI_ADDR)):
        sensor_raw = get_all_sensors(IPMI_IP, IPMI_ADDR[i])
        for s in sensor_raw:
            #print(s)
            s[0] = s[0].rstrip('\.')
            #if tempstr.search(s[0]) or fanstr.search(s[0]) or OpenIPMC.search(s[0]) :
            if s[1] != 'na':
                sensors[IPMI_STR[i]+s[0]] = s[1]
    time_epoch= int(time.time())

    for key in sensors.keys():
       try:
           header = (carbon_directory + key).replace(" ", "_")
           if sensors[key][0] == '0' and sensors[key][1] == 'x':
               val = float.fromhex(sensors[key])
           else:
               val = float(sensors[key])
           db.append((header,(time_epoch, val)))
       except ValueError:
           print("can't make this a float:", sensors[key])

    if len(db) > 50 :
        payload = pickle.dumps(db, protocol=2)
        header = struct.pack("!L", len(payload))
        print(db)
        message = header + payload
        sock.sendall(message)
        ii = ii+ 1
        print('sent packet ', ii)
        db = ([])
    # sleep, taking into account how long the times took. 
    time.sleep(sleeptime- ((time.time()-starttime)%sleeptime))

sock.detach()
sock.close()

