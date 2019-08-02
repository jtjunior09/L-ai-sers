import pygame
import random

from Definitions import *
from Laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        """ Player constructor """
        self.screen = screen

        self.state = PLAYER_ALIVE

        # Load player "sprite" and resize
        self.image = pygame.image.load(PLAYER_FILE)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        
        self.rect = self.image.get_rect()

        self.time_lived = 0

        self.set_pos(PLAYER_START_X, PLAYER_START_Y)
    
    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def handle_keys(self):
        """ Handles key inputs for movement. Left/Right = 2x speed"""
        key = pygame.key.get_pressed()

        if key[pygame.K_DOWN] or key[pygame.K_s]:
            action = 1
            self.do_action(action)
        if key[pygame.K_UP] or key[pygame.K_w]:
            action = 2
            self.do_action(action)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            action = 3
            self.do_action(action)
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            action = 4
            self.do_action(action)

    def do_action(self, action):
        """ Allows random action (left/right/up/down) to be taken """
        if action == 1:
            self.rect.y += PLAYER_SPEED
            if self.rect.y > DISPLAY_H - PLAYER_HEIGHT:
                self.rect.top = 0
        if action == 2:
            self.rect.y -= PLAYER_SPEED
            if self.rect.y < 0:
                self.rect.bottom = DISPLAY_H
        if action == 3:
            self.rect.x += (2 * PLAYER_SPEED)
            if self.rect.x > DISPLAY_W - PLAYER_WIDTH:
                self.rect.left = 0
        if action == 4:
            self.rect.x -= (2 * PLAYER_SPEED)
            if self.rect.x < 0:
                self.rect.right = DISPLAY_W

    def draw(self):
        """ Draw Player on screen """
        self.screen.blit(self.image, self.rect)

    def check_player_hits(self, lasers):
        """ See if player got hit by laser- dead player if so """
        for laser in lasers:
            if laser.rect.colliderect(self.rect):
                self.state = PLAYER_DEAD
                return

    def update(self, deltaTime):
        """ Update every game loop """
        if self.state == PLAYER_ALIVE:
            self.time_lived += deltaTime
            #self.handle_keys()
            self.do_action(random.randint(0,4))
            self.draw()