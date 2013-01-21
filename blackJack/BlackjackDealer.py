from BlackjackHand import BlackjackHand

#black jack dealer class. Uses the gameDeck obj
#from card deck class to create, get and play hands.
class BlackjackDealer():

  def __init__(self,gameDeck):
    self.gameDeck = gameDeck

  def createHand(self):
    self.hand = BlackjackHand(self.gameDeck)
    self.hand.getHand()

  def getHand(self):
    return self.hand.Hand

  def getHandValue(self):
    return self.hand.getValue()

  def playHand(self):
    while self.hand.getValue() < 17:
      self.hand.hit()
