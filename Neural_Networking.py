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

        #Outputs
        self.Thrust = Neuron(2)

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

        #Output
        return self.Thrust.ActivationFunction([e,f])

    def Scoring(self, Velo, Fuel, success):
        print(Velo)
        Score_V = Velo * (10^-2)
        Score_F = Fuel  * 10
        Score_S = 0
        if success == True:
            Score_S = 1 * 10^3

        self.score = Score_S + Score_F + Score_V

        return self.score   

class Neuron:
    def __init__(self, num_inputs):
        self.bias = 0
        self.weight = []
        for i in range(0,num_inputs):
            self.weight.append(random.uniform(-1,1))

    def ActivationFunction(self, Input):
        total = sum(numpy.multiply(Input,self.weight))
        return (self.step(total)+ self.bias)
    
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
        Netlist[len(Netlist)-1].Scoring(Pop[i].u, Pop[i].fuel, Pop[i].SUCCESS)
    
    Netlist = Sort(Netlist)
    
    #clone
    for i in range(0,3):
        result = clone(Netlist[0])
        NewNetlist.append(result)
        Netlist.pop(0)

    #breed
    #Breedlist = []
    #for i in range(0,7):
    #    Breedlist.append(Netlist[0])
    #    Netlist.pop(0)

    #Resultlist = breed(Breedlist)
   # NewNetlist = NewNetlist + Resultlist

    #mutate
    Mutatelist = []
    for i in range(0,len(NewNetlist)):
        if random.random()> 0.5:
            Mutatelist.append(mutate(NewNetlist[i]))
    NewNetlist = Mutatelist
    #The rest of Netlist are removed

    return NewNetlist

def Sort(List):
    pass

#def breed(Best):

def mutate(Net):
    #change the weights and biases a very small amount
    Neurons = ["Altitude", "Velocity", "Acceleration", "Fuel", "H1", "H2", "Thrust"]

    print("ya")
    for x in range(0, len(Neurons)):
        for y in range(0, len(Net.Neuron[x].weight)):
            Net.Neuron[x].weight[y] += 0.01
        Net.Neuron[x].bias += 0.01

    return result

def clone(TopPerformer):
    #take the top performers and take a copy to be used in the next generation
    #so there is no lost potential
    result = TopPerformer
    return result
