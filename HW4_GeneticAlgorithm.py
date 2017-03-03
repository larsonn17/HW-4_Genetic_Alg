__authors__ = 'Danh Nguyen and Nick Larson'

import random
import sys
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


#comment




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

        self.depthLimit = 1

        #list of lists to store our current population of genes
        self.curGenePop = []

        #list to store fitness of each gene in the population
        self.geneFitnessScores = []

        #index to track which gene in population is next to be evaluated
        self.currentGene = 0

        #records number of games agent has played
        self.gamesPlayed = 0

        self.firstMove

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
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
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
    # Parameters:
    #    currentState - The state of the current game waiting for the player's move (GameState)
    #
    # Return: None
    # #
    def initGenePop(self, geneSize):
        gene = []

        #initialize the two populations
        for i in range(0, popSize):
            #create the genes
            for j in range(0, geneSize):
            gene.append(random.randint(0, geneMax))

        return gene

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
        child1 = parent1[:geneSplitPos] + parent2[geneSplitPos:]
        child2 = parent2[:geneSplitPos] + parent2[geneSplitPos:]


    ##
    # generateNextGen
    # Description: Produces next generation of genes from the current population
    #
    # Parameters:
    #   population - the population of genes
    def generateNextGen(self, population):
        #calculate total fitness across all genes


        #return the new population
        return childPop



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
        if self.firstMove:
            asciiPrintState(currentState)
            self.firstMove = False

        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];

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
        #increment number of finished games
        self.gamesPlayed += 1

        if hasWon:
            print("Player wins the game!")




            #rest number of played games
            self.gamesPlayed = 0
