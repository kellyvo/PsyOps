from collections import namedtuple
import math
import re
import matplotlib.pyplot as pp
import numpy as np
import sys

TRAINING="training.txt"
OUTPUTS="output.txt"
LINE="line.txt"
LEARNING_RATE=.25

data=namedtuple("data", ("url", "opinionation"))
line=namedtuple("line", ("m", "b"))

"""
The sigmoid function for classification between range (0, 1)
Returns: the float result of running it through the sigmoid
"""
def sigmoid(x:float):
    return 1/(1+math.exp(-x))

"""
Uses linear regression to train the line
Parameter input: the input to the function
Parameter actual: the desired output
Parameter output: the output that occured
Parameter ln: the line to change
Returns: a changed line
"""

def regress(input:int, actual:int, output:float, ln:line):
    deltaM=(output-actual)*output*(1-output)*input*LEARNING_RATE
    deltaB=(output-actual)*output*(1-output)*LEARNING_RATE
    newM=ln.m-deltaM
    newB=ln.b-deltaB
    return line(newM, newB)

"""
Gets the output according to the line
Parameter input: the input opinionated percentage
Parameter line: the function to feed the input through
Returns: the float result of feeding it through the line
"""

def getOutput(input:float, ln:line):
    return sigmoid(input*ln.m+ln.b)

"""
Prints the cost of a training set
Returns: nothing
"""

def getCost(url, x, y, actual):
    print("Cost of " + url+"[Opinionation percent "+str(x)+"]" + "=" + str((1.0 / 2) * ((y-actual) ** 2)))

"""
Creates a line with an m of .5 and a b of 0
Returns: the default line with an m of .5 and b of 0
"""

def createLine():
    return line(.5, 0)

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
            opinionatedPercent = float(opinionatedRE.group(0))/100
            inputs.append(data(url, opinionatedPercent))

    return inputs, outputs

"""
Trains the AI
Parameter inputs:the inputs to train on
Parameter outputs: the outputs to train on
Returns: a trained line
"""
def train(inputs:list, actual:float, ln:line):
    for i in range(100):
        for iteration in range(len(inputs)):
            output=getOutput(inputs[iteration].opinionation, ln)
            #getCost(inputs[iteration].url, inputs[iteration].opinionation, output, actual[iteration])
            ln=regress(inputs[iteration].opinionation, actual[iteration], output, ln)
    return ln

"""
Gets the result of whether it is opinionated or not
Returns: true if the result is opinionated. False otherwise
"""

def getResult(x, ln:line):
    return getOutput(x, ln)>.5

"""
Serializes a line to a file
ln: a line to serialize
Returns: nothing
"""

def serializeLine(ln:line):
    with open(LINE, 'w') as f:
        f.write(str(ln.m)+"\n"+str(ln.b))

"""
Deserializes a line from a file
Returns: a line from the file
"""

def deserializeLine():
    m=.5
    b=0
    with open(LINE) as f:
        m=float(f.readline())
        b=float(f.readline())
    return line(m, b)

# def showTrainingData(articles, output):
#     opinionated=list()
#     unopinionated=list()
#     for article in range(len(articles)):
#         if(output[article]==1):
#             opinionated.append(articles[article].opinionation)
#         else:
#             unopinionated.append(articles[article].opinionation)
#     y=np.zeros(len(opinionated))
#     pp.plot(opinionated, y, 'bo')
#
#     y=np.zeros(len(unopinionated))
#     pp.plot(unopinionated, y, 'ro')
#
#     pp.show()

"""
The main method
"""

def main():
    if(len(sys.argv)!=2 or (sys.argv[1]!='yes' and sys.argv[1]!='no')):
        print("Error: python3 Linear_Regression -train[yes/no]")

    else:

        # If we want to retrain the linear regression algorithm
        if(sys.argv[1]=="yes"):
            ln=createLine()
            trainingData, outputs=readTrainingFile()
            ln=train(trainingData, outputs, ln)
            #showTrainingData(trainingData, outputs)
            serializeLine(ln)

        ln=deserializeLine()
        inputData = readOutputFile()
        for article in inputData:
            result=getResult(article.opinionation, ln)
            if(result):
                print("OPINIONATED: "+article.url)
            else:
                print("NOT OPINIONATED: "+article.url)

if __name__ == '__main__':
    main()