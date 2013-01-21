import random as r

#blackjack deck class. function to set up a deck of cards and their
#blackjack values. Used by the dealer and player to get cards and shuffle
#deck.

class BlackjackCardDeck:

    def __init__(self):

    self.cardDeck =   {'AH':11,'2H':2,'3H':3,'4H':4,'5H':5,'6H':6,'7H':7,'8H':8,'9H':9,'10H':10,'JH':10,'QH':10,'KH':10,
                       'AD':11,'2D':2,'3D':3,'4D':4,'5D':5,'6D':6,'7D':7,'8D':8,'9D':9,'10D':10,'JD':10,'QD':10,'KD':10,
                       'AC':11,'2C':2,'3C':3,'4C':4,'5C':5,'6C':6,'7C':7,'8C':8,'9C':9,'10C':10,'JC':10,'QC':10,'KC':10,
                       'AS':11,'2S':2,'3S':3,'4S':4,'5S':5,'6S':6,'7S':7,'8S':8,'9S':9,'10S':10,'JS':10,'QS':10,'KS':10}

  def getCard(self):
    card = r.choice(self.cardDeck.keys())
    cardValue = self.cardDeck[card]
    del self.cardDeck[card]
    return {card:cardValue}

  def shuffleDeck(self):
     self.cardDeck =   {'AH':11,'2H':2,'3H':3,'4H':4,'5H':5,'6H':6,'7H':7,'8H':8,'9H':9,'10H':10,'JH':10,'QH':10,'KH':10,
                'AD':11,'2D':2,'3D':3,'4D':4,'5D':5,'6D':6,'7D':7,'8D':8,'9D':9,'10D':10,'JD':10,'QD':10,'KD':10,
                'AC':11,'2C':2,'3C':3,'4C':4,'5C':5,'6C':6,'7C':7,'8C':8,'9C':9,'10C':10,'JC':10,'QC':10,'KC':10,
                'AS':11,'2S':2,'3S':3,'4S':4,'5S':5,'6S':6,'7S':7,'8S':8,'9S':9,'10S':10,'JS':10,'QS':10,'KS':10}

