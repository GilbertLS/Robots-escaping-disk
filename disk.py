import pygame


"""
    This class is used to draw the disk during the simulation
"""
class Disk:
    def __init__(self, radius=250, position=(300,300)):
        self.radius = radius
        self.x = position[0]
        self.y = position[1]

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (int(self.x), int(self.y)), self.radius, 1)
        screen.set_at((int(self.x), int(self.y)), (0,0,0))

    def getOrigin(self):
        return (self.x, self.y)

    def getRadius(self):
        return self.radius
