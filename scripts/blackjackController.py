import pygame
import random
from .card import Card

# This class handles the actual game logic
class BlackjackController:

    def __init__(self, display, cardBackImage):

        # META: Initialize objects
        self.drawables = list()
        self.display = display

        # ART: Initialize the card art
        self.cardBackImage = cardBackImage

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
        self.resetDeck()

    # Creates the deck with normal distribution of playing cards
    def resetDeck(self):
        
        # Initialize the deck
        for suit in self.cardSuits:
            for face in self.cardFaces:
                newCard = Card(0, 0, self.cardWidth, self.cardHeight, self.cardColor, self.cardBorderColor, self.cardBorderWidth, 1.0, face, suit)
                self.deck.append(newCard)

        random.shuffle(self.deck)

    # Calculates the score values of each player
    def calculateScore(self):

        # Calculate the users' score
        for card in self.userHand:
            self.userScore += card.getScore()

        # Calculate the dealers' score
        for card in self.dealerHand:
            self.dealerScore += card.getScore()
    
    # Move to the next turn. Technically made such that you can have more users
    def nextTurn(self):
        self.turnIndex += 1
        
        if self.turnIndex > len(self.turns):
            self.turnIndex = 0

    # Clear the hands and start a new round
    def newRound(self):
        
        # Clear both players' hands
        self.userHand.clear()
        self.dealerHand.clear()
        self.userScore = 0
        self.dealerScore = 0

        # Iterate through the players and present cards
        cardAmount = len(self.turns) * 2 # 2 Cards per player
        cardsDealt = 0
        while (cardsDealt < cardAmount):

            # Create the card object and send it to the correct players' hand
            drawnCard = self.getCard(self.userHandPosition[0], self.userHandPosition[1])
            self.turns[self.turnIndex].append(drawnCard)

            # Increment the cards dealt and the current player
            cardsDealt += 1
            self.nextTurn()


    # Draws a card from the deck and returns it
    def getCard(self, desiredX, desiredY):

        newCard = self.deck.pop()
        newCard.x = self.deckPosition[0]
        newCard.y = self.deckPosition[1]
        newCard.desiredX = desiredX
        newCard.desiredY = desiredY

        return newCard

    # Draw it's drawables to the screen
    def draw(self, surface: pygame.surface.Surface, uiFont: pygame.font.Font):
        
        # Draw the deck
        surface.blit(self.cardBackImage, self.deckPosition)

        # Draw the user score
        drawYOffset = 16.0
        drawXOffset = 6.0
        userScoreText = uiFont.render(f"User Score: {self.userScore}", False, self.display["WHITE_COLOR"])
        surface.blit(userScoreText, (drawXOffset, self.display["GAME_SIZE"][1] - drawYOffset))

        # Draw the dealer score
        drawYOffset = 6.0
        drawXOffset = 6.0
        dealerScoreText = uiFont.render(f"Dealer Score: {self.dealerScore}", False, self.display["WHITE_COLOR"])
        surface.blit(dealerScoreText, (drawXOffset, drawYOffset))

        # Draw all the drawables (cards)
        for card in self.drawables:
            card.draw()

    # Called every frame
    def update(self, controls):
        pass