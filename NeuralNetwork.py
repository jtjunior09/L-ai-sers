import numpy as np
import random
import scipy.special

from Definitions import *

class NeuralNetwork():
    def __init__(self, numInput, numHidden, numOutput):
        """ NeuralNetwork constructor """
        self.numInput = numInput
        self.numHidden = numHidden
        self.numOutput = numOutput

        # Inputs to Hidden layer weight
        self.weightInHdn = np.random.uniform(-0.5, 0.5, size=(self.numHidden, self.numInput))
        
        # Hidden layer to Outputs weight
        self.weightHdnOut = np.random.uniform(-0.5, 0.5, size=(self.numOutput, self.numHidden))

        # Sigmoud activation function, used to create hidden layer outputs and final outputs, post-weights
        self.activation_func = lambda x: scipy.special.expit(x)

    def modify_weights(self):
        """ Multi-dimensional iteration over weights, changing if random doesn't meet MUTATION_CHANCE threshold """
        for x in np.nditer(self.weightInHdn, op_flags=['readwrite']):
            if random.random() < MUTATION_CHANCE:
                x[...] = np.random.random_sample() - 0.5
        
        for x in np.nditer(self.weightHdnOut, op_flags=['readwrite']):
            if random.random() < MUTATION_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def mix_arrays(self, array_1, array_2):
        """ Randomly mix up two arrays, used for 'breeding' NeuralNetworks by mixing weights of two parents """
        # Both arrays are same size and dimensions
        size = array_1.size
        rows = array_1.shape[0]
        cols = array_1.shape[1]

        # How many to take from one parent array
        takeCount = size - int(size * MUTATION_MIX_PERCENT)

        # Array of random numbers, representing indices to keep from array_1
        randArray = np.random.choice(np.arange(size), takeCount, replace=False)

        arrayFinal = np.random.rand(rows, cols)

        for row in range(0, rows):
            for col in range(0, cols):
                currentIndex = row * cols + col
                if currentIndex in randArray:
                    arrayFinal[row][col] = array_1[row][col]
                else:
                    arrayFinal[row][col] = array_2[row][col]
        
        return arrayFinal

    def create_offspring(self, neuralNet_1, neuralNet_2):
        """ 'Breed' two Neural Networks, using mix_arrays helper """
        self.weightInHdn = self.mix_arrays(neuralNet_1.weightInHdn, neuralNet_2.weightInHdn)
        self.weightHdnOut = self.mix_arrays(neuralNet_1.weightHdnOut, neuralNet_2.weightHdnOut)

    def get_outputs(self, inputsList):
        # Create 2 dimensional array (matrix) using inputsList and transpose
        inputs = np.array(inputsList, ndmin=2).T

        hiddenInputs = np.dot(self.weightInHdn, inputs)
        hiddenOutputs = self.activation_func(hiddenInputs)

        finalOutputIns = np.dot(self.weightHdnOut, hiddenOutputs)
        finalOutputOuts = self.activation_func(finalOutputIns)
        
        return finalOutputOuts

    