import pygame

class Exit:
    def __init__(self, position=(300,300)):
        self.x = position[0]
        self.y = position[1]

    def draw(self, screen):
        pygame.draw.rect(screen, (128,0,128), (int(self.x)-10, int(self.y)-10, 20, 20), 0)
        screen.set_at((int(self.x), int(self.y)), (255,255,255))
