#!/usr/bin/python
# -*- coding: UTF-8 -*-

import serial
import RPi.GPIO as GPIO

import os
import sys
import time
import threading
# from ctypes import c_byte, c_ubyte, Structure, c_uint16

# class SerialData(Structure):
#     _pack_ = 1
#     _fields_ = [("seq", c_ubyte)
#                 , ("opcode", c_uint16)]
    
# seiral port
_serial0 = "/dev/ttyAMA0"
_serial1 = "/dev/ttyS0"
    
# baudRate
_1200    = 1200
_2400    = 2400
_4800    = 4800
_9600    = 9600
_19200   = 19200
_38400   = 38400
_57600   = 57600
_115200  = 115200

# setting
port = _serial0
baudRate = _9600

alivethread = True
ser = serial.Serial(port, baudRate, timeout=3)


gpioPin = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioPin, GPIO.OUT)


def readThread(ser):
# 쓰레드 종료될때까지 계속 돌림
    while alivethread:        
        print('read')

        if ser.isOpen():
            print("Open")
            res = ser.readline() # 시리얼 통신 타임아웃 설정 필요. rs485test.py line.38
            if res:
                print('res : ', res)

        if ser.inWaiting():
           print("Serial wating issue")

        time.sleep(0.25)
    
    #ser.close()


def main():
    # 시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readThread, args=(ser,))
    thread.start()
    
    seq = 0
    while alivethread:

        GPIO.output(gpioPin, GPIO.HIGH)
        print('GPIO.HIGH')

        strcmd = "ff ff 00 00"
        
        print('[ seq : {0} ] [ send data : {1} ]').format(seq, strcmd)

        seq = seq + 1
        #ser.write(strcmd.encode())
        ser.write(strcmd)
        time.sleep(1)

        GPIO.output(gpioPin, GPIO.LOW)
        print('GPIO.LOW')
        time.sleep(1)

        
main()