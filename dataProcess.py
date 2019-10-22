'''
Author : Kunchala Anil
Email : akunchala@lincoln.ac.uk / anilkunchalaece@gmail.com
Date : 21 oct 2019 

This script is used to process data available at https://zenodo.org/record/2654726#.Xa2_C_fTU5k
Grand-St-Bernard Deployment
'''
import os
import numpy as np
import matplotlib.pyplot as plt

class Data :
    def __init__(self) :
        self.dataDir = os.path.join(os.getcwd(),'data')


    def visualizeRandomStation(self):
        #this function will get function from random station and displays the graphs for all features
        randomNodeNum = np.random.randint(len(os.listdir(self.dataDir)))
        print("visualization of node num {0}".format(randomNodeNum))
        with open(os.path.join(self.dataDir,str(randomNodeNum)+'.txt')) as f:
            sensorData = f.readlines()
        # print(len(sensorData))
        aTemp = getDataBasedOnIndex(sensorData,8)
        sTemp = getDataBasedOnIndex(sensorData,9)
        rHumi = getDataBasedOnIndex(sensorData,11)
        wSpeed = getDataBasedOnIndex(sensorData,16)

        plt.subplot(4,1,1)
        plt.plot(aTemp)
        plt.title('Ambient Temperature ')

        plt.subplot(4,1,2)
        plt.plot(sTemp)
        plt.title('Surface Temperature ')

        plt.subplot(4,1,3)
        plt.plot(rHumi)
        plt.title('Relative Humidity ')

        plt.subplot(4,1,4)
        plt.plot(wSpeed)
        plt.title('Wind Speed ')

        plt.suptitle('Node no {} Sensor Values '.format(randomNodeNum))
        plt.tight_layout()
        plt.show()


    def visualizeSingleFeature(self,featureName,noOfStations=23) :
        #this function will plot the single feature from all the stations
        #viewing 23 stations is bit messy, we can pass number of stations to view parameters
        allFiles = os.listdir(self.dataDir)
        featureValues = []
        stationIds = []
        # get number of stations randomly
        for fileName in np.random.randint(len(allFiles),size=noOfStations) :
            print("processing for {} ".format(fileName))
            stationIds.append(fileName)
            with open(os.path.join(self.dataDir,str(fileName+1)+'.txt')) as f :
                sensorData = f.readlines()
            if featureName == 'aTemp' : # Ambient Temperature
                title = 'Ambient Temperature'
                featureValues.append(getDataBasedOnIndex(sensorData,8))
            elif featureName == 'sTemp' :
                title = 'Surface Temperature'
                featureValues.append(getDataBasedOnIndex(sensorData,9))
            elif featureName == 'rHumi' :
                title = 'Relative Humidity'
                featureValues.append(getDataBasedOnIndex(sensorData,11))
            elif featureName == 'wSpeed' :
                title = 'Wind Speed'
                featureValues.append(getDataBasedOnIndex(sensorData,16))
            else :
                print("Please check featureName")
        ymin = min([min(value) for value in featureValues])
        ymax = max([max(value) for value in featureValues])
        for featureIndex in range(len(featureValues)) :
            # plt.subplot(len(allFiles),1,featureIndex+1)
            plt.plot(featureValues[featureIndex],label='Station {}'.format(stationIds[featureIndex]))
            
        plt.title(title)
        plt.legend()
        plt.ylim(ymin, ymax)
        print('ymin is {0} and y max is {1}'.format(ymin,ymax))
        plt.show()
        

def getDataBasedOnIndex(data,index) :
    return [float(line.split()[index]) for line in data]




if __name__ == '__main__' :
    data = Data()
    # data.visualizeRandomStation()
    data.visualizeSingleFeature('aTemp')


        