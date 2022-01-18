#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from ast import Global
import serial
import RPi.GPIO as GPIO

import os
import sys
import time
from enum import Enum
import datetime
import multiThread

#seiral port
_serial0 = "/dev/ttyAMA0"
_serial1 = "/dev/ttyS0"
    
#baudRate
_1200    = 1200
_2400    = 2400
_4800    = 4800
_9600    = 9600
_19200   = 19200
_38400   = 38400
_57600   = 57600
_115200  = 115200
  
port = _serial0
baudRate = _9600

alivethread = True
ser = serial.Serial(port, baudRate, timeout=3)


gpioPin = 16
readCheck = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.OUT)


def readThread(ser):
# 쓰레드 종료될때까지 계속 돌림
    print("worker done")
    
    while alivethread:        
        #print(f'{readCheck}')
        if(readCheck):
            if ser.isOpen():
                res = ser.readline()
                if res:
                    print('res : ', res)

            if ser.inWaiting():
                print("Serial wating issue")

        time.sleep(0.25)
    
    ser.close()


def main():
    # 시리얼 읽을 쓰레드 생성 # multiThread에 있는 클래스로 이동필요
    thread = multiThread.Thread(target=readThread, args=(ser,))
    thread.start()
    seq = 0
    try:
        while alivethread:

            GPIO.output(gpioPin, GPIO.HIGH)
            #print('GPIO.HIGH')
            global readCheck
            readCheck = False
            #seq = hex(int(seq)).replace("0x","")
            today = datetime.datetime.now().strftime("%X")
            strcmd = f'{seq}:{today}'
            #strcmd = "{0}:{1}".format(seq, today)            

            #print('[ seq : {0} ] [ send data : {1} ]').format(seq, strcmd)
            print(f'[seq : {seq} ] [ send data : {strcmd} ]')

            seq = seq + 1
            ser.write(strcmd.encode())
            time.sleep(1)

            GPIO.output(gpioPin, GPIO.LOW)
            #print('GPIO.LOW')
            readCheck = True
            time.sleep(1)    
            
    except:
        pass
    
    print('exit')

    

main()