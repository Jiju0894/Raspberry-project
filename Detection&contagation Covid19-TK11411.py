import time
import RPi.GPIO as GPIO
##from pulsesensor import Pulsesensor
import serial
import sys
import urllib3
import time
from smbus2 import SMBus
from mlx90614 import MLX90614
import numpy as np
import os, time
import string
import pynmea2
from time import sleep


bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

#myAPI = 'G2G75TN9ACKZ0AAV' 
# URL where we will send the data, Don't change it
baseURL = 'http://covid11411.wizzie.online/notify.php?' #% myAPI


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

hb=16

GPIO.setup(hb,GPIO.IN)
beat=0
p=0
sec=0

def GPS_Info():
        global gps
        global map_link
        port="/dev/ttyS0"
        

        ser=serial.Serial(port,baudrate=9600,timeout=0.5)

        dataout =pynmea2.NMEAStreamReader()

        newdata=ser.readline()
        print(newdata)

        if newdata[0:6]==b'$GPRMC':
                newmsg=pynmea2.parse(newdata.decode('ASCII'))

                lat=newmsg.latitude

                lng=newmsg.longitude

                lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
                long_in_degrees = convert_to_degrees(lng)

                gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
                map_link='http://maps.google.com/?q=' + str(lat)+ ',' + str(lng)
                print(map_link)
                print(gps)

def convert_to_degrees(raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

    
gpgga_info = "$GPGGA,"
#ser = serial.Serial ("/dev/ttyS0")            #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

while True:
    
    cnt=GPIO.input(hb);
    if(cnt==False):
        beat=beat+1
        time.sleep(0.05)
        #print(beat)
    
    else:
        time.sleep(0.05);
        p+=1
    
        if(p>5):
            p=0
            sec=sec+1
   #print(sec);

            if(sec>60):
                sec=0
                print("beat:",beat)
                heart=str(beat)

##                print ("Ambient Temperature :", sensor.get_ambient())
                #print ("Object Temperature :", sensor.get_object_1())
                temp= sensor.get_object_1()
                #temp=str(obj_temp)
                print("Temperature= ",temp)

                print("Tracking gps")
                map_link=""
                GPS_Info()
                time.sleep(3)
                http = urllib3.PoolManager()
                url = baseURL +'&lat=%s' % ( lat_in_degrees)+'&lng=%s' % (long_in_degrees)+'&tem=%s' % (temp)+'&h_beat=%s' % (beat)
                print(url)
                resp = http.request('GET', url)
                print("Uploaded")

                beat=0
                p=0
                sec=0

                print()
                time.sleep(4)

time.sleep(4)
                

                

                

