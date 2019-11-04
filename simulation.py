from dataProcess import Data
from energy import Energy
from network import Network
from node import Node
import os,json
import datetime
import numpy as np
from collections import Counter

configFileLoc = os.path.join(os.getcwd(), 'config.json')
totalSimulationDuration = 10000 * 2 * 60# in seconds -> 10k samples with 2 min sample time
roundTime = 60*60 #in seconds [ 1 hour ]

USE_PREV_NODES = True

def loadConfig() :
    with open(configFileLoc) as f :
        data = json.load(f)
    return data

def pearsonCorrelation(X, Y):
   ''' Compute Pearson Correlation Coefficient. '''
   #convert X and Y to numpy arrays
   X = np.array(X)
   Y = np.array(Y)

   # Normalise X and Y
   X -= X.mean(0)
   Y -= Y.mean(0)
   # Standardise X and Y
   X /= X.std(0)
   Y /= Y.std(0)
   # Compute mean product
   return np.mean(X*Y)

# it takes matrix_m calculate the correlation for M in all SN pairs
def calculateCorelation(mat_M) :
    cnt = 0
    m_length = len(mat_M)
    corr_m = dict()
    for i in range(m_length) :
        corr_list = []
        index_list = []
        for j in range(m_length) :
            if i != j : #we dont need to correlation when i == j
            # print(i,j)
                cnt = cnt + 1
                corr = pearsonCorrelation(mat_M[i],mat_M[j])
                corr_list.append(corr) # corelation of each i compared with j
                index_list.append(j) # index of j
        corr_m[i] = {
            'corr' : corr_list,
            'index' : index_list
        }
        
    print('total number of corelations are {}'.format(cnt))
    return corr_m

def calculateMatrix_M_NAN(mat_m,m_samplingRate) :
    print(len(mat_m))
    print(len(m_samplingRate))
            

#get nodeObj based on nodeId
def getNodeObj(nodeId,nodeObjList) :
    for obj in nodeObjList :
        if obj.nodeId == nodeId :
            return obj

conf = loadConfig()

# ##### Ready sensor data #########
print("###### Processing data and loading into the memory ")
d = Data()
simStartTime = d.simulationStartTime
sensorData = d.loadSensorDataForSimulation(conf['nodeUpSamplingRate'])

###### Genearate Network ##########
print("###### Generating the network using uniform distribution ")
net = Network(conf['numberOfNodes'],conf['gridSize'],conf['nodeInitEnergy'],conf['nodeInitSamplingRate'])
randNet = net.generateRandomNetwork(usePrevNodes=USE_PREV_NODES)
# net.plotNetwork(randNet)

###### Simulation starts from HERE #########
numberOfRounds = int(totalSimulationDuration / roundTime)

print("total number of rounds are {0} number of samples per round are ".format(numberOfRounds))

# matrix_M = []

for roundIndex in list(range(numberOfRounds)):
    # print("round {0}".format(roundIndex))
    # Step 1 : Get the data from sensor nodes
    matrix_M = []
    m_samplingRate = []
    for nodeNumber in randNet :
        numberOfSamplesPerRound = int(roundTime / nodeNumber.samplingRate)
        # print("node number {}".format(nodeNumber.nodeId))
        temp_l = list()
        temp_t = list()
        for eachSampleTime in list(range(1,numberOfSamplesPerRound)) :
            nextSampleTime = (roundIndex * roundTime) + eachSampleTime * nodeNumber.samplingRate
            tDiff = d.simulationStartTime + datetime.timedelta(seconds=nextSampleTime)
            temp_l.append(sensorData[str(nodeNumber.nodeId+1)].loc[tDiff.strftime("%Y-%m-%d %H:%M")].tolist()[0])
            temp_t.append(nextSampleTime)
            # if eachSampleTime == 1 :
            #     print(nextSampleTime)
        
        print('for node {} sampling rate {} number of samples are {}'.format(nodeNumber.nodeId+1,nodeNumber.samplingRate,len(temp_l)))

        matrix_M.append(temp_l)
        m_samplingRate.append(temp_t)
    
    # Step 2: Get the correlation matrix 
    # print(matrix_M)
    
    #samplingrate,roundIndex is used to calculate starting timestamp for all nodes
    calculateMatrix_M_NAN(matrix_M,m_samplingRate)

    matrix_corr = calculateCorelation(matrix_M)
    
    #correlation table
    corr_table = dict()

    #node_j list -> to calculate number of occurances
    node_j_list = list()

    # Step 3 : find maximum correlation
    for corr in matrix_corr :
        node_i = corr
        max_corr = max(matrix_corr[node_i]['corr'])
        max_corr_index = matrix_corr[node_i]['corr'].index(max_corr)
        node_j  = matrix_corr[node_i]['index'][max_corr_index]
        # print('node {} max corr {} with respect to {}'.format(node_i,max_corr,node_j))
        corr_table[node_i] = {
            'j' : node_j,
            'mc' : max_corr
            }

        node_j_list.append(node_j)
    
    # we can later use it to print / save correlation tables
    # print("correlation table")
    # print(corr_table)
    print(" i,  j,  corr")
    for vl in corr_table :
        print(' {} , {} , {} '.format(vl,corr_table[vl]['j'],corr_table[vl]['mc']))

    # Step 4 : make node_j ordered list
    # node_j ordered list -> in ascending order
    node_j_ordered_list = Counter(node_j_list).most_common() #it gives us in descending order
    node_j_ordered_list.reverse() #change it into ascending order
    # print(node_j_ordered_list)

    # Step 5 : Calculate the new sampling rate according to correlation
    #modify the sampling rate according to the correlation
    sampling_decided = list() #used to store the nodeid's whose sampling ids are changed

    for n_j in node_j_ordered_list :
        # print(n_j[0])
        #get matching node and coorelation for n_j
        current_node = n_j[0]
        match_node = corr_table[current_node]['j']
        match_corr = corr_table[current_node]['mc']
        

        nodeObj = getNodeObj(current_node,randNet)
        
        # check if sampling_decided for matching node ?
        # according set the samping rate for each sensor
        if match_node not in sampling_decided :
            nodeObj.samplingRate = nodeObj.samplingRate + nodeObj.samplingRate * (1-match_corr)
            sampling_decided.append(current_node)
        else :
            match_corr = 1 - match_corr
            nodeObj.samplingRate = nodeObj.samplingRate + nodeObj.samplingRate * (1-match_corr)
    print(sampling_decided)

    #update correaltion for remaining nodes
    for n_i in corr_table :
        if n_i not in sampling_decided :
            current_node = n_i 
            nodeObj = getNodeObj(current_node,randNet)
            nodeObj.samplingRate = nodeObj.samplingRate + nodeObj.samplingRate * (1-match_corr)
    # break
        
        






