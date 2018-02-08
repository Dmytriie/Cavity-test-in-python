import socket #for internal Python3 libraries
import sys
import numpy as np
import datetime #work with current time

from networkanalyzer import * #for import my own classes
from potentiometer import *
from qfactortools import *

if __name__ == "__main__":
    qloadvalues=[]
    qunloadvalues=[]
    qextvalues=[]
    resistances=[]

    VNA=NetworkAnalyser()
    VNA.SetParam()
    VNA.Connect()
    #    print(VNA.GetData())
    
    DP=Potentiometer()
    DP.steps=100
    for i in range (DP.steps):
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_R_"+str(DP.resistance)+"Ohm"
        VNA.SavetoFile(filename,VNA.GetData())
        Qtools=Qfactortools(filename)

        qunloadvalues.append(Qtools.get_Qunload())
        qloadvalues.append(Qtools.get_Qload())
        qextvalues.append(Qtools.get_Qext())
        resistances.append(DP.resistance)
        DP.IncreaseR()

    DP.Cleanall()
#    
    Qtools.makeplot(resistances,qunloadvalues)
