
import pygame
from .blackjackController import BlackjackController
from .button import Button
from .general import *

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
        "MOUSE_PRESSED" : False,
        "MOUSE_PRESSED_ONCE" : False
    }

    INSTRUCTIONS = [
        "Goal: Get as close to 21 as possible without going over. Beat the dealer's hand.",
        "",
        "Card Values:",
        "Number cards = face value",
        "Face cards (J, Q, K) = 10",
        "Aces = 1 or 11 (whichever helps you more)",
        "",
        "Gameplay:",
        "You and the dealer each start with 2 cards",
        "Click the deck to draw another card (hit)",
        "Keep drawing until you're satisfied with your total, then stand",
        "If you go over 21, you lose immediately (bust)",
        "Whoever is closest to 21 without going over wins",
        "",
        "That's it! Click the deck to hit, and try to beat the dealer without going over."
    ]

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

        # ENTITY: Drawables list. This list will be iterated over and every object with a draw() function will be called here
        self.drawables = list()

        # UI: Initialize the main menu buttons
        self.gameStates = ("MAIN_MENU", "BLACKJACK_GAME", "HOW_TO_PLAY")
        self.currentGameState = self.gameStates[0]
        self.startGameButtonPosition = (self.DISPLAY["GAME_SIZE"][0] // 2 - 50, self.DISPLAY["GAME_SIZE"][1] // 2 - 30)
        self.howToPlayButtonPosition = (self.DISPLAY["GAME_SIZE"][0] // 2 - 50, self.DISPLAY["GAME_SIZE"][1] // 2 + 30)
        self.doInitializeState = True
        self.startGameButton = Button( self.startGameButtonPosition[0], self.startGameButtonPosition[1], 100, 40, self.DISPLAY["BLACK_COLOR"], "Start Game", self.fontAssets["uiFont"] )
        self.howToPlayButton = Button( self.howToPlayButtonPosition[0], self.howToPlayButtonPosition[1], 100, 40, self.DISPLAY["BLACK_COLOR"], "How to Play", self.fontAssets["uiFont"] )
        self.backButton = Button(self.DISPLAY["GAME_SIZE"][0] // 2 - 50, self.DISPLAY["GAME_SIZE"][1] - 50, 100, 40, self.DISPLAY["BLACK_COLOR"], "Back", self.fontAssets["uiFont"])
        self.startGameButton.doDraw = False
        self.startGameButton.disabled = True
        self.howToPlayButton.doDraw = False
        self.howToPlayButton.disabled = True
        self.backButton.doDraw = False
        self.backButton.disabled = True

        # CONTROLLER: Initialize the blackjack game controller
        self.blackjack = None

        # FUNCTIONAL: Initializing the clock, booleans, etc.
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.isDebugging = True
        self.isRunning = True
        self.isGamePaused = False

    # Call this when you're ready to start the blackjack game
    def startBlackjack(self):
        self.blackjack = BlackjackController(self.DISPLAY, self.CONTROLS, self.imageAssets, self.fontAssets)

    # This updates the controls
    def readControls(self):
        
        # Updates game events. Best practice to call it before getting information about controls.
        events = pygame.event.get()

        # Get current mouse button state
        currentMousePressed = pygame.mouse.get_pressed()[0]

        # Update MOUSE_PRESSED (continuous held state)
        self.CONTROLS["MOUSE_PRESSED"] = currentMousePressed

        # Only True if currently pressed AND was not pressed last frame
        if currentMousePressed and not self.CONTROLS.get("MOUSE_WAS_PRESSED", False):
            self.CONTROLS["MOUSE_PRESSED_ONCE"] = True
        else:
            self.CONTROLS["MOUSE_PRESSED_ONCE"] = False

        # Store current state for next frame
        self.CONTROLS["MOUSE_WAS_PRESSED"] = currentMousePressed

        # Update mouse position
        mouseX, mouseY = pygame.mouse.get_pos()
        self.CONTROLS["MOUSE_POSITION"] = (mouseX, mouseY)
        self.CONTROLS["MOUSE_SCALED_POSITION"] = (mouseX // self.DISPLAY["SCALE"], mouseY // self.DISPLAY["SCALE"])

        # Process events
        for event in events:
            
            if event.type == pygame.QUIT:
                self.isRunning = False
                pygame.quit()
                exit()

    # This is the game logic, updated every frame
    def run(self):
        
        # Lock the game at 60 FPS
        self.dt = self.clock.tick(60) / 1000.0

        # Update controls status
        self.readControls()

        # Clear background to color
        self.surface.fill( self.DISPLAY["TABLE_COLOR"] )

        match self.currentGameState:

            case "MAIN_MENU":

                # Initialize the main menu if needed
                if self.doInitializeState:
                    self.doInitializeState = False

                    self.blackjack = None
                    self.startGameButton.doDraw = True
                    self.howToPlayButton.doDraw = True
                    self.startGameButton.disabled = False
                    self.howToPlayButton.disabled = False
                    self.drawables.append(self.startGameButton)
                    self.drawables.append(self.howToPlayButton)

                # Update buttons
                if self.startGameButton.isMouseOver(self.CONTROLS["MOUSE_SCALED_POSITION"]) and self.CONTROLS["MOUSE_PRESSED_ONCE"]:
                    self.doInitializeState = True

                    self.currentGameState = "BLACKJACK_GAME"
                    self.drawables.clear()
                    self.startGameButton.doDraw = False
                    self.howToPlayButton.doDraw = False
                    self.startGameButton.disabled = True
                    self.howToPlayButton.doDraw = True

                if self.howToPlayButton.isMouseOver(self.CONTROLS["MOUSE_SCALED_POSITION"]) and self.CONTROLS["MOUSE_PRESSED_ONCE"]:
                    self.doInitializeState = True
                    self.drawables.clear()
                    self.currentGameState = "HOW_TO_PLAY"

            case "BLACKJACK_GAME":

                # Initialize the blackjack game if needed
                if self.doInitializeState:
                    self.startBlackjack()
                    self.doInitializeState = False
                
                # Update the blackjack game object
                if self.blackjack is not None:
                    self.blackjack.update(self.CONTROLS, self.dt)
                    self.blackjack.draw(self.surface)

                    if self.blackjack.isQuitting:
                        self.doInitializeState = True
                        self.blackjack = None
                        self.currentGameState = "MAIN_MENU"
                        self.drawables.clear()

            case "HOW_TO_PLAY":
                
                # Enable the back button
                if self.doInitializeState:
                    self.doInitializeState = False
                    self.backButton.disabled = False
                    self.backButton.doDraw = True
                    self.drawables.append(self.backButton)

                # Back button functionality
                if self.backButton.isMouseOver(self.CONTROLS["MOUSE_SCALED_POSITION"]) and self.CONTROLS["MOUSE_PRESSED_ONCE"]:
                    self.doInitializeState = True
                    self.backButton.disabled = True
                    self.backButton.doDraw = False
                    self.drawables.clear()
                    self.currentGameState = "MAIN_MENU"

                # Draw the HOW TO PLAY text
                textCoordinateStart = (self.DISPLAY["GAME_SIZE"][0] // 2, 10)
                textYSeparation = 10
                drawText(textCoordinateStart , "HOW TO PLAY", self.fontAssets["uiFont"], self.DISPLAY["WHITE_COLOR"], self.surface, "center")

                for index, value in enumerate(self.INSTRUCTIONS):
                    textCoordinates = (textCoordinateStart[0], textCoordinateStart[1] + (index + 2) * textYSeparation)
                    drawText(textCoordinates, self.INSTRUCTIONS[index], self.fontAssets["uiFont"], self.DISPLAY["WHITE_COLOR"], self.surface, "center")

        # Iterate through the drawables list
        for object in self.drawables:
            object.draw(self.surface, self.CONTROLS["MOUSE_SCALED_POSITION"])

        # Draw the scaled surface to the window
        self.scaledSurface = pygame.transform.scale(self.surface, (self.DISPLAY["WINDOW_WIDTH"], self.DISPLAY["WINDOW_HEIGHT"]))
        self.window.blit(self.scaledSurface, (0, 0))

        # Flip the display to put your work on screen
        pygame.display.flip()