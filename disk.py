import pygame

class Disk:
    def __init__(self, radius=250, position=(300,300)):
        self.radius = radius
        self.x = position[0]
        self.y = position[1]

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), self.radius, 1)
