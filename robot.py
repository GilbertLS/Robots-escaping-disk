import pygame
import math
from myMath import *

class Robot:
    def __init__(self, position, exitPos, startPointOnEdge, travelOnCircleEdge, movesClockWise):
        self.x = position[0]
        self.y = position[1]
        self.exitPos = exitPos
        self.movesClockWise = movesClockWise
        self.startPointOnEdge = startPointOnEdge
        self.speed = 125 #Amount of pixels moved per second

        """Fix this"""
        self.radius = 250
        self.origin = (300,300)

        self.reachedEdge  = False
        self.reachedAngle = False
        self.reachedExit  = False
        self.distanceTravelled = 0

        self.angleOnCircleEdge = getAngleFromArcLength(travelOnCircleEdge, self.radius)
        self.angle = getAngleBetweenPointsOnCircle(self.origin, (self.origin[0] + self.radius, self.origin[1]), self.startPointOnEdge)

        if(self.movesClockWise):
            self.angleOnCircleEdge = self.angle - self.angleOnCircleEdge
            self.color = (0,0,255)
        else:
            self.angleOnCircleEdge = self.angle + self.angleOnCircleEdge
            self.color = (255,0,0)

        print(self.movesClockWise, math.degrees(self.angle), math.degrees(self.angleOnCircleEdge))

    def draw(self, screen, font):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 1)
        screen.set_at((int(self.x), int(self.y)), self.color)
        text = font.render(str(self.distanceTravelled), 1, self.color)

        if(self.movesClockWise):
            screen.blit(text, (400, 20))
        else:
            screen.blit(text, (400, 40))

    def update(self, elapsedTime):
        if(not self.reachedEdge):
            """Move robot towards point on edge"""
            self.reachedEdge = self._moveRobotToPoint(self.startPointOnEdge, elapsedTime)

        if(self.reachedEdge and not self.reachedAngle):
            """Move robot on circle edge"""
            self.reachedAngle = self._moveRobotOnCircleEdge(elapsedTime);

        if(self.reachedAngle and not self.reachedExit):
            self.reachedExit = self._moveRobotToPoint(self.exitPos, elapsedTime)


    def _moveRobotToPoint(self, point, elapsedTime):
        distance = math.sqrt(math.pow(point[0] - self.x, 2) + math.pow(point[1] - self.y, 2));

        if(abs(distance) == 0):
            return True;

        directionX = (point[0] - self.x) / distance
        directionY = (point[1] - self.y) / distance

        if(abs(distance) <= self.speed * elapsedTime):
            self.x = point[0];
            self.y = point[1];
            return True

        oldX = self.x
        oldY = self.y

        self.x += directionX * self.speed * elapsedTime
        self.y += directionY * self.speed * elapsedTime

        self.distanceTravelled += getDistanceBetweenTwoPoints((self.x, self.y), (oldX, oldY))

        return False

    def _moveRobotOnCircleEdge(self, elapsedTime):
        angleThatWillBeMoved = (self.speed / self.radius) * elapsedTime

        if(abs(self.angle - self.angleOnCircleEdge) <= angleThatWillBeMoved):
            self.angle = self.angleOnCircleEdge
        elif(self.movesClockWise):
            self.angle -= angleThatWillBeMoved
        else:
            self.angle += angleThatWillBeMoved

        self.x = math.cos(self.angle) * self.radius + self.origin[0]
        self.y = -1 * math.sin(self.angle) * self.radius + self.origin[1] #negate because y goes down

        self.distanceTravelled += getArcLength(angleThatWillBeMoved, self.radius)

        return (self.angle == self.angleOnCircleEdge)
