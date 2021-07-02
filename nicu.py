import RPi.GPIO as GPIO
import time
import threading
from mcp3208 import MCP3208
import Adafruit_DHT
import serial
import sys
import urllib3
import sys
import cv2
#print(cv2.__version__)
import numpy as np
import os, time
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser                  
import serial
import pynmea2
import smtplib
import os.path
import threading
from time import sleep
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders


dispW=640
dispH=480
flip=2

key = cv2. waitKey(1)
cam=cv2.VideoCapture(0)
frame_width = int(cam.get(3)) 
frame_height = int(cam.get(4))
size = (frame_width, frame_height) 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

myAPI = 'CC6OSRV7J2L36FU2' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

hb=23
m1=2
m2=3
relay=17

rs=21
en=20


d4=26
d5=19
d6=13
d7=6

GPIO.setup(hb,GPIO.IN)
GPIO.setup(m1, GPIO.OUT)
GPIO.setup(m2, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

GPIO.output(m1,GPIO.LOW)
GPIO.output(m2,GPIO.LOW)
GPIO.output(relay,GPIO.LOW)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)


beat=0
p=0
sec=0

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

email = 'ymtstraining2020@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijumolbabu75@gmail.com'
subject = 'This is the subject'
message = 'This is Message about NICU'
file_location1 = '/home/pi/NICU/filename.avi'
msg1 = MIMEMultipart()#Create the container (outer) email message.
msg1['From'] = email
msg1['To'] = send_to_email
msg1['Subject'] = subject
'''as.string()  
 |
 +------------MIMEMultipart  
              |                                                |---content-type  
              |                                   +---header---+---content disposition  
              +----.attach()-----+----MIMEBase----|  
                                 |                +---payload (to be encoded in Base64)
                                 +----MIMEText'''
msg1.attach(MIMEText(message, 'plain'))#attach new  message by using the Message.

file_location2 = '/home/pi/NICU/NewPicture.jpg'
msg2 = MIMEMultipart()#Create the container (outer) email message.
msg2['From'] = email
msg2['To'] = send_to_email
msg2['Subject'] = subject
'''as.string()  
 |
 +------------MIMEMultipart  
              |                                                |---content-type  
              |                                   +---header---+---content disposition  
              +----.attach()-----+----MIMEBase----|  
                                 |                +---payload (to be encoded in Base64)
                                 +----MIMEText'''
msg2.attach(MIMEText(message, 'plain'))

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        
        if ((adcnum > 7) or (adcnum < 0)):
                
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(14):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


def Convert_volt(data):
        volts=(data*3.3)/float(1023)
        volts=round(volts,2)
        return volts

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
                                lcd_cmd(0x01)
                                lcd_string("HEART BEAT:")
                                lcd_cmd(0x8c)
                                lcd_string(heart)
                                time.sleep(3)

                                temperature = sensor.get_temperature()
                                temp=str(temperature)
                                print("The temperature in celsius:" , temperature)
                                lcd_cmd(0xc0)
                                lcd_string("TEMP:")
                                lcd_cmd(0xc7)
                                lcd_string(temp)
                                time.sleep(3)

                                humidity, temperature1 = Adafruit_DHT.read_retry(11, 12)
                ##                tem=str(temperature1)
                                hum=str(humidity)
                ##                print("temperature"  ,temperature1)
                                print("humidity"  ,humidity)
                                lcd_cmd(0x01)
                                lcd_string("HUMI:")
                                lcd_cmd(0x87)
                                lcd_string(hum)
                                time.sleep(3)
                        
                                x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
                                y= readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
                                z= readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
                                print("X-axis:" ,x, "Y-axis:" ,y,"Z-axis:" ,z);
                                ldr= readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
                                light=Convert_volt(ldr)
                                print("Light Intensity:" ,light, "v");
                                time.sleep(0.5)

                                
                                if((beat<30) and (beat!=0) or (beat>120)):
                                        print("heart beat exceeded---- Turn ON ventilator")
                                        lcd_cmd(0x01)
                                        lcd_string("HB Exceeded")
                                        lcd_cmd(0xc0)
                                        lcd_string("ON Ventilator")
                                        time.sleep(3)
                                        GPIO.output(m1,GPIO.HIGH)
                                        GPIO.output(m2,GPIO.LOW)
                                        print("Ventilator ON")
                                    
                          
                                if((beat>30) or (beat<120)):
                                        print("heart beat  normal")
                                        lcd_cmd(0x01)
                                        lcd_string("HB Normal")
                                        lcd_cmd(0xc0)
                                        lcd_string("Ventilator OFF")
                                        time.sleep(3)
                                        GPIO.output(m1,GPIO.LOW)
                                        GPIO.output(m2,GPIO.LOW)
                                        print("Ventilator OFF")

                                if light<1:
                                        print("DARK----Turn ON Light")
                                        lcd_cmd(0x01)
                                        lcd_string("   DARK   ")
                                        lcd_cmd(0xc0)
                                        lcd_string("  TURN ON Light")
                                        time.sleep(3)
                                        GPIO.output(relay,GPIO.HIGH)
                                        print("Light ON")

                                if light>1:
                                        print("ENOUGH LIGHt----Turn OFF Light")
                                        lcd_cmd(0x01)
                                        lcd_string("   LIGHT  ")
                                        lcd_cmd(0xc0)
                                        lcd_string("  TURN OFF Light")
                                        time.sleep(3)
                                        GPIO.output(relay,GPIO.LOW)
                                        print("Light OFF")

                                if  x<1350 or x>1450 or y<1300 or y>1400 or temperature>32 or humidity>95:
                                        print("   EMERGENCY  ")
                                        lcd_cmd(0x01)
                                        lcd_string("  EMERGENCY  ")
                                        lcd_cmd(0xc0)
                                        lcd_string("Camera ON...")
                                        time.sleep(3)
                                        print("with in cemara")
                                        check, frame = cam.read()
                                        print(check) #prints true as long as the webcam is running
                                        print(frame) #prints matrix values of each framecd
                                        #result.write(frame)
                                        cv2.imshow("Capturing", frame)
                                        for i in range(0, 25):
                                                print('frame #:', i)
                                                check, frame = cam.read()
                                                #frame = cv2.QueryFrame(capture)
                                                #cv2.ShowImage("w1", frame)
                                                result.write(frame)
                                                cv2.imwrite("NewPicture.jpg",frame)
                                                cv2.imshow("Capturing", frame)
                                                cv2.moveWindow('Capturing',0,0)

                                        if (i==25):
                                                cam.release()
                                                cam.release()
                                                break
                                        print ('released capture')

                                        filename = os.path.basename(file_location1)#function returns the tail of the path
                                        attachment = open(file_location1, "rb") #“rb” (read binary)
                                        part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
                                        part.set_payload((attachment).read())
                                        encoders.encode_base64(part)
                                        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
                                        msg1.attach(part)
                                        server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
                                        print("with in msg")
                                        lcd_cmd(0x01)
                                        lcd_string("Sending Mail...")
                                        time.sleep(3)
                                        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
                                        server.login(email, password)
                                        text = msg1.as_string()
                                        server.sendmail(email, send_to_email, text)
                                        print("mail sended")
                                        lcd_cmd(0xc0)
                                        lcd_string("Sended Mail")
                                        time.sleep(3)
                                        server.quit()

                                        time.sleep(5)

                                        filename = os.path.basename(file_location2)#function returns the tail of the path
                                        attachment = open(file_location2, "rb") #“rb” (read binary)
                                        part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
                                        part.set_payload((attachment).read())
                                        encoders.encode_base64(part)
                                        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
                                        msg2.attach(part)
                                        server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
                                        print("with in msg")
                                        lcd_cmd(0x01)
                                        lcd_string("Sending Mail...")
                                        time.sleep(3)
                                        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
                                        server.login(email, password)
                                        text = msg2.as_string()
                                        server.sendmail(email, send_to_email, text)
                                        print("mail sended")
                                        lcd_cmd(0xc0)
                                        lcd_string("Mail Sended")
                                        time.sleep(3)
                                        server.quit()

                                else:
                                        print("   SAFE  ")
                                        

                                      
                                        

                                http = urllib3.PoolManager()
                                url = baseURL +'&field1=%s' % (beat)+'&field2=%s' % (humidity)+'&field3=%s' % (temperature)+'&field4=%s' % (light)
                                print(url)
                                resp = http.request('GET', url)
                                beat=0
                                p=0
                                sec=0
                       
                                print()
                                time.sleep(4)

