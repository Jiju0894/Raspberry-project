import sys
import Adafruit_DHT
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import os
import Adafruit_DHT
import smbus
import time
import serial
from mcp3208 import MCP3208
from tkinter import *
from tkinter import messagebox

#Register Address
regCall   = 0xAA
regMean   = 0xF4
regMSB    = 0xF6
regLSB    = 0xF7
regPres   = 0x34
regTemp   = 0x2e

DEBUG = 1
sample = 2
deviceAdd =0x77

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

##bus = smbus.SMBus(0)  #for Pi1 uses 0
I2cbus = smbus.SMBus(1) # for Pi2 uses 1

sensor_name = Adafruit_DHT.DHT11 #we are using the DHT11 sensor
sensor_pin = 17 #The sensor is connected to GPIO17 on Pi

class Table:
      
    def __init__(self,root):
          
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                  
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                  
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])

def close_window():
    root.destroy()

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

def convert1(data, i):   # signed 16-bit value
  return ((data[i]<< 8) + data[i + 1])#.value
 
def convert2(data, i):   # unsigned 16-bit value
  return (data[i]<< 8) + data[i+1] 
   
def readBmp180(addr=deviceAdd):
  value = I2cbus.read_i2c_block_data(addr, regCall, 22)  # Read calibration data

  # Convert byte data to word values
  AC1 = convert1(value, 0)
  AC2 = convert1(value, 2)
  AC3 = convert1(value, 4)
  AC4 = convert2(value, 6)
  AC5 = convert2(value, 8)
  AC6 = convert2(value, 10)
  B1  = convert1(value, 12)
  B2  = convert1(value, 14)
  MB  = convert1(value, 16)
  MC  = convert1(value, 18)
  MD  = convert1(value, 20)

    # Read temperature
  I2cbus.write_byte_data(addr, regMean, regTemp)
  time.sleep(0.005)
  (msb, lsb) = I2cbus.read_i2c_block_data(addr, regMSB, 2)
  P2 = (msb << 8) + lsb
 
  # Read pressure
  I2cbus.write_byte_data(addr, regMean, regPres + (sample << 6))
  time.sleep(0.05)
  (msb, lsb, xsb) = I2cbus.read_i2c_block_data(addr, regMSB, 3)
  P1 = ((msb << 16) + (lsb << 8) + xsb) >> (8 - sample)

   # Refine temperature
  X1 = ((P2 - AC6) * AC5) >> 15
  X2 = (MC << 11) / (X1 + MD)
  B5 = X1 + X2
  temperature = int(B5 + 8) >> 4
 
  # Refine pressure
  B6  = B5 - 4000
  B62 = int(B6 * B6 )>> 12
  X1  = int(B2 * B62) >> 11
  X2  = int(AC2 * B6) >> 11
  X3  = X1 + X2
  B3  = (((AC1 * 4 + X3) << sample) + 2) >> 2
 
  X1 = int(AC3 * B6) >> 13
  X2 = int(B1 * B62) >> 16
  X3 = int((X1 + X2) + 2) >> 2
  B4 = int(AC4 * (X3 + 32768)) >> 15
  B7 = (P1 - B3) * (50000 >> sample)
 
  P = (B7 * 2) / B4
 
  X1 = (int (P) >> 8) * (int (P) >> 8)
  X1 = (int(X1 * 3038)) >> 16
  X2 = (7357 * int (P)) >> 16
  pressure = -(P + ((X1 + X2 + 3791) >> 4))
  
  return (str(pressure/1000.0))

while True:
    
    humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin)
    pressure =readBmp180()
    x= readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
    y= readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
    z= readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
    print("Temperature = ", temperature)
    print("Humidity = ", humidity)
    print(" Pressure= ", pressure)
    print("Gas value:" ,x)
    print("Air Quality:",y)
    print("Methane :" ,z)

    lst = [(1,'Temperature',temperature),
       (2,'Humidity',humidity),
       (3,'Pressure',pressure),
       (4,'Gas value',x),
       (5,'Air Quality',y),
       (6,'Methane ',z)]
    total_rows = len(lst)
    total_columns = len(lst[0])

    root = Tk()
    root.title("Air Quality Monitoring")
    t = Table(root)
    lst = [(1,'Temperature',temperature),
       (2,'Humidity',humidity),
       (3,'Pressure',pressure),
       (4,'Gas value',x),
       (5,'Air Quality',y),
       (6,'Methane ',z)]
    total_rows = len(lst)
    total_columns = len(lst[0])
    #root.mainloop()
    root.update()
    time.sleep(3)
    root.destroy()
    
    
    
    
    

