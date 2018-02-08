import socket #for internal Python3 libraries
import sys
import numpy as np
import datetime #work with current time

from networkanalyzer import * #for import my own classes
from potentiometer import *
from qfactortools import *

if __name__ == "__main__":
    ql=[]
    qun=[]
    qext=[]
    resist=[]
    beta=[]
    
    VNA=NetworkAnalyser()
    VNA.SetParam()
    VNA.Connect()
    DP=Potentiometer()
    DP.steps=100

    for i in range (100):
        filename = "datafiles/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_R_"+str(DP.resistance)+"_Ohm"
        VNA.SavetoFile(filename,VNA.GetData())
        print("I saved file number ", i)
        Qtools=Qfactortools(filename)

        qun.append(Qtools.get_Qunload())
        ql.append(Qtools.get_Qload())
        qext.append(Qtools.get_Qext())
        resist.append(DP.resistance)
        beta.append(Qtools.get_beta())
        DP.IncreaseR()

    DP.Cleanall()
    
    #Qtools.makeplot(resist,qun)
    Qtools.merge_qvalues(qun, ql, qext, beta, resist)
