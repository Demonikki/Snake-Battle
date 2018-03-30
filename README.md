# Snake Battle - AI
## CSE 150 W18 Extra Credit Report

**Creating and experimenting with multiple AI's performance using a 2-player Snake Battle.**

*Credits: Scriptim's [Snake-Battle](https://github.com/Scriptim/Snake-Battle) for the base game engine*


-----

## Abstract
This paper focuses on the implementation of an AI player for a modified version of the classic ‘Snake’ game. This is implemented using a simple depth-1 “cowardly” search AI, and then improved upon with a depth-3 adversarial search AI. The focus is on improving the win% of the player against other AI over multiple simulations.

## Modifications

This version of Snake has been modified so that 

* There is no ‘candy’ to eat
* There are 2 snakes on the board instead of one
* Each snake grows by length 1 each turn, and the tail end is fixed

### Rules

The goal of the game is to survive for as long as possible without dying. A snake can die by bumping into the boundaries, the other snake, or itself. If one snake dies, the other snake is automatically the winner. If both snakes’ heads bump into each other, the game ends in a Draw. Snakes start at a random location somewhere on the board, and start by facing upward.


## Strategies and Implementation

**Random_ai**

An AI Snake that just moves in a random path. Makes a random move each step and usually self-destructs in a few turns.
Simple_ai
I implemented a simple AI Player that always moves in a diagonal path toward the upper right corner. This is a good baseline against which to test the performance of the other AI.


**Original_ai**

This AI is a Depth-1 search that looks at the current board position, and attempts to move in the direction of least interference i.e. it runs away from walls and the other snake, and attempts to head toward the largest open space. This most closely resembles the original submission from the hackathon submission. Note that this AI does not consider the opponent’s possible movements at all. 


**Adverse_ai**

This improved AI runs a Depth-3 adversarial search that considers all 4 possible moves of the current (max) player, 4 possible moves of the opponent (min-player) and subsequent 4 final moves of the current player. This leads to 4 + 16 + 64 = 84 total game states to be considered. 
This builds off of the Original_ai, but once one move in taken, 4 states for the opponent’s move are created. The score is generated for all of those states and stored. Then, for each of those 4 moves, the player’s head position is moved into 4 more states, and the scores for those are calculated. The final score for the original 4 states is calculated as 	
Max (1st level scores) + Min (2nd level scores) + Max (3rd level scores)
Therefore, this calculates the first move that contains the path that will minimize the opponent’s score and maximize the player’s score. Note that it does not necessarily follow this path – it only returns the first step that should be taken along that path. Subsequent steps are calculated from scratch again.

### Calculating Score
Each AI aims to maximize the score of the board. The score is a measure of how far away from obstacles the player’s head position is. Moving closer toward the opponent’s tail, or the boundaries reduces the score and the likelihood of moving in that direction. Therefore, the score is calculated as the Sum of the squares of distances from obstacles. I square the distances to weigh more heavily toward directions that have more open space (i.e. run away from obstacles).For the opponent (min player), we calculate the score the same way and pick the move that moves it closer to obstacles (lower score). 
