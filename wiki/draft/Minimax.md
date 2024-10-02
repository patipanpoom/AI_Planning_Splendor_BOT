# AI Method 1 - Minimax with Alpha-Beta pruning

# Table of Contents
  * [Motivation](#motivation)
  * [Application](#application)
  * [Trade-offs](#trade-offs)     
     - [Advantages](#advantages)
     - [Disadvantages](#disadvantages)
  * [Challenges](#challenges)
  * [Future improvements](#future-improvements)



### Motivation  
Minimax is very well-suited to 2 player because when you consider 2 players who play optimally, you will always get your predicted best reward or better (if they play sub-optimally you will reap a better reward). It is also appropriate to perform minimax as game is semi-deterministic as the only thing you can’t see is what card will draw next. This is only a small amount of uncertainty as you should be able to win the knowledge of how many gems you and have opponent has as well as what cards are available to buy. We are also able to code our own utility function as we know some strategies to help us play the game. 

[Back to top](#table-of-contents)

### Application 
Since there was already a class called SplendorGameRule that you are able to generate the successor board from a {state, action, player_id}, it was relatively easy to implement minimax here. I have just used the general template for an minimax algorithm with alpha beta pruning and the only key difference is the evaluate function. 
My evaluate function is as follows:
![image](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/aa10cfee-53df-4b00-a36c-53d634b426d9)

Since each agent is able to keep track of its own ID and the opponentID, we can just assume that it will always be the max player that calls the SelectAction.
![image](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/ff50e3cc-2d05-4124-bb80-10e828564286)
I have also chosen for it to have a depth of 3 because I believe 3 is the sweet spot for predicting actions within the time limit. The utility function was is also relatively simple. It is measured by the total score as well as how many gem cards you need to get to the nearest noble. 

Here we can see how the alpha_beta functions were implemented
![image](https://github.com/COMP90054-2024s1/a3-jmp/assets/140671016/da2d01ef-b3f2-4499-83cb-4ebfb6c1ffb3)
To prune actions early, it will break when the score is not in bounds. We can also see the otherplayer function, or the successor player. 

[Back to top](#table-of-contents)

### Trade-offs  
#### *Advantages*  
* You will always get the maximizing score you predicted or better; as discussed above, since minimax looks at future actions and predicts that the other player also does, an opponent you would have picked the best option for an agent that plays optimally. 
* Looking at reserve actions or in general what actions our opponent will perform; it is hard to measure how good a reserve action is with 1 depth because we can not see what actions an adversary can take. A good example is that we have been collecting specific gems to buy a card, but our opponent decides to reserve or buy it first. Since minimax is able to look at the opponent’s future actions, it is able to understand how good a reserve action is compared to other agents.
* Buying nobles: since there is some priority to attract a nobles attention and nobles are not able to be reserved, Minimax is able to see and collect different colours fast. 

#### *Disadvantages*
* Search tree is quite large; although we have implemented alpha beta pruning to narrow down the search tree, the tree is still relatively big. This is because at every state an agent can perform upwards of 50 actions. This really big branching factor makes it really hard to compute within the thinktime. 
* Limitation of depth: Our depth can only look at 3 actions ahead which means actions that have good effects in longer then 3 actions are not accounted for
* Long term rewards: Minimax is unable to learn that some gem colours are better then others, if the card generates and there are many cards that need a specific colour, it is unable to predict this in 3 moves. 

[Back to top](#table-of-contents)

### Challenges
* Utility Function: It was very hard to come up with a good utility function that was able to measure how good a board is
* Time: instead of implementing a general minimax function I also added alpha beta pruning in hopes of being able to get the complete tree before the think time.
* Pruning bad actions: I have used our findings from BFS to prune bad actions earlier as well as alpha beta pruning, yet it seems that I am unable to do a search depth of anything more then 3. It would have been nice to do 5 or more. 


[Back to top](#table-of-contents)

### Future improvements  
* Have some way to measure how good gem colours are: as discussed in the disadvantages, Having some way to say this gem colour should be prioritised over another colour would be nice 
* Ordering my actions: This could be ordering them in a way that the predicted better actions could go first. This will help with pruning branches earlier and possibly let me increase the depth


[Back to top](#table-of-contents)
