import random

class Card:
    suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
    def __init__(self, value, suitNum):
        self.value = value
        self.suit = Card.suits[suitNum]
    
    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    def nicePrint(self):
        print(Card.name[self.value -1] + " of " + self.suit)
