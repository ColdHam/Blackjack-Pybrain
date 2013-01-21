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

from BlackjackTask import BlackjackTask
from BlackjackEnv import BlackjackEnv
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.learners import Q, SARSA
from pybrain.rl.experiments import Experiment
from pybrain.rl.explorers import EpsilonGreedyExplorer, DiscreteStateDependentExplorer

from BlackjackCardDeck import BlackjackCardDeck
from BlackjackDealer import BlackjackDealer

import matplotlib.pyplot as plt
from pylab import *

# Number of players that will be playing against the dealer
N = 5

#Some arrays for the games won, and games tied
GamesAgentWon = []
GamesTied = []

#Initialize the games won, and games tied to 0 so that they can
#be accumulated as play goes on.
for i in range (0,N):
  GamesAgentWon.append(0)
  GamesTied.append(0)

#Create a vaiable to hold the total number of games played.
TotalGames = 0

#This is the subroutine called from the main which is listed
#at the bottom of this file.
def runMainProg():
  # define Q-learning agents with different attributes to see
  # which one will come out as the better player.

  # It would be possible to loop through the number of players N
  # and create them, however they would all have to be the same
  # or other code would have to be added to dynamically create
  # thier attributes.
  learner = []
  learner.append(Q(0.9, 0.0))
  learner[0]._setExplorer(EpsilonGreedyExplorer(0.,0.5))
  learner.append(Q(0.5, 0.5))
  learner[1]._setExplorer(EpsilonGreedyExplorer(0.29,0.))
  learner.append(Q(0.1, 0.5))
  learner[2]._setExplorer(EpsilonGreedyExplorer(0.29,0.5))
  learner.append(Q(0.5, 0.0))
  learner[3]._setExplorer(DiscreteStateDependentExplorer(0.,0.5))
  learner.append(Q(0.5, 0.5))
  learner[4]._setExplorer(DiscreteStateDependentExplorer(0.29,0.5))


  #define a blackjack deck
  theDeck = BlackjackCardDeck()

  #define action value table, agent, task, and environment arrays
  av_table = []
  agent = []
  env = []
  task = []

  #Loop through the number of players, and set up the action value table,
  #associated agent, environment, and task, so they can play the game
  for i in range(0,N):
    av_table.append(ActionValueTable(22, 2))
    av_table[i].initialize(0.)
    agent.append(LearningAgent(av_table[i], learner[i]))
    env.append(BlackjackEnv(theDeck))
    env[i].createHand()
    task.append(BlackjackTask(env[i]))

  #define a Dealer
  dealer = BlackjackDealer(theDeck)

  #run the game for a total of 1000 games. This value can be changed.
  for i in range(0,1000):
    #This is the function that plays the game. The code for it is below.
    playGame(dealer, task, env, agent)

  #All of the games have been played, and now the results of the games played, 
  #games won, tied, and lost are displayed.
  for i in range(0,N):
    print "Games Player ",i+1," Won Against The Dealer: ", GamesAgentWon[i]
    print "Games Player ", i+1," Lost Against The Dealer: ", TotalGames - GamesTied[i] - GamesAgentWon[i]
    print "Games Player ",i+1," Tied With The Dealer: ", GamesTied[i]
    print
  print "Total Games Played: ", TotalGames
  print

  #Create some arrays for the action value values, and the hits, and stands.
  #A new array is needed for the AV values because the AV table used for the program
  #is not an array that can be easily used to plot results, so below the AV values are
  #transfered to the array below for processing.
  theAVTables = []
  hits = []
  stands = []

  #Move the values from the AV table to the array created above, and populate the
  #hits, and stands tables as well. The values in these tables will be used in the plot below.
  for i in range(0,N):
    print "Action Table Values for Player ",i+1,":"
    theAVTables.append([])
    hits.append([])
    stands.append([])
    for j in range (0,22):
      print "The AV Value At ",(j + 1)," for Player ",i+1," is: ", av_table[i].getActionValues(j)
      theAVTables[i].append(av_table[i].getActionValues(j))
      hits[i].append(theAVTables[i][j][0])
      stands[i].append(theAVTables[i][j][1])
    print
    print

  subPlotVal = 511

  #The following uses matplot lib to display a nice graph about the results.
  for i in range(0,N):
    plt.figure(1)
    plt.subplot(subPlotVal)
    plot(hits[i],label="Hits")
    plot(stands[i],label="Stands")
    plt.ylabel('Probability')
    plt.title('Player '+ str(i+1))
    plt.axis([0,30,-3,3])
    plt.legend()
    subPlotVal += 1

  plt.xlabel('Hand Value')

  plt.show()


def playGame(dealer, task, env, agent):
  global GamesAgentWon
  global GamesAgent2Won
  global GamesDealerWon
  global GamesTied
  global GamesTied2
  global TotalGames
  global N

  dealer.createHand()

  #used to keep track on whether the player won, lost, or tied dealer
  PlayerResult = []

  print "------------------------------------------"
# print "Player Hand"
  for i in range(0,N):
    print "Player ",i+1," Hand ",env[i].hand.Hand, " ", env[i].hand.getValue()
    PlayerResult.append(0)

# print "Dealer Hand"
  print "Dealer Hand ",dealer.getHand(), " ", dealer.getHandValue()
  print
# experiment.doInteractions(1)
# although in real blackjack, the deal goes last, it was easier to have
# the dealer go first.
  dealer.playHand()

# Each player will take thier turn now. The following for loop loops througn
# all of the players, in this case, 5.
  for i in range(0,N):
    print "----Player",i+1,"'s Turn----"

    #set up a flag to use so that each player will continue playing until
    #they either stand, or bust.
    ExitBool = True

    #Start loop for the turn
    while ExitBool:

      #agent i starts thier turn
      agent[i].integrateObservation(task[i].getObservation())
      actionFlag = task[i].performAction(agent[i].getAction())

      # get the actionflag back, and see what action the player took

      # Action flag == to 0 means that they hit.
      if actionFlag == 0:
        print "Player",i+1," Hits ", env[i].hand.Hand, " ", env[i].hand.getValue()

        #get the reward to pass on to agent
        reward = task[i].getReward()

        # give the reward to the agent
        agent[i].giveReward(reward)

        #Tell the agent to learn now that they have received thier reward.
        agent[i].learn()

        #if the reward received is -2, then the player busted.
        if reward == -2:
          print "Player",i+1," Busted!"
          #Set the result of the hand to -1 since they lost by busting.
          PlayerResult[i] = -1
          #Set the exitbool to false because hand is over from bust
          ExitBool = False


      else:#agent has chosen to stand. Need to compare hand values now
        print "Player",i+1," Stands ", env[i].hand.Hand, " ", env[i].hand.getValue()

        #check to see if dealer busted, and if not
        #get the dealers hand value for comparison
        if dealer.getHandValue() <= 21:
          if dealer.getHandValue() < env[i].hand.getValue():
            #agent won, set rewards, and flags for later processing
            PlayerResult[i] = 1
            GamesAgentWon[i] += 1
            agent[i].giveReward(2)

          #else if the dealer and player tied, do the following
          elif dealer.getHandValue() == env[i].hand.getValue():
            #agent tied dealer, set rewards, and flags
            PlayerResult[i] = 0
            GamesTied[i] += 1
            agent[i].giveReward(0)

          else:
            #dealer beat player, set rewards and flags
            PlayerResult[i] = -1
            agent[i].giveReward(-1)

        else:#dealer busted here, agent won
          #agent won, set reward, and flags
          PlayerResult[i] = 1
          GamesAgentWon[i] += 1
          agent[i].giveReward(1)

        #The outcome of the game for the player is done, tell the player to
        #learn now that the appropriate reward has been given from above.
        agent[i].learn()

        #set exit bool to false because game is over
        ExitBool = False

  #Increment the total number of games player. All players will have
  #taken and completed thier turn by the time the program reaches this point.
  TotalGames += 1

  print #Even though the dealer played his hand first, we print that he is playing now.
  print "Dealer Played His Hand"

  print #Print the final hands for the game.
  print "----Final Hands----"

  #Print each players hand
  for i in range(0,N):
    print "Player",i+1," Hand ",env[i].hand.Hand, " ", env[i].hand.getValue()

  #Print the dealers hand
  print "Dealer Hand ",dealer.hand.Hand, " ", dealer.getHandValue()
  print

  #Print the result of the game for each player
  for i in range(0,N):
    if PlayerResult[i] == -1:
      print "Player",i+1," lost to the Dealer"
    elif PlayerResult[i] == 1:
      print "Player",i+1," beat the Dealer"
    else:
      print "Player",i+1," tied the Dealer"

    #reset the agent and environment for each player to start another game.
    agent[i].reset()
    env[i].reset()

  #Just some lines and space to make the output more readable
  print "------------------------------------------"
  print
  print

#This is the end of the loop for the number of games played by all players.

#main execution
if __name__ == "__main__":

  runMainProg()

