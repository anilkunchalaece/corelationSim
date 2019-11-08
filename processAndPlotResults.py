import os,json
import matplotlib.pyplot as plt
import numpy as np

roundTimeList = [5,10] # in hours
nodeInitSamplingRateList  = [2,10,20] # in minutes 
import matplotlib.pyplot as plt
def totalNumberOfSamplesPerRound(data,key):   
    samplesPerRound = []
    for round in data['rounds'] :
        totalSamples = 0
        for node in round :
            totalSamples = totalSamples + round[node][key]
        samplesPerRound.append(totalSamples)
    # print(sum(samplesPerRound))
    return samplesPerRound,sum(samplesPerRound)

def processData() :
    result = dict()

    #process data
    for roundTime in roundTimeList :
        roundTime = roundTime*60*60
        result_ = list()
        for nodeInitSamplingRate in nodeInitSamplingRateList :
            nodeInitSamplingRate = nodeInitSamplingRate*60
            keys = ['noOfSamples','samplingRate','transmitEnergy','sensingEnergy']
            rd = dict()
            for key in keys :
                fileName = "result-{}-{}.json".format(nodeInitSamplingRate,roundTime)
                fileNameNA = "result-{}-NA-{}.json".format(nodeInitSamplingRate,roundTime)
                with open(os.path.join('results',fileName)) as f:
                    data = json.load(f)
                # print(fileName)
                withSampling = totalNumberOfSamplesPerRound(data,key)
                with open(os.path.join('results',fileNameNA)) as f:
                    data = json.load(f)
                # print(fileNameNA)
                withoutSampling = totalNumberOfSamplesPerRound(data,key)
                rd[key] =  {
                        'withSampling' : {
                            'roundWise' : withSampling[0],
                            'total' : withSampling[1]
                        },
                        'withoutSampling' : {
                            'roundWise' : withoutSampling[0],
                            'total' : withoutSampling[1]
                        }
                    }

            result_.append(rd)
        result[roundTime] = result_
    return result 
# print(result)

def plotGraphs() :
    data = processData()
    # print(data)
    #plot energy consumption for single round
    objects = ('2M', '10M','20M')
    y_pos = np.arange(len(objects))
    E_values = []
    S_values = []
    E_values_NA = []
    S_values_NA = []
    totalNumberOfNodes = 23

    for val in data[36000] :
        TE = val['transmitEnergy']['withSampling']['total']
        SE = val['sensingEnergy']['withSampling']['total']
        E_values.append((TE+SE)/totalNumberOfNodes)
        
        TE_NC = val['transmitEnergy']['withoutSampling']['total']
        SE_NC = val['sensingEnergy']['withoutSampling']['total']
        E_values_NA.append((TE_NC+SE_NC)/totalNumberOfNodes)

        NS = val['noOfSamples']['withSampling']['total']
        S_values.append(NS/totalNumberOfNodes)
        NS_NC = val['noOfSamples']['withoutSampling']['total']
        S_values_NA.append(NS_NC/totalNumberOfNodes)

    plotBarWidth = 0.35
    plt.bar(y_pos, E_values,plotBarWidth,align='center',color='green')
    plt.xticks(y_pos, objects)
    plt.ylabel('Energy Consumption')
    plt.xlabel('Sampling Rate')
    plt.title('Average Energy Consumption vs Sampling rate')
    plt.savefig(os.path.join('plots','averageEnergyConsumption.png'))
    plt.show()

    plt.bar(y_pos, E_values,plotBarWidth,align='center',color='green')
    plt.bar(y_pos+plotBarWidth, E_values_NA, plotBarWidth, align='center',color='red')
    plt.xticks(y_pos, objects)
    plt.ylabel('Avearge Energy Consumption')
    plt.xlabel('Sampling Rate')
    plt.title('Average Energy Consumption with and without Correlation')
    plt.legend(['With Correlation','Without Correlation'])
    plt.savefig(os.path.join('plots','energyConsumptionWithAndWithoutCorrelation.png'))
    plt.show()


    plt.bar(y_pos, S_values,plotBarWidth, align='center',color='green')
    plt.xticks(y_pos, objects)
    plt.ylabel('Avearage Number of Samples')
    plt.xlabel('Sampling Rate')
    plt.title('Average Number of Samples vs Sampling rate')
    plt.savefig(os.path.join('plots','averageNumberOfSamples.png'))
    plt.show()

    plt.bar(y_pos, S_values,plotBarWidth,align='center',color='green')
    plt.bar(y_pos+plotBarWidth, S_values_NA, plotBarWidth, align='center',color='red')
    plt.xticks(y_pos, objects)
    plt.ylabel('Average Number Of Samples')
    plt.xlabel('Sampling Rate')
    plt.title('Average Number of Samples with and without Correlation')
    plt.legend(['With Correlation','Without Correlation'])
    plt.savefig(os.path.join('plots','NoOfSamplesWithAndWithoutCorrelation.png'))
    plt.show() 

if __name__ == '__main__' :
    plotGraphs()