import RPi.GPIO as GPIO
import sys
import time
import smtplib

class Potentiometer:
    def __init__(self,resistance):
        self.inc_pin=5
        self.up_down_pin=3
        self.steps=100
        self.resistance=resistance
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.inc_pin, GPIO.OUT)
        GPIO.setup(self.up_down_pin, GPIO.OUT)

        for i in range (self.steps):
            self.decrease_r()

        self.resistance=30

    def decrease_r(self):
        GPIO.output(self.up_down_pin, GPIO.LOW)
        GPIO.output(self.inc_pin, GPIO.LOW)
        GPIO.output(self.inc_pin, GPIO.HIGH)
        self.resistance-=91

    def increase_r(self):
        GPIO.output(self.up_down_pin, GPIO.HIGH)
        GPIO.output(self.inc_pin, GPIO.LOW)
        GPIO.output(self.inc_pin, GPIO.HIGH)
        self.resistance+=91

    def clean_all(self):
        GPIO.cleanup()

if __name__=="__main__":

    DP=Poteclean_allntiometer(10000)

    while(1):


        a=input("u/d: ")
        if a=='u':
            DP.increase_r()
        if a=='d':
            DP.decrease_r()
        if a=='e':
            DP.clean_all()
            break
