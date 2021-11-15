import serial
import RPi.GPIO as GPIO
from time import sleep
import sys
import time
import dlib
from time import sleep
from urllib.request import urlopen
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import urllib3
import os


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

##BASE_URL = "http://emblocation.wizzie.online/notify.php?"
BASE_URL = "http://traffic11691.wizzie.online/"

ser = serial.Serial ("/dev/ttyAMA0", baudrate=9600)

red_led=38
green_led=40
flag=0

rs=36
en=32
d4=37
d5=35
d6=33
d7=31

GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

GPIO.output(green_led,GPIO.LOW)
GPIO.output(red_led,GPIO.LOW)

a=""

def lcd_cmd(cmd):
    #cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x10==0x10):
        GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
        GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
        GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
        GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)
   

def lcd_data(cmd):
    cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.HIGH)
    
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)

    
    if(cmd & 0x10==0x10):
        GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
        GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.0005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.0005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
        GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
        GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)
    

def lcd_ini():

  lcd_cmd(0x33) 
  lcd_cmd(0x32) 
  lcd_cmd(0x06)
  lcd_cmd(0x0C) 
  lcd_cmd(0x28) 
  lcd_cmd(0x01) 
  time.sleep(0.0005)


def lcd_string(c):
      l=len(c)
      print(c)
      
      for i in range(l):
          lcd_data(c[i])

lcd_ini()
lcd_cmd(0x01)
lcd_string("TRAFFIC VIOLATION")
lcd_cmd(0xc0)
lcd_string("   MONITORING  ")
time.sleep(3)

while True:
    
    if flag==0:
        GPIO.output(red_led,GPIO.LOW)
        GPIO.output(green_led,GPIO.HIGH)
        print("GREEN")
        lcd_cmd(0x01)
        lcd_string("  GO  ")
        time.sleep(3)
        time.sleep(5)
        flag=1
    if flag==1:
        GPIO.output(green_led,GPIO.LOW)
        GPIO.output(red_led,GPIO.HIGH)
        print("RED")
        lcd_cmd(0x01)
        lcd_string("  STOP ")
        time.sleep(5)
        if ser.in_waiting:
            received_data = ser.read()              #read serial port
            sleep(0.03)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            data=str(received_data,'utf-8')
            print(data)
            time.sleep(3)

            if(data== '2E00BD0CD44B'):
                a="AP26Z452"
                print(a)
                print("Card Number",data)
                lcd_cmd(0x01)
                lcd_string("SIGNAL VIOLATED")
                lcd_cmd(0xc0)
                lcd_string(a)
                time.sleep(3)
                time.sleep(3)

            if(received_data== '2E00BD0F53CF'):
                a="KA6B666"
                print(a)
                print("Card Number",data)
                lcd_cmd(0x01)
                lcd_string("SIGNAL VIOLATED")
                lcd_cmd(0xc0)
                lcd_string(a)
                time.sleep(3)
                time.sleep(3)
            if(received_data== '2E00BD0ED14C'):
                a="TS1A141"
                print("Card Number",data)
                print(a)
                lcd_cmd(0x01)
                lcd_string("SIGNAL VIOLATED")
                lcd_cmd(0xc0)
                lcd_string(a)
                time.sleep(3)
                time.sleep(3)
            time.sleep(3)
            hom = 'http://traffic11691.wizzie.online/violations.php?'+'b='+str(a)
            http = urllib3.PoolManager()
            resp = http.request('GET', hom)
            print(resp.status)
            print(hom)
    
            print("sent")
        flag=0



