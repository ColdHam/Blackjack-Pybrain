#Reinforcement Learning Blackjack
#Authors: David Barnes, Carl Oldham

#This program uses the reinforcement learning aspect of pyBrain to
#allow some computer controlled players to play black jack against a
#computer controlled dealer who follows standard casino rules.

#The program has an Ace set as a hard 11. Aces can not be counted as
#a 1. Programming them to count as both would have proved a bit more
#challenging, and we wanted to provide a simple demonstration of what
#could be done with pyBrain. Allowing for Ace to be 1 or 11 would have
#greatly complicated the demonstration of this program. Because Aces
#can be only 11, it is possible for a player and the dealer to be delt
#a 22 from the start, and instanly bust the game. Although this is a
#problem the only other option was to make aces a hard 1, which would never
#allow a player to get delt 21.

#This file is pretty well commented, but the rest of the program is not. Each
#class that this program uses is pretty self explanitory, but does assume that
#the reader has some idea of python, and how pyBrain works.

#This file is not commented as extensively as to what is happening as much as
#the blackjackMulti.py file is. This file is the single player representation
#of the same multi player game in blackjackMulti. blackjackMulti is extensively
#commented about what is happening at each point in the program.

from BlackjackTask import BlackjackTask
from BlackjackEnv import BlackjackEnv
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer

from BlackjackCardDeck import BlackjackCardDeck
from BlackjackDealer import BlackjackDealer


#global GamesAgentWon
GamesAgentWon = 0
#global GamesDealerWon
GamesDealerWon = 0
#global GamesTied
GamesTied = 0
#global TotalGames
TotalGames = 0

def runMainProg():
  # define action value table
  av_table = ActionValueTable(32, 2)
  av_table.initialize(0.)
  for i in range (0,32):
    print "The AV Value At ",i," is: ", av_table.getActionValues(i)

  # define Q-learning agent
  learner = Q(0.5, 0.0)
  learner._setExplorer(EpsilonGreedyExplorer(0,0))
  agent = LearningAgent(av_table, learner)

  #define a blackjack deck
  theDeck = BlackjackCardDeck()

  #define the environment
  env = BlackjackEnv(theDeck)
  env.createHand()

  #define a Dealer
  dealer = BlackjackDealer(theDeck)

  #define the task
  task = BlackjackTask(env)

  #define the experiment
  experiment = Experiment(task, agent)

  #run the game
  for i in range(0,10000):
    playGame(dealer, task, env, experiment, agent)
  print "Games Agent Won: ", GamesAgentWon
  print "Games Dealer won: ", GamesDealerWon
  print "Games Tied: ", GamesTied
  print "Total Games Played: ", TotalGames
  for i in range (0,32):
    print "The AV Value At ",i," is: ", av_table.getActionValues(i)


def playGame(dealer, task, env, experiment, agent):
  global GamesAgentWon
  global GamesDealerWon
  global GamesTied
  global TotalGames

  ExitBool = True
  dealer.createHand()
  while ExitBool:
    print "------------------------------------------"
    print "Player Hand"
    print env.hand.Hand, " ", env.hand.getValue()
    print "Dealer Hand"
    print dealer.getHand(), " ", dealer.getHandValue()
    print
#  experiment.doInteractions(1)
    agent.integrateObservation(task.getObservation())
    rewardFlag = task.performAction(agent.getAction())
#  print "rewardFlag", rewardFlag
    if rewardFlag == 0:
      reward = task.getReward()
#    print "reward from not exit part is", reward
      agent.giveReward(reward)
      agent.learn()
      if reward == -2:
        print "Dealer Hand Doesn't Matter"
        print "Player Busted!"
        GamesDealerWon += 1
        ExitBool = False
    else:
      dealer.playHand()
      if dealer.getHandValue() <= 21:
        if dealer.getHandValue() < env.hand.getValue():
          print "AGENT WON!!!!!!!!!!!!"
          GamesAgentWon += 1
          agent.giveReward(2)
        elif dealer.getHandValue() == env.hand.getValue():
          print "IT WAS A TIE!!!!!!!!"
          GamesTied += 1
          agent.giveReward(0)
        else:
          print "DEALER WON!!!!!!!!!!!"
          GamesDealerWon += 1
          agent.giveReward(-1)
      else:
        print "AGENT WON!!!!!!!!!!!"
        GamesAgentWon += 1
        agent.giveReward(1)
      agent.learn()
#    print "exit bool false"
      ExitBool = False

  TotalGames += 1
  print "Player Hand"
  print env.hand.Hand, " ", env.hand.getValue()
  agent.reset()
  env.reset()
  print "------------------------------------------"
  print
  print

#main execution
if __name__ == "__main__":

  runMainProg()

