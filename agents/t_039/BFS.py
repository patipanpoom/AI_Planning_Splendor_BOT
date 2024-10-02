import math
import random
from Splendor.splendor_model import SplendorGameRule, SplendorState
from template import Agent
import time
from copy import deepcopy
from collections import deque
import numpy as np

PREPARE_TIME = 14.5
STEP_TIME = 0.95
NUM_AGENTS = 2

THRESHOLD = 9

class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.rule = SplendorGameRule(NUM_AGENTS)
        self.state = SplendorState(NUM_AGENTS)

    # use some hard coded rules to prune the search tree
    def getPrunedActions(self, state):
        total_gems = sum(state.agents[self.id].gems.values())
        actions = self.rule.getLegalActions(state, self.id)

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
            return buy_actions, 'b'
        elif collect_actions:
            return collect_actions, 'c'
        elif reserve_actions:
            return reserve_actions, 'r'
        else:
            return actions, None

    
    def SelectAction(self, actions, state):

        startTime = time.time()
        queue = deque([(deepcopy(state), [])])
        curScore = self.rule.calScore(state, self.id)

        while len(queue) > 0 and (time.time() - startTime) < STEP_TIME:
            state, path = queue.popleft()
            score = self.rule.calScore(state, self.id)
            x = len(state.agents[self.id].agent_trace.action_reward)

            # terminate if already find a path reach 15
            if score >= 15: 
                return path[0]
            
            selected_action = self.getPrunedActions(state) 
            
            new_actions, actionsType = selected_action
            self.BFS(new_actions, state, queue, path, actionsType)

            selected_action = path[0] if path else random.choice(new_actions)
            print(f'my agent id {state.agent_to_move}')

            print(self.rule.generateSuccessor(deepcopy(state), selected_action, self.id).agent_to_move)

        return path[0] if path else random.choice(new_actions)

    def BFS(self, actions, state, queue, path, actionsType):

        if actionsType == 'b':
            actions.sort(key=lambda x: x['card'].points, reverse=True)

        for action in actions:
            if actionsType:
                next_state = self.rule.generateSuccessor(deepcopy(state), action, self.id)
                # print(next_state.agent_to_move)
                next_path = path + [action]
                queue.append((next_state, next_path))
                return
        
    
