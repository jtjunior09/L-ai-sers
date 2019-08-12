import pygame
import random

from Definitions import *
from Laser import LaserGroup
from Player import PlayerGroup


def render_label(title, info, font, x, y, screen):
    """ Renders [title]: [info] to game screen. """
    label = font.render('{}: {}'.format(title, info), 1, BLACK)
    screen.blit(label, (x, y))
    return y # to keep track of where to place next label

def update_text_labels(deltaTime, gameTime, generationCount, generationTime, numAlive, font, screen):
    """ Update game text labels, pass-through function to render_label for each. """
    y = 5
    x = 5
    y_gap = 20
    y = render_label('FPS', round(1000/deltaTime, 2), font, x, y, screen)
    y = render_label('Total Time', round(gameTime/1000, 2), font, x, y + y_gap, screen)
    y = render_label('Generation', generationCount, font, x, y + y_gap, screen)
    y = render_label('Gen Time', round(generationTime/1000, 2), font, x, y + y_gap, screen)
    y = render_label('# Alive', numAlive, font, x, y + y_gap, screen)

def create_laser_list():
    laserList = [ [0] * 2 for i in range(106) ]
    x = 0
    for i in range(100):
        laserList[i][0] = x
        laserList[i][1] = random.randint(0, DISPLAY_H)
        x -= LASER_WIDTH
    laserList[101][0] = DISPLAY_W/2
    laserList[101][1] = DISPLAY_H -20
    
    laserList[102][0] = DISPLAY_W/2
    laserList[102][1] = 20
    laserList[103][0] = DISPLAY_W/2
    laserList[103][1] = DISPLAY_H/random.randint(1,5)
    laserList[104][0] = DISPLAY_W/4
    laserList[104][1] = DISPLAY_H/random.randint(1,5)
    laserList[105][0] = DISPLAY_W/4
    laserList[105][1] = DISPLAY_H/random.randint(1,5)

    return laserList

def run_game():
    """ Game initialization and main event loop. """
    # Initialize pygame engine and get handle to screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption(GAME_TITLE)

    # Get background image and resize to size of the screen
    backgroundImg = pygame.image.load(BG_FILE_PATH)
    backgroundImg = pygame.transform.scale(backgroundImg, SCREEN_SIZE)

    # Set up label once outside of game loop
    labelFont = pygame.font.SysFont(FONT_TYPE, FONT_SIZE, bold=True)

    # Setup clock/counters
    gameClock = pygame.time.Clock()
    deltaTime = 0
    totalTime = 0
    generationTime = 0
    generationCount = 1

    # Create Player
    players = PlayerGroup(screen)

    # Create Laser
    lasers = LaserGroup(screen)
    laserList = create_laser_list()
    lasers.create_initial_lasers(laserList)

    # Game Loop
    isRunning = True
    while isRunning:
        # FPS handling
        deltaTime = gameClock.tick(FPS)
        totalTime += deltaTime
        generationTime += deltaTime

        # Redraw background to remove previous game state from screen
        screen.blit(backgroundImg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
        
        # Update Lasers
        lasers.update(deltaTime)
        
        # Check alive count and evolve if necessary
        numAlive = players.update(deltaTime, lasers.lasers)
        if numAlive == 0:
            lasers.lasers.clear()
            lasers.create_initial_lasers(laserList)
            generationTime = 0
            players.evolve_pop()
            generationCount += 1

        # Update labels
        update_text_labels(deltaTime, totalTime, generationCount, generationTime, numAlive, labelFont, screen)

        pygame.display.update()

if __name__ == '__main__':
    run_game()