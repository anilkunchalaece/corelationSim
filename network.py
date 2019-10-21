'''
Author : Kunchala Anil
Email : akunchala@lincoln.ac.uk
Date : 18 oct 2019 

This is the base class for network - used to generate network
'''
import numpy as np 
import matplotlib.pyplot as plt

from node import Node

class Network:
    def __init__(self,numberOfNodes,gridSize,nodeInitEnergy,nodeSamplingRate):
        self.numberOfNodes = numberOfNodes
        self.gridSize = gridSize
        self.nodeInitEnergy = nodeInitEnergy
        self.nodeSamplingRate = nodeSamplingRate

    
    def generateRandomNetwork(self):
        '''
        It will generate nodes with random placements using size value
        '''
        xPos = np.random.randint(self.gridSize,size=self.numberOfNodes)
        yPos = np.random.randint(self.gridSize,size=self.numberOfNodes)
        
        nodeList = list() #this will hold all node objects
        for nodeNum in range(self.numberOfNodes) :
            # index is used as nodeId
            nodeList.append(Node(xPos[nodeNum],yPos[nodeNum],self.nodeInitEnergy,self.nodeSamplingRate,nodeId))
        
        return nodeList

    def plotNetwork(self,nodeList) :
        '''
        @nodeList -> nodeObjectsList of the network
        it will plot the network as a scatter plot
        '''
        plt.scatter([n.xPos for n in nodeList],[n.yPos for n in nodeList],marker='o',s=80)
        #consider sink node / base station location is middle of grid
        plt.scatter(self.gridSize*1.5,self.gridSize/2,marker=(5, 0), s=100)
        plt.show()


if __name__ == '__main__' :
    net = Network(23,50,10,10)
    randNet = net.generateRandomNetwork()
    net.plotNetwork(randNet)