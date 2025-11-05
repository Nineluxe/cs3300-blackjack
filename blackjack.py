
import pygame
import math
import random

#################### CONSTANTS ####################
BASE_WIDTH, BASE_HEIGHT = 640, 360
SCALE = 2
WINDOW_WIDTH, WINDOW_HEIGHT = BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE
WHITE = (250, 250, 250)
BLACK = (20, 20, 20)
RED = (210, 30, 45)
SHADOW = (0, 0, 0, 90)
TABLE = (6, 105, 75)

#################### INITIALIZATION ####################
pygame.init()
clock = pygame.time.Clock()
entityList = list()
pygame.font.init()

fontSize = 9
font = pygame.font.Font("assets/fonts/dungeon-mode.ttf", fontSize)  # None = default system font, 24 = size
mouse = pygame.mouse.get_pos()
mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)
debugging = True

# Create surfaces
base_surface = pygame.Surface( (BASE_WIDTH, BASE_HEIGHT) )
window = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
pygame.display.set_caption("Super Blackjack 9000")


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


###################### CREATE CARDS ####################
cards = [
    Card(40, 20, faceText="A", suitChar="♥")
]

def createCard(x, y, faceText, suitChar):

    # Create new card and add to list
    newCard = Card(x, y, faceText=faceText, suitChar=suitChar)
    cards.append(newCard)

    return newCard

def destroyCard(card):
    if card in cards:
        cards.remove(card)


###################### CONTROLS ####################
def processControls():
    
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
            running = False
            exit()

    # Get mouse position and scale it based on window size
    mouse = pygame.mouse.get_pos()
    mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)


#################### MAIN LOOP ####################
running = True
game_paused = False
while running:
    
    # Handle controls
    processControls()

    # Draw background
    base_surface.fill( (29, 71, 46) )

    # Draw cards
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

