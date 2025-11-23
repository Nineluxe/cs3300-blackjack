
import pygame
from scripts.gameController import GameController

# FILE DESCRIPTION: This is the main entry point of the program. Keep this as sparse as possible by abstracting most
# components of the game design into separate files and classes.

# TODO: Fix the issue with calculating score. When we add a face card, the score is not updated properly. Could be an issue with how aces are handled, though.

# INITIALIZE: Initialize the game controller and pygame functions
pygame.init()
pygame.font.init()
game = GameController()

# UPDATE: Called every frame
while (game.isRunning):
    game.run()

# CONTROL: End the program
pygame.quit()