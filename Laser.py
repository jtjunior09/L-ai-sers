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
        if self.rect.left > DISPLAY_W:
            self.finished = True
    
    def update(self, deltaTime):
        self.move_laser(LASER_SPEED * deltaTime, 0)
        self.check_laser()
        self.draw()
