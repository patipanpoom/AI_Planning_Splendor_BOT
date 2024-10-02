from template import Agent
import random
import Splendor.splendor_utils as utils
import Splendor.splendor_model as model
import numpy as np
import copy

# Create all possible combinations and then filter actions by legal_action
# Create 5 fixed actions
# 0=collect_diff, 1=collect_same, 2=reserve, 3=buy_available, 4=buy_reserve
TYPES_REWARDS = {
                    0: -10,
                    1: -15,
                    2: -30,
                    3: -9,
                    4: -8
                 }

TYPES_INDEX = {
                    'collect_diff': 0,
                    'collect_same': 1,
                    'reserve': 2,
                    'buy_available': 3,
                    'buy_reserve': 4
                 }

class QLearning():
    
    def __init__(self, game_state, agent_id, actions):
        self.id = agent_id
        self.current_game_state = game_state
        self.current_actions = actions
        self.game_rule = model.SplendorGameRule(len(game_state.agents))
        self.discount_factor = 0.5
        self.learning_rate = 0.9
        self.episodes = 20
        
    def get_legal_actions(self, game_state):
        return self.game_rule.getLegalActions(game_state, self.id)
    
    def select_action(self, q_values, state_idx, actions, game_state):
        type_idx = np.argmax(q_values[state_idx])
        type_actions = [action for action in actions if TYPES_INDEX[action['type']] == type_idx]
        q_values_copy = copy.deepcopy(q_values)
        while len(type_actions) == 0:
            # Exclude the current max q_value
            q_values_copy[state_idx][type_idx] = -np.inf
            # Find the next max q_value
            type_idx = np.argmax(q_values_copy[state_idx])
            # Get actions of the newly selected type
            type_actions = [action for action in actions if TYPES_INDEX[action['type']] == type_idx]

        # Get cards on the table
        table_cards = sum(game_state.board.dealt, [])
        # Get agent gem
        agent_gems = game_state.agents[self.id].gems
        # Get noble cards on the table
        noble_cards = game_state.board.nobles
        # Get sorted list of card point
        sorted_card_point, sorted_card_point_real = self.find_most_promissing_cards(table_cards)
        # Get dict of freq colour
        card_colour_freq = self.find_most_promissing_gems(table_cards)
        noble_colour_freq = self.find_noble_freq(noble_cards)
        # Which action in type_actions provide the most promissing
        promissing_actions = np.array([])
        for type_action in type_actions:
            reward = 0
            # If get gem then check with possible card on hand and table
            if 'collect' in type_action['type']:
                if sum(agent_gems.values()) >= 8:
                    reward -= 5
                for gem in type_action['collected_gems']:
                    reward += self.cal_reward(type_action) + card_colour_freq[gem] + noble_colour_freq[gem]
                promissing_actions = np.append(promissing_actions, [reward])
            # If reserve card only reserve the most promissing one 
            elif type_action['type'] == 'reserve':
                if type_action['card'].code in sorted_card_point:
                    reward += sorted_card_point.index(type_action['card'].code) + card_colour_freq[type_action['card'].colour] + noble_colour_freq[type_action['card'].colour]
                promissing_actions = np.append(promissing_actions, self.cal_reward(type_action) + reward)
            # If buy card then check if which card the most promissing
            else:
                if type_action['card'].code in sorted_card_point:
                    reward += sorted_card_point.index(type_action['card'].code) + card_colour_freq[type_action['card'].colour] + noble_colour_freq[type_action['card'].colour]
                else: 
                    reward += card_colour_freq[type_action['card'].colour] + noble_colour_freq[type_action['card'].colour]
                if game_state.agents[self.id].score < 15 and (game_state.agents[self.id].score + type_action['card'].points) >= 15:
                    reward += 1000 
                promissing_actions = np.append(promissing_actions, self.cal_reward(type_action) + reward)
        for action in actions:
            if 'buy' in action['type']:
                if game_state.agents[self.id].score < 15 and (game_state.agents[self.id].score + action['card'].points) >= 15:
                    return action, 1000
        return type_actions[np.argmax(promissing_actions)], max(promissing_actions)
    
    # Find noble cost colour freq
    def find_noble_freq(self, noble_cards):
        card_colour_freq = {
            'black': 0,
            'white': 0,
            'green': 0,
            'blue': 0,
            'red': 0,
        }
        for card in noble_cards:
            for colour, _ in card[1].items():
                card_colour_freq[colour] = card_colour_freq[colour] + 1
        return card_colour_freq
    
    # Get the agent resources including gems and agent cards resources
    def get_agent_resource(self, agent_cards, agent_gems):
        agent_support_gems = {
            'black': 0,
            'white': 0,
            'green': 0,
            'blue': 0,
            'red': 0,
            'yellow': 0,
        }
        for colour, cards in agent_cards.items():
            if "yellow" not in colour:
                agent_support_gems[colour] = agent_support_gems[colour] + len(cards)
        combined_gems = {}
        for key in agent_support_gems.keys():
            combined_gems[key] = agent_support_gems[key] + agent_gems[key]
        return combined_gems
    
    # Find combination of gems that promissing
    def find_most_promissing_gems(self, table_cards):
        card_colour_freq = {
            'black': 0,
            'white': 0,
            'green': 0,
            'blue': 0,
            'red': 0,
        }
        for card in table_cards:
            for colour, _ in card.cost.items():
                card_colour_freq[colour] = card_colour_freq[colour] + 1
        sorted_card_colour_freq = sorted(card_colour_freq, key=lambda x: card_colour_freq[x], reverse=False)
        for i, colour in enumerate(sorted_card_colour_freq):
                    card_colour_freq[colour] = i
        return card_colour_freq
    
    
    def find_most_promissing_cards(self, table_cards):
        # Get sorted list of card base on point
        cards_score = []
        cards_code = []
        for card in table_cards:
            cards_score.append(card.points)
            cards_code.append(card.code)
        sorted_card_point = [cards_code[i] for i in np.argsort(cards_score)]
        sorted_card_point_real = [table_cards[i] for i in np.argsort(cards_score)]
        
        return sorted_card_point, sorted_card_point_real
    
    def cal_reward(self, action):
        if action['type'] == 'collect_diff' or action['type'] == 'collect_same':
            return TYPES_REWARDS[TYPES_INDEX[action['type']]] - len(action['returned_gems'])*2 + len(action['collected_gems'])
        elif action['type'] == 'reserve':
            return TYPES_REWARDS[TYPES_INDEX[action['type']]] - len(action['returned_gems'])*2 + len(action['collected_gems'])
        else:
            noble_reward = 0
            if action['noble']:
                noble_reward = len(action['noble']) * 2
            # Maybe add more about cost
            return TYPES_REWARDS[TYPES_INDEX[action['type']]] + action['card'].points + 1 - len(action['returned_gems']) + noble_reward
     
     
    def compute_td(self, reward, t_q_value, t1_q_values):
        if not t1_q_values:
            return None, None  # If there are no next state Q-values, return None for Q-value and index
        else:
            max_q_value_next_state = max(t1_q_values)
            max_q_value_index = t1_q_values.index(max_q_value_next_state)
            td = reward + (self.discount_factor * max_q_value_next_state) - t_q_value
            return td, max_q_value_index
           
        
    def q_learning(self, game_state):
        round_ahead = 1
        q_values = [[0] * 5] * (round_ahead + 1)
        for _ in range(self.episodes):
            state_idx = 0
            state_copy = copy.deepcopy(game_state)
            for i in range(round_ahead):
                if state_copy.agents[self.id].score >= 15:
                    break
                t_actions = self.get_legal_actions(state_copy)
                t_action, _ = self.select_action(q_values, state_idx, t_actions, state_copy)
                # Use Action for Agent0 and get new state
                self.game_rule.generateSuccessor(state_copy, t_action, self.id)
                t1_actions = self.get_legal_actions(state_copy)
                t1_action, t1_reward = self.select_action(q_values, state_idx, t1_actions, state_copy)
                t1_reward = self.cal_reward(t1_action)
                t_q_value = q_values[state_idx][TYPES_INDEX[t_action['type']]]
                td, q_index = self.compute_td(t1_reward, t_q_value, q_values[state_idx + 1])
                q_values[state_idx][q_index] = t_q_value + self.learning_rate * td
                state_idx += 1
        best_action, _ = self.select_action(q_values, 0, self.current_actions, game_state)
        return best_action
    
# First version ignore opponent resources
class myAgent(Agent):
    def __init__(self,_id):
        super().__init__(_id)
    
    def SelectAction(self, actions, game_state):
        policy = QLearning(game_state, self.id, actions)
        action = policy.q_learning(game_state)
        return action
