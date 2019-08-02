import pygame

from Definitions import *

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
            self.rect.y += PLAYER_SPEED
            if self.rect.y > DISPLAY_H - PLAYER_HEIGHT:
                self.rect.y = 0
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
            if self.rect.y < 0:
                self.rect.y = DISPLAY_H - PLAYER_HEIGHT
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.rect.x += (2 * PLAYER_SPEED)
            if self.rect.x > DISPLAY_W - PLAYER_WIDTH:
                self.rect.x = 0
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.rect.x -= (2 * PLAYER_SPEED)
            if self.rect.x < 0:
                self.rect.x = DISPLAY_W

    def draw(self):
        """ Draw Player on screen """
        self.screen.blit(self.image, self.rect)

    def update(self, deltaTime):
        """ Update every game loop """
        if self.state == PLAYER_ALIVE:
            self.time_lived += deltaTime
            self.handle_keys()
            self.draw()