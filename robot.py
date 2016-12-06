import pygame
import math
from myMath import *

class Robot:
    def __init__(self, position, startPointOnEdge, travelOnCircleEdge, movesClockWise):
        self.x = position[0]
        self.y = position[1]
        self.movesClockWise = movesClockWise

        if(self.movesClockWise):
            self.color = (0,0,255)
        else:
            self.color = (255,0,0)

        self.startPointOnEdge = startPointOnEdge
        self.reachedEdge = False
        self.travelOnCircleEdge = travelOnCircleEdge
        self.speed = 250 #Amount of pixels moved per second

        """Fix this"""
        self.angle = getAngleBetweenPointsOnCircle((300,300), self.startPointOnEdge, (250+300, 300))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 1)
        screen.set_at((int(self.x), int(self.y)), self.color)

    def update(self, elapsedTime):
        if(not self.reachedEdge):
            """Move robot towards point on edge"""
            self.reachedEdge = self._moveRobotToPoint(self.startPointOnEdge, elapsedTime)

        if(self.reachedEdge):
            """Move robot on circle edge"""
            self._moveRobotOnCircleEdge(elapsedTime);


    def _moveRobotToPoint(self, point, elapsedTime):
        distance = math.sqrt(math.pow(point[0] - self.x, 2) + math.pow(point[1] - self.y, 2));
        directionX = (point[0] - self.x) / distance
        directionY = (point[1] - self.y) / distance

        if(abs(distance) <= self.speed * elapsedTime):
            self.x = point[0];
            self.y = point[1];
            return True

        self.x += directionX * self.speed * elapsedTime
        self.y += directionY * self.speed * elapsedTime

        return False

    def _moveRobotOnCircleEdge(self, elapsedTime):
        origin = (300,300) #fix this
        radius = 250 #fix this

        if(self.movesClockWise):
            self.angle += (self.speed / radius) * elapsedTime
        else:
            self.angle -= (self.speed / radius) * elapsedTime
        self.x = math.cos(self.angle) * radius + origin[0]
        self.y = math.sin(self.angle) * radius + origin[1]
