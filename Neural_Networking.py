#wall of Richard Burgins hard work, may it stand eternal and unto it I pledge my life===============================================================================
#===================================================================================================================================================================
#===================================================================================================================================================================

import math
import random
import numpy

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
         

class Neuron:
    def __init__(self, num_inputs):
        self.bias = 0
        self.weight = []
        for i in range(0,num_inputs):
            self.weight.append(random.random())

    def ActivationFunction(self, Input):
        total = sum(numpy.multiply(Input,self.weight))
        return (self.sigmoid(total)+ self.bias)
    
    def sigmoid(self, x):
        result = 1/(1+math.exp(-x))
        return result


def scoring():
    #Score_S = 0
    Score_V = Velocity * 10^4
    Score_F = Fuel  * 10^4
    #Score_A = 0 
    score =  + Score_F + Score_V

    return score


def breed():
    #take top nets and iterate through their weights finding an average , then creating a new net with it.
    #simple mathematics
    pass

def mutate():
    #change the weights and biases a very small amount
    pass

def clone():
    #take the top performers and take a copy to be used in the next generation
    #so there is no lost potential
    pass

def NextGeneration(Netlist, Scorelist):
    pass



    return NewNetlist