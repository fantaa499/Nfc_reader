#!/usr/bin/python2.7
import sys
print(sys.version)

import MFRC522
import signal
import time
import os
import RPi.GPIO as GPIO
from datetime import datetime

class Card:
        def __init__(self, uid, time):
                self.uid  = uid
                self.into = False
                self.time = time
        uid = [0, 0, 0, 0, 0]
        into = False
        time = 0



continue_reading = True
MIFAREReader = MFRC522.MFRC522()

cardA = Card([210,125,221,43,89], datetime.now())

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

def end_read(signal, frame):
  global continue_reading
  continue_reading = False
  print "Ctrl+C captured, ending read."
  MIFAREReader.GPIO_CLEEN()

signal.signal(signal.SIGINT, end_read)

while continue_reading:
  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
  if status == MIFAREReader.MI_OK:
    print "Card detected"
  (status,backData) = MIFAREReader.MFRC522_Anticoll()
  if status == MIFAREReader.MI_OK:
    print "Card read UID: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4])
    if ( backData == cardA.uid ):
      print "welcome"
      GPIO.output(7, 1)
      if cardA.into:
	cardA.into = False
	delt = (datetime.now()-cardA.time).seconds/60
        if delt > 60: 
	  cost = 300 + (delt-60)*3.5
        else:
	  cost = 300 
	f1 = open("../telegram/text1.txt", 'wb')
        f1.write("User with cardA is left at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
	f1.write("!!!Total = " +str(delt)+"min " +  str(cost) + "rub" + '\n')
        f1.close()
        f2 = open("../telegram/text2.txt", 'ab')
        f2.write("User with cardA is left at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
	f2.write("!!!Total = " +str(delt)+"min " +  str(cost) + "rub" + '\n') 
	f2.close()
        os.system('python telegram.py')
	time.sleep(1)
	GPIO.output(7, 0)
      else:
	cardA.into = True
	f1 = open("../telegram/text1.txt", 'wb')
        f1.write("User with cardA is comming at " + cardA.time.strftime("%Y-%m-%d %H:%M:%S") )
        f1.close()
        f2 = open("../telegram/text2.txt", 'ab')
        f2.write("User with cardA is comming at " + cardA.time.strftime("%Y-%m-%d %H:%M:%S") + '\n')	
        f2.close()
        os.system('python telegram.py')
        time.sleep(1)
	GPIO.output(7, 0)
    else:
      print "wrong Card"

