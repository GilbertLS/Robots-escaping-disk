import pygame
import math

class Robot:
    def __init__(self, position, startPointOnEdge, travelOnCircleEdge, color=(0,0,255)):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.startPointOnEdge = startPointOnEdge
        self.reachedEdge = False
        self.travelOnCircleEdge = travelOnCircleEdge
        self.speed = 250

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10, 1)
        screen.set_at((int(self.x), int(self.y)), self.color)

    def update(self, elapsedTime):
        if(not self.reachedEdge):
            """Move robot towards point on edge"""
            self.reachedEdge = self._moveRobotToPoint(self.startPointOnEdge, elapsedTime)


    def _moveRobotToPoint(self, point, elapsedTime):
        distance = math.sqrt(math.pow(point[0] - self.x, 2) + math.pow(point[1] - self.y, 2));
        directionX = (point[0] - self.x) / distance
        directionY = (point[1] - self.y) / distance

        self.x += directionX * self.speed * elapsedTime
        self.y += directionY * self.speed * elapsedTime

        if(abs(distance) <= self.speed * elapsedTime):
            self.x = point[0];
            self.y = point[1];
            return True

        return False
