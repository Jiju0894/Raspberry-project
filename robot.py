from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time
from time import sleep
import serial
import smtplib

app = Flask(__name__)
##app.run(debug=False)
##app.run(debug=True, use_reloader=False)

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  #Email Server(don't change)
SMTP_PORT = 587 #Server Port (don't change)
GMAIL_US ='ymtstraining2021@gmail.com'
GMAIL_P ='Ymts@Takeoff'

ir=2
sound=3
m11=26
m12=19
m21=13
m22=6
buzzer=21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ir, GPIO.IN)
GPIO.setup(sound, GPIO.IN)
GPIO.setup(m11, GPIO.OUT)
GPIO.setup(m12, GPIO.OUT)
GPIO.setup(m21, GPIO.OUT)
GPIO.setup(m22, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

GPIO.output(m11 , GPIO.LOW)
GPIO.output(m12 , GPIO.LOW)
GPIO.output(m21, GPIO.LOW)
GPIO.output(m22, GPIO.LOW)
GPIO.output(buzzer, GPIO.LOW)
print("DOne")

############################ MAILLL #################################

class Emailer :
    def sendmail(self,recipient,subject,content):
               
        # create Headers
        headers = ["From: "+ GMAIL_US, "Subject: "+subject, "To: "+recipient,
                   "MIME-Version: 1.0","Content-Type: text/html"]
        headers = "\r\n".join(headers)

        # Connect to GmailServer

        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
        #Login to Gmail
        session.login(GMAIL_US,GMAIL_P)
        #send Email & Exit
        session.sendmail(GMAIL_US,recipient,headers+"\r\n\r\n"+ content)
        session.quit

a=1
@app.route("/")
def index():
    return render_template('robot.html')

@app.route('/left_side')
def left_side():
    print("-------LEFT---------")
    ir_val = GPIO.input(ir)
    sound_val = GPIO.input(sound)
    data1="LEFT"
    GPIO.output(m11 , GPIO.LOW)
    GPIO.output(m12 , GPIO.HIGH)
    GPIO.output(m21 , GPIO.HIGH)
    GPIO.output(m22 , GPIO.LOW)
    if ir_val==0:
        GPIO.output(m11 , GPIO.HIGH)
        GPIO.output(m12 , GPIO.LOW)
        GPIO.output(m21 , GPIO.LOW)
        GPIO.output(m22 , GPIO.HIGH)
    if sound_val==0:
        print("SOUND DETECTED")
        stop()
        mail()
    return 'true'

@app.route('/right_side')
def right_side():
    print("-------RIGHT---------")
    ir_val = GPIO.input(ir)
    sound_val = GPIO.input(sound)
    data1="RIGHT"
    GPIO.output(m11 , GPIO.HIGH)
    GPIO.output(m12 , GPIO.LOW)
    GPIO.output(m21 , GPIO.LOW)
    GPIO.output(m22 , GPIO.HIGH)
    if ir_val==0:
        GPIO.output(m11 , GPIO.LOW)
        GPIO.output(m12 , GPIO.HIGH)
        GPIO.output(m21 , GPIO.HIGH)
        GPIO.output(m22 , GPIO.LOW)
    if sound_val==0:
        
        print("SOUND DETECTED")
        stop()
        mail()
    return 'true'

@app.route('/up_side')
def up_side():
    print("-------FORWARD---------")
    ir_val = GPIO.input(ir)
    sound_val = GPIO.input(sound)
    data1="FORWARD"
    GPIO.output(m11 , GPIO.HIGH)
    GPIO.output(m12 , GPIO.LOW)
    GPIO.output(m21 , GPIO.HIGH)
    GPIO.output(m22 , GPIO.LOW)
    if ir_val==0:
        GPIO.output(m11 , GPIO.HIGH)
        GPIO.output(m12 , GPIO.LOW)
        GPIO.output(m21 , GPIO.LOW)
        GPIO.output(m22 , GPIO.HIGH)
    if sound_val==0:
        print("SOUND DETECTED")
        stop()
        mail()
    return 'true'

@app.route('/down_side')
def down_side():
    print("-------BACKWARD---------")
    ir_val = GPIO.input(ir)
    sound_val = GPIO.input(sound)
    data1="BACK"
    GPIO.output(m11 , GPIO.LOW)
    GPIO.output(m12 , GPIO.HIGH)
    GPIO.output(m21 , GPIO.LOW)
    GPIO.output(m22 , GPIO.HIGH)
    if ir_val==0:
        GPIO.output(m11 , GPIO.HIGH)
        GPIO.output(m12 , GPIO.LOW)
        GPIO.output(m21 , GPIO.LOW)
        GPIO.output(m22 , GPIO.HIGH)
    if sound_val==0:
        print("SOUND DETECTED")
        stop()
        mail()
    return 'true'

@app.route('/stop')
def stop():
    print("-------STOP---------")
    data1="STOP"
    GPIO.output(m11 , GPIO.LOW)
    GPIO.output(m12 , GPIO.LOW)
    GPIO.output(m21 , GPIO.LOW)
    GPIO.output(m22 , GPIO.LOW)
    return  'true'

def mail():
    print("Sounddddddddddddd------")
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(buzzer, GPIO.LOW)
    sender = Emailer()
    print("Sending Mail....")

    sendto = 'jijumolbabu75@gmail.com'
    emailSub = "WOMEN SFETY"
    emailCon = "Unusual Sound Detected"

        #Sends an email to the "sendto" address
    sender.sendmail(sendto,emailSub,emailCon)
    print("Mail sended")
    
    
while True:
    
    ir_val = GPIO.input(ir)
    sound_val = GPIO.input(sound)
    print("IR----",ir_val)
    print("Sound----",sound_val)

    if ir_val==0:
        print("OBSTACLE DETECTED")
        right_side()

    if sound_val==0:
        print("SOUND DETECTED")
        stop()
    

    if __name__ == "__main__":
        print("Start")
        app.run(host='192.168.0.174',port=5010)


