import random

class Card:
    #String array of suit names
    suits = ["Spades", "Clubs", "Hearts", "Diamonds"]

    #String array of names of cards for displaying
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

    def __init__(self, value, suitNum):
        self.value = value
        self.suit = Card.suits[suitNum]

        #Have to make a seperate function to get the cards actual value for the game, 
        #since face cards and aces value don't match their index in the array unlike numbered cards
        self.scoreValue = self.generateScoreValue()

    def getValue(self):
        return self.value
    
    def getSuit(self):
        return self.suit
    
    #Gets the actual scoring value for the card
    #Note: Will likely need to add something to this for aces later, 
    #since their value can change to 1 if 11 would put the total score over 21
    #could handle that outside of the class though
    def generateScoreValue(self):
        if(self.value <= 10): #Numbered cards
            num = self.value
        elif(self.value in range(11, 14)): #Face cards
            num = 10
        elif(self.value == 14): #Aces
            num = 11 
        return num
    
    def getScoreValue(self):
        return self.scoreValue
    
    #Prints the cards name and value in the form of "Ace of Hearts"
    def nicePrint(self):
        print(Card.names[self.value -1] + " of " + self.suit)

testDeck = []
for i in range(4):
    for j in range(1, 15):
        testDeck.append(Card(j, i))

for card in testDeck:
    card.nicePrint()