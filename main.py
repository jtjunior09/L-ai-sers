import pygame
from Definitions import *

def render_label(title, info, font, x, y, screen):
    """ Renders [title]: [info] to game screen. """
    label = font.render('{}: {}'.format(title, info), 1, BLACK)
    screen.blit(label, (x, y))
    return y # to keep track of where to place next label

def update_text_labels(deltaTime, gameTime, font, screen):
    """ Update game text labels, pass-through function to render_label for each. """
    y = 5
    x = 5
    y_gap = 20
    y = render_label('FPS', round(1000/deltaTime, 2), font, x, y, screen)
    y = render_label('Game Time', round(gameTime/1000, 2), font, x, y + y_gap, screen)

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
    gameTime = 0

    # Game Loop
    isRunning = True
    while isRunning:
        # FPS handling
        deltaTime = gameClock.tick(FPS)
        gameTime += deltaTime

        # Redraw background to remove previous game state from screen
        screen.blit(backgroundImg, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
        

        # Update labels
        update_text_labels(deltaTime, gameTime, labelFont, screen)

        pygame.display.update()

if __name__ == '__main__':
    run_game()