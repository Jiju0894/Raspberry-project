import os.path
import time
#import urllib3
import sys
import urllib3
#import RPi.GPIO as GPIO
from random import *
#import adafruit_character_lcd.character_lcd as characterlcd
import os
import cv2
import numpy
import pynmea2
import smtplib
import pandas as pd
from PIL import Image, ImageTk
from subprocess import call
##import speech_recognition as sr
import serial
import RPi.GPIO as GPIO      
import os, time
import smtplib
from smbus2 import SMBus
from mlx90614 import MLX90614
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)



# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  #Email Server(don't change)
SMTP_PORT = 587 #Server Port (don't change)
GMAIL_US ='ymtstraining2020@gmail.com'
GMAIL_P ='Ymts@Takeoff'

##r= sr.Recognizer()

text = {}
text1 = {}
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

m1=14
m2=15

rs=21
en=20

d4=26
d5=19
d6=13
d7=6


Id = 0
i=0
j=0

GPIO.setup(m1, GPIO.OUT)
GPIO.setup(m2, GPIO.OUT)

GPIO.output(m1,GPIO.LOW)
GPIO.output(m2,GPIO.LOW)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
            # names related to ids: example ==> Marcelo: id=1,  etc
names = ['user.123', 'user.456', ] 


cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Desktop/Smart Camera Security/dataset/Trainner.yml')
cascadePath = "/home/pi/Desktop/Smart Camera Security/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

dispW=640
dispH=480
flip=2

key = cv2. waitKey(1)
##cam=cv2.VideoCapture(0)
frame_width = int(cam.get(3)) 
frame_height = int(cam.get(4))
size = (frame_width, frame_height) 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size)

############################ MAILLL #################################

email = 'ymtstraining2020@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijumolbabu75@gmail.com'
subject = 'This is the subject'
message = 'This is Message from Home'


file_location2 = '/home/pi/Desktop/Smart Camera Security/NewPicture.jpg'
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
##
############################################## temp sensing ####################################
def temp():
    bus = SMBus(1)
    sensor = MLX90614(bus, address=0x5A)
##    print ("Ambient Temperature :", sensor.get_ambient())
    print ("Object Temperature :", sensor.get_object_1())
    time.sleep(3)
    temp=sensor.get_object_1()
    temp_str=str(temp)
    lcd_cmd(0xc0)
    lcd_string("TEMP::")
    lcd_cmd(0xc4)
    lcd_string(temp_str)
    time.sleep(3)
    bus.close()
    
    if temp>35:
        print("High Temperature")
        lcd_cmd(0x01)
        lcd_string("HIGH TEMP")
        time.sleep(3)
        GPIO.output(m1,GPIO.LOW)
        GPIO.output(m2,GPIO.LOW)
        print("Stop:---- Not allowed")
        lcd_cmd(0xc0)
        lcd_string("NOT ALLOWED")
        time.sleep(3)
        time.sleep(5)

    else:
        print("Normal temperature")
        time.sleep(1)
        lcd_cmd(0x01)
        lcd_string("NORMAL TEMP")
        time.sleep(3)
        print("Allow Inside ")
        lcd_cmd(0xc0)
        lcd_string("ALLOW GO INSIDE")
        time.sleep(3)
        print("Please wait...Door Opening ")
        lcd_cmd(0x01)
        lcd_string("Door Opening..")
        time.sleep(3)
        time.sleep(5)
        time.sleep(2)
        GPIO.output(m1,GPIO.HIGH)
        GPIO.output(m2,GPIO.LOW)
        time.sleep(1)
        GPIO.output(m1,GPIO.LOW)
        GPIO.output(m2,GPIO.LOW)
        time.sleep(3)
        lcd_cmd(0x01)
        lcd_string("Door Closed")
        time.sleep(3)
        GPIO.output(m1,GPIO.LOW)
        GPIO.output(m2,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(m1,GPIO.LOW)
        GPIO.output(m2,GPIO.LOW)


########################################### LCD  ####################################

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

          
##################################################################################### 
lcd_ini()

while True:
      lcd_cmd(0x01)
      lcd_string("   CONTACLESS  ")
      lcd_cmd(0xc0)
      lcd_string("  SCANNING ")
      time.sleep(3)
      ret, img =cam.read()
            #img = cv2.flip(img, -1) # Flip vertically
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
      faces = faceCascade.detectMultiScale(gray,1.2,5)

      for(x,y,w,h) in faces:
          cv2.rectangle(img, (x,y), (x+w,y+h), (225,0,0), 2)
          Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
          idd=str(Id)


            # Check if confidence is less them 100 ==> "0" is perfect match 
          if (confidence < 60):
              if(j==0):
                    
                    
                    print("+++++++++++++++++++++++++")
                    print(Id)                         
                    time.sleep(2)
                    lcd_cmd(0x01)
                    lcd_string("RECOGNISED:")
                    lcd_cmd(0x0c)
                    lcd_string(idd)
                    time.sleep(3)
                    
                    
                    #id = list(names[id])  
                    confidence = "  {0}%".format(round(100 - confidence))
                    j=1
              if i==0:
                print(".................")
                print("Matched")
                i=1
                time.sleep(1)
                lcd_cmd(0xc0)
                lcd_string("MATCHED")
                time.sleep(3)
            
                print("\n [INFO] Initializing temperature checking please show hand and wait ...")
                time.sleep(2)
                lcd_cmd(0x01)
                lcd_string("Temp Checking...")
                time.sleep(3)
                temp()
                time.sleep(3)

                                        
          else:
                                  
                Id = "unknown"
                #print(id)
                print('Not Matched')
                time.sleep(2)
                lcd_cmd(0x01)
                lcd_string("NOT MATCHED")
                time.sleep(3)
                lcd_cmd(0xc0)
                lcd_string("Please Wait...")
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
##
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
                lcd_string("Mail Send")
                time.sleep(3)
                server.quit()          


                confidence = "  {0}%".format(round(100 - confidence))
                i=0
                j=0
                    #time.sleep(0.1)
                    
      cv2.imshow('camera',img)
      if cv2.waitKey(100) & 0xff== ord('q'):
          break
      time.sleep(3)
 

print("\n [INFO] Exiting Program and cleanup stuff")

bus.close()
GPIO.cleanup()
cam.release()
cv2.destroyAllWindows()
time.sleep(5)
