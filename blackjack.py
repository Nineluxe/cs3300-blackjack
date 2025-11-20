
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
cardFont = pygame.font.Font("assets/fonts/dungeon-mode.ttf", 9)  # None = default system font, 24 = size
uiFont = pygame.font.Font("assets/fonts/monogram-extended.ttf", 16)
mouse = pygame.mouse.get_pos()
mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)
debugging = True
running = True
game_paused = False
drawables = list()

# Card types
cardFaces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
cardSuits = ['♠', '♣', '♥', '♦']
cardBack = pygame.image.load("assets/pixelCardback.png")
cardWidth = 60
cardHeight = 100

# Create surfaces
base_surface = pygame.Surface( (BASE_WIDTH, BASE_HEIGHT) )
window = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
pygame.display.set_caption("Super Blackjack 9000")


# Simple linear interpolation function
def lerp(start, stop, amount):
    return start + (stop - start) * amount

###################### CARD CLASS ####################
class Card:

    ###### INITIALIZATION ######
    def __init__(self, x, y, faceText="A", suitChar="♥",
                 fillColor=WHITE, borderColor=BLACK, borderWidth=2, cornerRadius=2):

        # Functional properties
        self.score = self.getScore(faceText)

        # Drawing properties
        self.x, self.y = x, y
        self.desiredX, self.desiredY = x, y
        self.w, self.h = cardWidth, cardHeight
        self.shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.doDrawShadow = True
        self.shadowOffset = (6, 6)
        self.isFaceUp = True
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
    
    ###### UPDATE METHOD ######
    def update(self, dt):
        if self.x != self.desiredX:
            self.x = lerp(self.x, self.desiredX, dt * 10)
        if self.y != self.desiredY:
            self.y = lerp(self.y, self.desiredY, dt * 10)

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
        rankText = cardFont.render(self.faceText, False, rankColor)
        suitText = cardFont.render(self.suitChar, False, rankColor)
        surface.blit(rankText, (self.x + 8, self.y + 6))
        surface.blit(suitText, (self.x + 8, self.y + 8 + rankText.get_height()))

        # big center suit
        centerSuit = cardFont.render(self.suitChar, False, rankColor)
        surface.blit(centerSuit, centerSuit.get_rect(center=rect.center))

###################### POPUP CLASS ######################
class Popup:
    def __init__(self, text):
        self.text = text

    def draw(self, surface):
        popup_surf = uiFont.render(self.text, True, WHITE)
        rect = popup_surf.get_rect(center=(BASE_WIDTH // 2, BASE_HEIGHT // 2))

        # background box
        pygame.draw.rect(surface, BLACK, rect.inflate(20, 20), border_radius=8)

        # draw text
        surface.blit(popup_surf, rect)


###################### BUTTON CLASS ######################
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, imagePath=None, text="", textxOffset = 0, textyOffset = 0, w=140, h=40):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.doDrawShadow = True

        if imagePath:
            self.image = pygame.image.load(imagePath).convert_alpha()
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.image = None

        drawables.append(self)

    # Check if mouse is over button
    def isMouseOver(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
    # Draw method
    def draw(self, surface):
        # shadow
        if self.doDrawShadow:
            shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            pygame.draw.rect(shadowSurf, SHADOW, shadowSurf.get_rect(), border_radius=6)
            surface.blit(shadowSurf, (self.x + 6, self.y + 6))

        # draw button image if available
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # draw plain rectangle
            pygame.draw.rect(surface, BLACK, self.rect, border_radius=6)
            pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)

        # draw text
        if self.text != "":
            surf = uiFont.render(self.text, True, WHITE)
            text_rect = surf.get_rect(center=self.rect.center)
            surface.blit(surf, text_rect)


        #Greys out hit button if player cannot hit
        if self.text == "Hit me!" and game.playerCanHit == False:
            temp = self.image.copy()
            temp.fill((50, 50, 50, 120), None, pygame.BLEND_RGBA_MULT)
            surface.blit(temp, (self.x, self.y))
            return

        if debugging:
            pass
            #pygame.draw.rect(surface, RED, self.rect, 1)

# Initialize deck button
deck = Button(BASE_WIDTH - (cardWidth + 20), 20, "assets/pixelCardback.png", "Hit me!")
stand_Button = Button(BASE_WIDTH - (cardWidth + 20), 140, "assets/stand_button.png", "Stand")
# Initialize play again button (removed from drawables until needed)
play_again_button = Button(x=(BASE_WIDTH // 2) - 70, y=(BASE_HEIGHT // 2) + 40,text="Play Again")
drawables.remove(play_again_button)
###################### GAME CLASS ######################
class Game:    

    def __init__(self):
        self.x = BASE_WIDTH - (cardWidth + 20)
        self.y = BASE_HEIGHT + (cardHeight + 20)
        self.deck = []
        self.initializeDeck()
        self.playerCanHit = True

        # Add deck to drawables for drawing
        drawables.append(self)

    # Draw back of card to represent deck
    def draw(self, surface):
        if len(self.deck) > 0:
            surface.blit(cardBack, (self.x, self.y))

    # Initializes deck with 52 cards and shuffles them
    def initializeDeck(self):
        for suit in cardSuits:
            for face in cardFaces:
                newCard = Card(0, 0, face, suit)
                self.deck.append(newCard)

        # It literally did not feel shuffled enough
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        random.shuffle(self.deck)

    def winner(self):
        if user.score > 21 and dealer.score <= 21:
            return "You busted! Dealer wins!"
        elif dealer.score > 21 and user.score <= 21:
            return "Dealer busted! You win!"
        elif user.score > 21 and dealer.score > 21:
            return "Both players busted! No winner!"
        elif user.score == dealer.score:
            return "It's a tie!"
        elif user.score > dealer.score:
            return "You win!"
        elif dealer.score > user.score:
            return "Dealer wins!"
        else:
            return "Error in determining winner."

###################### PLAYER CLASS ####################
class Player:

    def __init__(self, name, handPosition=[0,0]):
        self.name = name
        self.hand = []
        self.score = 0
        self.handPosition = handPosition
    
    # Add a card to the player's hand
    def addCard(self, card):

        # Add card to the relevant lists
        self.hand.append(card)
        drawables.append(card)

        # Update all the cards desired positions
        totalCards = len(self.hand)
        for index, card in enumerate(self.hand):

            cardIndex = index - (totalCards - 1) / 2

            # Update desired positions of cards hand
            card.desiredX = self.handPosition[0] + (cardIndex * (cardWidth + 10))
            card.desiredY = self.handPosition[1]

        # Update your hand score
        self.updateScore()

    def updateScore(self):
        self.score = sum(card.score for card in self.hand)
        #Check for aces and adjust score if over 21
        if self.score > 21:
            for card in self.hand:
                if card.faceText == 'A' and card.score == 11:
                    card.score = 1
                    self.score -= 10
                    if self.score <= 21:
                        break

    def drawScore(self, surface, x, y):
        scoreText = uiFont.render(f"{self.name} Score: {self.score}", True, WHITE)
        surface.blit(scoreText, (x, y))

    def destroyCard(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.updateScore()  


###################### HAND ####################
userStartingHandPosition = [
    (BASE_WIDTH // 2) - (cardWidth // 2), 
    BASE_HEIGHT - (cardHeight + 20)
]

game = Game()
user = Player("User", userStartingHandPosition)
dealer = Player("Dealer", handPosition=(BASE_WIDTH // 2, cardHeight + 20))

# Creates a card object and returns it
def drawDeckCard(x, y):
    newCard = game.deck.pop()
    newCard.x = x
    newCard.y = y
    return newCard


#################### MAIN LOOP ####################
winner_popup = None
round_over = False

while running:

    # Get mouse position and scale it based on window size
    mouse = pygame.mouse.get_pos()
    mouse_scaled = (mouse[0] / SCALE, mouse[1] / SCALE)
    
    # Handle events
    for event in pygame.event.get():

        # Debug: Quit game
        #Moved this up here cause otherwise it wouldn't quit when hitting the X
        if event.type == pygame.QUIT:
            running
            pygame.quit()
            exit()

        # Controls: Change size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                fontSize += 1
                uiFont = pygame.font.Font("assets/fonts/monogram-extended.ttf", fontSize)
                print("Font size:", fontSize)
            elif event.key == pygame.K_DOWN:
                fontSize = max(1, fontSize - 1)
                uiFont = pygame.font.Font("assets/fonts/monogram-extended.ttf", fontSize)
                print("Font size:", fontSize)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            # Debug: Add card to user hand
            if event.key == pygame.K_0:
                xPos = user.handPosition[0]
                yPos = user.handPosition[1]
                user.addCard(drawDeckCard(xPos, yPos))
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            # HIT (only allowed if player_can_hit is True)
            if game.playerCanHit and deck.isMouseOver(mouse_scaled):
                xPos = deck.x
                yPos = deck.y
                user.addCard(drawDeckCard(xPos, yPos))
                #Dealer hits after every player hit as long as dealer score is below threshold
                if dealer.score < 17:
                    dealer.addCard(drawDeckCard(dealer.handPosition[0], dealer.handPosition[1]))

            # STAND
            if stand_Button.isMouseOver(mouse_scaled):
                game.playerCanHit = False

            #Dealer finishes turn only once
            if not game.playerCanHit and not round_over:

                # Dealer hits until 17+
                while dealer.score < 17:
                    dealer.addCard(drawDeckCard(dealer.handPosition[0], dealer.handPosition[1]))

                # round ends → create popup
                winner_popup = Popup(game.winner())
                round_over = True

            # PLAY AGAIN
            if round_over and play_again_button.isMouseOver(mouse_scaled):
                user.hand.clear()
                dealer.hand.clear()
                dealer.score = 0
                user.score = 0
                drawables[:] = [deck, stand_Button, game]  # reset drawables
                game.initializeDeck()
                game.playerCanHit = True
                round_over = False
                winner_popup = None


    # Draw background
    base_surface.fill( (29, 71, 46) )

    # Draw every object in drawables list
    for obj in drawables:
        obj.draw(base_surface)

    # Use update method to move cards toward desired positions
    for card in user.hand:
        card.update(clock.get_time() / 1000.0)
    for card in dealer.hand:
        card.update(clock.get_time() / 1000.0)

    # Draw player score
    user.drawScore(base_surface, 10, BASE_HEIGHT - 30)
    dealer.drawScore(base_surface, BASE_WIDTH - 150, 10)

    if debugging:
        mousePosText = uiFont.render(f"Mouse: {mouse_scaled[0]:.1f}, {mouse_scaled[1]:.1f}", True, WHITE)
        base_surface.blit(mousePosText, (10, 10))
    
    # Draw popup if it exists
    if winner_popup:    
        winner_popup.draw(base_surface)
        play_again_button.draw(base_surface)

    # Scale and blit to window
    scaled_surface = pygame.transform.scale(base_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_surface, (0, 0))

    # Flip the display to put your work on screen
    pygame.display.flip()

    # Limit the FPS to 60
    clock.tick(60)
    
pygame.quit()