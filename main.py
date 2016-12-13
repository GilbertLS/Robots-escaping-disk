import os, sys, getopt
import math
import random
import bisect

import utilities
from classes.window import Window
from calculateTravel import calculateTravel

"""Get a random exit position on circle edge"""
def randomExit(origin, radius):
    angle = random.random() * math.pi * 2;
    x = math.cos(angle) * radius + origin[0]
    y = math.sin(angle) * radius + origin[1]
    return (x,y)

"""Get a random robot position inside circle"""
def randomRPos(origin, radius):
    angle = random.random() * math.pi * 2;
    randomRadius = random.random() * radius;
    x = math.cos(angle) * randomRadius + origin[0]
    y = math.sin(angle) * randomRadius + origin[1]
    return (x,y)

"""Create data needed to calculate execution time and run simulation"""
def setupNew(scenario=1, window=None, debug=False):
    diskPos = (300,300)
    radius  = 250
    r1Pos   = diskPos
    r2Pos   = diskPos
    exitPos = randomExit(diskPos, radius)

    if(scenario == 2):
        if(random.randint(0, 1)):
            r1Pos = randomRPos(diskPos, radius)
        else:
            r2Pos = randomRPos(diskPos, radius)
    elif(scenario == 3):
        r1Pos = randomRPos(diskPos, radius)
        r2Pos = randomRPos(diskPos, radius)

    if(debug is False):
        with utilities.suppress_stdout():
            data = calculateTravel(diskPos, radius, r1Pos, r2Pos, exitPos, True)
    else:
        data = calculateTravel(diskPos, radius, r1Pos, r2Pos, exitPos, True)

    if(window is not None):
        window.new(radius, r1Pos, r2Pos, exitPos, data[0], data[1], data[2], data[3], data[4])

    return data[5] / radius

"""Prints how to use the program"""
def printUsage():
    print('Usage: main.py [ options ... ]')
    print('')
    print('Options')
    print(' -h:             Print this message')
    print(' --nosimulation: Remove simulation of the escape algorithm')
    print(' --scenario:     Which escape scenario to run (default:1) [1,2,3]')
    print(' --iterations:   Number of iterations of the algorithm (default: 1, max: 1000)')

"""Loops through every iteration, running simulation if needed"""
def loop(scenario, iterations, debug, simulate):
    MainWindow = None
    results = []

    if(simulate is True):
        MainWindow = Window()

    for i in range(1, iterations + 1):
        result = setupNew(scenario, MainWindow, debug)
        bisect.insort_left(results, result)
        print('Iteration ', i, ' Time:\t', result)

        if(simulate is True):
            MainWindow.MainLoop()

    print('-------------------')
    print('Performed', iterations, 'iterations of scenario', scenario)
    print('Average time:\t', sum(results)/iterations)
    print('Worst time:\t', results[-1])
    print('-------------------')

"""Gets the arguments from the input and starts the program"""
def main(argv):
    scenario   = 1
    iterations = 1
    debug      = False
    simulate   = True

    try:
        opts, args = getopt.getopt(argv,'h',['help', 'scenario=','nosimulation','iterations=', 'debug'])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printUsage()
            sys.exit()
        elif opt == '--debug':
            debug = True
        elif opt == '--nosimulation':
            simulate = False
        elif opt == '--iterations':
            try:
                iterations = int(arg)
                if(iterations < 1 or iterations > 1000): raise ValueError()
            except ValueError:
                print('Error: --iterations needs an integer (1 to 1000)')
                sys.exit(2)
        elif opt == '--scenario':
            try:
                scenario = int(arg)
                if(scenario < 1 or scenario > 3): raise ValueError()
            except ValueError:
                print('Error: --scenario needs an integer [1,2,3]')
                sys.exit(2)

    loop(scenario, iterations, debug, simulate)

if __name__ == "__main__":
    main(sys.argv[1:])
