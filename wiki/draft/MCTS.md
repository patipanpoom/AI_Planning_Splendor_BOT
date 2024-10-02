# AI Method # - Monte Carlo Tree Search
This method is adapted Monte Carlo Tree Search (MCTS) to navigate the decision-making process of splendor. 
 play splendor

# Table of Contents
  * [Motivation](#motivation)
  * [Design Decision](#design-decision)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Challenges](#challenges)
  * [Future improvements](#future-improvements)


### Motivation  
I decided to use the . The main reason for choosing Monte Carlo Tree search (MCTs) framework is the large state space. Because of the large state space and limited time, exploring every state becomes infeasible. In contrast to exhaustive search, MCTS estimates state rewards by running multiple simulations and saves the computational resources.

[Back to top](#table-of-contents)

### Assumption
- Assumes that future states can be explored by running random simulations from the current state to the end of the game.
- UCB1 can balance exploration and exploitation.
- Assumes that future states can be explored by random simulations.

### Design Decision
Splendor is a turn-based game involving strategic interaction between two players. Each player takes an action to finish a turn based on the current game state and anticipating the opponent's moves. Compared to basic MCTs, my agent also simulates the opponent's actions. 

MCTS uses simulation to explore possible future states of the game. By running multiple simulations, MCTS can estimate the long-term value of different actions. I set the simulation depth to 10, because if the depth is too large the reward cannot be accurately estimated and the simulation time is large. However, as a relatively small simulation depth, the quality of heuristic can significantly affect the performance of MCTs 

Inside the MCTS, UCB is used to balance the exploration and exploitation during the selection based on their average reward and the number of times they have been visited. The C parameter is set to be 2.  

Heuristics is a key element of my game agent to explore and evaluate the large amount of game state. My heuristic function consists of three components including score difference (my score - opponent score), number of cards in hand and cost efficiency of gem (ratio of point gain and gem spent).

[Back to top](#table-of-contents)

### Application 
![alt text](images/MCTS/heuristics.png)
![alt text](images/MCTS/node.png)
![alt text](images/MCTS/mcts.png)



[Back to top](#table-of-contents)

### Trade-offs  
#### *Advantages*  
- MCTs effectively handle the large state space in Splendor by estimating the rewards using simulation. Instead of exhaustively exploring all possible states, MCTs estimates the rewards of future states by simulation and balances the exploration and exploitation by UCB strategy. 

- This game agent also considers the multi-player interaction. MCTs simulate the opponent moves and strategies using random simulation,  leading to more robust and competitive gameplay.


#### *Disadvantages*
- trade off between exploration and exploitation
- The heuristic cannot represent the furture state properly 

[Back to top](#table-of-contents)

### Challenges 
- Balancing exploration and exploitation: Ensuring that the MCTS algorithm effectively balances between exploring new actions and exploiting known good actions.

- choosing proper simulation depth: 



[Back to top](#table-of-contents)



### Future improvements  

There are three main directions to improve the current MCTS: better heuristics, heuristic-guided simulation, and tuning hyperparameters.

The quality of heuristics can significantly impact the performance of MCTS, especially with shallow search depths. With shallow depth, most simulations do not reach the goal state, so a well-designed heuristic can provide a better estimation of the future state. In addition to the current heuristics that consider score difference, the number of cards in hand, and cost efficiency, additional factors such as the previous actions and potential future moves, potential nobles and game phase timing.

Second of all, combining heuristics into the simulation phase can significantly improve the quality of the information obtained from simulations.  By guiding simulations with heuristics, the algorithm can focus on more promising paths, leading to more realistic and valuable insights into potential future states. 

Third of all, Fine-tuning hyperparameters, such as the exploration constant c in the UCB formula and the simulation depth, can also lead to better performance of MCTS. The exploration constant balances the trade-off between exploration and exploitation, and finding the optimal value can enhance the search efficiency. Additionally, adjusting the simulation depth to match the complexity of the game phase can improve the accuracy of state evaluations. 




[Back to top](#table-of-contents)