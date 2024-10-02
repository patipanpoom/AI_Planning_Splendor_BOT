# AI Method 3 - Computational Approach

Our first technique is classical Q-learning

# Table of Contents
  * [Motivation](#motivation)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Challenges](#challenges)
  * [Future improvements](#future-improvements)

### Justification for Technique Selected
The reason why we chose to implement Q-learning is because of its capability to learn and adapt to complex decision-making scenarios iteratively by learning from past experiences and rewards, making it particularly suitable for the dynamic and strategic nature of the game Splendor.

### Motivation  
In the preliminary round, we introduced a variant of classical Q-learning by constraining the number of actions per state to five: collecting different gems, collecting the same gems, reserving a gem, buying a card, and purchasing a reserved card. Additionally, we modified the Q-table update process to consider only the current and next actions. This approach resembles online reinforcement learning, as the model does not simulate potential outcomes beforehand. Instead, it initiates from the current state-action pair and try to simulate one turn ahead to inform its decision-making process. After the preliminary round, we explored the SARSA algorithm to assess if an on-policy approach could enhance our agent's performance. Unlike Q-learning, SARSA does not bootstrap future actions but updates Q-values based on the current action and the next action actually taken. However, becuase the model only consider current and next actions, it may result in decisions yielding uncertain outcomes due to the limited scope of information considered. To improve the model's performance, we incorporate a 15-second precomputation phase to initialize the Q-table. Moreover, instead of solely relying on the Q-table trained during the precomputation phase, we fine-tune it at each state to improve the model's decision-making.

[Back to top](#table-of-contents)

### Application  
Firstly, we would like to explain how we assign rewards to each action. As mentioned in the motivation section, we limit the number of actions for each state to five broad categories. However, by restricting the available actions to these categories, the model cannot determine the best specific action within each category. For example, while the model can decide that the agent needs to pick a gem, it cannot discern which gem to select. Therefore, we iterate through each action within the category selected by our Q-learning algorithm and apply a set of rule-based criteria to assign suitable rewards for each action. The code and explanation below will demonstrate how this process works.

1. Get the best category action from q table, now we get the list of all possible actions belong to that
category. The while loop uses in case the model select category that does not have any valid actions
(empty set).

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/reward1.png)

2. Create a calculate reward function that will penalise the gem return and will give more reward for
more collected gems; card point and noble card.

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/reward2.png)

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/reward3.png)

3. Iterate through each action, and if the action belongs to collecting gems, utilize the 'cal_reward' function to assign higher rewards if the selected gems are the most frequently required gems for all available cards and noble cards.

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/reward4.png)

4. The reward criteria for the reserve and buy actions are similar to the aforementioned process. However, for the buy action, if the action results in the agent's score exceeding 15, assign additional reward to that action. Then return action which has the most reward.

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/reward5.png)

Next we try to implent and test SARSA, the results did not show improved performance. Therefore, we decided to use an initialized Q-table trained during the precomputation phase as our foundation. The code below shows how we train the model during the precomputation phase.

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/train-qlearning.png)

 Now we can evaluate the performance of the actual Q-learning model. However, the model does not perform well because it was trained with only 5 episodes due to the 15-second timeout limitations. Additionally, the dynamic nature of gameplay means the pre-trained Q-learning model might not adapt effectively to new game states. As a result, we decided to continually update the Q-table based on the current game state during actual gameplay. The code below shows how we update the Q-table during each current state.

![My Image](https://github.com/COMP90054-2024s1/a3-jmp/blob/main/wiki/images/q_learning/interact-update-qlearning.png)

This adaptation is crucial because the states encountered during training may differ from those experienced during testing, as per the rules of the Splendor game. By updating the Q-table in real time, our model can better capture and respond to the nuances of the gameplay environment.

[Back to top](#table-of-contents)

### Trade-offs  
#### *Advantages*  
By testing this improved version against the previous one from the preliminary round, our new model demonstrates significant advantages. Specifically, this enhanced model outperforms its predecessor by consistently achieving higher win rates and making more efficient decisions in Splendor gameplay. This improvement is partly due to pretraining the Q-learning model during the precomputation phase, which provides a better initial policy and jumpstarts the learning process. Although limited to 5 episodes due to the 15-second timeout, this pretraining phase allows the model to encounter a variety of game states and refine its strategy. Combined with continual updates to the Q-table based on the current game state during actual gameplay, our model is better equipped to handle the dynamic nature of the game environment.

#### *Disadvantages*
Despite the improvements, our model faces notable disadvantages. The inherent uncertainty regarding opponent actions limits the model's ability to make optimal decisions, as it cannot anticipate the true strategies employed by opponents. Additionally, the limited pretraining phase of only 5 episodes due to the 15-second timeout constraints means the Q-table may not be adequately initialized, potentially leading to poor performance in new or drastically different game states. While real-time updates improve adaptability, they also introduce computational overhead and potential delays, which may not be feasible in all game environments.

[Back to top](#table-of-contents)

### Challenges
One challenge we face is the potential for certain game states to have a large number of possible actions, leading to computational bottlenecks during successor generation. This can cause timeouts, even with only few training episodes. Addressing this requires optimizing algorithms and leveraging parallelisation to efficiently handle large action spaces.

[Back to top](#table-of-contents)

### Future improvements  
For future improvements, our plan is to pre-train the model in advance and fine-tune it by update the Q-table during a 15-second precomputation phase and continuously refine it during gameplay to enhance our model's decision-making capabilities. This strategy aims to make the model more generalisable to the current gameplay environment. Additionally we're considering implementing deep Q-learning techniques. This approach uses neural networks to handle complex decision-making in large and diverse action spaces. By integrating deep Q-learning, we may be able to improve the model's performance and adaptability in Splendor gameplay. 

[Back to top](#table-of-contents)
