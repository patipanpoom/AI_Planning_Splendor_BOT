import math
import random
from Splendor.splendor_model import SplendorGameRule, SplendorState
from template import Agent
import time
from copy import deepcopy

WARMUP_TIME = 14.5
STEP_TIME = 0.9
NUM_AGENTS = 2
MAX_SIMULATION_DEPTH = 30


def next_id(current_id):
    if current_id == 1:
        return 0
    else:
        return 1


class Node:
    def __init__(self, state: SplendorState, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = None
        self.action = action
        self.game_rule = SplendorGameRule(NUM_AGENTS)


    def is_fully_expanded(self):
        return not self.untried_actions

    def get_best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]
    
class MCTS:
    def __init__(self):
        self.game_rule = SplendorGameRule(NUM_AGENTS)

    def search(self, initial_state, game_startTime):
        start_time = time.time()
        root = Node(initial_state)
        root.untried_actions = self.game_rule.getLegalActions(initial_state, initial_state.agent_to_move)
        while (time.time() - start_time < STEP_TIME
               or time.time() - game_startTime < WARMUP_TIME
               ):
            node = self.select(root)
            score = self.simulate(node.state, start_time, game_startTime)
            self.backpropagate(node, score)

        return root.get_best_child(c_param=0).action

    def select(self, node:Node):
        while node.is_fully_expanded() and node.children:
            node = node.get_best_child()
        if not node.is_fully_expanded():
            return self.expand(node)
        return node

    def expand(self, node:Node):
        action = node.untried_actions.pop()
        next_state = self.game_rule.generateSuccessor(deepcopy(node.state), action, node.state.agent_to_move)
        child_node = Node(next_state, node, action)
        child_node.untried_actions = self.game_rule.getLegalActions(next_state, next_state.agent_to_move)
        node.children.append(child_node)
        return child_node

    def backpropagate(self, node:Node, result):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    def isTerminal(self, state):
        for agent in state.agents:
            if agent.score >= 15 and state.agent_to_move==0: 
                return True
        return False

    def simulate(self, state, start_time, game_startTime):
        my_id = state.agent_to_move

        current_state = deepcopy(state)
        print(current_state)
        depth = 0

        while (not self.isTerminal(current_state)
               and depth < MAX_SIMULATION_DEPTH
               and (time.time() - start_time < STEP_TIME or time.time() - game_startTime < WARMUP_TIME) 
               ):

            action = random.choice(self.game_rule.getLegalActions(current_state, current_state.agent_to_move))

            current_state = self.game_rule.generateSuccessor(current_state, action, current_state.agent_to_move)
            current_state.agent_to_move = next_id(current_state.agent_to_move)
            depth += 1

        my_score = self.game_rule.calScore(current_state, my_id)
        op_score = self.game_rule.calScore(current_state, next_id(my_id))

        if my_score > op_score:
            return 1
        elif my_score == op_score:
            return 0
        else:
            return -1
        # return self.game_rule.calScore(current_state, current_state.agent_to_move)


class myAgent(Agent): 
    def __init__(self, _id):
        super().__init__(_id)
        self.game_rule = SplendorGameRule(NUM_AGENTS)
        self.round = 0
        self.game_startTime = time.time()
        self.mcts = MCTS()

    def getAction(self, game_state):
        return self.game_rule.getLegalActions(game_state, self.id)
    
    def GreedySelection(self, actions, game_state):
        total_gems = sum(game_state.agents[self.id].gems.values())

        buy_actions = [action for action in actions if 'buy' in action['type']]
        if buy_actions:
            return random.choice(buy_actions)
        
        if total_gems <= 8:
            collect_actions = [action for action in actions if 'collect' in action['type']]
            if collect_actions and sum(game_state.board.gems.values()) >= 3:
                return random.choice(collect_actions)
        

        
        reserve_actions = [action for action in actions if  action['type'] == 'reserve']
        if reserve_actions:
            return random.choice(reserve_actions)
        
        return random.choice(actions)
    
    def SelectAction(self, actions, game_state):
        if len(actions) == 1:
            return actions[0]
        
        best_action = self.mcts.search(game_state, self.game_startTime)
        
        if best_action in actions:
            return best_action
        else:
            return self.GreedySelection(actions, game_state)
