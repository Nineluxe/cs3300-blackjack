import pygame
from .general import *

# ###################### CARD CLASS ####################
class Card:

    def __init__(self, x, y, cardWidth, cardHeight, fillColor, borderColor, borderWidth, cornerRadius, faceText, suitChar, cardBackImage, cardFont):

        # Functional properties
        self.faceText = faceText
        self.score = self.getScore()

        # Drawing properties
        self.x, self.y = x, y
        self.desiredX, self.desiredY = x, y
        self.w, self.h = cardWidth, cardHeight
        self.cardFont = cardFont
        self.cardBack = cardBackImage
        self.shadowColor = pygame.color.Color(0, 0, 0, 100)
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
        self.redColor = pygame.color.Color(255, 0, 0, 1)
        self.blackColor = pygame.color.Color(0, 0, 0, 1)

    # Get the score value of the current card
    def getScore(self):
        if self.faceText in ['J', 'Q', 'K']:
            return 10
        elif self.faceText == 'A':
            return 11
        else:
            return int(self.faceText)

    # UPDATE: Move towards desired position
    def update(self, dt):
        if self.x != self.desiredX:
            self.x = lerp(self.x, self.desiredX, dt * 10)
        if self.y != self.desiredY:
            self.y = lerp(self.y, self.desiredY, dt * 10)

    # DRAW: Draw front or back of card 
    def draw(self, surface):

        # Draw back of card if face down
        if not self.isFaceUp:

            surface.blit(self.cardBack, (self.x, self.y))
            return
        
        # Card rectangle
        rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # shadow
        shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(shadowSurf, (0, 0, 0, 100), shadowSurf.get_rect(), border_radius=self.cornerRadius)
        surface.blit(shadowSurf, (self.x + 6, self.y + 6))

        # fill
        pygame.draw.rect(surface, self.fillColor, rect, border_radius=self.cornerRadius)

        # border
        pygame.draw.rect(surface, self.borderColor, rect, width=self.borderWidth, border_radius=self.cornerRadius)

        # corner pips (rank + suit)
        rankColor = self.redColor if self.suitChar in ("♥", "♦") else self.blackColor
        rankText = self.cardFont.render(self.faceText, False, rankColor)
        suitText = self.cardFont.render(self.suitChar, False, rankColor)
        surface.blit(rankText, (self.x + 8, self.y + 6))
        surface.blit(suitText, (self.x + 8, self.y + 8 + rankText.get_height()))

        # big center suit
        centerSuit = self.cardFont.render(self.suitChar, False, rankColor)
        surface.blit(centerSuit, centerSuit.get_rect(center=rect.center))
