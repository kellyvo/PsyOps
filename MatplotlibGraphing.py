import matplotlib.pyplot as plt
import numpy as np
import random

"""
Graphs by sources. These are the scores of the top 10 news sources
"""

def main():
    resultsTest()

def cnn():
    els = [48.39,50.0,50.0,55.56,51.85,53.57,59.26,50.0,50.0,50.0,55.17,50.0,]
    return sum(els) / len(els)

def fox():
    els = [51.19,]
    return sum(els) / len(els)

def nbc():
    els = [52.34,55.6,51.02, 53.43,55.67,51.96,52.7,53.37,51.22,53.32,53.68,52.69,54.2,53.08,54.17,55.68,]
    return sum(els) / len(els)

def abc():
    els = [54.7, 54.25,52.27,49.81,]
    return sum(els) / len(els)

def bbc():
    els = [53.49,54.08,52.27,54.67,52.72,55.51,54.21,55.28,]
    return sum(els) / len(els)

def theguardian():
    els = [50.72,55.05,57.14,54.98,52.0,52.84,]
    return sum(els) / len(els)

def ap():
    els = [52.66,53.13,56.12,51.95,54.99,56.37,55.36,51.92,]
    return sum(els) / len(els)

def reuters():
    els = [51.6,55.93,54.68,55.68,53.72,54.12,56.48,54.46,53.77,57.45,52.21,]
    return sum(els) / len(els)

def time():
    els = [54.45,54.62, ]
    return sum(els) / len(els)

def cbs():
    els = [52.91, 52.48,]
    return sum(els) / len(els)

# Results graphing
def resultsTest():
    # Mockup code
    #names = ['NBC', 'ABC', 'Fox', 'BBC', 'CNN', 'CBS']
    #values = [random.randint(0,100)/100 for i in range(len(names))]

    names = ['CNN', 'Fox', 'NBC', 'ABC', 'BBC', 'The Guardian', 'AP News', 'Reuters', 'Time', 'CBS']
    values = [cnn(), fox(), nbc(), abc(), bbc(), theguardian(), ap(), reuters(), time(), cbs()]

    namesSorted = [x for _, x in sorted(zip(values, names))]
    valuesSorted = sorted(values)

    fig = plt.figure(figsize=(9, 3))

    plt.scatter(namesSorted, valuesSorted)
    plt.plot(namesSorted, valuesSorted)
    plt.suptitle('Average Scores by Source')
    plt.show()
    fig.savefig('RealResults.png', dpi=fig.dpi)

main()
