import RPi.GPIO as GPIO
import time

import serial
import math, random
import cv2
import numpy as np
import os
import os.path
import digitalio
import os.path
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
import sys
import board
from Adafruit_IO import Client, Feed, RequestError
import smtplib


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SMTP_SERVER = 'smtp.gmail.com'  #Email Server(don't change)
SMTP_PORT = 587 #Server Port (don't change)
GMAIL_US ='ymtstraining2021@gmail.com'
GMAIL_P ='Ymts@Takeoff'


ADAFRUIT_IO_KEY = 'aio_bQHt96DGNdgLajQZ4xsaLY6IX3OJ' # Set your APIO Key
 # Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'JijuGrace'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



L1 = 18
L2 = 23
L3 = 24
L4 = 25

C1 = 10
C2 = 9
C3 = 11

m1=27
##m2=17

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(m1, GPIO.OUT)
##GPIO.setup(m2, GPIO.OUT)

GPIO.output(m1,GPIO.LOW)
##GPIO.output(m2,GPIO.LOW)


k=0
a=0
secretCode = "1133"
input = ""
count_char=0
pass_key="2222"
val=0



Id = 0
i=0
j=0
names = ['user.123', 'user.456', ] 


cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Desktop/Smart Door/dataset/Trainner.yml')
cascadePath = "/home/pi/Desktop/Smart Door/data/haarcascade_frontalface_default.xml"
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

email = 'ymtstraining2021@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijumolbabu75@gmail.com'
subject = 'msg from Home. Someone at door'
message = 'Captured Image'
##file_location = '/home/pi/Desktop/sourcecode/AGRI0.png'
##msg = MIMEMultipart()#Create the container (outer) email message.
##msg['From'] = email
##msg['To'] = send_to_email
##msg['Subject'] = subject


file_location1 = '/home/pi/Desktop/Smart Door/NewPicture.jpg'
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
msg1.attach(MIMEText(message, 'plain'))


##file_location2 = '/home/pi/Desktop/Smart Door/unknown.jpg'
##msg2 = MIMEMultipart()#Create the container (outer) email message.
##msg2['From'] = email
##msg2['To'] = send_to_email
##msg2['Subject'] = subject
##'''as.string()  
## |
## +------------MIMEMultipart  
##              |                                                |---content-type  
##              |                                   +---header---+---content disposition  
##              +----.attach()-----+----MIMEBase----|  
##                                 |                +---payload (to be encoded in Base64)
##                                 +----MIMEText'''
##msg2.attach(MIMEText(message, 'plain'))


try: 
    digital = aio.feeds('door')
    
except RequestError: 
    feed = Feed(name="door")
    LED = aio.create_feed(feed)
# led set up
led = digitalio.DigitalInOut(board.D6)
led.direction = digitalio.Direction.OUTPUT


def sendmail():
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
    server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
    server.login(email, password)
    text = msg1.as_string()
    server.sendmail(email, send_to_email, text)
    print("mail sended")
    server.quit()
    door()

def door():
    print("Someone at Door... Please Open")
    print("Click adafruit")
    time.sleep(8)
    
    data = aio.receive(digital.key)
    if int(data.value) == 1:
        print('Door Opening.. Please Wait')
        time.sleep(3)
        GPIO.output(m1,GPIO.HIGH)
##        GPIO.output(m2,GPIO.LOW)
        time.sleep(1)
        GPIO.output(m1,GPIO.LOW)
##        GPIO.output(m2,GPIO.LOW)
        print("Door Opened")
        time.sleep(2)
        print("Door Closing...")
        GPIO.output(m1,GPIO.HIGH)
##        GPIO.output(m2,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(m1,GPIO.LOW)
##        GPIO.output(m2,GPIO.LOW)
        time.sleep(2)
            
            
            
    elif int(data.value) == 0:
        print('No one at Home')
        GPIO.output(m1,GPIO.LOW)
##        GPIO.output(m2,GPIO.LOW)

    
    

def readLine(line, characters):
    count_char=0
    global input, key,s,a
    while a==1 :
##        print("enter")
        GPIO.output(line, GPIO.HIGH)
        
        
        if(GPIO.input(C1) == 1): 
            print(characters[0])
            count_char=count_char+1
            key=characters[0]
            input = input + characters[0]
            time.sleep(2)

        if(GPIO.input(C2) == 1):
            print(characters[1])
            count_char=count_char+1
            key=characters[1]
            input = input + characters[1]
            time.sleep(2)

        if(GPIO.input(C3) == 1):
            
            print(characters[2])
            count_char=count_char+1
            key=characters[2]
            input = input + characters[2]

            time.sleep(2)

        if count_char==4:
            
            if input == secretCode :
                print("Code correct!")
                time.sleep(1)
                input=""
                a=0
                door()

            else:
                print("Code Incorrect!")
                time.sleep(1)
                input=""
                a=0
                sendmail()

        GPIO.output(line, GPIO.LOW)
##    return input


def keypad():
    
    readLine(L1, ["1","2","3"])
    readLine(L2, ["4","5","6"])
    readLine(L3, ["7","8","9"])
    readLine(L4, ["*","0","#"])


while True:

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
                    
                    #id = list(names[id])  
                confidence = "  {0}%".format(round(100 - confidence))
                j=1
            if i==0:
                print(".................")
                print("Matched")
                i=1
                time.sleep(1)
                a=1
                keypad()
                time.sleep(1)            
                                    
        else:
                                        
            Id = "unknown"
            #print(id)
            print('Not Matched')
            time.sleep(2)
                       
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
            filename = os.path.basename(file_location1)#function returns the tail of the path
            attachment = open(file_location1, "rb") #“rb” (read binary)
            part = MIMEBase('application', 'octet-stream')#Content-Type: application/octet-stream , image/png, application/pdf
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)#Content-Disposition: attachment; filename="takeoff.png"
            msg1.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)# Send the message via local SMTP server.
            print("with in msg")
            server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
            server.login(email, password)
            text = msg1.as_string()
            server.sendmail(email, send_to_email, text)
            print("mail sended")
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


    
