"""
Propogation model used to calculate the Recevied power at the CH from each node considering
shadowing and rayleigh fading

Friis free space equation:
         
                Pt * Gt * Gr * (lambda^2)
            Prx = --------------------------
                (4 * pi * d)^2 

shadowing path loss
            PL = PL(d0) + 10 * n * log (d/d0) + X

        n -> path loss exponent
        X -> zero mean gaussian distributed random variable with standard deviation (signma) 

"""

import numpy as np
from numpy import log10,pi

class Propogation :
    
    def __init__(self) :
        self.pathLossExponent = 3.5
        self.TxGain = 1.0
        self.RxGain = 1.0
        self.speedOfLight = 3E8
        self.sigmaDb = 4 #gaussian noise standard deviation
        self.refDistance = 1.0
        self.freq =  2.4E9  # 2.4Ghz

    def freeSpace(self,pTx,d) :
        """
        pTx - Transmitter power
        d   - distance
        """
        wavelength = self.speedOfLight/self.freq
        m = wavelength / ( 4 * pi * d )
        rTx = pTx * self.TxGain * self.RxGain * m * m
        return rTx

    def logNormalShadowing(self,pTx,d) :
        d0 = self.refDistance
        pr0 = self.freeSpace(pTx,d0)
        distComponentDb = -10.0 * self.pathLossExponent * log10(d/d0) #why negative 
        pathLossDb = distComponentDb + np.random.normal(0, self.sigmaDb)
        pr = pr0 * pow(10, pathLossDb/10.0) # pow component converts DB to watts 
        return pr



if __name__ == "__main__" :
    p = Propogation()
    print(10 * log10(p.logNormalShadowing(3E-3,10)))
    print(10 * log10(p.freeSpace(3E-3,10)))


