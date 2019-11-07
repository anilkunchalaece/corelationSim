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
    objects = ('2M','2M-NC', '10M','10M-NC','20M','20M-NC')
    y_pos = np.arange(len(objects))
    E_values = []
    for val in data[18000] :
        TE = val['transmitEnergy']['withSampling']['total']
        SE = val['sensingEnergy']['withSampling']['total']
        E_values.append(TE+SE)
        TE_NC = val['transmitEnergy']['withoutSampling']['total']
        SE_NC = val['sensingEnergy']['withoutSampling']['total']
        E_values.append(TE_NC+SE_NC)
    plt.bar(y_pos, E_values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Energy Consumption')
    plt.title('Sampling Rate')
    plt.show()

if __name__ == '__main__' :
    plotGraphs()