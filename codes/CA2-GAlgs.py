import random
import math

crossoverRate = 0.25
mutationRate = 0.1
populationSize = 100

def printMathematicalPhrase(equation):
    for i in equation:
        print(i, end = "")

class EquationBuilder:

    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber

        self.population = self.makeFirstPopulation()

    def makeFirstPopulation(self):
        chromosome = []
        temp = ['0']*self.equationLength
        for k in range(populationSize):
            chromosome.append(temp.copy())
        for j in range(populationSize):
            for i in range(0, self.equationLength, 2):
                rand_index1 = random.randrange(len(self.operands))
                randomOperand = self.operands[rand_index1]
                chromosome[j][i] = str(randomOperand)
                if (i != self.equationLength - 1):
                    rand_index2 = random.randrange(len(self.operators))
                    randomOperator = self.operators[rand_index2]
                    chromosome[j][i + 1] = randomOperator
        return chromosome

    def mathematicalPhrase(self, chromosome):
        phrase = ""
        for element in chromosome:
            phrase += element
        return phrase
    
    def calculateProbability(self, fitnesses, sumOfFitnesses):
        probability = [0]*populationSize
        for i in range(populationSize):
            probability[i] = fitnesses[i] / sumOfFitnesses[0]
        return probability

    def calculateCumulativeProb(self, probability):
        cumulativeProb = [0]*populationSize
        for i in range(populationSize):
            if (i == 0):
                cumulativeProb[i] = probability[i]
            else:
                cumulativeProb[i] = cumulativeProb[i - 1] + probability[i]
        return cumulativeProb

    def createMatingPool(self, cumulativeProb):
        newChromosome = [0]*populationSize
        for i in range(populationSize):
            randNumber = random.uniform(0, 1)
            for j in range(populationSize - 1):
                if (randNumber < cumulativeProb[0]):
                    newChromosome[i] = self.population[0]
                elif (randNumber > cumulativeProb[populationSize - 1]):
                    newChromosome[i] = self.population[populationSize - 1]
                else:
                    if (randNumber > cumulativeProb[j] and randNumber < cumulativeProb[j + 1]):
                        newChromosome[i] = self.population[j + 1]
        return newChromosome
    
    def createCrossoverPool(self, newChromosome):
        crossoverPool = []
        idxOfNewChromosome = []

        for i in range(populationSize):
            randNumber = random.uniform(0, 1)
            if (randNumber < crossoverRate):
                crossoverPool.append(newChromosome[i])
                idxOfNewChromosome.append(i)

        allCrossoverPool = []
        allCrossoverPool = [0]*len(crossoverPool)

        for j in range(len(crossoverPool)):
            randNumber = random.randint(1, self.equationLength - 1)
            crossChromosome1 = crossoverPool[j].copy()
            crossChromosome2 = crossoverPool[(j + 1) % len(crossoverPool)].copy()
            for k in range(randNumber):
                crossChromosome1[k] , crossChromosome2[k] = crossoverPool[(j + 1) % len(crossoverPool)][k], crossoverPool[j][k]
            allCrossoverPool[j] = crossChromosome1
            if (j != len(crossoverPool) - 1):
                allCrossoverPool[(j + 1) % len(crossoverPool)] = crossChromosome2
        
        counter = 0
        for k in idxOfNewChromosome:
            newChromosome[k] = allCrossoverPool[counter]
            counter = counter + 1

        return newChromosome
    
    def mutateChromosome(self, chromosome):
        for i in range(math.floor(self.equationLength * populationSize * mutationRate)):
            randNumber1 = random.randint(0, populationSize - 1)
            randNumber2 = random.randint(0, self.equationLength - 1)
            if (randNumber2 % 2 == 0):
                randNumber3 = random.randrange(len(self.operands))
                randomOperand = self.operands[randNumber3]
                chromosome[randNumber1][randNumber2] = str(randomOperand)
            else:
                randNumber3 = random.randrange(len(self.operators))
                randomOperator = self.operators[randNumber3]
                chromosome[randNumber1][randNumber2] = randomOperator
        return chromosome

    def calculatefitnesses(self, sumOfFitnesses):
        fitnesses = []
        fitnesses = [0]*populationSize
        for i in range(populationSize):
            difference = abs(eval(self.mathematicalPhrase(self.population[i]))  - self.goalNumber)
            if (difference == 0):
                return self.population[i]
            fitnesses[i] = 1 / (1 + difference)
            sumOfFitnesses[0] = sumOfFitnesses[0] + fitnesses[i]
        return fitnesses

    def findEquation(self):
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            sumOfFitnesses = [0]
            fitnesses = self.calculatefitnesses(sumOfFitnesses)
            checkType = '021'
            if (type(fitnesses[0]) == type(checkType)):
                return fitnesses

            probability = []
            probability = self.calculateProbability(fitnesses, sumOfFitnesses)

            cumulativeProb = []
            cumulativeProb = self.calculateCumulativeProb(probability)

            newChromosome = []
            newChromosome = self.createMatingPool(cumulativeProb)

            crossoverPool = []
            crossoverPool = self.createCrossoverPool(newChromosome)

            self.population.clear()

            mutationPool = []
            mutationPool = self.mutateChromosome(crossoverPool)

            self.population.extend(mutationPool)

operands = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
operators = ['+', '-', '*', '%']
equationLength = 51
goalNumber = 10202

equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
printMathematicalPhrase(equation)