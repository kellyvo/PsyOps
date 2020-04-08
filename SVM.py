
from collections import namedtuple
from sklearn import svm
import matplotlib.pyplot as pp
import numpy as np
import re

data=namedtuple("data", ("url", "opinionation"))
data2d=namedtuple("data2d", ("url", "x", "y"))

TRAINING="training.txt"
OUTPUTS="output.txt"

"""
Reads the output file
Returns: the a list of data namedtuples representing
each input
"""

def readOutputFile():
    inputs=list()
    with open(OUTPUTS) as f:
        lines=f.readlines()
        for line in range(0, len(lines), 5):
            url=lines[line].strip()
            opinionatedRE=re.search("[0-9.]+", lines[line+1])
            opinionatedPercent=float(opinionatedRE.group(0))/100
            inputs.append(data(url, opinionatedPercent))

    return inputs

"""
Reads the training files to get training data
Returns: a list of the url and opinionated percent and 
whether or not something is opinionated(as an 0/1 integer) 
"""

def readTrainingFile():
    inputs = list()
    outputs = list()
    with open(TRAINING) as f:
        lines = f.readlines()
        for line in range(0, len(lines), 6):
            if(lines[line].strip()=="OPINIONATED ARTICLE"):
                outputs.append(1)
            else:
                outputs.append(0)
            url = lines[line+1].strip()
            opinionatedRE = re.search("[0-9.]+", lines[line + 2])
            opinionatedPercent = float(opinionatedRE.group(0))
            inputs.append(data(url, opinionatedPercent))

    return inputs, outputs

"""
Maps the 1 dimensional data to a second dimension to create 
Parameter lst: the list to get the data from
Returns: the two dimensional version of the list
"""

def map1dTo2d(lst:list):
    lst2d=list()

    for dataPoint in lst:
        lst2d.append(data2d(dataPoint.url, dataPoint.opinionation, dataPoint.opinionation**2))

    return lst2d

"""
Shows the training data in a graph
Parameter  articles: a list of data to show in a 1 dimensional graph
Parameter output: the output of the graph for each of the articles (1 for opinionated 0 for not)
Returns: nothing
"""

def showTrainingData1d(articles, output):
    opinionated=list()
    unopinionated=list()
    for article in range(len(articles)):
        if(output[article]==1):
            opinionated.append(articles[article].opinionation)
        else:
            unopinionated.append(articles[article].opinionation)
    y=np.zeros(len(opinionated))
    pp.plot(opinionated, y, 'bo')

    y=np.zeros(len(unopinionated))
    pp.plot(unopinionated, y, 'ro')

def showTrainingData2d(articles, output):
    opinionated=list()
    unopinionated=list()
    for article in range(len(articles)):
        if(output[article]==1):
            opinionated.append(articles[article])
        else:
            unopinionated.append(articles[article])

    opinionated=map1dTo2d(opinionated)
    unopinionated=map1dTo2d(unopinionated)

    x=list()
    y=list()

    for dataElement in opinionated:
        x.append(dataElement.x)
        y.append(dataElement.y)

    pp.plot(x, y, 'bo')

    x=list()
    y=list()

    for dataElement in unopinionated:
        x.append(dataElement.x)
        y.append(dataElement.y)

    pp.plot(x, y, 'ro')


def train(inputs, outputs):
    inputs=map1dTo2d(inputs)

    # Create a map of 2-dimensional data for the opinionated/unopinionated articles
    x=list()
    for article in inputs:
        x.append([article.x, article.y])

    machine=svm.SVC()
    machine.fit(x, outputs)

    return machine

def classify(inputs, machine):
    outputs=list()

    for input in inputs:
        outputs.append(machine.predict([[input.opinionation, input.opinionation**2]]))

    return inputs, outputs

def printOutputs(inputs, outputs):
    for input in range(len(inputs)):
        if(outputs[input]==1):
            print("OPINIONATED: "+inputs[input].url)
        else:
            print("UNOPINIONATED: "+inputs[input].url)

def main():
    inputs, outputs=readTrainingFile()

    #showTrainingData1d(inputs, outputs)
    #showTrainingData2d(inputs, outputs)

    machine=train(inputs, outputs)

    inputs=readOutputFile()
    inputs, outputs=classify(inputs, machine)
    printOutputs(inputs, outputs)

if __name__=='__main__':
    main()