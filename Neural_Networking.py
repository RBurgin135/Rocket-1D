#wall of Richard Burgins hard work, may it stand eternal and unto it I pledge my life===============================================================================
#===================================================================================================================================================================
#===================================================================================================================================================================

import math
import random
import numpy

#Objects==========
class NeuralNet:
    def __init__(self):
        #Inputs
        self.Altitude = Neuron(1)
        self.Velocity = Neuron(1)
        self.Acceleration = Neuron(1)
        self.Fuel = Neuron(1)

        #Hidden
        self.H1 = Neuron(4)
        self.H2 = Neuron(4)
        self.H3 = Neuron(4)
        self.H4 = Neuron(4)

        #Outputs
        self.Thrust = Neuron(4)

        #Score
        self.score = 0


    def Forward(self, Alt, Velo, Acc, Fuel):
        #Input
        a = self.Altitude.ActivationFunction(Alt)
        b = self.Velocity.ActivationFunction(Velo)
        c = self.Acceleration.ActivationFunction(Acc)
        d = self.Fuel.ActivationFunction(Fuel)
        
        #Hidden
        HiddenInputs = [a,b,c,d]
        e = self.H1.ActivationFunction(HiddenInputs)
        f = self.H2.ActivationFunction(HiddenInputs)
        g = self.H3.ActivationFunction(HiddenInputs)
        h = self.H4.ActivationFunction(HiddenInputs)

        #Output
        return self.Thrust.ActivationFunction([e,f,g,h])

    def Scoring(self, Velo, Fuel, success):
        Score_V = -Velo *10
        Score_F = Fuel
        Score_S = 0
        if success == True:
            Score_S = 10000

        self.score = Score_S  + Score_V + Score_F

#=======
class Neuron:
    def __init__(self, num_inputs):
        self.bias = 0
        self.weight = []
        for i in range(0,num_inputs):
            self.weight.append(random.uniform(-1,1))

    def ActivationFunction(self, Input):
        total = sum(numpy.multiply(Input,self.weight))
        return (self.ReLU(total)+ self.bias)

    def ReLU(self, x):
        result = max(x, 0)
        return result

    def sigmoid(self, x):
        result = 1/(1+math.exp(-x))
        return result

    def step(self, x):
        if x > 0:
            return 1
        else:
            return -1

#Functions==========
def Review(Pop):
    #for generation size 20
    Netlist = []
    NewNetlist = []
    for i in range(0,len(Pop)):
        Netlist.append(Pop[i].Nn) 
        Netlist[len(Netlist)-1].Scoring(Pop[i].testU, Pop[i].fuel, Pop[i].SUCCESS)
    
    Netlist = Sort(Netlist)
    
    #clone
    for i in range(0,int(len(Pop)//6)):
        result = clone(Netlist[0])
        NewNetlist.append(result)
        Netlist.pop(0)


    #mutate
    Mutatelist = []
    for i in range(0,int(len(Netlist)/2)):
        result = Netlist[i]
        if random.uniform(0,1)> 0.5:
            result = Mutate(Netlist[i])
        Mutatelist.append(result)

    #The rest of Netlist are removed
    NewNetlist = NewNetlist + Mutatelist

    return NewNetlist

def Sort(List):
    #Bubble sort
    Sorted = False
    while Sorted == False:
        Sorted = True
        for i in range(0, len(List)-1):
            if List[i].score < List[i+1].score:
                Sorted = False
                Buffer = List[i]
                List[i] = List[i+1]
                List[i+1] = Buffer
    
    return List

def Mutate(Net):
    #change the weights and biases a very small amount
    fence = 0.05
    #Inputs
    Net.Altitude.weight[0] += random.uniform(-fence,fence)
    Net.Altitude.bias += random.uniform(-fence,fence)
    Net.Velocity.weight[0] += random.uniform(-fence,fence)
    Net.Velocity.bias += random.uniform(-fence,fence)
    Net.Acceleration.weight[0] += random.uniform(-fence,fence)
    Net.Acceleration.bias += random.uniform(-fence,fence)
    Net.Fuel.weight[0] += random.uniform(-fence,fence)
    Net.Fuel.bias += random.uniform(-fence,fence)

    #Hidden
    for i in range(0,len(Net.H1.weight)):
        Net.H1.weight[i] += random.uniform(-fence,fence)
    Net.H1.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H2.weight)):
        Net.H2.weight[i] += random.uniform(-fence,fence)
    Net.H2.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H3.weight)):
        Net.H3.weight[i] += random.uniform(-fence,fence)
    Net.H3.bias += random.uniform(-fence,fence)
    for i in range(0,len(Net.H4.weight)):
        Net.H4.weight[i] += random.uniform(-fence,fence)
    Net.H4.bias += random.uniform(-fence,fence) 

    #Outputs
    for i in range(0,len(Net.Thrust.weight)):
        Net.Thrust.weight[i] += random.uniform(-fence,fence)
    Net.Thrust.bias += random.uniform(-fence,fence)

    return Net

def clone(TopPerformer):
    result = TopPerformer
    return result
