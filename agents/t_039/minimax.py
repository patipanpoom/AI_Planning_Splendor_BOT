from template import Agent
import random
from collections import Counter
import time
import heapq
from Splendor.splendor_model import SplendorGameRule
from copy import deepcopy


COLOURS = ['red', 'green', 'blue', 'black', 'white', 'yellow']
WINNING_SCORE = 15
NOBLES_SCORE = 3


# u can only think for 1 second
THINKTIME = 0.95
THRESHOLD = 9

class myAgent(Agent):


    def __init__(self, _id):
        super().__init__(_id)
        self.rule = SplendorGameRule(2)
        self.id = _id

        # you will always be the max player 
        self.e_id = (self.id+1)%2

    def getPrunedActions(self, state, id):
        total_gems = sum(state.agents[self.id].gems.values())
        actions = self.rule.getLegalActions(state, id)

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
            return buy_actions
        elif collect_actions:
            return collect_actions
        elif reserve_actions:
            return reserve_actions
        else:
            return actions

    def evaluate(self, state):
        my_score = self.utility(state, self.id)
        enemy_score = self.utility(state, self.e_id)
        return my_score - enemy_score

    def max_alpha_beta(self, alpha, beta, depth, currState, player):
        if(depth == 0):
            return self.evaluate(currState)

        maxScore = -float('inf')
        actions = self.getPrunedActions(currState, player)

        for a in actions:
            next_board = self.rule.generateSuccessor(deepcopy(currState), a, player)
            score = self.min_alpha_beta(alpha, beta, depth-1, next_board, self.otherPlayer(player))
            if(score > maxScore):
                maxScore = score
            if(score > alpha):
                alpha = score
            if beta <= alpha:
                break

        return maxScore
    
    def min_alpha_beta(self, alpha, beta, depth, currState, player):
        if(depth == 0):
            return self.evaluate(currState)
        
        minScore = float('inf')
        actions = self.getPrunedActions(currState, player)

        for a in actions:
            next_board = self.rule.generateSuccessor(deepcopy(currState), a, player)
            score = self.max_alpha_beta(alpha, beta, depth-1, next_board, self.otherPlayer(player))
            if(score < minScore):
                minScore = score
            if score < beta:
                    beta = score
            if beta <= alpha:
                break

        return minScore
    
    def otherPlayer(self, player):
        if player == self.id:
            return self.e_id
        if player == self.e_id:
            return self.id

    def SelectAction(self, actions, state):
        infinity = float('inf')
        best_val = -infinity # MAX PLAY - best val is alpha
        beta = infinity
        best_action = actions[0]
        actions = self.getPrunedActions(state, self.id)
        start_time = time.time()

        for action in actions:
            if time.time() - start_time < THINKTIME:
                next_board = self.rule.generateSuccessor(deepcopy(state), action, self.id)
                value = self.min_alpha_beta(best_val, beta, 3, next_board, self.id)
                if (value > best_val):
                    best_val = value
                    best_action = action
            else:
                break

        return best_action
        
    def utility(self, board, id):
        curr_score, curr_gems, curr_gems_cards, curr_nobles = self.get_board_state(board, id)

        normalized_distance = 0
        if (len(curr_nobles)):
            distances_to_nobles = []
            for noble in curr_nobles:
                distance = abs(sum(dict(Counter(noble) - Counter(curr_gems_cards)).values()))
                distances_to_nobles.append(distance)
            total_distance = sum(distances_to_nobles)
            max_distance_per_noble = 15
            max_total_distance = max_distance_per_noble * len(curr_nobles)

            normalized_distance = (1 - (total_distance / max_total_distance))*3

        return curr_score + normalized_distance


    # function to read the state of the board into several dictionaries so it is easier to use later
    def get_board_state(self, state, id):
        score = state.agents[id].score
        gems = {}
        gems_cards = {}
        nobles = []

        ## get the agent's gems and gemcards from state
        this_agent_gems = state.agents[id].gems
        this_agent_cards = state.agents[id].cards

        ## for each colour count it, put it into the count
        for colour in COLOURS:
            this_gems_cards = len(this_agent_cards.get(colour, []))
            total_gems = this_agent_gems.get(colour, 0) + this_gems_cards
            gems[colour] = total_gems
            gems_cards[colour] = this_gems_cards

        for noble in state.board.nobles:
            nobles.append(noble[1])

        ## return dictionaries of the current score, gems, gem cards, and nobles
        return score, gems, gems_cards, nobles
