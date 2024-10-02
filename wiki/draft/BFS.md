# AI Method 3 - Breadth First Search

This method employs Breadth-First Search (BFS) combined with hardcoded strategies to prune the search tree in the game of Splendor. The approach implements specific game rules to optimize decision-making and reduce computational overhead.

# Table of Contents
  * [Motivation](#motivation)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Challenges](#challenges)
  * [Future improvements](#future-improvements)



### Motivation  
This game agent is primarily using BFS as its search algorithm with several hardcoded strategies to prune the search tree. 

Considering the Splendor game, there are 12 cards, 6 diamonds, and up to 3 reserved cards. In the worst-case scenario, 2 cards are reserved with all diamonds and all cards available. The action related card is 12+12+2 and the action related to diamond is C(6,3) + 6. Therefore the complexity is bounded by O(32^n).

Because of this exponential complexity, BFS cannot search all possible nodes in the search tree. To manage this, some hard coded strategies have been implemented to prune the search space.

#### Hard coded strategies:
- Only one of the following actions is considered at a time with the following order: buy, collect, reserve.
- For the buy action, never purchase a level 2 card that only offers one point.
- Collect gems if currently holding fewer than 9 gems.
- Reserve cards that are worth more than 2 points.


[Back to top](#table-of-contents)

### Application 
* 'getPrunedActions' is to filter the actions and prune the search tree by some hard-coded rules, which is crucial for decreasing the complexity and improving the efficiency.

  This function categorise actions into three types: buy_actions, collect_actions, and reserve_actions. And filter level 2 cards with 1 point, only considers collect actions if the total number of gems is below 9 and only considers reserve actions if the card's points exceed 2.
  

  ![image (1)](images/BFS/prunedaction.png)



* This is the main BFS framework. It systematically explores potential actions within limited time (1s) or already reached 15 points.

  ![image (1)](images/BFS/selectAction.png)

* The 'getChild' method generates successor states and appends these states to the queue for further exploration.

  ![image (1)](images/BFS/getChild.png)

[Back to top](#table-of-contents)

### Trade-offs  
#### *Advantages*  
- The hardcoded rules for pruning reduce the number of actions to evaluate, speeding up the decision-making process.

- The approach is straightforward to implement and understand, relying on basic BFS and custom pruning criteria.

#### *Disadvantages*
- This method is not felxible, Hardcoded rules may not adapt well to all game situations.

- Pruning may lead to missing out on potentially beneficial actions that are filtered out by the hardcoded rules.

[Back to top](#table-of-contents)

### Challenges
- Balancing pruning rules: Ensuring that the rules are neither too strict nor too lenient, which could either miss good moves or include too many options.

- Time constraints: Managing the limited time available for each decision step, because it is not possible to reach the goal state.

[Back to top](#table-of-contents)



### Future improvements  
- Dynamic Strategy: instead of using the same strategy for every state, a dynamic strategy can be used according to different state of game. For example, the first few round can prefer reserve gem, and in the late game like after round 20 prefer buy beneficial card

- Advanced Algorithm: use other algorithm instead of exhaustive search like Monte Carlo tree search. By simulating multiple, it balanced the exploration and exploitation compared to BFS which exhaustively explored every branch. And the 15 seconds warmup time can be used more efficiently to do the simulation and saved to benefit the search of the child states.

- Game Theory: Splendor is a competitive game, therefore, the opponent's behaviour can also affect the next search space. Using the Minimax algorithm can take the opponent's potential moves into consideration and react accordingly. This would help predict and counter the opponent's strategies, leading to more wins.


[Back to top](#table-of-contents)