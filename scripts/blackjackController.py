import pygame
import random
from .general import *
from .card import Card
from .button import Button

# This class handles the actual game logic
class BlackjackController:

    def __init__(self, display, controls, imageAssets, fontAssets):

        # META: Initialize objects
        self.cardDrawables = list()
        self.uiDrawables = list()
        self.display = display
        self.controls = controls
        self.isAnimating = False
        self.animatingTimer = 0.0
        self.cardDrawAnimationTime = 0.5
        self.eventQueue = list()
        self.doDrawDealerScore = False
        self.doDrawDeckText = False
        self.isQuitting = False

        # ART: Get references to the asset managers
        self.imageAssets = imageAssets
        self.fontAssets = fontAssets
        self.cardBackImage = self.imageAssets["cardBack"]
        self.cardFont = self.fontAssets["cardFont"]
        self.whiteColor = self.display["WHITE_COLOR"]
        self.blackColor = self.display["BLACK_COLOR"]
        self.redColor = self.display["RED_COLOR"]
        self.uiFont = self.fontAssets["uiFont"]

        # GAME LOGIC: Blackjack game logic information
        self.cardFaces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cardSuits = ['♠', '♣', '♥', '♦']
        self.cardWidth = 60
        self.cardHeight = 100
        self.cardBorderWidth = 2
        self.cardColor = self.whiteColor
        self.cardBorderColor = self.blackColor

        # GAME LOGIC: Initialize the two players
        self.gameSize = self.display["GAME_SIZE"]
        self.cardPositionOffset = 10
        self.userHandPosition = ( (self.gameSize[0] // 2) - (self.cardWidth // 2), self.gameSize[1] - (self.cardHeight + self.cardPositionOffset) )
        self.dealerHandPosition = ( (self.gameSize[0] // 2) - (self.cardWidth // 2), self.cardPositionOffset )
        self.userHand = list()
        self.dealerHand = list()
        self.userScore = self.dealerScore = 0

        # GAME LOGIC: Initialize turns
        self.turns = (self.userHand, self.dealerHand)
        self.turnIndex = 0 # This is the index of the self.turns tuple
        self.gamePhases = ("START", "INITIAL_DRAW", "USER_TURN", "DEALER_TURN", "ROUND_END")
        self.currentPhase = self.gamePhases[0]

        # GAME LOGIC: Deck initialization
        self.deck = list()
        self.deckPosition = ( self.gameSize[0] - (self.cardWidth + self.cardPositionOffset), self.cardHeight + self.cardPositionOffset )
        self.deckCollisionRect = pygame.Rect(self.deckPosition[0], self.deckPosition[1], self.cardWidth, self.cardHeight)

        # UI: Create buttons
        self.stayButtonPosition = (self.gameSize[0] - 110, self.gameSize[1] - 50)
        self.quitButtonPosition = (10, self.gameSize[1] // 2 + 30)

        self.newRoundButton = Button( self.stayButtonPosition[0], self.stayButtonPosition[1], 100, 40, self.blackColor, "New Round", self.uiFont )
        self.quitButton = Button( self.quitButtonPosition[0], self.quitButtonPosition[1], 100, 40, self.redColor, "Quit", self.uiFont )
        self.stayButton = Button( self.stayButtonPosition[0], self.stayButtonPosition[1], 100, 40, self.blackColor, "Stay", self.uiFont )

        self.uiDrawables.append(self.newRoundButton)
        self.uiDrawables.append(self.quitButton)
        self.uiDrawables.append(self.stayButton)

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
        self.eventQueue.clear()
        self.resetDeck()
        self.cardDrawables.clear()

        # Clear both players' hands
        self.userHand.clear()
        self.dealerHand.clear()
        self.userScore = 0
        self.dealerScore = 0

        # Create the card object and send it to the correct players' hand
        self.eventQueue.append(lambda: self.drawCard(self.userHand))
        self.eventQueue.append(lambda: self.drawCard(self.dealerHand, False))
        self.eventQueue.append(lambda: self.drawCard(self.userHand))
        self.eventQueue.append(lambda: self.drawCard(self.dealerHand))

    # Draws a card from the deck and sends it to the correct players' hand
    def drawCard(self, player, isFaceUp=True):
        
        # Initialize variables
        self.isAnimating = True
        self.animatingTimer = self.cardDrawAnimationTime

        # Draw the card from the deck
        newCard = self.deck.pop()
        newCard.isFaceUp = isFaceUp
        newCard.x = self.deckPosition[0]
        newCard.y = self.deckPosition[1]

        # Add the card to the drawables and to the correct players' hand
        self.cardDrawables.append(newCard)
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

    # Check the hover status of the UI buttons
    def checkUIButtons(self, controls):
        
        if self.newRoundButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
            self.newRound()

        if self.stayButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
            
            # Dealer draws cards until score is at least 17
            while (self.dealerScore < 17):
                self.drawCard(self.dealerHand)


    # Draw it's drawables to the screen
    def draw(self, surface):
        
        # Draw the deck
        surface.blit(self.cardBackImage, self.deckPosition)

        # Draw the user score
        drawYOffset = 16.0
        drawXOffset = 6.0
        userScoreText = self.uiFont.render(f"User Score: {self.userScore}", False, self.whiteColor)
        surface.blit(userScoreText, (drawXOffset, self.gameSize[1] - drawYOffset))

        # Draw the dealer score
        if self.doDrawDealerScore:
            drawYOffset = 6.0
            drawXOffset = 6.0
            dealerScoreText = self.uiFont.render(f"Dealer Score: {self.dealerScore}", False, self.whiteColor)
            surface.blit(dealerScoreText, (drawXOffset, drawYOffset))

        # Draw where to draw cards from
        if self.doDrawDeckText:
            deckTextPosition = (self.deckPosition[0] + 3, self.deckPosition[1] + self.cardHeight + 4)
            drawText(deckTextPosition, "Draw Card", self.uiFont, self.whiteColor, surface)

        # Draw all the cards
        for drawable in self.cardDrawables:
            drawable.draw(surface)

        # Draw all the UI
        for drawable in self.uiDrawables:
            drawable.draw(surface, self.controls["MOUSE_SCALED_POSITION"])

        # Draw the initial text
        if self.currentPhase == "START":
            resultText = "Push new round."
            drawText((self.gameSize[0] // 2, self.gameSize[1] // 2), resultText, self.uiFont, self.whiteColor, surface, "center")

        # Draw game over screen
        if self.currentPhase == "ROUND_END":
            resultText = ""
            if self.userScore > 21:
                resultText = "BUST! Dealer Wins!"
            elif self.dealerScore > 21:
                resultText = "Dealer BUSTS! You Win!"
            elif self.userScore > self.dealerScore:
                resultText = "You Win!"
            elif self.userScore < self.dealerScore:
                resultText = "Dealer Wins!"
            elif self.userScore == self.dealerScore:
                resultText = "TIE!"
            else:
                resultText = "Push new round."

            drawText((self.gameSize[0] // 2, self.gameSize[1] // 2), resultText, self.uiFont, self.whiteColor, surface, "center")

    # Called every frame
    def update(self, controls, dt):
        
        # Work through animations
        if (self.isAnimating and self.animatingTimer > 0.0):
            self.animatingTimer -= dt
        elif (self.animatingTimer <= 0.0):
            self.isAnimating = False

        # Update the active cards
        for card in self.cardDrawables:
            card.update(dt)

        # Update the active cards
        for ui in self.uiDrawables:
            ui.update(dt)

        # Quit button
        if self.quitButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
            self.isQuitting = True

        # Perform actions if not currently animating
        if (self.isAnimating):
            return

        # Check if the event queue has events
        if ( len(self.eventQueue) > 0 ):
            event = self.eventQueue.pop(0)
            event()  # Call whatever function is next in the queue
            return

        # Game logic
        match self.currentPhase:

            case "START":
                # Set the stay button to invisible
                self.stayButton.doDraw = False
                self.stayButton.disabled = True

                self.newRoundButton.doDraw = True
                self.newRoundButton.disabled = False

                if self.newRoundButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
                    self.currentPhase = "INITIAL_DRAW"

            case "INITIAL_DRAW":
                
                # Draw the "draw card" text under the deck
                self.doDrawDeckText = True

                # Set dealers score invisible
                self.doDrawDealerScore = False

                # Set the stay button to invisible
                self.stayButton.doDraw = True
                self.stayButton.disabled = False

                self.newRoundButton.doDraw = False
                self.newRoundButton.disabled = True

                self.newRound()
                self.currentPhase = "USER_TURN"

            case "USER_TURN":

                if self.userScore > 21:
                    self.currentPhase = "ROUND_END"
                else:               
                    # Check if deck is pressed
                    if (controls["MOUSE_PRESSED"]) and (self.deckCollisionRect.collidepoint(controls["MOUSE_SCALED_POSITION"])):
                        self.eventQueue.append(lambda: self.drawCard(self.userHand))

                    # Check for stay button press
                    if (controls["MOUSE_PRESSED"]) and (self.stayButton.isMouseOver(controls["MOUSE_SCALED_POSITION"])):
                        self.currentPhase = "DEALER_TURN"

            case "DEALER_TURN":
                if self.dealerScore > 21:
                    self.currentPhase = "ROUND_END"
                elif self.dealerScore >= 17:
                    self.currentPhase = "ROUND_END"
                else:
                    self.eventQueue.append(lambda: self.drawCard(self.dealerHand))

            case "ROUND_END":
                
                # Set the dealers cards as visible
                for card in self.dealerHand:
                    card.isFaceUp = True

                # Set the dealers score to be visible
                self.doDrawDealerScore = True

                # Set the stay button to invisible
                self.stayButton.doDraw = False
                self.stayButton.disabled = True

                self.newRoundButton.doDraw = True
                self.newRoundButton.disabled = False

                if self.newRoundButton.isMouseOver(controls["MOUSE_SCALED_POSITION"]) and controls["MOUSE_PRESSED_ONCE"]:
                    self.currentPhase = "INITIAL_DRAW"

