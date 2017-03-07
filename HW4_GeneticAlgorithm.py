__authors__ = 'Danh Nguyen and Nick Larson'

import random
import sys
import unittest
import itertools
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *

#for now, the size (length) of a gene
geneSize = 30

#general population size to create
popSize = 8

geneMax = 9

##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "SPORE")

        #list of genes to store our current population of genes
        #each gene containts 11 pair of numbers that represent the layout coordinates
        self.curGenePop = []

        #list to store fitness of each gene in the population
        self.geneFitnessScores = []

        #records number of games agent has played
        self.gamesPlayed = 0

        #stores the most moves taken so far for any games
        self.mostTurnsTaken = 0
        #stores the farthest food distance seen so far
        self.greatestFoodDist = 0
        #turn counter, reset once individual game over
        self.turnCounter = 0

        #self.firstMove

    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        #create an initial set of random genes if we dont have any
        if not self.curGenePop:
            self.initGenePop()

        moves = []
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            #print self.gamesPlayed
            #print self.curGenePop
            #print "new line"
            for coords in self.curGenePop[self.gamesPlayed]:
                moves.append(coords)
            return moves

        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            moves = []
            for i in range(0, 2):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]

    ##########################################################################################
    ################################# HW4: Genetic Algorithm #################################
    ##########################################################################################

    # initGenePop
    # Description: Initializes the population of genes with random values and reset
    #              the fitness list to default values
    #
    # Return: None
    # #
    def initGenePop(self):
        index = 0 #counter for constructs and grass we will place
        count = 0 #counter for gene indexes of population list
        tempList = [] #holds the coordinates in a list

        while count < popSize:
            if index < 11:
                #Choose any x location
                x = random.randint(0, 9)
                #Choose any y location on your side of the board
                y = random.randint(0, 3)
                tup = (x, y)
                tempList.append(tup)
                badCoords = False
                for x,y in itertools.combinations(tempList, 2):
                    if cmp(x,y) == 0: #check that x and y are not the same coords
                        badCoords = True
                if badCoords:#remove the just added index as it was redundant
                    tempList.pop()
                else:
                    index += 1
            else:
                self.curGenePop.append(tempList)
                tempList = [] #empty the the tempList so it can be used again
                count += 1
                index = 0

    # #
    # mateParents
    # Description: Mates two parent genes and returns a child gene
    # Parameters:
    #    parentOne - First gene to mate
    #    parentTwo - Second gene to mate
    #
    # Return: the child gene that's a result of mating
    # #
    def mateParents(self, parent1, parent2):

        #Initialize a point to splt the gene for mating
        geneSplitPos = random.randint(0, len(parent1))

        #mate the two parents thru crossover
        mateOrder = random.randint(0,1)
        if mateOrder == 0:
            child = parent1[:geneSplitPos] + parent2[geneSplitPos:]
        else:
            child = parent2[:geneSplitPos] + parent1[geneSplitPos:]

        #make sure there aren't any duplicates
        #if there is a duplicate, generate a new random value for the 2nd occurance,
        #this also serves as a form of random mutation
        for a, b in itertools.combinations(child, 2):
            if cmp(a,b) == 0:
                print "matching coordinates"
                print "A =" + str(a)
                print "B =" + str(b)
                #Choose any x location
                x = random.randint(0, 9)
                #Choose any y location on your side of the board
                y = random.randint(0, 3)
                b = (x, y)
                print "New B =" + str(b)
        #tempList.append(tup)
        #badCoords = False
        #for x,y in itertools.combinations(tempList, 2):
        #    if cmp(x,y) == 0: #check that x and y are not the same coords
        #        badCoords = True
        #if badCoords:#remove the just added index as it was redundant
        #    tempList.pop()
        #else:
        #    index += 1


        return child


    ##
    #evaluateFitness
    #
    #Description: Looks at the gene and determines its fitness score
    #
    #Parameters:
    #   turns - an integer value that indicats the number of turns taken
    #           by our ai before its epic defeat at the hands of booger
    #
    #Return:
    #       score: the evaluation of the gene
    def evaluateFitness(self, turns):
        score = self.turnCounter
        if score > self.mostTurnsTaken:
            self.mostTurnsTaken = score
        return score
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        #print state layout in first phase of game
        #if self.firstMove:
        #    asciiPrintState(currentState)
        #    self.firstMove = False

        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];


        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];

        if selectedMove.moveType == END:
            self.turnCounter += 1
        return selectedMove

    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #Description: Tells the player if they won or not
    #
    #Parameters:
    #   hasWon - True if the player won the game. False if they lost (Boolean)
    #
    def registerWin(self, hasWon):
        #score the gene, add the score to the fitness list
        self.geneFitnessScores.append(self.evaluateFitness(self.turnCounter))
        print "Fitness list " +str(self.geneFitnessScores)
        #increment number of finished games
        self.gamesPlayed += 1
        print "Game Count " + str(self.gamesPlayed)
        #Reset the turn counter for the next game

        print "Turns this Game " + str(self.turnCounter)
        self.turnCounter = 0

        if self.gamesPlayed == popSize:
            self.gamesPlayed = 0
            self.generateNextGen(self.curGenePop)

    ##
    # generateNextGen
    # Description: Produces next generation of genes from the current population
    #
    # Parameters:
    #   population - the population of genes
    def generateNextGen(self, population):
        #Reset the child populations
        childPop = []
        #use the longest game as the best score to compare the other parents against
        localPerfect = self.mostTurnsTaken * 2
        #reset most turns taken
        self.mostTurnsTaken = 0

        count = 0
        while count < popSize:
            parent1Index = random.choice(range(0, popSize))
            parent2Index = random.choice(range(0, popSize))
            while parent2Index == parent1Index:
                parent2Range = random.choice(range(0, popSize))
            #else:
            #    parent2Range = range(0,parent1Index)
            #parent2Index = random.choice(parent2Range)
            if(parent1Index == parent2Index):
                print "Error, parents indexes are the same for child gene #" + str(count)
                print "parent indexs :" + str(parent1Index) + str(parent2Index)
            parent1 = population[parent1Index]
            parent2 = population[parent2Index]

            summedScores = self.geneFitnessScores[parent1Index] + self.geneFitnessScores[parent2Index]
            passingScore = random.choice(range(0, localPerfect))
            print "passing score :" + str(passingScore)
            print "summed score :" + str(summedScores)
            if summedScores > passingScore:
                count += 1
                childPop.append(self.mateParents(parent1, parent2))
        #reset the fitness scores
        self.geneFitnessScores = []
        #set the new child pop as the current gene population
        self.curGenePop = childPop[:]

################################################################################
## UNIT TESTS
class geneticTests(unittest.TestCase):

    def test_RegisterWin(self):
        #testSize = random.randint(0,10)
        #self.assertFalse(True)
        movesToLose = 10
        #closestDist = 10
        fitness = 0.0
        #registerWin should take movesToLose, and closestDist as variables
        #fitness will be subbed in directly for now, will be updated soon
        fitness = movesToLose*MOVESTAT # + closestDist * ENEMYFOODDIST
        #fitness should equal 10 in this case, pretending best score modifyer is 12
        fitnessPercentage =  fitness/12
        print "Fitness Score:" + str(fitnessPercentage)
        self.assertGreater(1, fitnessPercentage), "Bad score, fitnessPercentage greater than 1"


if __name__ == '__main__':
    unittest.main()
