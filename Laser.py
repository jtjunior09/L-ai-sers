import pygame
import random

from Definitions import *


class Laser():
    def __init__(self, x, y, screen):
        """ Laser constructor """
        self.screen = screen

        # Basic rectangle for laser
        self.image = pygame.Surface([LASER_WIDTH, LASER_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.set_pos(x, y)
        
        self.remove = False

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def move_laser(self, deltaX, deltaY):
        """ Move laser across screen """
        self.rect.centerx += deltaX
        self.rect.centery += deltaY

    def draw(self):
        """ Draw Player on screen """
        self.screen.blit(self.image, self.rect)

    def check_laser(self):
        """ Check if laser is off screen """
        if self.rect.left > DISPLAY_W:
            self.remove = True
    
    def update(self, deltaTime):
        """ Update every game loop """
        self.move_laser(LASER_SPEED * deltaTime, 0)
        self.check_laser()
        self.draw()

class LaserGroup():
    def __init__(self, screen):
        """ LaserGroup constructor """
        self.screen = screen
        self.lasers = []

    def add_new_lasers(self, x, y):
        """ Add new Laser(s) to the game """
        new_laser = Laser(x, y, self.screen)
        self.lasers.append(new_laser)

    def create_initial_lasers(self, lasers):
        self.lasers = []
        for laser in lasers:
            self.add_new_lasers(laser[0], laser[1])
        """self.add_new_lasers(DISPLAY_W/2, DISPLAY_H -20)
        self.add_new_lasers(DISPLAY_W/2, 20)
        self.add_new_lasers(DISPLAY_W/2, DISPLAY_H/random.randint(1,5))
        self.add_new_lasers(DISPLAY_W/4, DISPLAY_H/random.randint(1,5))
        self.add_new_lasers(DISPLAY_W/4, DISPLAY_H/random.randint(1,5))
        self.add_new_lasers(DISPLAY_W/4, DISPLAY_H/random.randint(1,5))"""

    def update(self, deltaTime):
        """ Update every game loop """        
        #earlyLaserFound = False

        # Update each laser, find out if an early laser exists (one that is still passing left window edge)
        for laser in self.lasers:
            laser.update(deltaTime)
            #if laser.rect.left < 0:
                #earlyLaserFound = True
        
        #self.lasers = [las for las in self.lasers if las.remove == False]

        #if not earlyLaserFound:
           # self.add_new_lasers(-LASER_WIDTH, random.randint(0, DISPLAY_H))
