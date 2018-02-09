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
    fres=[]

    VNA=Network_analyser()
    VNA.set_param()
    VNA.connect()
    DP=Potentiometer(10000)
    DP.steps=100

    for i in range (DP.steps):
        filename = "datafiles/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_R_"+str(DP.resistance)+"_Ohm"
        VNA.save_to_file(filename,VNA.GetData())
        print("I saved file number ", i)

        Qtools=Qfactortools(filename)

        fres.append(Qtools.get_fres())
        qun.append(Qtools.get_Qunload())
        ql.append(Qtools.get_Qload())
        qext.append(Qtools.get_Qext())
        resist.append(DP.resistance)
        beta.append(Qtools.get_beta())

        DP.increase_r()

    DP.clean_all()

    Qtools.merge_qvalues(resist, fres, qun, ql, qext, beta)
