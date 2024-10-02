# Proble Analysis
## Table of Contents
* [Introduction](#introduction)
* [Game Feature](#game-feature)
* [Complexity and Challenges](#complexity-and-challenges)
    - [Complexity](#complexity)
    - [Limited search time](#limited-search-time)

## Introduction
Splendor is a multi-agent competitive board game where players aim to acquire prestige. In this particular analysis, we focus on two-player games. The objective of Splendor is to gain more than 15 prestige points with the fewest cards possible by purchasing development cards and acquiring nobles.

This analysis covers four aspects: a game overview, the Markov Decision Process model, complexity, and common strategies.

[Back to top](#table-of-contents)

## Game Feature
* Turn base
* Large state space
* Probabilistic transition
* Game theory
* Opportunity cost: buy some card will lose opportunity to buy some other card 
* Time limit

[Back to top](#table-of-contents)

## Complexity and Challenges
### Complexity

Due to the five different types of actions and large amount of elements on the board, the state space in Splendor is enormous. With 12 cards, 6 gem tokens, and up to 3 reserved cards on the table, the worst-case scenario is 2 reserved cards, all 6 gem tokens, and all cards available.

The actions related to cards are 'buy 1 of 12 cards,' 'reserve 1 of 12 cards,' and 'buy 1 of 2 reserved cards.' Therefore, the total resulting state space is 12 + 12 + 2 = 26.

The actions to collect gem tokens are taking 2 of the same gem type or taking 3 of the different gem type. Therefore the the total resulting state space is C(6,3) + 6 = 20 + 6 = 26.

In total, there are maximum 52 potential actions that can be taken in a state, and each action can lead to a different state.

### Limited search time
Because of the large state space, it is impossible to search all possible state within a limited time (1s). This short search period makes exhaustive search methods impractical, and even simulation methods like Monte Carlo Tree Search (MCTS) might not accurately estimate the state. Therefore, heuristics becomes necessary to navigate the vast state space efficiently. A good heuritic can benefit with exhaustive search or simulation search. However, the quality of the heuristic function is crucial, as it significantly affects the accuracy and effectiveness of the search results.


[Back to top](#table-of-contents)

