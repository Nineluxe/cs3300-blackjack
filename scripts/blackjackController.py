import pygame
import random
from .card import Card
from .button import Button

# This class handles the actual game logic
class BlackjackController:

    def __init__(self, display, imageAssets, fontAssets):

        # META: Initialize objects
        self.drawables = list()
        self.display = display
        self.isAnimating = False
        self.animatingTimer = 0.0
        self.cardDrawAnimationTime = 0.5
        self.eventQueue = list()

        # ART: Get references to the asset managers
        self.imageAssets = imageAssets
        self.fontAssets = fontAssets
        self.cardBackImage = self.imageAssets["cardBack"]
        self.cardFont = self.fontAssets["cardFont"]

        # GAME LOGIC: Blackjack game logic information
        self.cardFaces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cardSuits = ['♠', '♣', '♥', '♦']
        self.cardWidth = 60
        self.cardHeight = 100
        self.cardBorderWidth = 2
        self.cardColor = display["WHITE_COLOR"]
        self.cardBorderColor = display["BLACK_COLOR"]

        # GAME LOGIC: Initialize the two players
        self.gameSize = self.display["GAME_SIZE"]
        self.cardPositionOffset = 10
        self.userHandPosition = ( (self.display["GAME_SIZE"][0] // 2) - (self.cardWidth // 2), self.display["GAME_SIZE"][1] - (self.cardHeight + self.cardPositionOffset) )
        self.dealerHandPosition = ( (self.display["GAME_SIZE"][0] // 2) - (self.cardWidth // 2), self.cardPositionOffset )
        self.userHand = list()
        self.dealerHand = list()
        self.userScore = self.dealerScore = 0

        # GAME LOGIC: Initialize turns
        self.turns = (self.userHand, self.dealerHand)
        self.turnIndex = 0 # This is the index of the self.turns tuple

        # GAME LOGIC: Deck initialization
        self.deck = list()
        self.deckPosition = ( self.display["GAME_SIZE"][0] - (self.cardWidth + self.cardPositionOffset), self.cardHeight + self.cardPositionOffset )
        self.deckCollisionRect = pygame.Rect(self.deckPosition[0], self.deckPosition[1], self.cardWidth, self.cardHeight)
        self.newRound()

        # UI: Create buttons
        self.newRoundButtonPosition = (10, self.display["GAME_SIZE"][1] // 2 - 30)
        self.stayButtonPosition = (self.display["GAME_SIZE"][0] - 110, self.display["GAME_SIZE"][1] - 50)
        self.quitButtonPosition = (10, self.display["GAME_SIZE"][1] // 2 + 30)

        self.newRoundButton = Button( self.newRoundButtonPosition[0], self.newRoundButtonPosition[1], 100, 40, self.display["BLACK_COLOR"], "New Round", self.fontAssets["uiFont"] )
        self.quitButton = Button( self.quitButtonPosition[0], self.quitButtonPosition[1], 100, 40, self.display["RED_COLOR"], "Quit", self.fontAssets["uiFont"] )
        self.stayButton = Button( self.stayButtonPosition[0], self.stayButtonPosition[1], 100, 40, self.display["BLACK_COLOR"], "Stay", self.fontAssets["uiFont"] )

        self.drawables.append(self.newRoundButton)
        self.drawables.append(self.quitButton)
        self.drawables.append(self.stayButton)

    # Creates the deck with normal distribution of playing cards
    def resetDeck(self):
        
        # Initialize the deck
        for suit in self.cardSuits:
            for face in self.cardFaces:
                newCard = Card(0, 0, self.cardWidth, self.cardHeight, self.cardColor, self.cardBorderColor, self.cardBorderWidth, 1, face, suit, self.cardBackImage, self.cardFont)
                self.deck.append(newCard)

        random.shuffle(self.deck)

    # Calculates the score values of each player
    def calculateHandScore(self, playerHand):
        
        # Initialize variables
        totalScore = cardScore = aces = 0

        # Calculate the users' score
        for card in playerHand:
            cardScore = card.getScore()
            totalScore += cardScore

            if (cardScore == 11):
                aces += 1

        # Calculate ace score
        while (aces > 0 and totalScore > 21):
            totalScore -= 10 # Reduce the value of an ace to 1 by subtracting 10
            aces -= 1

        # Set the total score
        if playerHand == self.userHand:
            self.userScore = totalScore
        else:
            self.dealerScore = totalScore

    
    # Move to the next turn. Technically made such that you can have more users
    def nextTurn(self):
        self.turnIndex += 1
        
        if self.turnIndex > len(self.turns):
            self.turnIndex = 0

    # Clear the hands and start a new round
    def newRound(self):
        
        # Shuffle the deck
        self.resetDeck()
        self.drawables.clear()

        # Clear both players' hands
        self.userHand.clear()
        self.dealerHand.clear()
        self.userScore = 0
        self.dealerScore = 0

        # Create the card object and send it to the correct players' hand
        self.eventQueue.append(lambda: self.drawCard(self.userHand))
        self.eventQueue.append(lambda: self.drawCard(self.dealerHand))
        self.eventQueue.append(lambda: self.drawCard(self.userHand))
        self.eventQueue.append(lambda: self.drawCard(self.dealerHand))

    # Draws a card from the deck and sends it to the correct players' hand
    def drawCard(self, player):
        
        # Initialize variables
        self.isAnimating = True
        self.animatingTimer = self.cardDrawAnimationTime

        # Draw the card from the deck
        newCard = self.deck.pop()
        newCard.x = self.deckPosition[0]
        newCard.y = self.deckPosition[1]

        # Add the card to the drawables and to the correct players' hand
        self.drawables.append(newCard)
        player.append(newCard)

        # Get the initial position of the players' hand
        if (player == self.userHand):
            startingX = self.userHandPosition[0]
            startingY = self.userHandPosition[1]
        else:
            # Else: send the card to the dealer
            startingX = self.dealerHandPosition[0]
            startingY = self.dealerHandPosition[1]

        # Update the desired position of the card based on how many cards there are
        totalCards = len(player)
        for index, card in enumerate(player):

            cardIndex = index - (totalCards - 1) / 2

            # Update desired positions of cards hand
            card.desiredX = startingX + (cardIndex * (self.cardWidth + 10))
            card.desiredY = startingY

        # Update the player's score
        self.calculateHandScore(player)

    def checkUIButtons(self, controls):
        
        if self.newRoundButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
            self.newRound()

        if self.quitButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
            pygame.quit()
            exit()

    # Draw it's drawables to the screen
    def draw(self, surface):
        
        # Draw the deck
        surface.blit(self.cardBackImage, self.deckPosition)

        # Draw the user score
        drawYOffset = 16.0
        drawXOffset = 6.0
        userScoreText = self.fontAssets["uiFont"].render(f"User Score: {self.userScore}", False, self.display["WHITE_COLOR"])
        surface.blit(userScoreText, (drawXOffset, self.display["GAME_SIZE"][1] - drawYOffset))

        # Draw the dealer score
        drawYOffset = 6.0
        drawXOffset = 6.0
        dealerScoreText = self.fontAssets["uiFont"].render(f"Dealer Score: {self.dealerScore}", False, self.display["WHITE_COLOR"])
        surface.blit(dealerScoreText, (drawXOffset, drawYOffset))

        # Draw all the drawables (cards)
        for drawable in self.drawables:
            drawable.draw(surface)

    # Called every frame
    def update(self, controls, dt):
        
        # Work through animations
        if (self.isAnimating and self.animatingTimer > 0.0):
            self.animatingTimer -= dt
        elif (self.animatingTimer <= 0.0):
            self.isAnimating = False

        # Check buttons for use
        self.checkUIButtons(controls)

        # Perform actions if not currently animating
        if (not self.isAnimating):

            # Iterate through the event queue
            if ( len(self.eventQueue) > 0 ):
                event = self.eventQueue.pop(0)
                event()  # Call draw card
            
            # Check controls
            else:
                if (controls["MOUSE_PRESSED"]) and (self.deckCollisionRect.collidepoint(controls["MOUSE_SCALED_POSITION"])):
                    self.eventQueue.append(lambda: self.drawCard(self.userHand))

                    if (self.dealerScore <= 16):
                        self.eventQueue.append(lambda: self.drawCard(self.dealerHand))

        # Update the active cards
        for card in self.drawables:
            card.update(dt)