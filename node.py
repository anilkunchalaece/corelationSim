'''
Author : Kunchala Anil
Email : akunchala@lincoln.ac.uk
Date : 18 oct 2019 

This is the base class for node - used to define nodes and their properties
'''

class Node :
    def __init__(self,xPosition,yPoistion,initEnergy,samplingRate,nodeId):
        self.nodeId = nodeId
        self.xPos = xPosition
        self.yPos = yPoistion
        self.energy = initEnergy
        self.cluster = 0 #cluster node belong to -> initially 0
        self.samplingRate =samplingRate  # TODO is it array [seperate for each sensor] or single value [same for all sensors] ?
    
    def getEnergy(self) :
        #get residue energy of the node
        return self.energy
    
    def updateEnergy(self) :
        #update the energy of the node i.e after each transmission or sensor sampling we need to update the energy
        # TODO
        self.energy = self.energy
    
    def updateSamplingRate(self) :
        # update sampling rate based on correlation
        # TODO
        self.samplingRate = self.samplingRate

    def readSensorData(self) :
        #this function is used to emulate the sensor readings from the node
        return '1x,2y,3z'
    

if __name__ == '__main__' :
    import numpy as np
    import matplotlib.pyplot as plt

    numOfNodes = 50
    size = 50 # 100x100
    xList = np.random.randint(size,size=numOfNodes)
    yList = np.random.randint(size,size=numOfNodes)
    nodeList = list() #this is where we store all the objects
    for nodeNumber in range(numOfNodes) :
        nodeList.append(Node(xList[nodeNumber],yList[nodeNumber],2))
    # print(nodeList[3].xPos)
    plt.scatter([n.xPos for n in nodeList],[n.yPos for n in nodeList])
    plt.show()