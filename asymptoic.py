import RPi.GPIO as GPIO
import time
import serial
import sys
import urllib3
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

myAPI = 'CI55Z0R5EXVQJMEC' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI


relay=3
HIGH=1
LOW=0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, 0)

ser = serial.Serial(
port='/dev/ttyAMA0',
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)

##def gsm():
##    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
##    port.write(b'AT\r\n')
##    rcv = port.read(10)
##    print(rcv)
##    time.sleep(1)
##
##    port.write(b"AT+CMGF=1\r")
##    print("Text Mode Enabled…")
##    time.sleep(3)
##    port.write(b'AT+CMGS="9526234625"\r')
##    msg = "ALERT:: Asymptotic Patient\n Temperature="+ str(temperature)
##    print("sending message….")
##    time.sleep(3)
##    port.reset_output_buffer()
##    time.sleep(1)
##    port.write(str.encode(msg+chr(26)))
##    time.sleep(1)
##    print("message sent…")
##
##def gsm_2():
##    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
##    port.write(b'AT\r\n')
##    rcv = port.read(10)
##    print(rcv)
##    time.sleep(1)
##
##    port.write(b"AT+CMGF=1\r")
##    print("Text Mode Enabled…")
##    time.sleep(3)
##    port.write(b'AT+CMGS="9526234625"\r')
##    msg = "ALERT:: Asymptotic Patient\n Blood Pressure="+ str(bp) 
##    print("sending message….")
##    time.sleep(3)
##    port.reset_output_buffer()
##    time.sleep(1)
##    port.write(str.encode(msg+chr(26)))
##    time.sleep(1)
##    print("message sent…")
##
##
##
##def gsm_3():
##    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
##    port.write(b'AT\r\n')
##    rcv = port.read(10)
##    print(rcv)
##    time.sleep(1)
##
##    port.write(b"AT+CMGF=1\r")
##    print("Text Mode Enabled…")
##    time.sleep(3)
##    port.write(b'AT+CMGS="9526234625"\r')
##    msg = "ALERT:: Asymptotic Patient oXYGEN out of range\n Oxygen="+ str(oxygen)
##    print("sending message….")
##    time.sleep(3)
##    port.reset_output_buffer()
##    time.sleep(1)
##    port.write(str.encode(msg+chr(26)))
##    time.sleep(1)
##    print("message sent…")
##
##
##def gsm_4():
##    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
##    port.write(b'AT\r\n')
##    rcv = port.read(10)
##    print(rcv)
##    time.sleep(1)
##
##    port.write(b"AT+CMGF=1\r")
##    print("Text Mode Enabled…")
##    time.sleep(3)
##    port.write(b'AT+CMGS="9526234625"\r')
##    msg = "ALERT:: Asymptotic Patient BPM out of range\n PULse="+ str(pulse)
##    print("sending message….")
##    time.sleep(3)
##    port.reset_output_buffer()
##    time.sleep(1)
##    port.write(str.encode(msg+chr(26)))
##    time.sleep(1)
##    print("message sent…")

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
    msg = "ALERT---Asymptotic Patient::\n Temperature="+ str(temp)+ "\n Blood Pressure="+ str(bp)+ "\n Oxygen="+ str(oxygen)+ "\n BPM="+ str(pulse)
    print(msg)
    print("sending message….")
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(1)
    print("message sent…")        
    
while True:

    time.sleep(3 )
    GPIO.output(relay, 1)
    time.sleep(2)
    data=ser.read()
    time.sleep(0.03)
    data_incoming=ser.inWaiting()
    data+=ser.read(data_incoming)
    new_data=str(data,'utf-8')
    bpm=new_data[4:14]
    oxy=new_data[15:17]
    
    print("Oxygen= ",oxy)
    oxygen=int(oxy)

    if oxygen<96:
        print("LOW Oxygen")
        GPIO.output(relay, 0)
        time.sleep(2)
        while 1:
            ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )
            while ser.in_waiting:
                received_data=ser.readline()
                time.sleep(0.03)
##                data_left=ser.inWaiting()
##                received_data+=ser.read(data_left)
                r1=str(received_data,'utf-8')
                print(r1)
                bp_h=r1[0:4]
                bp_l=r1[6:9]
                bpm=r1[11:14]
                bp=r1[0:9]
                
        ##        bp_con=int(bp)
                bp_high=int(bp_h)
                bp_low=int(bp_l)

                pulse=int(bpm)
                
                print("BP = ",bp)
                print("BPM=  ",bpm)
                
               
                
        ##        print("Oxygen= ",oxygen)
        ##        print(new_data)
        ##        print("BPM= ",bpm)
                
                time.sleep(2)
                GPIO.output(relay, 0)

                temperature = sensor.get_temperature()
                temp=(temperature *1.8)+32
                print("The temperature in Farenheit: ", temp)

                gsm()
                
##                if temperature>29:
##                    print("High Temperature")
##                    gsm()
##                   
##
##                if oxygen<92:
##                    print("ALERT::: LOW OXYGEN LEVEL") 
##                    gsm_3()
##                   
##
##                if bp_high>120 or bp_low<60:
##                    print("BP Out of range")
##                    gsm_2()
##
##                if pulse>120 or pulse<40:
##                    print("BPM Out of range")
##                    gsm_4()

                time.sleep(5)

                http = urllib3.PoolManager()
                url = baseURL +'&field1=%s' % (bp_high)+'&field2=%s' % (bp_low)+'&field3=%s' % (oxygen)+'&field4=%s' % (temp)+'&field5=%s' % (pulse)
                print(url)
                resp = http.request('GET', url)

    else:
        print("Normal Oxygen Level")

time.sleep(7)
        

    

    



    

    
    
        


