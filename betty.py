import pygame
import sqlite3
import time
import os

from time import sleep

from datetime import datetime

logperiod = 1
FuelTank1 = 1000000 # starting with a big number to avoid devision by 0
FuelConsumptionRate = 20 # litres per hour

pygame.mixer.pre_init(8000, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
pygame.mixer.init()


#get the database ready
memdb = sqlite3.connect('/memdb/memdb.db')
cursor = memdb.cursor()
cursor.execute('''PRAGMA journal_mode=WAL''')

while True:
    cursor.execute("SELECT CANid, Param_Text, Param_Value FROM messages")
    results = cursor.fetchall()
    for row in results:
        if (row[1]=='Pitch' and row[2]<-20):
            pygame.mixer.music.load('pull-up.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        if (row[1]=='Roll' and abs(row[2])>45):
            pygame.mixer.music.load('warnbkangle.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        if (row[1]=='FuelTank1' and abs(FuelTank1-row[2])/FuelTank1 > 0.3):
            RemainingMinutes = round(row[2]*60/FuelConsumptionRate)
            cmd = 'pico2wave -w tmp_wav.wav "Remaining fuel ' + str(RemainingMinutes) + ' minutes "'
            os.system(cmd)
            pygame.mixer.music.load('tmp_wav.wav')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            os.system('rm tmp_wav.wav')
            FuelTank1 = row[2]
            if (FuelTank1 == 0):
                FuelTank1 = 1 # dirty hack to avoid dev by zero
    time.sleep(logperiod)
