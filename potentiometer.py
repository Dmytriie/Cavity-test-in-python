import RPi.GPIO as GPIO
import sys
import time
import smtplib

class Potentiometer:
    def __init__(self,resistance):
        self.INCPIN=5  
        self.UPDOWNPIN=3
        self.steps=100
        self.resistance=resistance
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.INCPIN, GPIO.OUT)
        GPIO.setup(self.UPDOWNPIN, GPIO.OUT)

        for i in range (self.steps):
            self.DecreaseR()

        self.resistance=30
        
    def DecreaseR(self):
        GPIO.output(self.UPDOWNPIN, GPIO.LOW)
        GPIO.output(self.INCPIN, GPIO.LOW)
        GPIO.output(self.INCPIN, GPIO.HIGH)
        self.resistance-=91

    def IncreaseR(self):
        GPIO.output(self.UPDOWNPIN, GPIO.HIGH)
        GPIO.output(self.INCPIN, GPIO.LOW)
        GPIO.output(self.INCPIN, GPIO.HIGH)
        self.resistance+=91

    def Cleanall(self):
        GPIO.cleanup()

if __name__=="__main__":

    DP=Potentiometer(10000)
        
    while(1):

        
        a=input("u/d: ")
        if a=='u':
            DP.IncreaseR()
        if a=='d':
            DP.DecreaseR()
        if a=='e':
            DP.Cleanall()
            break
