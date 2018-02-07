import socket #for internal Python3 libraries
import sys
import numpy as np
import datetime #work with current time

from NetworkAnalyzer import * #for import my own classes
from Potentiometer import *

if __name__ == "__main__":
    VNA=NetworkAnalyser()
    VNA.SetParam()
    VNA.Connect()
    #VNA.GetData()

    DP=Potentiometer()
    DP.steps=10
    for i in range (DP.steps):
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"_R_"+str(DP.resistance)+"Ohm.txt"
        VNA.SavetoFile(filename,VNA.GetData())
        print(DP.resistance)
        DP.IncreaseR()

    DP.Cleanall()
'''
    S11Raw=np.genfromtxt(filename)
    freqs=S11Raw[:,0]
    cplx = np.vectorize(complex)(S11Raw[:, 1], S11Raw[:, 2])

    # find resonant frequency
    idx_res = np.argmin(np.abs(cplx))
    f_res = freqs[idx_res]
    print(f_res)
'''
'''
    # determine the rotation angle from the offset for detuned short location
    idx_max = np.argmin(np.abs(cplx)) + 100
    idx_min = np.argmin(np.abs(cplx)) - 100
    print (idx_max, idx_min)
    
    rotation = (np.angle(cplx[idx_min]) + np.angle(cplx[idx_max])) / 2

    # find the detuned short position
    real_shifted = np.abs(cplx) * np.cos(np.angle(cplx) - rotation)
    imag_shifted = np.abs(cplx) * np.sin(np.angle(cplx) - rotation)
    cplx_shifted = np.vectorize(complex)(real_shifted, imag_shifted)
    # without multiplication with 50 ohm. so it is normalized
    impz_shifted = (1 + cplx_shifted) / (1 - cplx_shifted) * 50

    # find detuned open position
    real_dop = np.abs(cplx_shifted) * np.cos(np.angle(cplx_shifted) - np.pi)
    imag_dop = np.abs(cplx_shifted) * np.sin(np.angle(cplx_shifted) - np.pi)
    cplx_dop = np.vectorize(complex)(real_dop, imag_dop)
    impz_dop = (1 + cplx_dop) / (1 - cplx_dop) * 50
    
    # find the index of the point where Re(Z) = |Im(Z)| left of the resonance and call it f5
    f5 = freqs[np.argmin(np.abs(np.real(impz_shifted)[:idx_res] - np.abs(np.imag(impz_shifted)[:idx_res])))]

    # find the index of the point where Re(Z) = |Im(Z)| right of the resonance and call it f6
    f6 = freqs[np.argmin(np.abs(np.real(impz_shifted)[idx_res:] - np.abs(np.imag(impz_shifted)[idx_res:]))) + idx_res]

    # These are the point needed for the unloaded Q
    delta_f_u = np.abs(f5 - f6)
    Qu = f_res / delta_f_u
    print('Qu: ', Qu, '?fu: ', delta_f_u, 'MHz')
    
    # These are the point needed for the loaded Q
    f1 = freqs[np.argmax(np.imag(cplx_shifted))]
    f2 = freqs[np.argmin(np.imag(cplx_shifted))]
    delta_f_l = np.abs(f1 - f2)
    Ql = f_res / delta_f_l
    print('Ql: ', Ql, '?fl: ', delta_f_l, 'MHz')

    # Calculate the external Q from the other two Qs
    Qext = 1 / (1 / Ql - 1 / Qu)
    print('Qext: ', Qext)

    # Calculate the coupling factor
    beta = Qu / Qext
    print('beta', beta)

'''
