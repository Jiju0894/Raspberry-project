import RPi.GPIO as GPIO
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
import serial
import os, time
import string
import pynmea2


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

m1= 38 
alco_senor=5
i=0
buzz=40
vibr_sensor=7



GPIO.setup(buzz,GPIO.OUT)
GPIO.setup(vibr_sensor,GPIO.IN)
GPIO.setup(alco_senor,GPIO.IN)
GPIO.setup(m1,GPIO.OUT)

GPIO.output(buzz,GPIO.LOW)
GPIO.output(m1,GPIO.LOW)

def GPS_Info():
    global gps
    global map_link
    port="/dev/ttyAMA0"
    

    ser=serial.Serial(port,baudrate=9600,timeout=0.5)

    dataout =pynmea2.NMEAStreamReader()

    newdata=ser.readline()
    #print(newdata)

    if newdata[0:6]==b'$GPRMC':
        
        newmsg=pynmea2.parse(newdata.decode('ASCII'))

        lat=newmsg.latitude

        lng=newmsg.longitude

##        lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
##        long_in_degrees = convert_to_degrees(lng)
##
        gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
        map_link='http://maps.google.com/?q=' + str(lat)+ ',' + str(lng)
        print(map_link)
        print(gps)
        

def gsm():
        global gps
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        port.write(b'AT\r\n')
        rcv = port.read(10)
        print(rcv)
        time.sleep(1)

        port.write(b"AT+CMGF=1\r")
        print("Text Mode Enabled…")
        time.sleep(3)
        port.write(b'AT+CMGS="9526234625"\r')
        msg = "Accident Occured "+ str(map_link)
        print("sending message….")
        time.sleep(3)
        port.reset_output_buffer()
        time.sleep(1)
        port.write(str.encode(msg+chr(26)))
        time.sleep(1)
        print(msg)
        print("message sent…")

        

def euclidean_dist(ptA, ptB):
                                            # compute and return the euclidean distance between the two
                                            # points
        return np.linalg.norm(ptA - ptB)
def eye_aspect_ratio(eye):
        A = euclidean_dist(eye[1], eye[5])
        B = euclidean_dist(eye[2], eye[4])

        C = euclidean_dist(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)

        return ear

def final_ear(shape):
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        return (ear, leftEye, rightEye)

def lip_distance(shape):
        top_lip = shape[50:53]
        top_lip = np.concatenate((top_lip, shape[61:64]))

        low_lip = shape[56:59]
        low_lip = np.concatenate((low_lip, shape[65:68]))

        top_mean = np.mean(top_lip, axis=0)
        low_mean = np.mean(low_lip, axis=0)

        distance = abs(top_mean[1] - low_mean[1])
        return distance


EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 15
YAWN_THRESH = 30
COUNTER = 0

print("-> Loading the predictor and detector...")
    #detector = dlib.get_frontal_face_detector()
detector = cv2.CascadeClassifier("/home/pi/Desktop/Driver Drowsiness/haarcascade_frontalface_default.xml")    #Faster but less accurate
predictor = dlib.shape_predictor('/home/pi/Desktop/Driver Drowsiness/shape_predictor_68_face_landmarks.dat')
                                                                
print("-> Starting Video Stream")
vs = VideoStream(src=0).start()
    #vs= VideoStream(usePiCamera=True).start()       //For Raspberry Pi
time.sleep(1.0)

while True:
        GPIO.output(m1,GPIO.HIGH)

        frame = vs.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #rects = detector(gray, 0)
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                    minNeighbors=5, minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE)

        #for rect in rects:
        for (x, y, w, h) in rects:
            rect = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))
            
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            eye = final_ear(shape)
            ear = eye[0]
            leftEye = eye [1]
            rightEye = eye[2]

            distance = lip_distance(shape)

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            lip = shape[48:60]
            cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)
            cv2.putText(frame, "EYE: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if ear < EYE_AR_THRESH:
                COUNTER += 1

                if COUNTER >= EYE_AR_CONSEC_FRAMES or distance > YAWN_THRESH :
                   
                    
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "Yawn Alert", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                               
                    GPIO.output(buzz,GPIO.HIGH)
                            

            else:
                COUNTER = 0
                GPIO.output(buzz,GPIO.LOW)
                

        
        if GPIO.input(alco_senor)==0:
            GPIO.output(m1,GPIO.LOW)
            GPIO.output(buzz,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(buzz,GPIO.LOW)
            print("Alcohol Detected")
            time.sleep(0.5)

        if GPIO.input(alco_senor)==1:
            print(" NO Alcohol Detected")
            time.sleep(0.5)

        if GPIO.input(vibr_sensor)==0:
                print("Accident....")
                map_link=""
                GPS_Info()
                time.sleep(2)
                gsm()
                time.sleep(1)
##                print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, " speed in km/hr: ", spd_in_kmphr, '\n')
####                print("<<<<<<<<press ctrl+c to plot location on google maps>>>>>>\n")               #press ctrl+c to plot on map and exit 
####                print("------------------------------------------------------------\n")
##        
##                print("sent")
                
               


        if GPIO.input(vibr_sensor)==1:
                print("Safe Driving")


            
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

cv2.destroyAllWindows()
vs.stop()
