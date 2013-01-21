from pybrain.rl.environments.environment import Environment
from scipy import zeros

from BlackjackHand import BlackjackHand
#overidden Environment Class from pybrain. Black Jack Environment.
#Functions to create hand which utilized the deck class and hand class.
# also uses sensors and action to choose to hit or stand for the player
#based on hand values.

class BlackjackEnv(Environment):

  # the number of action values the environment accepts
  #indim = 2

  # the number of sensor values the environment produces
  #outdim = 21

  def __init__(self, GameDeck):
    self.gameDeck = GameDeck
    self.indim = 2
    self.outdim = 32

  def createHand(self):
    self.hand = BlackjackHand(self.gameDeck)
    self.hand.getHand()

  def getSensors(self):
    handValue = self.hand.getValue()-1
    return [float(handValue),]

  def performAction(self, action):
    if action == 0.:
      self.hand.hit()
    return action

  def reset(self):
    self.gameDeck.shuffleDeck()
    self.hand.getHand()
