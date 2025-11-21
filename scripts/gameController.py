
import pygame
from .blackjackController import BlackjackController

# The game controller handles display, blackjack logic, and asset loading
class GameController():

    # CONSTANTS: Unchanging variables that do not rely on anything else
    DISPLAY = {
        "GAME_SIZE" : (640, 360),
        "SCALE" : 2,
        "WINDOW_WIDTH" : 1280, 
        "WINDOW_HEIGHT" : 720,
        "WHITE_COLOR" : (250, 250, 250),
        "BLACK_COLOR" : (20, 20, 20),
        "RED_COLOR" : (210, 30, 45),
        "SHADOW_COLOR" : (0, 0, 0, 90),
        "TABLE_COLOR" : (29, 71, 46)
    }

    CONTROLS = {
        "MOUSE_POSITION" : (0, 0),
        "MOUSE_SCALED_POSITION" : (0, 0),
        "MOUSE_PRESSED" : False
    }

    # INIT: Most variables should be defined here, only constants outside
    def __init__(self):

        # DISPLAY: Initialize the display
        self.surface = pygame.Surface( (self.DISPLAY["GAME_SIZE"][0], self.DISPLAY["GAME_SIZE"][1]) )
        self.scaledSurface = pygame.transform.scale(self.surface, (self.DISPLAY["WINDOW_WIDTH"], self.DISPLAY["WINDOW_HEIGHT"]))
        self.window = pygame.display.set_mode((self.DISPLAY["GAME_SIZE"][0] * self.DISPLAY["SCALE"], self.DISPLAY["GAME_SIZE"][1] * self.DISPLAY["SCALE"]))
        pygame.display.set_caption("Blackjack")

        # ASSETS: Initialize the assets
        self.fontAssets = dict()
        self.imageAssets = dict()
        self.fontAssets["cardFont"] =  pygame.font.Font("assets/fonts/dungeon-mode.ttf", 9)
        self.fontAssets["uiFont"] = pygame.font.Font("assets/fonts/monogram-extended.ttf", 16)
        self.imageAssets["cardBack"] = pygame.image.load("assets/pixelCardback.png").convert_alpha()

        # CONTROLLER: Initialize the blackjack game controller
        self.blackjack = BlackjackController(self.DISPLAY, self.imageAssets["cardBack"])

        # CONTROLS: Reading controls
        # self.mouse = pygame.mouse.get_pos()
        # self.mouseScaled = (self.mouse[0] / self.DISPLAY["SCALE"], self.mouse[1] / self.DISPLAY["SCALE"])
        # self.mousePressed = False

        # FUNCTIONAL: Initializing the clock, booleans, etc.
        self.clock = pygame.time.Clock()
        self.isDebugging = True
        self.isRunning = True
        self.isGamePaused = False

        # ENTITY: Drawables list. This list will be iterated over and every object with a draw() function will be called here
        self.drawables = list()

    # This updates the controls
    def readControls(self):
        
        # Updates game events. Best practice to call it before getting information about controls.
        events = pygame.event.get()

        # Update the mouse position on the screen (scaled)
        self.CONTROLS["MOUSE_POSITION"] = pygame.mouse.get_pos()
        self.CONTROLS["MOUSE_SCALED_POSITION"] = (self.CONTROLS["MOUSE_POSITION"][0] / self.DISPLAY["SCALE"], self.CONTROLS["MOUSE_POSITION"][1] / self.DISPLAY["SCALE"])

        # Check if left mouse button pressed
        self.CONTROLS["MOUSE_PRESSED"] = pygame.mouse.get_pressed()[0]

        # Process events
        for event in events:
            
            if event.type == pygame.QUIT:
                self.isRunning = False
                pygame.quit()
                exit()

    # This is the game logic, updated every frame
    def run(self):
        
        # Lock the game at 60 FPS
        self.clock.tick(60)

        # Update controls status
        self.readControls()

        # Clear background to color
        self.surface.fill( self.DISPLAY["TABLE_COLOR"] )

        # Iterate through the entity list for update functions
        self.blackjack.update(self.CONTROLS)
        self.blackjack.draw(self.surface, self.fontAssets["uiFont"])

        # Iterate through the drawables list
        for object in self.drawables:
            object.draw(self.surface)

        # Draw the scaled surface to the window
        self.scaledSurface = pygame.transform.scale(self.surface, (self.DISPLAY["WINDOW_WIDTH"], self.DISPLAY["WINDOW_HEIGHT"]))
        self.window.blit(self.scaledSurface, (0, 0))

        # Flip the display to put your work on screen
        pygame.display.flip()