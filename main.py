import os, sys
import math
import random
import pygame
from pygame.locals import *

"""Import classes needed for simulation"""
from disk import Disk
from robot import Robot
from exit import Exit
from myMath import *

def calcData(diskPos, radius, r1StartPos, r2StartPos, exitPos, verbose=False):
    """
    Both robots start in the center of disk
    Both robots must travel a distance of radius to reach same point on disk edge
    """
    r1TravelToEdge = radius
    r2TravelToEdge = radius
    pointOnCircleAtAngleZero = getPointOnCircleEdgeFromAngle(diskPos, radius, 0)
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

        r1TravelToEdge = getDistanceBetweenTwoPoints(r1StartPos, startPointOnEdge)
        r2TravelToEdge = getDistanceBetweenTwoPoints(r2StartPos, startPointOnEdge)
        print('r1TravelToEdge:', r1TravelToEdge)
        print('r2TravelToEdge:', r2TravelToEdge)
        print('------------------------------')

    """
    We now need to find which robot will find exit first
    R1 always goes CCW and R2 always goes CW
    CCW is positive and CW is negative
    """
    angleBetweenStartAndEnd = getAngleBetweenPointsOnCircle(diskPos, startPointOnEdge, exitPos)
    print('angleBetweenStartAndEnd:', math.degrees(angleBetweenStartAndEnd))

    r1Angle = angleBetweenStartAndEnd
    r2Angle = angleBetweenStartAndEnd

    if(r1Angle < 0):
        r1Angle = 2 * math.pi + r1Angle
    if(r2Angle > 0):
        r2Angle = 2 * math.pi - r2Angle
    print('r1Angle:', r1Angle, math.degrees(r1Angle))
    print('r2Angle:', r2Angle, math.degrees(r2Angle))

    r1TravelOnCircleEdge = getArcLength(r1Angle, radius)
    r2TravelOnCircleEdge = getArcLength(r2Angle, radius)

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
        tempAngle = -1 * getAngleFromArcLength(r1TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    else:
        tempAngle = getAngleFromArcLength(r2TravelOnCircleEdge, radius)
        posOfRobotWhoDidntFindExit = getPointOnCircleEdgeFromAngle(diskPos, radius, tempAngle - getAngleBetweenPointsOnCircle(diskPos, pointOnCircleAtAngleZero, startPointOnEdge))
    print('posOfRobotWhoDidntFindExit:', posOfRobotWhoDidntFindExit)

    """Distance traveled for second robot to exit"""
    travelToEnd = getDistanceBetweenTwoPoints(posOfRobotWhoDidntFindExit, exitPos)
    print('travelToEnd:', travelToEnd)

    if(whichRobotDidntFindExit == 1):
        totalTravel = r1TravelToEdge + r1TravelOnCircleEdge + travelToEnd
    else:
        totalTravel = r2TravelToEdge + r2TravelOnCircleEdge + travelToEnd

    print('r1Travel:', r1TravelToEdge + r1TravelOnCircleEdge)
    print('r2Travel:', r2TravelToEdge + r2TravelOnCircleEdge)

    if(verbose):
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
    point1DistanceFromEdge = (radius - getDistanceBetweenTwoPoints(point1Pos, originPos))
    point2DistanceFromEdge = (radius - getDistanceBetweenTwoPoints(point2Pos, originPos))
    angleToEdge = 0
    print('Distances from edge of circle', point1DistanceFromEdge, point2DistanceFromEdge)

    """Need to find angle that creates point on edge with shortest distance from closest point"""
    if(point1DistanceFromEdge <= point2DistanceFromEdge):
        angleToEdge = getAngleBetweenPointsOnCircle(originPos, point1Pos, getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point1:', angleToEdge, math.degrees(angleToEdge))
    else:
        angleToEdge = getAngleBetweenPointsOnCircle(originPos, point2Pos, getPointOnCircleEdgeFromAngle(originPos, radius, 0))
        print('angleToEdge point2:', angleToEdge, math.degrees(angleToEdge))

    return getPointOnCircleEdgeFromAngle(originPos, radius, angleToEdge)


"""This class handles the main initialization"""
class Main:
    def __init__(self):
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = 600
        self.height = 600
        """Create the Screen"""
        self.font = pygame.font.SysFont("monospace", 20)
        self.screen = pygame.display.set_mode((self.width, self.height))

    def new(self, radius, r1StartPos, r2StartPos, exitPos,
           startPointOnEdge, r1TravelToEdge, r2TravelToEdge,
           r1TravelOnCircleEdge, r2TravelOnCircleEdge):
        """Create our classes"""
        self.disk  = Disk(radius, (300,300))
        self.r1    = Robot(self.disk, r1StartPos, exitPos, startPointOnEdge, r1TravelToEdge, r1TravelOnCircleEdge, False)
        self.r2    = Robot(self.disk, r2StartPos, exitPos, startPointOnEdge, r2TravelToEdge, r2TravelOnCircleEdge, True)
        self.exit  = Exit(exitPos)
        self.clock = pygame.time.Clock()

    def _draw(self):
        self.screen.fill(pygame.Color(255,255,255))

        self.disk.draw(self.screen)
        self.exit.draw(self.screen)
        self.r1.draw(self.screen, self.font)
        self.r2.draw(self.screen, self.font)

        pygame.display.update()

    def _update(self):
        elapsedTime = self.clock.tick_busy_loop(60)/1000 #Seconds since last update
        self.r1.update(elapsedTime)
        self.r2.update(elapsedTime)

    def MainLoop(self):
        """This is the Main Draw Loop"""
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self._update()
            self._draw()

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

if __name__ == "__main__":
    diskPos = (300,300)
    radius = 250

    r1Pos = (300, 300)
    r2Pos = (300, 300)
    exitPos = randomExit(diskPos, 250)

    r1Pos = randomRPos(diskPos, radius)
    r2Pos = randomRPos(diskPos, radius)
    exitPos = randomExit(diskPos, radius)

    data = calcData(diskPos, radius, r1Pos, r2Pos, exitPos, True)
    print(data)
    MainWindow = Main()
    MainWindow.new(radius, r1Pos, r2Pos, exitPos, data[0], data[1], data[2], data[3], data[4])
    MainWindow.MainLoop()
