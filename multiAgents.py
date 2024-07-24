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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        new_pos = successorGameState.getPacmanPosition()
        new_food = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
       

        distance = 0
        ghost = newGhostStates[0].getPosition()
        distance_ghost = manhattanDistance(new_pos,ghost)
        if distance_ghost > 0:
            distance -= 1.1/ distance_ghost

        distances_food = [manhattanDistance(new_pos , x) for x in  new_food.asList()]
        if len(distances_food):
           distance += 1.0 / min(distances_food)
        return distance +successorGameState.getScore()
        


        
        

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState,0)
    
    def minimax(self, gameState,agentIndex):
        best_action = None
        best_value = -float("inf")

        for action in gameState.getLegalActions(agentIndex):
            value = self.min_value(gameState.generateSuccessor(agentIndex, action), 1, 1)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
  
    def max_value(self, gameState,agentIndex, depth):
        if depth > self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        u = -float("inf")

        for a in gameState.getLegalActions(agentIndex) :
            u = max(u, self.min_value(gameState.generateSuccessor(agentIndex, a), 1, depth))
        return u

    def min_value(self, gameState, agentIndex, depth):
        if depth > self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        u = float("inf")

        for a in gameState.getLegalActions(agentIndex):
            if agentIndex + 1== gameState.getNumAgents() :
                u = min(u, self.max_value(gameState.generateSuccessor(agentIndex, a), 0, depth+1))
            else:
                u = min(u, self.min_value(gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth))
        return u
        util.raiseNotDefined()
       

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        alpha = -float('inf')
        beta = float('inf')
        actions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, a) for a in actions]
        max_value = -float('inf')
        goal = 0
        for i in range(len(successors)):
            v = self.value(successors[i], 1, 0, alpha, beta)
            if v > max_value:
                max_value = v
                alpha = v
                goal = i
        
        return actions[goal]
    
        
    def max_value(self, gameState, agentIndex, depth, alpha, beta):
        
        v = -float('inf')
        for a in gameState.getLegalActions(agentIndex):
            v = max(v, self.value(gameState.generateSuccessor(agentIndex, a), 1, depth, alpha, beta))
            if v > beta:return v
            alpha = max(alpha, v)
        return v
        
    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        v = float('inf')
        for a in gameState.getLegalActions(agentIndex):
            if agentIndex + 1 == gameState.getNumAgents():
                v = min(v, self.value(gameState.generateSuccessor(agentIndex, a), 0, depth + 1, alpha, beta))
            else:
                v = min(v, self.value(gameState.generateSuccessor(agentIndex, a), agentIndex + 1, depth, alpha, beta))
            if v < alpha:return v
            beta = min(beta, v)
        return v
        
    def value(self, gameState, agentIndex, depth, alpha, beta):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.max_value(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.min_value(gameState, agentIndex, depth, alpha, beta)
            




        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, a) for a in actions]
        max_value = -float('inf')
        goal = 0
        for i in range(len(successors)):
            v = self.Expectimax(successors[i], 1, 0)
            if v > max_value:
                max_value = v
                goal = i
        
        return actions[goal]
    def Expectimax(self, gameState, agentIndex, depth):
        
        "If requisite no. of searches complete, evaluation function"
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex > 0:
            return self.exp_value(gameState, agentIndex, depth)
        else:
            return self.max_value(gameState, agentIndex, depth)   
    def max_value(self, gameState, agentIndex, depth):
        v = -float('inf')
        for a in gameState.getLegalActions(agentIndex):
            v = max(v, self.Expectimax(gameState.generateSuccessor(agentIndex, a), 1, depth))
        return v
        
    def exp_value(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, a) for a in actions]
        v = 0.0
        for successor in successors:
            if agentIndex + 1 == gameState.getNumAgents():
                v += self.Expectimax(successor, 0, depth + 1)
            else:
                v += self.Expectimax(successor, agentIndex + 1, depth)
        return v/len(successors)
        
    

            
        
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    Για κάθε κατηγορία χαρακτήρων υπολογίζω το κόστος που έχουν στο 
    παιχνίδι το οποίο εξαρτάται από την απόσταση αυτών και του pacman.
    Τέλος επιστρέφω το άρθοισμα αυτών συν του τρέχοντος score του παιχνιδιού

    """
   
    new_pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    food_dist = -float("inf")
    for food in currentGameState.getFood().asList():
        food_dist = max(food_dist,10.0/manhattanDistance(new_pos, food))
    if food_dist>0:
        score += food_dist
    
    for ghost in currentGameState.getGhostStates():
        ghost_dist = manhattanDistance(new_pos, ghost.getPosition())
    if ghost.scaredTimer > 0:
        score += pow(max(8 - ghost_dist, 0), 18)
    else:
        score -= pow(max(7 - ghost_dist, 0), 12)
    capsules_score = -float("inf")
    for capsule in currentGameState.getCapsules():
        capsules_score = max(capsules_score,30.0/manhattanDistance(new_pos, capsule))
    if capsules_score > 0:
        score += capsules_score
    return score





    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
