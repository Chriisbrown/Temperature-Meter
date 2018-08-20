# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:34:09 2018

@author: chris
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 12:12:21 2018

@author: chris
"""

import paho.mqtt.publish as publish

MQTT_SERVER = "10.0.100.181"
MQTT_PATH = "time"
MQTT_PATH2 = "Temperature 1" 
MQTT_PATH3 = "Temperature 2"
MQTT_PATH4 = "Temperature 3"

import time
from time import sleep
import numpy as np
import datetime
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
#imports, all essential, all already installed on the Pi. If using a new pi to install
#a module type "sudo apt-get install python3-modulename" you will need an internet connection

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
#Sets the LED pins, if the wiring for the LEDs is changed these pins will be incorrect

def inputno(g, a, lim1, lim2):
#This defines the function used to check user inputs are within range and of correct data type
    if g == 1:
        while True:
            try:
                h = int(input(a))
                if lim1 <= h <= lim2:
                    return h
                else:
                    GPIO.output(17,GPIO.HIGH)
                    time.sleep(0.033)
                    GPIO.output(17,GPIO.LOW)
            except ValueError:
                GPIO.output(17,GPIO.HIGH)
                time.sleep(0.033)
                GPIO.output(17,GPIO.LOW)
                continue
#If a wrong value is entered the Red LED will flash
                
def temperatures():
#Temperature probe management, this will not break and manages any exceptions, if the incorrect
    data =[]
    d = time.time()
    GPIO.output(18,GPIO.HIGH)
    for sensor in W1ThermSensor.get_available_sensors():
        data.append(sensor.get_temperature())
    y = (time.time()-d)
    data.append(time.time()-start_time)
    GPIO.output(18,GPIO.LOW)
#For each available sensor the data from the sensor will be printed into the data list, this
#will cycle for as many sensors. The final insertion of the time ensures that the correct
#time corresponding to the final probe entering its data into the list is recorded
    return(data,y)
	
Menu = '0'
while Menu != 'q':
    Menu = input('Press 1 to begin log, press q to quit: ')
    GPIO.output(18,GPIO.HIGH)
#Menu setup allowing the program to be run multiple times without turning the pi off
    now = datetime.datetime.now()
    if Menu == '1':
        frequency = inputno(1,'Frequency of data reading: ',1,100)
        length = int((inputno(1,'Run test for how many minutes: ',1,1500))*60/frequency)
#All relevant parameters, with incorrect user input checking
        i = 0
        start_time = time.time()
        array = np.zeros(len(W1ThermSensor.get_available_sensors()+1))
#sets up final array for data printing 
        try:
            while i <= length:
                GPIO.output(18,GPIO.LOW)
                GPIO.output(17,GPIO.HIGH)
#When recording the red light shows
                t = time.time() - start_time
                z = temperatures()
                array = np.vstack([array,z[0]])
                print(t,z[0][0],z[0][1],z[0][2])
                try:
                    msgs = [{'topic':MQTT_PATH2, 'payload':z[0][0]},(MQTT_PATH3,z[0][1],0,False),(MQTT_PATH4,z[0][2],0,False),(MQTT_PATH,t,0,False)]
                    publish.multiple(msgs,hostname=MQTT_SERVER)
                except:
                    with open('backuptemps.txt' ,'a+') as f:
                         print(t,z[0][0],z[0][1],z[0][2], file=f)
                time.sleep(frequency-z[1])
                i += 1
#Uses the temperature function to read the temperatures and insert them into the array, at 
#the frequency specified by the user
        except KeyboardInterrupt:
            pass            
#Allows the user to manually terminate the logging but preserve the data
        np.savetxt('Temperature Log-'+now.strftime("%Y-%m-%d %H-%M")+'.txt', array,fmt='%+3.3f')
        GPIO.output(17,GPIO.LOW)
#Final data printing into a file named with the time and date, final light switching to show the
#program has finished.	

        
            
            
            
            

 
