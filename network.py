'''
Author : Kunchala Anil
Email : akunchala@lincoln.ac.uk
Date : 18 oct 2019 

This is the base class for network - used to generate network
'''
import numpy as np 
import matplotlib.pyplot as plt
import json,os
from node import Node

class Network:
    def __init__(self,numberOfNodes,gridSize,nodeInitEnergy,nodeSamplingRate):
        self.numberOfNodes = numberOfNodes
        self.gridSize = gridSize
        self.nodeInitEnergy = nodeInitEnergy
        self.nodeSamplingRate = nodeSamplingRate


    def generateRandomCoordinates(self):
        """
        This function will generate random coordinates and dump them into the file named 'prevNodes.json'
        """
        xPos =np.random.randint(self.gridSize,size=self.numberOfNodes).tolist()
        yPos = np.random.randint(self.gridSize,size=self.numberOfNodes).tolist()
        with open('prevNodes.json','w') as f :
            json.dump({
                'xPos' : xPos,
                'yPos' : yPos
            },f)
        return [xPos,yPos]         
    
    def generateRandomNetwork(self,usePrevNodes):
        '''
        It will generate nodes with random placements using size value
        '''
        if usePrevNodes == True :
            if os.path.isfile('prevNodes.json') :
                with open('prevNodes.json') as f :
                    nodeData = json.load(f)
                    xPos = nodeData['xPos']
                    yPos = nodeData['yPos']
            else :
                print('PrevNodes.json files does not exist, so creating and adding nodes to it')
                xPos,yPos = self.generateRandomCoordinates()
        else :
            print('generating the random coorinates for new simulation')
            xPos,yPos = self.generateRandomCoordinates()

        # nodePos= np.random.rand(2,self.numberOfNodes)*self.gridSize
        # # print(nodePos)
        # xPos = nodePos[0]
        # yPos = nodePos[1]
        nodeList = list() #this will hold all node objects
        for nodeNum in range(self.numberOfNodes) :
            # index is used as nodeId
            nodeList.append(Node(xPos[nodeNum],yPos[nodeNum],self.nodeInitEnergy,self.nodeSamplingRate,nodeNum))
        
        return nodeList

    def plotNetwork(self,nodeList) :
        '''
        @nodeList -> nodeObjectsList of the network
        it will plot the network as a scatter plot
        '''
        plt.scatter([n.xPos for n in nodeList],[n.yPos for n in nodeList],marker='o',s=80)
        #consider sink node / base station location is middle of grid
        plt.scatter(self.gridSize*0.5,self.gridSize*0.5,marker=(5, 0), s=100)
        plt.show()
    
    def getBaseStationCoOrdinates(self) :
        return (self.gridSize*0.5,self.gridSize*0.5)

if __name__ == '__main__' :
    numberOfNodes = 23
    gridSize = 100
    nodeInitEnergy = 10
    nodeSamplingRate = 10
    # 
    # random distribution of nodes uniform, gaussion, poisson with a reason
    # cluster head location -> minimum distance from all nodes
    # dont change node locations , provide option to use previous network placement
    # send paper with all lines where we need clarification
    # remove project from github
    net = Network(numberOfNodes,gridSize,nodeInitEnergy,nodeSamplingRate)
    randNet = net.generateRandomNetwork(True)
    net.plotNetwork(randNet)
