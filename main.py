
import pygame
from scripts.gameController import GameController

# FILE DESCRIPTION: This is the main entry point of the program. Keep this as sparse as possible by abstracting most
# components of the game design into separate files and classes.

# INITIALIZE: Initialize the game controller and pygame functions
pygame.init()
pygame.font.init()
game = GameController()
game.initialize()

# UPDATE: Called every frame
while (game.isRunning):
    game.run()

# CONTROL: End the program
pygame.quit()