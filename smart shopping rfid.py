import serial
import RPi.GPIO as GPIO
from time import sleep
import sys
import time
import dlib
from urllib.request import urlopen
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import urllib3
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)



BASE_URL = "http://shopping12979.wizzie.tech/"

sw1=3  #### TOTAL
sw2=5  ### DELETE 
sw3=7  ### ADD

echo=16
trig=18
buzzer=12

rs=40
en=38
d4=37
d5=35
d6=33
d7=31

GPIO.setup(sw1, GPIO .IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(sw2, GPIO .IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(sw3, GPIO .IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

GPIO.output(buzzer, GPIO.LOW)

flag=0
temp=3
total=0

rice=100
dal=80
oil=200
sugar=40
salt=20

r=str(rice)
d=str(dal)
o=str(oil)
s=str(sugar)
sa=str(salt)
##t=str(total)

ser = serial.Serial ("/dev/ttyS0", baudrate=9600)


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

    lcd_cmd(0x01)
    lcd_string(" SMART SHOPPING ")
##    lcd_cmd(0x85)
##    lcd_string(tem)
##    lcd_cmd(0xc0)
##    lcd_string("   WORLD  ")
##    lcd_cmd(0xc4)
##    lcd_string(hum)
    time.sleep(3)

    pulse_end=0
    count=0
    GPIO.output(trig,False)
    time.sleep(0.2)
    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)
    while GPIO.input(echo)==0:
        pulse_start=time.time()
        count=count+1
        if count>1000:
            count=0
            break
    count=0
    while GPIO.input(echo)==1:
        pulse_end=time.time()
        count=count+1
        if count>1000:
            count=0
            break

    pulse_duration=pulse_end - pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("Distance:: ",distance)
    time.sleep(3)

    if distance<10:
        print("Maintain social distance");
        GPIO.output(buzzer, GPIO.HIGH)
        lcd_cmd(0x01)
        lcd_string("MAINTAIN DISTANCE")
        time.sleep(2)

    else:
        
        GPIO.output(buzzer, GPIO.LOW)
        lcd_cmd(0x01)
        lcd_string("START SHOPPING")
        time.sleep(2)

        while(1):

            val1=GPIO.input(sw1)
            val2=GPIO.input(sw2)
            val3=GPIO.input(sw3)
                      

            if val1==0:
                print("End of Shopping")
                temp=0
                flag=0
                val=1
        ##        if flag==0 and temp==0:
                hom = 'http://shopping12979.wizzie.tech/billing.php?'+'active='+str(val) ##+'lat='+str(lat_in_degrees)+'&&lng='+ str(long_in_degrees) +'&&spd='+str(spd_in_kmphr)#+'&&id=user1'
                http = urllib3.PoolManager()
                resp = http.request('GET', hom)
                print(resp.status)
                print(hom)    
                print("sent")
                print("Total bill:: ",total)            
                lcd_cmd(0x01)
                lcd_string("END OF SHOPPING")
                lcd_cmd(0xc0)
                lcd_string("TOTAL:: ")
                lcd_cmd(0xc9)
                lcd_string(t)
                time.sleep(1)
                msg = "Total ="+str(total)
                send_data = ser.write(str.encode(msg))
                print (send_data)
                
             
            if val2==0:
                print("REMOVING.... ")
                lcd_cmd(0x01)
                lcd_string("REMOVING...")
                temp=1
                flag=0
                val=0
                if temp==1:
                    received_data = ser.read()              #read serial port
                    sleep(0.03)
                    data_left = ser.inWaiting()             #check for remaining byte
                    received_data += ser.read(data_left)
                    print (received_data)
            ##        time.sleep(3)
                    if(received_data== b'3500643C2B46'):
                        print("Removing Rice Price")
                        total=total-rice
                        t=str(total)
                        product=prod006
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("RICE:: ")
                        lcd_cmd(0xc8)
                        lcd_string(r)
                        time.sleep(2)        
                    if(received_data== b'3500643A402B'):
                        print("Removing Dal Price")
                        total=total-dal
                        t=str(total)
                        product=prod007
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("DAL:: ")
                        lcd_cmd(0xc7)
                        lcd_string(d)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCF1A47'):
                        print("Removing Oil Price")
                        total=total-oil
                        t=str(total)
                        product=prod008
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("OIL:: ")
                        lcd_cmd(0xc7)
                        lcd_string(o)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCDC39C'):
                        print("Removing Sugar Price")
                        total=total-sugar
                        t=str(total)
                        product=prod009
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("SUGAR:: ")
                        lcd_cmd(0xc9)
                        lcd_string(s)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCC4917'):
                        print("Removing Salt Price")
                        total=total-salt
                        t=str(total)
                        product=prod010
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("SALT:: ")
                        lcd_cmd(0xc8)
                        lcd_string(sa)
                        time.sleep(2)

                    hom = 'http://shopping12979.wizzie.tech/billing.php?'+'p_id='+str(product)+'&active='+str(val) ##+'lat='+str(lat_in_degrees)+'&&lng='+ str(long_in_degrees) +'&&spd='+str(spd_in_kmphr)#+'&&id=user1'
                    http = urllib3.PoolManager()
                    resp = http.request('GET', hom)
                    print(resp.status)
                    print(hom) 
                    
            if val3==0:
                print("ADDING.... ")
                lcd_cmd(0x01)
                lcd_string("ADDING...")
                temp=0
                flag=1
                val=0
                if temp==0:
                    received_data = ser.read()              #read serial port
                    sleep(0.03)
                    data_left = ser.inWaiting()             #check for remaining byte
                    received_data += ser.read(data_left)
                    print (received_data)
            ##        time.sleep(3)
                    if(received_data== b'3500643C2B46'):
                        print("Adding Rice Price")
                        total=total+rice
                        t=str(total)
                        product=106
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("RICE:: ")
                        lcd_cmd(0xc8)
                        lcd_string(r)
                        time.sleep(2) 
                    if(received_data== b'3500643A402B'):
                        print("Adding Dal Price")
                        total=total+dal
                        t=str(total)
                        product=107
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("DAL:: ")
                        lcd_cmd(0xc8)
                        lcd_string(d)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCF1A47'):
                        print("Adding Oil Price")
                        total=total+oil
                        t=str(total)
                        product=108
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("OIL:: ")
                        lcd_cmd(0xc8)
                        lcd_string(o)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCDC39C'):
                        print("Adding Sugar Price")
                        total=total+sugar
                        t=str(total)
                        product=109
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("SUGAR:: ")
                        lcd_cmd(0xc8)
                        lcd_string(s)
                        time.sleep(2) 
                    if(received_data== b'2E00BCCC4917'):
                        print("Adding Salt Price")
                        total=total+salt
                        t=str(total)
                        product=110
                        print("Total Bill:: ",total)
                        lcd_cmd(0xc0)
                        lcd_string("SALT:: ")
                        lcd_cmd(0xc8)
                        lcd_string(sa)
                        time.sleep(2)

                    hom = 'http://shopping12979.wizzie.tech/billing.php?'+'p_id='+str(product)+'&active='+str(val) ##+'lat='+str(lat_in_degrees)+'&&lng='+ str(long_in_degrees) +'&&spd='+str(spd_in_kmphr)#+'&&id=user1'
                    http = urllib3.PoolManager()
                    resp = http.request('GET', hom)
                    print(resp.status)
                    print(hom) 


                
    time.sleep(4)
            

           
        
        
   
