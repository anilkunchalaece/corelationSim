"""
Propogation model used to calculate the Recevied power at the CH from each node considering
shadowing and rayleigh fading

Friis free space equation:
         
                Pt * Gt * Gr * (lambda^2)
            Prx = --------------------------
                (4 * pi * d)^2 

Simplified path loss model
        PL(d0) + 10 * n * log (d/d0) 


shadowing path loss
            PL = PL(d0) + 10 * n * log (d/d0) + X

        n -> path loss exponent
        X -> zero mean gaussian distributed random variable with standard deviation (signma) 

rayleigh fading + shadowing + path loss
    signal power at receiver
        Pr = alpha^2 * 10^(x/10) * g(d) * Pt * Gt * Gr
        
        alpha -> rayleigh fading
        10^(x/10) -> log normal shadowing
        g(d) -> path loss
        Pt -> Transmitter power
        Gt -> Transmitter gain
        Gr -> Receiver gain

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
        self.rayleighScaleParameter = 2 # scale parameter for rayleigh distribution

    @staticmethod
    def powerToDb(pr) :
        return 10 * log10(pr)

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
        distComponentDb = -10.0 * self.pathLossExponent * log10(d/d0) #why negative  #simplified path loss model
        pathLossDb = distComponentDb + np.random.normal(0, self.sigmaDb) # added shadow component
        pr = pr0 * pow(10, pathLossDb/10.0) # pow component converts DB to watts 
        return pr

    def rayleighFading(self,pTx,d) :
        d0 = self.refDistance
        pr0 = self.freeSpace(pTx,d0)
        distComponentDb = -10.0 * self.pathLossExponent * log10(d/d0) #why negative  #simplified path loss model
        pathLossDb = distComponentDb + pow(abs(np.random.rayleigh(self.rayleighScaleParameter)),2) # added rayleigh component
        pr = pr0 * pow(10, pathLossDb/10.0) # pow component converts DB to watts 
        return pr

    def rayleighFadingAndLogNormalShadowing(self,pTx,d):
        d0 = self.refDistance
        pr0 = self.freeSpace(pTx,d0)
        distComponentDb = -10.0 * self.pathLossExponent * log10(d/d0) #why negative  #simplified path loss model
        pathLossDb = distComponentDb + pow(abs(np.random.rayleigh(self.rayleighScaleParameter)),2) # added rayleigh component
        pathLossDb = pathLossDb + np.random.normal(0, self.sigmaDb) # added shadow component
        pr = pr0 * pow(10, pathLossDb/10.0) # pow component converts DB to watts 
        return pr
    



if __name__ == "__main__" :
    p = Propogation()
    txPower = 3E-3
    distance = 50
    print("TX power {}".format(10 * log10(txPower)))
    print("RX power with freespace {}".format(10 * log10(p.freeSpace(txPower,distance))))
    print("Rx power with shadowing {} ".format(10 * log10(p.logNormalShadowing(txPower,distance))))
    print("RX power with rayleigh {} ".format(10 * log10(p.rayleighFading(txPower,distance))))
    print("RX power with shadowing and rayleigh {} ".format(10 * log10(p.rayleighFadingAndLogNormalShadowing(txPower,distance))))


