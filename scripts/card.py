# import pygame

# ###################### CARD CLASS ####################
class Card:

    def __init__(self, x, y, cardWidth, cardHeight, fillColor, borderColor, borderWidth, cornerRadius, faceText, suitChar):

        # Functional properties
        self.score = self.getScore(faceText)

        # Drawing properties
        self.x, self.y = x, y
        self.desiredX, self.desiredY = x, y
        self.w, self.h = cardWidth, cardHeight
#         self.shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
#         self.doDrawShadow = True
#         self.shadowOffset = (6, 6)
        self.isFaceUp = True
        self.faceText = faceText
        self.suitChar = suitChar
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.cornerRadius = cornerRadius

    # Get the score value of the current card
    def getScore(self, faceText):
        if faceText in ['J', 'Q', 'K']:
            return 10
        elif faceText == 'A':
            return 11
        else:
            return int(faceText)
    
#     ###### TO STRING METHOD ######
#     def toString(self):
#         return f"{self.faceText} of {self.suitChar} (Score: {self.score})"
    
#     ###### UPDATE METHOD ######
#     def update(self, dt):
#         if self.x != self.desiredX:
#             self.x = lerp(self.x, self.desiredX, dt * 10)
#         if self.y != self.desiredY:
#             self.y = lerp(self.y, self.desiredY, dt * 10)

#     ###### DRAW METHOD ######
#     def draw(self, surface):

#         # Draw back of card if face down
#         if not self.isFaceUp:

#             surface.blit(cardBack, (self.x, self.y))
#             return
        
#         # Card rectangle
#         rect = pygame.Rect(self.x, self.y, self.w, self.h)

#         # shadow
#         shadowSurf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
#         pygame.draw.rect(shadowSurf, SHADOW, shadowSurf.get_rect(), border_radius=self.cornerRadius)
#         surface.blit(shadowSurf, (self.x + 6, self.y + 6))

#         # fill
#         pygame.draw.rect(surface, self.fillColor, rect, border_radius=self.cornerRadius)

#         # border
#         pygame.draw.rect(surface, self.borderColor, rect, width=self.borderWidth, border_radius=self.cornerRadius)

#         # corner pips (rank + suit)
#         rankColor = RED if self.suitChar in ("♥", "♦") else BLACK
#         rankText = cardFont.render(self.faceText, False, rankColor)
#         suitText = cardFont.render(self.suitChar, False, rankColor)
#         surface.blit(rankText, (self.x + 8, self.y + 6))
#         surface.blit(suitText, (self.x + 8, self.y + 8 + rankText.get_height()))

#         # big center suit
#         centerSuit = cardFont.render(self.suitChar, False, rankColor)
#         surface.blit(centerSuit, centerSuit.get_rect(center=rect.center))
