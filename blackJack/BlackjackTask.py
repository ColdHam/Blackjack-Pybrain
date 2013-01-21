from scipy import clip, asarray
from pybrain.rl.environments.task import Task
from numpy import *

#overridden task class from pybrain for blackjack.

class BlackjackTask(Task):

  def __init__(self, environment):
    self.env = environment

    self.lastReward = 0


  def performAction(self, action):

    self.action = self.env.performAction(action)
    return self.action

  def getObservation(self):

    sensors = self.env.getSensors()
    return sensors

  def getReward(self):
    if self.action == 0:
      if self.env.hand.getValue()-1 < 21:
        self.reward = 0.5
      else:
        self.reward = -2

    currentReward = self.lastReward
    self.lastReward = self.reward

#used to be currentReward here, trying something else
    return self.reward

  @property
  def indim(self):
    return self.env.indim

  @property
  def outdim(self):
    return self.env.outdim

