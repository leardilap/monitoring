#!/usr/bin/env python3

import logging
import pickle
import sys
import re
import time
import snap7
import struct
import colorsys
import os
import socket
import datetime
from bs4 import BeautifulSoup
import sys
import urllib.request as urllib2
import requests

def readtemp(address, sensor):
  #stream = os.popen('ssh root@192.168.10.22 "clia sensordata '+address+' 0:'+sensor+' | grep Processed | cut -b 21-25"')
  stream = os.popen('ipmitool -H 192.168.10.22 -P "" -t ' + address + ' sensor | grep "' + sensor + '" | cut -b 20-25')
  temp_cc=""
  for i in stream.read():
    temp_cc+=i
  print(sensor + " " + temp_cc)
  return float(temp_cc)
  
PIM400KZ_current=readtemp("0x8c","CURRENT PIM400")

timestamp = time.time()

dblist = []
if PIM400KZ_current!="na": dblist.append(["kit_atca_007.temperatues.PIM400KZ_current", ( timestamp, PIM400KZ_current) ])

payload = pickle.dumps(dblist, protocol=2)
header = struct.pack("!L", len(payload))
message = header + payload

retrycount = 0
while (retrycount < 10):

  sock = socket.socket()
  sock.settimeout(1)

  try :
    sock.connect(('127.0.0.1', 2004))
    sock.send(message)
    break;

  except (socket.timeout, socket.error) as error:
    logging.error('connect error: %s', error)
    retrycount += 1

sock.close()
