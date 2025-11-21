
import pygame

# The game controller handles display, blackjack logic, and asset loading
class GameController():

    # CONSTANTS: Unchanging variables that do not rely on anything else
    BASE_WIDTH, BASE_HEIGHT = 640, 360
    SCALE = 2
    WINDOW_WIDTH, WINDOW_HEIGHT = BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE
    WHITE_COLOR = (250, 250, 250)
    BLACK_COLOR = (20, 20, 20)
    RED_COLOR = (210, 30, 45)
    SHADOW_COLOR = (0, 0, 0, 90)
    TABLE_COLOR = (29, 71, 46)

    # INIT: Anything that requires other context needs to be initialized here
    def __init__(self):

        # DISPLAY: Initialize the display
        self.surface = pygame.Surface( (self.BASE_WIDTH, self.BASE_HEIGHT) )
        self.scaledSurface = pygame.transform.scale(self.surface, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.window = pygame.display.set_mode((self.BASE_WIDTH * self.SCALE, self.BASE_HEIGHT * self.SCALE))
        pygame.display.set_caption("Blackjack")

        # CONTROLS: Reading controls
        self.mouse = pygame.mouse.get_pos()
        self.mouseScaled = (self.mouse[0] / self.SCALE, self.mouse[1] / self.SCALE)
        self.mousePressed = False

        # FUNCTIONAL: Initializing the clock, booleans, etc.
        self.clock = pygame.time.Clock()
        self.isDebugging = True
        self.isRunning = True
        self.isGamePaused = False
        self.mouse = tuple
        self.mouseScaled = tuple
        self.mousePressed = bool    

        # ASSETS: Initialize the assets
        self.fontAssets = dict()
        self.imageAssets = dict()

        # ENTITY: Drawables list. This list will be iterated over and every object with a draw() function will be called here
        self.drawables = list()

        # GAME LOGIC: Blackjack game logic information
        self.cardFaces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cardSuits = ['♠', '♣', '♥', '♦']
        self.cardWidth = 60
        self.cardHeight = 100






    # Call once when the object is created
    def initialize(self):

        self.fontAssets["cardFont"] =  pygame.font.Font("assets/fonts/dungeon-mode.ttf", 9)
        self.fontAssets["uiFont"] = pygame.font.Font("assets/fonts/monogram-extended.ttf", 16)
        self.imageAssets["cardBack"] = pygame.image.load("assets/pixelCardback.png")

    # This updates the controls
    def readControls(self):
        
        # Updates game events. Best practice to call it before getting information about controls.
        events = pygame.event.get()

        # Update the mouse position on the screen (scaled)
        self.mouse = pygame.mouse.get_pos()
        self.mouseScaled = (self.mouse[0] / self.SCALE, self.mouse[1] / self.SCALE)

        # Check if left mouse button pressed
        self.mousePressed = pygame.mouse.get_pressed()[0]

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
        self.surface.fill( self.TABLE_COLOR )

        # Iterate through the entity list for update functions

        # Iterate through the drawables list
        for object in self.drawables:
            object.draw(self.surface)

        # Draw the scaled surface to the window
        self.scaledSurface = pygame.transform.scale(self.surface, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.window.blit(self.scaledSurface, (0, 0))

        # Flip the display to put your work on screen
        pygame.display.flip()