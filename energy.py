'''
Author : Kunchala Anil
Email : akunchala@lincoln.ac.uk / anilkunchalaece@gmail.com
Date : 23 oct 2019 

This script is used to calculate energy consumation of node 
based on paper - An estimation of sensor energy consumption M.N. Halgamuge, M.Zukerman and K.Ramamohanarao
'''

class Energy :
    def __init__(self):
        self.initEnergy = 2
    
    def energyConsumptionHalgamuge(self,numberOfBitsPerSample,numberOfSamples) :
        #All these constants are shamelessly copied from refered paper
        # for now assuming number of bits are constants - later need to change it with channel attributes
        # Sensing energy is calculated for each round , so we need to specify maximum samples we take for round to calculate 
        # currently using only sampling and transmit energy
        #b = 50 # 2kb Transmit packet size
        tr_factor = 1.5 # weight factor used to add extrabits required for communication TODO- need to replace with edmond channel model
        b_transmit = numberOfBitsPerSample * numberOfSamples * tr_factor
        N_cyc = 0.97E6 # number of clock cycles per task 
        C_avg = 22E-12 # Avg capacitance witch per cycle
        V_sup = 2.7 # Supply voltage to sensor
        f = 191.42E3 # sensor frequnecy
        n_p = 21.26 # constant depending on the processor
        n = 2 # path loss exponent
        I_o = 1.196E-3 # leakage current
        V_t = 0.2 # thermal voltage
        E_elec = 50E-9 # Energy dissipation : electronics Joules/bit
        E_amp = 100E-12 # Energy dissipation : power amplifier J/bit/m2
        E_ini = 1E-6 # energy for starting up radio in joules
        T_tranON = 2450E-6 # Time duration sleep -> idle
        T_tranOFF = 250E-6 # Time duration idle -> sleep 
        I_A = 8E-3 # Current: wake up mode
        I_S = 1E-6 # Current: sleeping mode
        T_A = 1E-3 # Active time
        T_S = 299E-3 # Sleeping time
        T_tr = 300E-3 # Time between consecutive packets
        T_sens = 0.05E-4 #Time duration : sensor node sensing
        I_sens = 0.7E-3 # Current : Sensing activity
        I_write = 18.4E-3 #Current : Flash writing 1 byte data
        I_read = 6.2E-3 # Current : Flash reading 1 byte of data
        T_write = 12.9E-3 # Time duration : Flash writing
        T_read = 565E-6 # Time duration : flash reading
        E_actu = 0.02E-3 # Energy dissipation : actuation

        d = 40 # TODO distance from from node to base station. for now consider it as constant. later we have to calculate distance base on node and base station location

        EnergySensing = numberOfBitsPerSample * V_sup * I_sens * T_sens
        # EnergyDataLogging = b * V_sup * ((I_write*T_write) + (I_read * T_read))
        EnergyTransmit = b_transmit*E_elec + b * (d^2) * E_amp + E_ini # check 'd' -> distance

        # CN = (T_tranON + T_A +T_tranOFF) / (T_tranON+ T_A + T_tranOFF + T_S) # Duty cycle for sensor node
        # EnergyTransient = T_A*V_sup *(CN*I_A + (1-CN) * I_S)

        # print('EnergySensing {0} EnergyTransmit{1}'.format(EnergySensing,EnergyTransmit))

        # totalEnergyConsumed = EnergySensing + EnergyDataLogging + EnergyTransmit # + EnergyTransient #for now lets ignore this - cause duty cycle may change with sampling time
        EnergySensingPerRound = EnergySensing * numberOfSamples

        return EnergySensingPerRound,EnergyTransmit
         
if __name__ == '__main__' :
    e = Energy()
    TE = e.energyConsumptionHalgamuge()
    print(TE)