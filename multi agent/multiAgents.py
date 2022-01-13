# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newXY = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newFoodLst = newFood.asList()

        xy = currentGameState.getPacmanPosition()
        foodLst = currentGameState.getFood().asList()

        minGhostDist = min([manhattanDistance(newXY, state.getPosition()) for state in newGhostStates])

        scoreChange = successorGameState.getScore() - currentGameState.getScore()

        nearestFoodDistance = min([manhattanDistance(xy, food) for food in foodLst])
        newFoodsDistances = [manhattanDistance(newXY, food) for food in newFoodLst]
        newNearestFoodDistance = min(newFoodsDistances) if newFoodsDistances !=[] else 0

        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()

        #better actions get higher results
        if minGhostDist <= 1 or action == Directions.STOP:
            return 0
        elif scoreChange > 0:
            return 4
        elif isFoodNearer > 0:
            return 3
        elif action == direction:
            return 2
        else:
            return 1

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def maxVal(gameState, depth):
            currentDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currentDepth==self.depth:
                return self.evaluationFunction(gameState)
            maxValue = float("-inf")
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0,action)
                maxValue = max (maxValue, minVal(successor, currentDepth, 1))
            return maxValue

        def minVal(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            minValue = float("inf")
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    minValue = min (minValue, maxVal(successor, depth))
                else:
                    minValue = min(minValue, minVal(successor, depth, agentIndex+1))
            return minValue

        actions = gameState.getLegalActions(0)
        currentScore = float("-inf")
        minimaxAction = ""
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            newScore = minVal(nextState, 0, 1)
            if newScore > currentScore:
                minimaxAction = action
                currentScore = newScore
        return minimaxAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxVal(gameState, depth):
            currentDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currentDepth==self.depth:
                return self.evaluationFunction(gameState)
            maxValue = float("-inf")
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0,action)
                maxValue = max (maxValue, expVal(successor, currentDepth, 1))
            return maxValue

        def expVal(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            expValue = float("inf")
            actions = gameState.getLegalActions(agentIndex)
            total = 0
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    expValue = maxVal(successor, depth)
                else:
                    expValue = expVal(successor, depth, agentIndex+1)
                total += expValue
            return float(total)/float(len(actions))

        actions = gameState.getLegalActions(0)
        currentScore = float("-inf")
        expectimaxAction = ""
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            newScore = expVal(nextState, 0, 1)
            if newScore > currentScore:
                expectimaxAction = action
                currentScore = newScore
        return expectimaxAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
