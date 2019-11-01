from dataProcess import Data
from energy import Energy
from network import Network
from node import Node
import os,json

configFileLoc = os.path.join(os.getcwd(), 'config.json')

def loadConfig() :
    with open(configFileLoc) as f :
        data = json.load(f)
    return data

conf = loadConfig()
net = Network(conf['numberOfNodes'],conf['gridSize'],conf['nodeInitEnergy'],conf['nodeSamplingRate'])
randNet = net.generateRandomNetwork()
net.plotNetwork(randNet)
