import RPi.GPIO as GPIO
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
from time import sleep
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

#sys.path.append('/home/pi/MFRC522-python')
sys.path.append('/home/pi/pi-rfid/Write.py')
from mfrc522 import SimpleMFRC522


GPIO.setmode(GPIO.BOARD)  
GPIO.setwarnings(False)
reader = SimpleMFRC522()

print("Hold a tag near the reader")

email = 'ymtstraining2020@gmail.com'
password = 'Ymts@Takeoff'
send_to_email = 'jijugracebabu10@gmail.com'
subject = 'This is the subject'
message = 'This is my message from home'
file_location1 = '/home/pi/Desktop/New/Jiju/filename.avi'
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

file_location2 = '/home/pi/Desktop/New/Jiju/NewPicture.jpg'
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

def GPS_Info():
        global gps
        global map_link
        port="/dev/ttyUSB0"
        

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

        #return gps

##def GPS_Info():
##    print("hello")
##    global NMEA_buff
##    global lat_in_degrees
##    global long_in_degrees
##    nmea_time = []
##    nmea_latitude = []
##    nmea_longitude = []
##    nmea_time = NMEA_buff[0]               #extract time from GPGGA string
##    nmea_latitude = NMEA_buff[1]               #extract latitude from GPGGA string
##    nmea_longitude = NMEA_buff[3]            #extract longitude from GPGGA string
##    
##    print("NMEA Time: ", nmea_time,'\n')
##    print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
##    
##    lat = float(nmea_latitude)                  #convert string into float for calculation
##    longi = float(nmea_longitude)               #convertr string into float for calculation
##    
##    lat_in_degrees = convert_to_degrees(nmea_latitude)    #get latitude in degree decimal format
##    long_in_degrees = convert_to_degrees(nmea_longitude) #get longitude in degree decimal format
##



#convert raw NMEA string into degree decimal format   
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

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

def delay(a):
        for i in range (0,a):
            for j in range (0,5000):
                b=0
                b=b+1
                
def serial_receive() :
        while True :
                received_data = port.read(10)              #read serial port
                print (received_data)
                if(received_data) :
                        received_data=0
                        break
def serial_Print(text):
        _text=str(text)
        _length=len(_text)
        for i in range (0,_length):
            _a=_text[i].encode()
            port.write(_a)

def gsm():
        global gps
        #port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
        print("SENDING SMS")
        delay(10)
        serial_Print('AT\r\n')
        delay(100)
        #serial_receive()
        serial_Print('AT+CMGF=1\r\n')
        delay(100)
        #serial_receive()
        serial_Print('AT+CMGS=\"09526234625\"\r')
        delay(500)
        serial_Print(" Child is Outside "+map_link)
        delay(500)
        ##port.write(26.encode())
        serial_Print("\x1A")
        #serial_receive()
        #serial_receive()
        print("SMS SEND")
        delay(1000)

##def gsm():
##    global gps
##    port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
##    port.write(b'AT\r\n')
##    rcv = port.read(10)
##    print(rcv)
##    time.sleep(1)
##
##    port.write(b"AT+CMGF=1\r")
##    print("Text Mode Enabled…")
##    time.sleep(3)
##    port.write(b'AT+CMGS="9526234625"\r')
##    #port.write(gps + " Child is Outside")
##    #msg = gps + " Child is Outside"
##    print("sending message….")
##    time.sleep(3)
##    port.reset_output_buffer()
##    time.sleep(1)
##    port.write(str.encode(msg+chr(26)))
##    time.sleep(1)
##    print("message sent…")

##received_data = (str)(ser.readline())#read NMEA string received
##        #print("hello")
##GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
##
##if (GPGGA_data_available>0):
##    GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
##    NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
##    GPS_Info()                                          #get time, latitude, longitude
##
##    print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
##    map_link = 'http://maps.google.com/?q=' + lat_in_degrees + ',' + long_in_degrees    #create link to plot location on Google map
##    print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
##    print("------------------------------------------------------------\n")
##    time.sleep(5)

    

while True:
        id, text = reader.read()
        #  print(id)
        print(text)
        #GPS_Info()

        if "Park" in text:
            print("Tracking gps")
            map_link=""
            GPS_Info()
            gsm()

###----- webcam recording  for 25 sec and sending##         
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
            server.quit()


            
GPIO.cleanup()
cam.release()

cv2.destroyAllWindows()
