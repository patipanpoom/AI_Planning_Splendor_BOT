# Experiment
This section of our wiki outlines what experiments we did throughout our work to find out the pros and cons of each agent. Each experiment was conducted as such:
* Play 10 games, alternating who starts
* The actions from several games were analyzed to see why an agent is dominant over another.
* Ideas of changes to be made to improve the performance is discussed

## BFS vs Greedy
### Scores:
| Match  | BFS | Greedy |
|--------|--------|--------|
| 1      | 16     | 9      |
| 2      | 16     | 3      |
| 3      | 2      | 15     |
| 4      | 12     | 17     |
| 5      | 16     | 5      |
| 6      | 16     | 15     |
| 7      | 16     | 11     |
| 8      | 15     | 14     |
| 9      | 18     | 6      |
| 10     | 15     | 5      |

BFS wins with a score of 8 wins
* The greedy agent will perform any buy it can and if not it will randomly pick to collect. 
* Sometimes was lucky and as able to beat the BFS agent because it bought a lot of gems that the noble took interest in.
* BFS is dominant over greedy in this case because our greedy agent just takes the next best move, our BFS picks the first move that has a path to victory, so at some point it will reach. 
* We need to find a way to modify the BFS agent so that it can look to collect gems if it is close to noble. 


## BFS vs MCTS
### Scores:
| Match  | BFS    | MCTS   |
|--------|--------|--------|
| 1      | 15     | 10     |
| 2      | 11     | 17     |
| 3      | 11     | 15     |
| 4      | 18     | 12     |
| 5      | 10     | 15     |
| 6      | 15     | 10     |
| 7      | 15     | 7      |
| 8      | 16     | 14     |
| 9      | 9      | 16     |
| 10     | 13     | 15     |

BFS and MCTS tied with 5 wins each
* Through looking at the games it seems that it was very close and in most cases one agent was able to beat the other because a noble had taken interest. Whilst there is still no priority coded, it is clear that collecting nobles caused each agent the win.
* In game 10, in 1 turn MCTS was able to gain 7 points making it go from 6 to 15 and win in a single turn. This is because it bought a card worth 4 points and a noble also took interest. This kind of move is very powerful and we should think about agents that are able to implement this. 
* It is also interesting to see the MCTS uses its 15 second 1st turn computation time, sometimes it does a reserve yet never proceeds to buy from reserve. It seems that it believes that the gold gem is very important, as you can buy your first card faster? However we should think about this. 
* It is hard to say which agent performed better in this case as it was a tie. It seems like the agent that is able to collect more nobles won
* Although looking at the games it seems that MCTS is better the BFS. This is because it is able to make moves with long term rewards. Our BFS agent was likely able to win in most cases because we have a pruning method that removes "bad" moves
* Coding some sort of noble priority functionality here will help the agent a lot. 

## MCTS vs Minimax 
### Scores:
| Match  | MCTS   | Minimax|
|--------|--------|--------|
| 1      | 11     | 16     |
| 2      | 12     | 16     |
| 3      | 6      | 15     |
| 4      | 5      | 19     |
| 5      | 6      | 15     |
| 6      | 14     | 15     |
| 7      | 17     | 12     |
| 8      | 15     | 17     |
| 9      | 14     | 22     |
| 10     | 13     | 17     |

Minimax wins with a score of 9 wins
* MCTS seems to have a habit of reserving cards just to use the gold gems
* Since MCTS has no noble configuration, it only ever won if it bought high value cards faster
* Minimax is dominate over MCTS in this game because of how efficient Minimax is at 2 player games. Since it is able to predict that each player will play optimally, it will always get the board it predicted or better.
* Whilst MCTS uses UCB to calculate exploration vs exploitation, this means that the predicted paths might not be the optimal moves. 
* It seems that even coding a little bit of noble functionality goes a long way, this is because you can not reserve nobles

## Minimax vs Qlearning
### Scores
| Match  | Minimax | QLearning |
|--------|--------|--------|
| 1      | 16     | 4      |
| 2      | 12     | 15     |
| 3      | 13     | 15     |
| 4      | 17     | 11     |
| 5      | 14     | 15     |
| 6      | 12     | 18     |
| 7      | 16     | 10     |
| 8      | 11     | 18     |
| 9      | 15     | 14     |
| 10     | 16     | 12     |

Minimax and Qlearning tied with 5 wins each.
* Whilst this was a tie, q learning is still better (discussed below)
* Who won each game was heavily decided on these factors:
    * Who went first
    * If there was a dominant gem colour
    * Who got the nobles interest faster
    * If they are aiming for the same card
* Games were there was a more dominant colour (ie most cards can be on discount with the same gem colour) Q learning was far better than Minimax. This is because through training, it is able to see the long term impact of moves whilst minimax can only see 3 moves ahead.
* Games where there was no dominant colour, Minimax was able to beat Qlearning; this is because it often just bought gems cards that would bring it closer to a noble and intern closer to the cards on the board

![image (1)](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/a8db6702-e0f1-43c3-8b2d-7047494b84fd)

* One interesting game which show cased that Q learning was more efficient than Minimax was shown in this screenshot, here we can see that Q learning was able to take the card that minimax was aiming for. You can see how Qlearning reserves a 5 score 7 blue 3 green that Minimax is very close to buying. This what caused Minimax to lose as it can could not predict this with only looking at 3 moves ahead. 
* Another interesting game was here (just interesting to include) where minimax won because it top decked a card ! This shows that there is always a bit of luck even if you do play optimally

![1](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/76bcd252-571b-439f-9429-4646c498a063)
Qlearning (agent 0) did the best move where it can buy the 5 point card, this wouldve given it a very large advantage over Minimax

![2](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/815469de-1a3e-4cc0-aa79-3f7bc042cf8a)
The card that was replaced was a 5 point card that Minimax had the perfect number of gems for ! this gace Minimax 16 points to win the game!



Through our experiments we learned several things and placed it into our final agent. Whilst it is important to prioritize gem cards that brought you closer to a noble, it is also important to see what gems will reap long term rewards (gems that will give you discount for many cards). Due to nature of this game where building a lot of the same colours requires a lot of steps, our Qlearning algorithm was deemed most suitable for this game. 

