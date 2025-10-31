import random

class Card:
    #String array of suit names
    suits = ["Spades", "Clubs", "Hearts", "Diamonds"]

    #String array of names of cards for displaying
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]

    #Parameters:
    #Value, an int(1-15) representing the card's index in the names array and will also be modified and used for the card's scoring value
    #suitNum, an int(0-3) representing the card's index in the suits array 
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

#End of Card Class

class Hand():
    #Parameters:
    #Flag, an int(0-1) indicating whether the hand belongs to a player or a CPU
    def __init__(self, flag):
        self.hand = []
        self.flag = flag

    #Iterates through hand array, calling each card's nicePrint function
    #And displays total score of hand
    def displayHand(self):
        print("Current hand:")
        if self.hand == []:
            print("Empty")
        else:
            for card in self.hand:
                card.nicePrint()
            print("Current score: " + str(self.getHandScore()) + "\n")
    
    #Gets and displays final score, with appropriate fanfare
    def finalScore(self):
        score = self.getHandScore()
        print("\nFinal score is : " + str(score))
        if score < 21:
            print("You win!")
        elif score > 21:
            print("You lose! Good DAY SIR!")
        else:
            print("You got an invalid score. Congratulations, that shouldn't be possible!")

    #Gets the sum of the score of all cards in hand
    def getHandScore(self):
        score = 0
        for card in self.hand:
            score += card.getScoreValue()
        return score
    
    #Lets user draw cards until they decide to stop
    #Probably needs a better name
    def playing(self, deck):
        hitting = True
        while hitting == True:
            self.displayHand()
            choice = input("Enter 1 to hit or anything else to pass: ").strip()
            if choice == "1":
                self.hand.append(draw(deck))
            else:
                hitting = False
#End of Hand class

#Gets a random valid index from the given deck array, and removes it
#Returning it to be appended to a hand array
#Could be added to a Player class or something
def draw(deck):
    index = random.randrange(len(deck))
    return deck.pop(index)




def main():
    testDeck = []
    #i and j are in reverse order for the card initialization because doing it this way
    #orders them by suit, rather than by value.
    for i in range(4):
        for j in range(1, 15):
            testDeck.append(Card(j, i))

    yourHand = Hand(1)
    CPUHand = Hand(0)

    yourHand.playing( testDeck)
    yourHand.finalScore()

#end of Main

if __name__ == "__main__":
    main()