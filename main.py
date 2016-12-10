import os, sys, getopt
import math
import random
import pygame
from pygame.locals import *

import myMath
from classes.window import Window
from suppress import suppress_stdout

def calculateTravel(diskPos, radius, r1StartPos, r2StartPos, exitPos, simulate=False):
    """
    Both robots start in the center of disk
    Both robots must travel a distance of radius to reach same point on disk edge
    """
    r1TravelToEdge = radius
    r2TravelToEdge = radius
    pointOnCircleAtAngleZero = myMath.getPointOnCircleEdgeFromAngle(diskPos, radius, 0)
    startPointOnEdge = pointOnCircleAtAngleZero
    r1TravelOnCircleEdge = 0
    r2TravelOnCircleEdge = 0
    whichRobotDidntFindExit = 0
    posOfRobotWhoDidntFindExit = (0,0)

    """
    One or both robots do not start on center position
    Find which robot is closest to edge of circle and find closest point to reach it
    Calculate distance from both robots to point on the edge
    """
    if(r1StartPos != diskPos or r2StartPos != diskPos):
        startPointOnEdge = getClosestPointOnEdge(r1StartPos, r2StartPos, diskPos, radius)
        print('startPointOnEdge:', startPointOnEdge)

        r1TravelToEdge = myMath.getDistanceBetweenTwoPoints(r1StartPos, startPointOnEdge)
        r2TravelToEdge = myMath.getDistanceBetweenTwoPoints(r2StartPos, startPointOnEdge)
        print('r1TravelToEdge:', r1TravelToEdge)
        print('r2TravelToEdge:', r2TravelToEdge)
        print('------------------------------')

    """
    We now need to find which robot will find exit first
    R1 always goes CCW and R2 always goes CW
    CCW is positive and CW is negative
    """
    angleBetweenStartAndEnd = myMath.getAngleBetweenPointsOnCircle(diskPos, startPointOnEdge, exitPos)
    print('angleBetweenStartAndEnd:', math.degrees(angleBetweenStartAndEnd))

    r1Angle = angleBetweenStartAndEnd
    r2Angle = angleBetweenStartAndEnd

    if(r1Angle < 0):
        r1Angle = 2 * math.pi + r1Angle
    if(r2Angle > 0):
        r2Angle = 2 * math.pi - r2Angle
    print('r1Angle:', r1Angle, math.degrees(r1Angle))
    print('r2Angle:', r2Angle, math.degrees(r2Angle))

    r1TravelOnCircleEdge = myMath.getArcLength(r1Angle, radius)
    r2TravelOnCircleEdge = myMath.getArcLength(r2Angle, radius)

    """Robot with shortest travel must find exit first"""
    if(r1TravelOnCircleEdge + r1TravelToEdge <= r2TravelOnCircleEdge + r2TravelToEdge):
        r2TravelOnCircleEdge = r1TravelOnCircleEdge - (r2TravelToEdge - r1TravelToEdge)
        whichRobotDidntFindExit = 2
    else:
        r1TravelOnCircleEdge = r2TravelOnCircleEdge - (r1TravelToEdge - r2TravelToEdge)
        whichRobotDidntFindExit = 1

    if(r1TravelOnCircleEdge < 0):
        r1TravelOnCircleEdge = 0
    if(r2TravelOnCircleEdge < 0):
        r2TravelOnCircleEdge = 0
    print('r1TravelOnCircleEdge:', r1TravelOnCircleEdge)
    print('r2TravelOnCircleEdge:', r2TravelOnCircleEdge)
    print('------------------------------')
    print('whichRobotDidntFindExit:', whichRobotDidntFindExit)

    if(whichRobotDidntFindExit == 1 and r2TravelToEdge + r2TravelOnCircleEdge < r1TravelToEdge):
        r1TravelToEdge = r2TravelToEdge + r2TravelOnCircleEdge
        r1TravelOnCircleEdge = 0
    elif(whichRobotDidntFindExit == 2 and r1TravelToEdge + r1TravelOnCircleEdge < r2TravelToEdge):
        r2TravelToEdge = r1TravelToEdge + r1TravelOnCircleEdge
        r2TravelOnCircleEdge = 0

    """Find position of robot when exit is found by the other robot"""
    if(whichRobotDidntFindExit == 1):
        tempAngle = -1 * myMath.getAngleFromArcLength(r1TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = myMath.getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - myMath.getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    else:
        tempAngle = myMath.getAngleFromArcLength(r2TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = myMath.getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - myMath.getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    print('posOfRobotWhoDidntFindExit:', posOfRobotWhoDidntFindExit)

    """Distance traveled for second robot to exit"""
    travelToEnd = myMath.getDistanceBetweenTwoPoints(posOfRobotWhoDidntFindExit, exitPos)
    print('travelToEnd:', travelToEnd)

    if(whichRobotDidntFindExit == 1):
        totalTravel = r1TravelToEdge + r1TravelOnCircleEdge + travelToEnd
    else:
        totalTravel = r2TravelToEdge + r2TravelOnCircleEdge + travelToEnd

    print('r1Travel:', r1TravelToEdge + r1TravelOnCircleEdge)
    print('r2Travel:', r2TravelToEdge + r2TravelOnCircleEdge)

    if(simulate):
        return(
            startPointOnEdge,
            r1TravelToEdge,
            r2TravelToEdge,
            r1TravelOnCircleEdge,
            r2TravelOnCircleEdge,
            totalTravel
        )
    else:
        return totalTravel


def getClosestPointOnEdge(point1Pos, point2Pos, originPos, radius):
    point1DistanceFromEdge = (radius - myMath.getDistanceBetweenTwoPoints(point1Pos, originPos))
    point2DistanceFromEdge = (radius - myMath.getDistanceBetweenTwoPoints(point2Pos, originPos))
    angleToEdge = 0
    print('Distances from edge of circle', point1DistanceFromEdge, point2DistanceFromEdge)

    """Need to find angle that creates point on edge with shortest distance from closest point"""
    if(point1DistanceFromEdge <= point2DistanceFromEdge):
        angleToEdge = myMath.getAngleBetweenPointsOnCircle(originPos, point1Pos, myMath.getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point1:', angleToEdge, math.degrees(angleToEdge))
    else:
        angleToEdge = myMath.getAngleBetweenPointsOnCircle(originPos, point2Pos, myMath.getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point2:', angleToEdge, math.degrees(angleToEdge))

    return myMath.getPointOnCircleEdgeFromAngle(originPos, radius, angleToEdge)


def randomExit(origin, radius):
    angle = random.random() * math.pi * 2;
    x = math.cos(angle) * radius + origin[0]
    y = math.sin(angle) * radius + origin[1]
    return (x,y)

def randomRPos(origin, radius):
    angle = random.random() * math.pi * 2;
    randomRadius = random.random() * radius;
    x = math.cos(angle) * randomRadius + origin[0]
    y = math.sin(angle) * randomRadius + origin[1]
    return (x,y)

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
        with suppress_stdout():
            data = calculateTravel(diskPos, radius, r1Pos, r2Pos, exitPos, True)
    else:
        data = calculateTravel(diskPos, radius, r1Pos, r2Pos, exitPos, True)

    if(window is not None):
        window.new(radius, r1Pos, r2Pos, exitPos, data[0], data[1], data[2], data[3], data[4])

    return data[5] / radius

def printUsage():
    print('Usage: main.py [ options ... ]')
    print('')
    print('Options')
    print(' -h:             Print this message')
    print(' --nosimulation: Remove simulation of the escape algorithm')
    print(' --scenario:     Which escape scenario to run (default:1) [1,2,3]')
    print(' --iterations:   Number of iterations of the algorithm (default: 1, max: 1000)')

def loop(scenario, iterations, debug, simulate):
    MainWindow = None
    results = []

    if(simulate is True):
        MainWindow = Window()

    for i in range(1, iterations + 1):
        result = setupNew(scenario, MainWindow, debug)
        results.insert(i-1, result)
        print('Iteration ', i, ' Time:\t', result)

        if(simulate is True):
            MainWindow.MainLoop()

    print('-------------------')
    print('Average time over ', iterations, ' iterations: ', sum(results)/iterations)

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
