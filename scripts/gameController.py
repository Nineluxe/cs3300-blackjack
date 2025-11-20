import pygame

# The game controller handles display, game functions, etc.
def GameController():

    # DISPLAY: Window size, colors
    BASE_WIDTH, BASE_HEIGHT = 640, 360
    SCALE = 2
    WINDOW_WIDTH, WINDOW_HEIGHT = BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE
    WHITE = (250, 250, 250)
    BLACK = (20, 20, 20)
    RED = (210, 30, 45)
    SHADOW = (0, 0, 0, 90)
    TABLE = (6, 105, 75)

    # ASSETS: Initialize the assets
    cardFont = pygame.font.Font("assets/fonts/dungeon-mode.ttf", 9)
    uiFont = pygame.font.Font("assets/fonts/monogram-extended.ttf", 16)

    # CONTROLS: Reading controls
    mouse = pygame.mouse.get_pos()
    mouseScaled = (mouse[0] / SCALE, mouse[1] / SCALE)

    # FUNCTIONAL: Initializing the clock, booleans, etc.
    clock = pygame.time.Clock()
    isDebugging = True
    isRunning = True
    isGamePaused = False

    # ENTITY: Drawables list. This list will be iterated over and every object with a draw() function will be called here
    drawables = list()

    # This updates the controls
    def readControls():

        # Update the mouse position on the screen (scaled)
        mouse = pygame.mouse.get_pos()
        mouseScaled = (mouse[0] / SCALE, mouse[1] / SCALE)

    # This is the game logic, updated every frame
    def run():

        # Update controls status
        readControls()

        # Iterate through the entity list for update functions
    

        # Iterate through the drawables list
        for object in drawables:
            object.draw()
