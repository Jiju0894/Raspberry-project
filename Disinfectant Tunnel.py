import RPi.GPIO as GPIO
import sys
import cv2
#print(cv2.__version__)
import numpy as np
import os, time
import serial
import webbrowser           #import package for opening link in browser                  
import serial
import pynmea2
import smtplib
import os.path
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
from smbus2 import SMBus
from mlx90614 import MLX90614
from time import sleep
from email.mime.text import MIMEText#email.mime.text.MIMEText(_text[, _subtype[, _charset]])
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase#email.mime.base.MIMEBase(_maintype(e.g. text or image), _subtype(e.g. plain or gif), **_params(e.g.key/value dictionary))
from email import encoders
import pyttsx3
import time


engine = pyttsx3.init()

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
ir=23
soil=24
buzzer=21

rs=20
en=16

d4=26
d5=19
d6=13
d7=6

count=0
str_count=0

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

GPIO.setup(ir,GPIO.IN)
GPIO.setup(soil,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

email = 'ymtstraining2020@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijumolbabu75@gmail.com'
subject = 'This is the subject'
message = 'This is Message about Tunnel'
file_location1 = '/home/pi/Desktop/PyMLX90614-0.0.3/NewPicture.jpg'
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

########################### LCD fnnnnn ################################################
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

###########################################################################################################################################################

RST = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image1 = Image.new('1', (width, height))
draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()


bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

lcd_ini()

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.clear()
    disp.display()		
    draw.text((5, top+20),"DISINFECTANT TUNNEL", font=font, fill=255)
    draw.text((8, top+30),"MONITORING", font=font, fill=255)
    disp.image(image1)
    disp.display()
    
    lcd_cmd(0x01)
    lcd_string("DISINFECTANT ")
    lcd_cmd(0xc0)
    lcd_string("TUNNEL")
    time.sleep(4)
    
        
    ir_val=GPIO.input(ir)
    soil_val=GPIO.input(soil)
    
    if ir_val==0:
        count+=1
        print(count)
        lcd_cmd(0x01)
        lcd_string("Person Detected")
##        str_count= ' {0:0} '.format(count)
        str_count= str(count)
                
        ambient= sensor.get_ambient()
        temp= sensor.get_object_1()
        str_amb= ' {0:0.2f} *C '.format(ambient)	
        str_obj  = ' {0:0.2f} *C'.format(temp)
        print("Ambient Temperature = ", str_amb)
        print("Object Temperature = ", str_obj)

        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.clear()
        disp.display()		
        draw.text((3, top),    "Disinfectant Tunnel",  font=font, fill=255)
        draw.text((0, top+16),"Ambient Temp= ", font=font, fill=255)
        draw.text((74, top+16),str_amb, font=font, fill=255)
        draw.text((x, top+30), "Object Temp= ", font=font, fill=255)
        draw.text((74, top+30), str_obj, font=font, fill=255)
        disp.image(image1)
        disp.display()

        lcd_cmd(0x01)
        lcd_string("Object temp= ")
        lcd_cmd(0x0d)
        lcd_string(str_obj)
        lcd_cmd(0xc0)
        lcd_string("amb temp= ")
        lcd_cmd(0x0d)
        lcd_string(str_amb)
        time.sleep(3)
      

        if temp>35:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            disp.clear()
            disp.display()		
            draw.text((3, top),"Disinfectant Tunnel", font=font, fill=255)
            draw.text((0, top+16),"High Temperature ", font=font, fill=255)
            draw.text((x, top+30), "Not Allowed Inside ", font=font, fill=255)
            disp.image(image1)
            disp.display()
##            time.sleep(4)
            
            lcd_cmd(0x01)
            lcd_string("High Temp")
            lcd_cmd(0xc0)
            lcd_string("Not Allowed")
            time.sleep(3)
            id="high temperature"
            engine.say(id)
            print("High Temperature")
            engine.runAndWait()
            time.sleep(2)
            print("with in cemara")
            check, frame = cam.read()
            print(check) #prints true as long as the webcam is running
            print(frame) #prints matrix values of each framecd
            #result.write(frame)
            cv2.imshow("Capturing", frame)
            for i in range(0, 25):
                print('frame #:',i)
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
            server.starttls()# sendmail function takes 3 arguments: sender's address, recipient's address and message to send 
            server.login(email, password)
            text = msg1.as_string()
            server.sendmail(email, send_to_email, text)
            print("mail sended")
            server.quit()

        else:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            disp.clear()
            disp.display()		
            draw.text((3, top),"Disinfectant Tunnel", font=font, fill=255)
            draw.text((0, top+16),"Normal Temperature ", font=font, fill=255)
            draw.text((x, top+30), "Allowed Inside ", font=font, fill=255)
            disp.image(image1)
            disp.display()
##            time.sleep(4)
            
            lcd_cmd(0x01)
            lcd_string("Normal Temp")
            lcd_cmd(0xc0)
            lcd_string("Go Inside")
            time.sleep(3)
            id1="normal temperature"
            engine.say(id1)
            print("Normal Temperature")
            engine.runAndWait()
            time.sleep(2)

    print("No:of Persons Passed through Tunnel = ", count)
    lcd_cmd(0x01)
    lcd_string("No:of Person=")
    lcd_cmd(0x0e)
    lcd_string(str_count)
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.clear()
    disp.display()		
    draw.text((3, top),"Disinfectant Tunnel", font=font, fill=255)
    draw.text((0, top+16),"No:of Persons= ", font=font, fill=255)
    draw.text((84, top+16),str_count, font=font, fill=255)
    disp.image(image1)
    disp.display()
    time.sleep(4)

    if soil_val==0:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.clear()
        disp.display()		
        draw.text((3, top),"Disinfectant Tunnel", font=font, fill=255)
        draw.text((x, top+30), "Low Sanitizer", font=font, fill=255)
        disp.image(image1)
        disp.display()
        time.sleep(4)
        lcd_cmd(0x01)
        lcd_string("Low Sainitizer")
        time.sleep(3)
        print("LOW SAnitizer")
        GPIO.output(buzzer,GPIO.HIGH)
        

    else:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        disp.clear()
        disp.display()		
        draw.text((3, top),"Disinfectant Tunnel", font=font, fill=255)
        draw.text((x, top+30), "Full Sanitizer", font=font, fill=255)
        disp.image(image1)
        disp.display()
##        time.sleep(4)
        lcd_cmd(0x01)
        lcd_string("Full Sainitizer")
        time.sleep(3)
        print("Full SAnitizer")
        GPIO.output(buzzer,GPIO.LOW)
                
        

GPIO.cleanup()
cam.release()

cv2.destroyAllWindows()

