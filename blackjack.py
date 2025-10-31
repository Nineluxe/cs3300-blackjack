
import pygame
import math
import random

# Define constants
BASE_WIDTH, BASE_HEIGHT = 640, 360
SCALE = 2
WINDOW_WIDTH, WINDOW_HEIGHT = BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE

#################### INITIALIZATION ####################
pygame.init()
clock = pygame.time.Clock()
entityList = list()
pygame.font.init()

fontSize = 9
font = pygame.font.Font("assets/fonts/dungeon-mode.ttf", fontSize)  # None = default system font, 24 = size

debugging = False

# Create surfaces
base_surface = pygame.Surface( (BASE_WIDTH, BASE_HEIGHT) )
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Super Blackjack 9000")

###################### COLORS ####################
WHITE = (250, 250, 250)
BLACK = (20, 20, 20)
RED = (210, 30, 45)
SHADOW = (0, 0, 0, 90)
TABLE = (6, 105, 75)

###################### SHAPES ####################


###################### CARD CLASS ####################
class Card:

    ###### INITIALIZATION ######
    def __init__(self, x, y, w=60, h=100, faceText="A", suitChar="♥",
                 fillColor=WHITE, borderColor=BLACK, borderWidth=2, cornerRadius=2):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.faceText = faceText
        self.suitChar = suitChar
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.cornerRadius = cornerRadius

        # font sizes relative to card height
        #self.rankFont = font #pygame.font.SysFont(None, max(18, h // 5))
        #self.suitFont = font #pygame.font.SysFont(None, max(18, h // 5))

    ###### DRAW METHOD ######
    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # shadow
        shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(shadowSurf, SHADOW, shadowSurf.get_rect(), border_radius=self.cornerRadius)
        surface.blit(shadowSurf, (self.x + 6, self.y + 6))

        # fill
        pygame.draw.rect(surface, self.fillColor, rect, border_radius=self.cornerRadius)
        # border
        pygame.draw.rect(surface, self.borderColor, rect, width=self.borderWidth, border_radius=self.cornerRadius)

        # corner pips (rank + suit)
        rankColor = RED if self.suitChar in ("♥", "♦") else BLACK
        rankText = font.render(self.faceText, False, rankColor)
        suitText = font.render(self.suitChar, False, rankColor)
        surface.blit(rankText, (self.x + 8, self.y + 6))
        surface.blit(suitText, (self.x + 8, self.y + 8 + rankText.get_height()))

        # big center suit
        centerSuit = font.render(self.suitChar, False, rankColor)
        surface.blit(centerSuit, centerSuit.get_rect(center=rect.center))

        # tiny rotated corner (optional flair)
        #smallRank = pygame.transform.rotate(rankText, 180)
        #smallSuit = pygame.transform.rotate(suitText, 180)
        #surface.blit(smallRank, (self.x + self.w - 8 - smallRank.get_width(),
                                 #self.y + self.h - 6 - smallRank.get_height() - smallSuit.get_height()))
        #surface.blit(smallSuit, (self.x + self.w - 8 - smallSuit.get_width(),
                                 #self.y + self.h - 6 - smallSuit.get_height()))

###################### CREATE CARDS ####################
cards = [
    Card(40, 20, faceText="A", suitChar="♥")
]

#################### MAIN LOOP ####################
running = True
game_paused = False
while running:
    
    ###### CONTROLS ######
    for event in pygame.event.get():

        # Controls: Change size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                fontSize += 1
                font = pygame.font.Font("assets/fonts/dungeon-mode-inverted.ttf", fontSize)
                print("Font size:", fontSize)
            elif event.key == pygame.K_DOWN:
                fontSize = max(1, fontSize - 1)
                font = pygame.font.Font("assets/fonts/dungeon-mode-inverted.ttf", fontSize)
                print("Font size:", fontSize)

        # Debug: Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
      
    # Get key states
    keys = pygame.key.get_pressed()

    # Get mouse position and scale it based on window size
    mouse = pygame.mouse.get_pos()
    mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)

    # Draw background
    base_surface.fill( (29, 71, 46) )


    for c in cards:
        c.draw(base_surface)

    # Scale and blit to window
    scaled_surface = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit the FPS to 60
    clock.tick(60)
pygame.quit()

