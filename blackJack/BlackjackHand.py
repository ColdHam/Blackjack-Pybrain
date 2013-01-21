from BlackjackCardDeck import BlackjackCardDeck

#blackjack hand class. interacts with blackjack deck to get hands
#for players.
class BlackjackHand:

  def __init__(self,gameDeck):
    self.Hand = {}
    self.gameDeck = gameDeck

  def getHand(self):
    self.Hand = {}
    card = self.gameDeck.getCard()
    self.Hand[card.keys()[0]] = card.values()[0]
    card = self.gameDeck.getCard()
    self.Hand[card.keys()[0]] = card.values()[0]

  def hit(self):
    card = self.gameDeck.getCard()
    self.Hand[card.keys()[0]] = card.values()[0]

  def getValue(self):
    total = 0
    for card in self.Hand:
      total += self.Hand[card]
    return total
