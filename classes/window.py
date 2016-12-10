import sys
import time
import pygame
from pygame.locals import *
from classes.disk import Disk
from classes.robot import Robot
from classes.exit import Exit

"""
    This class is used for the simulation
    It loops 60 times a second so it can draw and update the simulation
"""
class Window:
    def __init__(self):
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width  = 600
        self.height = 600
        """Create the Screen"""
        self.font   = pygame.font.SysFont("monospace", 20)
        self.screen = pygame.display.set_mode((self.width, self.height))
        """Initialize classes as None"""
        self.disk  = None
        self.r1    = None
        self.r2    = None
        self.exit  = None
        self.clock = None

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

            if(None not in (self.r1, self.r2, self.disk, self.exit, self.clock)):
                if(self.r1.getIsFinished() and self.r2.getIsFinished()):
                    time.sleep(2)
                    return

                self._update()
                self._draw()
