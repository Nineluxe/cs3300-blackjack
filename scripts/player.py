import pygame
import card

class Player:

    def __init__(self):
        self.score = 0
        self.hand = list()

    def addCardToHand(self, card):
        self.hand.append(card)
    
    def clearHand(self):
        self.hand.clear()

    def calculateScore(self):
        
        for card in self.hand:
            self.score += card.getScore()
