import RPi.GPIO as GPIO
import time, sys
import sys
import cv2
import numpy as np
import os, time
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser                  
import serial
import smtplib
import os.path
from time import sleep
import time
import digitalio
import board
from Adafruit_IO import Client, Feed, RequestError
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
import pyttsx3
speak=pyttsx3.init()

ADAFRUIT_IO_KEY = 'aio_LMLN416srQxGaoj3xLKETeUHwvFf' # Set your APIO Key
 # Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'JijuGrace'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

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
GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

sw = 22
m1=27
m2=17

rs=21
en=20

d4=26
d5=19
d6=13
d7=6

GPIO.setup (sw, GPIO .IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(m1, GPIO.OUT)
GPIO.setup(m2, GPIO.OUT)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5,GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

GPIO.output(m1,GPIO.LOW)
GPIO.output(m2,GPIO.LOW)


email = 'ymtstraining2020@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijumolbabu75@gmail.com'
subject = 'Message From Home'
message = 'Someone At Door'
file_location1 = '/home/pi/Desktop/Smart Wifi DoorBell/filename.avi'
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

file_location2 = '/home/pi/Desktop/Smart Wifi DoorBell/NewPicture.jpg'
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

try: 
    digital = aio.feeds('digital')
    
except RequestError: 
    feed = Feed(name="digital")
    LED = aio.create_feed(feed)
# led set up
led = digitalio.DigitalInOut(board.D6)
led.direction = digitalio.Direction.OUTPUT

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
    
    GPIO.output(en,GPIO.HIGH)
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

def gsm():
          
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
    port.write(b'AT\r\n')
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(b"AT+CMGF=1\r")
    print("Text Mode Enabled…")
    time.sleep(3)
    port.write(b'AT+CMGS="9526234625"\r')
    msg = "Someone at Door"
    print("sending message….")
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(1)
    print("message sent…")


while True:
    lcd_cmd(0x01)
    lcd_string("SMART DOOR BELL")
    time.sleep(0.5)
    val=GPIO.input(sw)
    print(val)
    if val==0:
        print("Someone at Door")
        lcd_cmd(0x01)
        lcd_string("Calling Bell...")
        time.sleep(0.5)
        gsm()
        print("with in camera")
        check, frame = cam.read()
        print(check) #prints true as long as the webcam is running
        print(frame) #prints matrix values of each framecd
        #result.write(frame)
        cv2.imshow("Capturing", frame)
        lcd_cmd(0x01)
        lcd_string("CAPTURING...")
        time.sleep(0.5)
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
        lcd_cmd(0xc0)
        lcd_string("CAPTURED")
        time.sleep(0.5)

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
        lcd_string("SENDING MAIL...")
        time.sleep(0.5)
        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
        server.login(email, password)
        text = msg1.as_string()
        server.sendmail(email, send_to_email, text)
        print("mail sended")
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
        server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
        server.login(email, password)
        text = msg2.as_string()
        server.sendmail(email, send_to_email, text)
        print("mail sended")
        lcd_cmd(0xc0)
        lcd_string("MAIL SEND")
        time.sleep(0.5)
        server.quit()

        print("Someone at Door... Please Open")
        print("Click adafruit")
        time.sleep(8)
        
        data = aio.receive(digital.key)
        if int(data.value) == 1:
            speak.say("Door Opening.. Please Wait")
            speak.runAndWait()
            print('Door Opening.. Please Wait')
            time.sleep(3)
            GPIO.output(m1,GPIO.HIGH)
            GPIO.output(m2,GPIO.LOW)
            time.sleep(1)
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(m2,GPIO.LOW)
            time.sleep(2)
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(m2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(m2,GPIO.LOW)
            time.sleep(2)
            
            
            
        elif int(data.value) == 0:
            print('No one at Home')
            speak.say("noone at Home please come later")
            speak.runAndWait()
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(m2,GPIO.LOW)
 
    #led.value = int(data.value)

        

GPIO.cleanup()
cam.release()

cv2.destroyAllWindows()
