# UoM COMP90054 Splendor Contest Project

## Team Members
* QUANG CAT TUONG DUONG - quangcattuon@student.unimelb.edu.au - 1266256
* PATIPAN ROCHANAPON - prochanapon@student.unimelb.edu.au - 1117537
* ZHIQUAN LAI - zllai@student.unimelb.edu.au - 1118797


## Table of Content
This Wiki can be used as external documentation to the project.
1. [Home and Introduction](https://github.com/COMP90054-2024s1/a3-jmp/wiki)
2. [Problem Analysis](Problem-Analysis)

    2.1 [Q-learning](Q-learning)

    2.2 [Monte Carlo Tree Search](monte-carlo-tree-search)

    2.3 [Minimax](Minimax)

    2.4 [Breadth First Search](BFS)

3. [Experiments](Experiments)
4. [Conclusions and Reflections](Conclusions-and-Reflections)


## Game Overview
### Game elements
There are three main components in Splendor: gem tokens, development cards, and nobles.

* Gem Tokens: There are five types of gem tokens, with a total of 40 tokens: 7 emerald, 7 sapphire, 7 ruby, 7 diamond, 7 onyx, and 5 gold. Players can collect either two gems of the same color or three gems of different colors. Collected gems are used to buy development cards according to their cost.

* Development Cards: There are 90 development cards that can be either on the table or previously reserved. A development card has three components: prestige points, cost, and a bonus. Development cards are classified into three levels, with the required resources increasing as the level increases.

* Nobles: In a two-player game, there are 3 noble tiles selected from a total of 10. Each noble tile consists of specific bonuses, and players who meet the requirements to attract a noble gain 3 prestige points.

### Gameplay
* Table configuration:
    * Each player starts with no resources or reserved cards.
    * On the table, there are 4 cards from each of the three levels and 3 noble tiles.

* Turn play:
    * During a turn, a player can take one of the following five actions: 
        1. Collect 3 different gems.
        2. Collect 2 gems of the same color.
        3. Buy a reserved card.
        4. Reserve a card from the table.
        5. Buy an available card from the table.

