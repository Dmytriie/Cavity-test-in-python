'''
This module will work with Vector Network Analyzer ZVL Rohde and Schwarz
Connect, set parameters of measurement, get raw data in format 
(float) Re(S11) (float) Im(S11) and save data to .txt

06.02.2018 D.Dmytriiev
'''
import socket#to use TCP
import sys
import os
import numpy as np

class NetworkAnalyser:

    def __init__(self):#Initialize object. Socket, adress, everything for start work
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address='192.168.254.2'# VNA adress
        self.portnumber=5025
        self.BUFF_SIZE=1#I want take one symbol per time. TCP destroy every formatting and send bytes
        
    def SetParam(self): #Setting parameters of Network Analyzer instead of pressing buttons
        self.center = 407.0 # MHz
        self.span = 2000.0 # kHz
        self.NumberOfPoints = 4001
        self.bandwidth = 1.0 # kHz
        self.power = 0.0 #  dBm
        self.average = 10 #samples for averaging
        self.measurement = "S11" #S-parameter we measure

    def Connect(self): #connect to NA and tell it about settings and procedures
        self.sock.connect((self.address, self.portnumber)) #connect to VNA
        self.sock.send("@REM".encode('ascii')) # invoke remote mode
        self.sock.send("*RST;*WAI;*CLS".encode('ascii')) # reset everything
        self.sock.send(("CALC:PAR:MEAS 'TRC1','"+self.measurement+"'").encode('ascii'))
        self.sock.send("INIT:CONT OFF".encode('ascii')) # single sweep
        self.sock.send(("SWE:COUN " + str(self.average)).encode('ascii'))
        self.sock.send(("SWE:POIN " + str(self.NumberOfPoints)).encode('ascii'))
        self.sock.send(("AVER:COUN " + str(self.average)).encode('ascii'))
        self.sock.send("AVER ON".encode('ascii'))
        self.sock.send(("BAND " + str(self.bandwidth) + "KHZ").encode('ascii'))
        self.sock.send(("FREQ:CENT " + str(self.center) + "MHZ").encode('ascii'))
        self.sock.send(("FREQ:SPAN " + str(self.span) + "KHZ").encode('ascii'))
        self.sock.send(("SOUR:POW " + str(self.power)).encode('ascii'))
        #self.sock.send("MMEM:LOAD:CORR 1,'MOST_20150729_679.6_350.cal'") # calibration file, to be replaced in every test
        
    def GetData(self):#get string from TCP, char array to string, split string and convert to floats. Returns float array of data with frequencies
        data = [] #empty array to put symbols in it
        
        self.sock.send("*WAI;SYST:ERR:ALL?".encode('ascii'))
        self.sock.send("AVER:CLE\n".encode('ascii')) #clean previous frames
        self.sock.send("INIT\n".encode('ascii')) #initiate new cycle
        self.sock.send("*WAI;CALC:DATA? SDAT\n".encode('ascii')) #send data
        
        tmp = self.sock.recv(self.BUFF_SIZE).decode('ascii')#first symbol in TCP port in non-byte format. Normal number
        data.append(tmp)#add first symbol
    
        while tmp != '\n':#until the end of the data in TCP
            tmp = self.sock.recv(self.BUFF_SIZE).decode('ascii')

            if tmp == '\n': #stop-symbol is \n
                break        

            data.append(tmp) #add symbol to array
    
        data = (''.join(map(str, data))) #create string from char array
        data_array = np.fromstring(data, sep=',')
        data_array = np.reshape(data_array, (int(len(data_array)/2),2))
        freqs= np.linspace(start = self.center - self.span / 2000, stop = self.center + self.span / 2000, num = self.NumberOfPoints)
        freqs = np.reshape(freqs, (self.NumberOfPoints, 1))
        data_array = np.append(freqs, data_array, axis=1)
        return data_array
    
    def SavetoFile(self, filename, data_array): 

        np.savetxt(filename, data_array)
        
