
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
running = True
game_paused = False

# Card types
cardFaces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
cardSuits = ['♠', '♣', '♥', '♦']
cardBack = pygame.image.load("assets/pixelCardback.png")

# Create surfaces
base_surface = pygame.Surface( (BASE_WIDTH, BASE_HEIGHT) )
window = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
pygame.display.set_caption("Super Blackjack 9000")


###################### CARD CLASS ####################
class Card:

    ###### INITIALIZATION ######
    def __init__(self, x, y, faceText="A", suitChar="♥",
                 fillColor=WHITE, borderColor=BLACK, borderWidth=2, cornerRadius=2):
        
        # Functional properties
        self.score = self.getScore(faceText)

        # Drawing properties
        self.isFaceUp = False
        self.x, self.y = x, y
        self.w, self.h = 60, 100
        self.faceText = faceText
        self.suitChar = suitChar
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.cornerRadius = cornerRadius

    ###### GET SCORE METHOD ######
    def getScore(self, faceText):
        if faceText in ['J', 'Q', 'K']:
            return 10
        elif faceText == 'A':
            return 11
        else:
            return int(faceText)
    
    ###### TO STRING METHOD ######
    def toString(self):
        return f"{self.faceText} of {self.suitChar} (Score: {self.score})"
    
    ###### DRAW METHOD ######
    def draw(self, surface):

        # Draw back of card if face down
        if not self.isFaceUp:

            surface.blit(cardBack, (self.x, self.y))
            return
        
        # Card rectangle
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

###################### PLAYER CLASS ####################
class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
    
    def addCard(self, card):
        self.hand.append(card)
        self.updateScore()

    def updateScore(self):
        self.score = sum(card.score for card in self.hand)

    def destroyCard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.updateScore()  

###################### HAND ####################
user = Player("User")
dealer = Player("Dealer")

# Creates a card object and returns it
def createCard(x, y, faceText, suitChar):
    return Card(x, y, faceText, suitChar)

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
            
            if event.key == pygame.K_0:
                user.addCard(createCard(50, 50, 'A', '♠'))

        # Debug: Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            exit()

    # Get mouse position and scale it based on window size
    mouse = pygame.mouse.get_pos()
    mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)


#################### MAIN LOOP ####################

while running:
    
    # Handle controls
    processControls()

    # Draw background
    base_surface.fill( (29, 71, 46) )

    # Draw cards
    for card in user.hand:
        card.draw(base_surface)

    for card in dealer.hand:
        card.draw(base_surface)

    surface.draw
    # Scale and blit to window
    scaled_surface = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit the FPS to 60
    clock.tick(60)
    
pygame.quit()

