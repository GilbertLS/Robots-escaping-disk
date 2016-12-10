import pygame
import math
from myMath import *

class Robot:
    def __init__(self, disk, position, exitPos, startPointOnEdge, travelToEdge, travelOnCircleEdge, movesClockWise):
        self.speed = 125 #Amount of pixels moved per second
        self.reachedEdge  = False
        self.reachedAngle = False
        self.reachedExit  = False
        self.distanceTravelled = 0

        self.origin = disk.getOrigin()
        self.radius = disk.getRadius()
        self.x = position[0]
        self.y = position[1]
        self.exitPos = exitPos
        self.movesClockWise = movesClockWise
        self.travelOnCircleEdge = travelOnCircleEdge

        """Need to recalculate this in case exit is found before robot reaches circle edge"""
        self.startPointOnEdge = getPointBetweenTwoPoints((self.x, self.y), startPointOnEdge, travelToEdge)

        self.angleOnCircleEdge = getAngleFromArcLength(self.travelOnCircleEdge, self.radius)
        self.angle = getAngleBetweenPointsOnCircle(self.origin, (self.origin[0] + self.radius, self.origin[1]), self.startPointOnEdge)

        if(self.movesClockWise):
            self.angleOnCircleEdge = self.angle - self.angleOnCircleEdge
            self.color = (0,0,255)
        else:
            self.angleOnCircleEdge = self.angle + self.angleOnCircleEdge
            self.color = (255,0,0)

    def draw(self, screen, font):
        if(self.reachedExit):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 0)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 1)
        screen.set_at((int(self.x), int(self.y)), self.color)
        text = font.render(str(self.distanceTravelled), 1, self.color)

        if(self.movesClockWise):
            screen.blit(text, (400, 20))
        else:
            screen.blit(text, (400, 40))

    def update(self, elapsedTime):
        """Move robot towards point on edge"""
        if(not self.reachedEdge):
            self.reachedEdge = self._moveRobotToStartPointOnEdge(elapsedTime)

        """If other robot finds exit first, skip circle edge movement"""
        if(self.reachedEdge and self.travelOnCircleEdge == 0):
            self.reachedAngle = True

        """Move robot on circle edge"""
        if(self.reachedEdge and not self.reachedAngle):
            self.reachedAngle = self._moveRobotOnCircleEdge(elapsedTime);

        """Move robot to exit"""
        if(self.reachedAngle and not self.reachedExit):
            self.reachedExit = self._moveRobotToExitPoint(elapsedTime)

    def _moveRobotToStartPointOnEdge(self, elapsedTime):
        point    = self.startPointOnEdge
        distance = getDistanceBetweenTwoPoints(point, (self.x, self.y))

        return self._moveRobotToPoint(point, distance, elapsedTime)

    def _moveRobotToExitPoint(self, elapsedTime):
        point    = self.exitPos
        distance = getDistanceBetweenTwoPoints(point, (self.x, self.y))

        return self._moveRobotToPoint(point, distance, elapsedTime)

    def _moveRobotToPoint(self, point, distance, elapsedTime):
        oldX = self.x
        oldY = self.y

        if(distance == 0):
            return True
        elif(abs(distance) <= self.speed * elapsedTime):
            self.x = point[0];
            self.y = point[1];

            self.distanceTravelled += getDistanceBetweenTwoPoints((self.x, self.y), (oldX, oldY))

            return True
        else:
            directionX = (point[0] - self.x) / distance
            directionY = (point[1] - self.y) / distance

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
