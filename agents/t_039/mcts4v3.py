'''use heuristcs to early stop'''


import math
import random
from Splendor.splendor_model import SplendorGameRule, SplendorState
from template import Agent
import time
from copy import deepcopy

WARMUP_TIME = 14.5
STEP_TIME = 0.9

# Hyperparameter
NUM_AGENTS = 2

MAX_SIMULATION_DEPTH = 7
C_PARAM = 0

THRESHOLD = 9

def next_id(current_id):
    if current_id == 1:
        return 0
    else:
        return 1

def heuristic(state, agent_id):
    agent = state.agents[agent_id]
    opponent_id = 1 if agent_id == 0 else 0
    opponent = state.agents[opponent_id]
    agent_score = agent.score
    agent_num_cards = sum(len(cards) for cards in agent.cards.values())
    agent_num_gems = sum(agent.gems.values())
    opponent_score = opponent.score
    opponent_num_cards = sum(len(cards) for cards in opponent.cards.values())
    opponent_num_gems = sum(opponent.gems.values())
    agent_value = agent_score + 0.1 * agent_num_cards + 0.01 * agent_num_gems
    opponent_value = opponent_score + 0.1 * opponent_num_cards + 0.01 * opponent_num_gems
    return agent_value - opponent_value

def heuristic_v3(state, agent_id):
    agent = state.agents[agent_id]
    opponent = state.agents[next_id(agent_id)]
    score_diff = agent.score - opponent.score
    num_cards = sum(len(cards) for cards in agent.cards.values())
    opponent_num_cards = sum(len(cards) for cards in opponent.cards.values())

    gem_cost_efficiency = 0
    for color, cards in agent.cards.items():
        for card in cards:
            gem_cost = sum(card.cost.values())
            if gem_cost > 0:
                gem_cost_efficiency += card.points / gem_cost

    return (score_diff * 10) - num_cards + (gem_cost_efficiency * 5) - (opponent_num_cards * 2)


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

    def isTerminal(self, state):
        for agent in state.agents:
            if agent.score >= 15 and state.agent_to_move==0: 
                return True
        return False

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

        return root.get_best_child(c_param=C_PARAM).action

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

    def simulate(self, state, start_time, game_startTime):
        my_id = state.agent_to_move
        current_state = deepcopy(state)
        depth = 0

        while (not self.isTerminal(current_state)
               and depth < MAX_SIMULATION_DEPTH
               and (time.time() - start_time < STEP_TIME or time.time() - game_startTime < WARMUP_TIME) 
               ):
            
            action = random.choice(self.game_rule.getLegalActions(current_state, current_state.agent_to_move))

            current_state = self.game_rule.generateSuccessor(current_state, action, current_state.agent_to_move)
            current_state.agent_to_move = next_id(current_state.agent_to_move)
            depth += 1
            
        return self.heuristic_evaluation(current_state, my_id)

    def heuristic_evaluation(self, state, agent_id):
        return heuristic(state, agent_id)
        # return heuristic_v2(state, agent_id)

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
        '''
        rules:
            1. action prioirty: buy, collect, reserve
            2. never buy level 2 card with 1 point
            3. do not collect gems if number of gems in hand exceeds a THRESHOLD 
            4. do not reserve card less than 2 point 
            5. buy card with largest prestige point gain
        '''

        total_gems = sum(game_state.agents[self.id].gems.values())

        buy_actions, collect_actions, reserve_actions = [], [], []
        for action in actions:
            if 'buy' in action['type']:
                if not (action['card'].deck_id + 1 == 2 and action['card'].points == 1):
                    buy_actions.append(action)
            
            elif 'collect' in action['type']:
                if total_gems <= THRESHOLD:
                    collect_actions.append(action)
            
            elif action['type'] == 'reserve':
                if action['card'].points > 2:
                    reserve_actions.append(action)

        if buy_actions:
            
            return buy_actions.sort(key=lambda x: x['card'].points, reverse=True)[0]
        elif collect_actions:
            return random.choice(collect_actions)
        elif reserve_actions:
            return random.choice(reserve_actions)
        else:        
            return random.choice(actions)
    
    def SelectAction(self, actions, game_state):
        if len(actions) == 1:
            return actions[0]
        
        best_action = self.mcts.search(game_state, self.game_startTime)
        
        if best_action in actions:
            return best_action
        else:
            return self.GreedySelection(actions, game_state)
