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
    def __init__(self, uid, name, time):
        self.uid  = uid
        self.into = False
        self.time = time
        self.name = name
    self.uid = []
    self.into = False
    self.time = 0
    self.name = ""

class Employees:
    def __init__(self, cards):
        self.cards = cards

    def get_card_from_uid(self, card_uid):
        for card, i in enumerate(self.cards):
            if card.uid == card_uid:
                return card, i
        return None

    self.cards = []


continue_reading = True
MIFAREReader = MFRC522.MFRC522()

cardA = Card([102, 47, 169, 247, 23], "Islam", datetime.now())
cardB = Card([102, 182, 117, 247, 82], "Nimat", datetime.now())
cardC = Card([198, 76, 97, 247, 28], "brother of Daurona", datetime.now())
cardD = Card([217, 212, 198, 32, 235], "yong men", datetime.now())

employees = Employees([cardA, cardB, cardC, cardD])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    print ("Ctrl+C captured, ending read.")
    MIFAREReader.GPIO_CLEEN()

def diod_when_user_in():
    time.sleep(0.3)
    GPIO.output(7, 0)
    time.sleep(0.3)
    GPIO.output(7, 1)
    time.sleep(0.3)
    GPIO.output(7, 0)

def diod_when_user_out():
    time.sleep(0.1)
    GPIO.output(7, 0)
    time.sleep(0.1)
    GPIO.output(7, 1)
    time.sleep(0.1)
    GPIO.output(7, 0)
    time.sleep(0.1)
    GPIO.output(7, 1)
    time.sleep(0.1)
    GPIO.output(7, 0)
    time.sleep(0.1)
    GPIO.output(7, 1)
    time.sleep(0.1)
    GPIO.output(7, 0)


signal.signal(signal.SIGINT, end_read)

while continue_reading:
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    (status, backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print ("Card read UID: " + str(backData[0]) + ","
                                 + str(backData[1]) + ","
                                 + str(backData[2]) + ","
                                 + str(backData[3]) + ","
                                 + str(backData[4]))
        # карта считана, проверим корректен ли ее номер
        detected_card, i = employees.get_card_from_uid(backData)
        # Если номер карты не корректен
        if detected_card == None:
            print ("Wrong card")
            # выходим из итерации
            continue
        # в ином случае пользователь найден
        else:
            print ("welcome" + detected.name)
            # Включить диод
            GPIO.output(7, 1)
            if detected_card.into:
                detected_card.into = False
                delt = datetime.now() - detected_card.time

                f1 = open("../telegram/text1.txt", 'wb')
                f1.write(detected_card.name + " left at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
                f1.write("Total time = " + str(delt) + '\n')
                f1.close()
                f2 = open("../telegram/text2.txt", 'ab')
                f2.write(detected_card.name + " left at " + datetime.now().strftime("%m-%d %H:%M") + '\n')
                f2.write("Total = " + str(delt) + '\n')
                f2.close()
                os.system('python telegram.py')
                diod_when_user_out()
            else:
                detected_card.into = True
                detected_card.time = datetime.now()
                f1 = open("../telegram/text1.txt", 'wb')
                f1.write(detected_card.name +
                         " comes at " +
                         detected_card.time.strftime("%Y-%m-%d %H:%M:%S"))
                f1.close()
                f2 = open("../telegram/text2.txt", 'ab')
                f2.write(detected_card.name +
                         " comes at " +
                         detected_card.time.strftime("%m-%d %H:%M") +
                         '\n')
                f2.close()
                os.system('python telegram.py')
                diod_when_user_in()
            employees.cards[i] = detected_card
