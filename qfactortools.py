import numpy as np
import matplotlib.pyplot as plt

class Qfactortools:
    def __init__(self, filename):

        self.data=np.genfromtxt(filename)
        self.freqs=self.data[:,0]
        self.cplx = np.vectorize(complex)(self.data[:, 1],self.data[:, 2])

        # find resonant frequency
        self.idx_res = np.argmin(np.abs(self.cplx))
        self.idx_max = np.argmin(np.abs(self.cplx)) + 100
        self.idx_min = np.argmin(np.abs(self.cplx)) - 100
        
        # determine the rotation angle from the offset for detuned short location
        self.rotation = (np.angle(self.cplx[self.idx_min]) + np.angle(self.cplx[self.idx_max])) / 2

        # find the detuned short position
        self.real_shifted = np.abs(self.cplx) * np.cos(np.angle(self.cplx) - self.rotation)
        self.imag_shifted = np.abs(self.cplx) * np.sin(np.angle(self.cplx) - self.rotation)
        self.cplx_shifted = np.vectorize(complex)(self.real_shifted, self.imag_shifted)

        # without multiplication with 50 ohm. so it is normalized
        self.impz_shifted = (1 + self.cplx_shifted) / (1 - self.cplx_shifted) * 50

        # find detuned open position
        self.real_dop = np.abs(self.cplx_shifted) * np.cos(np.angle(self.cplx_shifted) - np.pi)
        self.imag_dop = np.abs(self.cplx_shifted) * np.sin(np.angle(self.cplx_shifted) - np.pi)
        self.cplx_dop = np.vectorize(complex)(self.real_dop, self.imag_dop)
        self.impz_dop = (1 + self.cplx_dop) / (1 - self.cplx_dop) * 50

    def get_fres(self):
        f_res = self.freqs[self.idx_res]
        return f_res
    
    def get_Qunload(self):

        # find the index of the point where Re(Z) = |Im(Z)| left of the resonance and call it f5
        f5 = self.freqs[np.argmin(np.abs(np.real(self.impz_shifted)[:self.idx_res] - np.abs(np.imag(self.impz_shifted)[:self.idx_res])))]

        # find the index of the point where Re(Z) = |Im(Z)| right of the resonance and call it f6
        f6 = self.freqs[np.argmin(np.abs(np.real(self.impz_shifted)[self.idx_res:] - np.abs(np.imag(self.impz_shifted)[self.idx_res:]))) + self.idx_res]

        # These are the point needed for the unloaded Q
        self.delta_f_u = np.abs(f5 - f6)
        Qu =self.get_fres() / self.delta_f_u
        return Qu

    def get_Qload(self):
        # These are the point needed for the loaded Q
        f1 = self.freqs[np.argmax(np.imag(self.cplx_shifted))]
        f2 = self.freqs[np.argmin(np.imag(self.cplx_shifted))]
        self.delta_f_l = np.abs(f1 - f2)
        Ql =  self.get_fres() / self.delta_f_l
        return Ql

    def get_Qext(self):
        # Calculate the external Q from the other two Qs
        Qext = 1 / (1 / self.get_Qload() - 1 / self.get_Qunload())
        return Qext

    def get_beta(self):
        # Calculate the coupling factor
        beta =  self.get_Qunload() / self.get_Qext()
        return beta

    def merge_qvalues(self, *args):
        qvalues=[]

        for i in range (len(args)):
            qvalues.append(args[i])
        
        qvalues[0] = np.reshape(qvalues[0], (len( qvalues[0]), 1))

#        for i in range (3):
#            qvalues[i+1] = np.reshape( qvalues[i+1], (len( qvalues[i+1]), 1))
#            mergedQ = np.append( qvalues[i],  qvalues[i+1], axis=1)

        qvalues[1]=np.reshape(qvalues[1],(len(qvalues[1]),1))
        mergedQ = np.append( qvalues[0],  qvalues[1], axis=1)
       
        qvalues[2] = np.reshape(qvalues[2], (len(qvalues[2]), 1))
        mergedQ = np.append(mergedQ, qvalues[2], axis=1)

        qvalues[3] = np.reshape(qvalues[3], (len(qvalues[3]), 1))
        mergedQ = np.append(mergedQ, qvalues[3], axis=1)

        qvalues[4] = np.reshape(qvalues[4], (len(qvalues[4]), 1))
        mergedQ = np.append(mergedQ, qvalues[4], axis=1)

        qvalues[5] = np.reshape(qvalues[5], (len(qvalues[5]), 1))
        mergedQ = np.append(mergedQ, qvalues[5], axis=1)

#        print (len(resist), len(Qu), len(Qu), len(Qu), len(Qu), len(Qu))
        
        np.savetxt("datafiles/Qmerged.txt",mergedQ)
        
    def makeplot(self, xvalues, yvalues):
        #build plots. Take arrays as arguments and later use numpy arrays
        #print("Plot,lol")
        xvalues = np.array(xvalues)
        yvalues = np.array(yvalues)
       # xvalues1 = np.array(xvalues1)
       # yvalues1 = np.array(yvalues1)

        plt.subplot(2, 1, 1)
        plt.plot(xvalues, yvalues, 'o-')
        plt.title('A tale of 2 subplots')
        plt.xlabel('time (s)')
        plt.ylabel('Damped oscillation')
#Uncomment this if you want to build two plots on the same layout. 
#Also uncomment and add to method additional arguments
#        plt.subplot(2, 1, 2)
#        plt.plot(xvalues1, yvalues1, '.-')
#        plt.ylabel('Undamped')
#
        plt.show()
        
        
if __name__=="__main__":
    
    Qtools=Qfactortools("datafiles/2018-02-08_18-00-10_R_6030.0Ohm")
    print(Qtools.get_fres())
    
    Qu=Qtools.get_Qunload()
    print ("Qu: ", Qu, "Delta F_u: ", Qtools.delta_f_u)
     
    Ql=Qtools.get_Qload()
    print ("Ql: ", Ql, "Delta F_l: ", Qtools.delta_f_l)
    
    print("Qext: ",Qtools.get_Qext())
    print("Beta: ",Qtools.get_beta())

    Qtools.makeplot(Qu,Ql)
    
