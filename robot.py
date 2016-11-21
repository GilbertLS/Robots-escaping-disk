import pygame

class Robot:
    def __init__(self, position, startPointOnEdge, travelOnCircleEdge, color=(0,0,255)):
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.startPointOnEdge = startPointOnEdge
        self.travelOnCircleEdge = travelOnCircleEdge

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10, 1)
        screen.set_at((self.x, self.y), self.color)
