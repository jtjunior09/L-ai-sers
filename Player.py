import pygame
import random
import numpy as np

from Definitions import *
from Laser import Laser
from NeuralNetwork import NeuralNetwork


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        """ Player constructor """
        self.screen = screen

        self.state = PLAYER_ALIVE

        # Load player "sprite" and resize
        self.image = pygame.image.load(PLAYER_FILE)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        
        self.rect = self.image.get_rect()

        self.fitness = 0
        self.time_lived = 0

        self.neuralNetwork = NeuralNetwork(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)

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

    def check_player_hits(self, lasers):
        """ See if player got hit by laser- dead player if so """
        for laser in lasers:
            if laser.rect.colliderect(self.rect):
                self.state = PLAYER_DEAD
                return

    def get_nn_inputs(self, lasers):
        """ 
            Gets Neural Network input array. 
            Consists of 8 normalized inputs:
                - closest laser left/right/up/down
                - distance to game window edges
        """
        # Set defaults to higher-than-possible
        closestLeft = 10000
        closestRight = 10000
        closestUp = 10000
        closestDown = 10000

        # Add buffer to player's coordinates so AI can "see" further
        playerXmin = self.rect.left - 2
        playerXmax = self.rect.right + 2
        playerYmin = self.rect.top - 2
        playerYmax = self.rect.bottom + 2

        # Get real distances for each var
        for las in lasers:
            if (las.rect.top >= playerYmin) and (las.rect.bottom <= playerYmax): # laser on same y-axis
                if self.rect.centerx - las.rect.centerx: # laser to left
                    dist = abs(self.rect.left - las.rect.right)
                    if dist < closestLeft:
                        closestLeft = dist
                else: #laser to right
                    dist = abs(las.rect.right - self.rect.right)
                    if dist < closestRight:
                        closestRight = dist
            elif (playerXmin <= las.rect.centerx + LASER_WIDTH/2) and (playerXmax >= las.rect.centerx - LASER_WIDTH/2): # laser on same x-axis
                if self.rect.centery - las.rect.centery >= 0: # las above
                    dist = abs(self.rect.top - las.rect.bottom)
                    if dist < closestUp:
                        closestUp = dist
                else: # las on bottom
                    dist = abs(self.rect.bottom - las.rect.top)
                    if dist < closestDown:
                        closestDown = dist

        # Get distances to game window edges
        distLeftEdge = self.rect.left
        distRightEdge = DISPLAY_W - self.rect.right
        distTopEdge = self.rect.top
        distBottomEdge = DISPLAY_H - self.rect.bottom

        # Create normalized array
        inputsArray = [
            1 - ((closestLeft / DISPLAY_W) * 0.99) + 0.01,
            1 - ((closestRight / DISPLAY_W) * 0.99) + 0.01,
            1 - ((closestUp / DISPLAY_H) * 0.99) + 0.01,
            1 - ((closestDown / DISPLAY_H) * 0.99) + 0.01,
            1 - ((distLeftEdge / DISPLAY_W) * 0.99) + 0.01,
            1 - ((distRightEdge / DISPLAY_W) * 0.99) + 0.01,
            1 - ((distTopEdge / DISPLAY_H) * 0.99) + 0.01,
            1 - ((distBottomEdge / DISPLAY_H) * 0.99) + 0.01
        ]

        return inputsArray

    def get_action_from_nn(self, lasers):
        """ Use the Neural Network to decide how(/if) character should move """
        inputs = self.get_nn_inputs(lasers)
        outputs = self.neuralNetwork.get_outputs(inputs)

        # Do actions dictated by Neural Network if they meet  NNET_DECISION_THRESHOLD
        action = 1
        for output in outputs:
            if output >= NNET_DECISION_THRESHOLD:
                self.do_action(action)
            action += 1

    def draw(self):
        """ Draw Player on screen """
        self.screen.blit(self.image, self.rect)

    def reset(self):
        """ Reset Player to default state """
        self.state = PLAYER_ALIVE
        self.fitness = 0
        self.time_lived = 0
        self.set_pos(PLAYER_START_X, PLAYER_START_Y)

    def update(self, deltaTime, lasers):
        """ Update every game loop """
        if self.state == PLAYER_ALIVE:
            self.time_lived += deltaTime
            #self.handle_keys()
            #self.do_action(random.randint(0,4))
            self.get_action_from_nn(lasers)
            self.check_player_hits(lasers)
            self.draw()

    def create_offspring(p_1, p_2, screen):
        """ Static function to generate offspring given two parent Players """
        newPlayer = Player(screen)
        newPlayer.neuralNetwork.create_offspring(p_1.neuralNetwork, p_2.neuralNetwork)

        return newPlayer

class PlayerGroup():
    def __init__(self, screen):
        """ PlayerGroup constructor. Handles a generation """
        self.screen = screen
        self.players = []
        self.create_new_generation()

    def create_new_generation(self):
        """ Create a new generation of #[GENERATION_POP] Players """
        self.players = []
        for i in range(0, GENERATION_POP):
            self.players.append(Player(self.screen))
    
    def evolve_pop(self):
        """ Evolve the population by "mating" best players, selecting random bad players, and creating new ones """
        for player in self.players:
            player.fitness += player.time_lived        

        # Sort by fitness, best at beginning of Array
        self.players.sort(key=lambda x:x.fitness, reverse=True)

        # Get number of good Players to save
        cutOff = int(len(self.players) * MUTATION_THRESHOLD)
        goodPlayers = self.players[0:cutOff]
        
        # Gotta hold onto bad players to mix them up- add diversity to pool
        badPlayers = self.players[cutOff:]
        numBadToTake = int(len(self.players) * MUTATION_BAD_KEEP)
        for player in badPlayers:
            player.neuralNetwork.modify_weights()

        newPlayers = []

        # Generate array of random indices to take random baddies
        randArray_bad = np.random.choice(np.arange(len(badPlayers)), numBadToTake, replace=False)
        for index in randArray_bad:
            newPlayers.append(badPlayers[index])
        
        # Add the good players and refill global player array via breeding
        newPlayers.extend(goodPlayers)
        while len(newPlayers) < len(self.players):
            # Breed two good players
            randArray_breed = np.random.choice(np.arange(len(goodPlayers)), 2, replace=False)
            newPlayer = Player.create_offspring(goodPlayers[randArray_breed[0]], goodPlayers[randArray_breed[1]], self.screen)
            
            # Randomly modify their weights if threshold not met
            if random.random() < MUTATION_MODIFY_CHANCE:
                newPlayer.neuralNetwork.modify_weights()
            newPlayers.append(newPlayer)
        
        for player in newPlayers:
            player.reset()

        self.players = newPlayers

    def update(self, deltaTime, lasers):
        """ Update all Players every game loop """
        numAlive = 0

        for player in self.players:
            player.update(deltaTime, lasers)
            if player.state == PLAYER_ALIVE:
                numAlive += 1
        
        return numAlive
