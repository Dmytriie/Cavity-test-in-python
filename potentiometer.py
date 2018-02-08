import RPi.GPIO as GPIO
import sys
import time
import smtplib

class Potentiometer:
    def __init__(self):
        self.INCPIN=5  
        self.UPDOWNPIN=3
        self.MaxR=10000
        self.resistance=10030
        self.steps=100
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.INCPIN, GPIO.OUT)
        GPIO.setup(self.UPDOWNPIN, GPIO.OUT)

        for i in range (100):
            self.IncreaseR()

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

    X3C10=Potentiometer()

#    for i in range(10):#X3C10.steps):
#        time.sleep(1)
#        X3C10.IncreaseR()   
#
    X3C10.Cleanall()
