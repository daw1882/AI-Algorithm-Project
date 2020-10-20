# Project #1
Dade Wood, daw1882


## Genetic Algorithm
There were two game files that posed the biggest issue for this algorithm: game 7 and game 24. Each of them bring up an issue with the fitness function that is
fairly hard to solve without just increasing the number of iterations the algorithm runs for. 

Game 7 starts the ship with only 2 units of fuel. What this means is that when the fitness function adds the remaining fuel as part of the overall fitness, 
the algorithm can get focused on trying to save as much fuel as possible instead of using all of it which is what is needed in the solution. If the fitness 
function decided to only optimize fuel when a valid solution has been found, then we would get the opposite problem (but for more games) where the algorithm 
would only focus on getting as far as possible without properly managing its fuel consumption on the way there. Ultimately it was decided to keep fuel in as 
part of the intermediate fitness score since the main game it affected was game 7.

Game 24 had a seperate problem. Its issue is that in order to make it fully across the board there are certain points in the environment where it is better 
stand still and wait for a good time to continue onwards. Standing still does not directly impact the fitness score at all so it neither encourages nor discourages
uses this move and thus it often ignores it and focuses on the moves that give the score progress. There's no easy way to account for this in the score and I 
decided to leave it out because if it were included in some form where the "survival time" was used instead, it would encourage the algorithm to just stand in 
place for all moves as long as possible. There may be a way to modify it such that it has enough constraints to be able to account for sitting still but it seemed
overly complex to implement for a single case.




## Simulated Annealing
Simulated Annealing had the exact same problems when it game to games 7 and 24 for its cost function. The two functions are fairly similar so they have the 
same issues for examples such as these.

**\*It should be noted that while game 7 and 24 do fail often for these two algorithms, they do not fail everytime. It is possible for the algorithm to find a solution 
for both but it just depends on the randomization aspect being in its favor.**





## Tree Search
Overall I'd say this was the best option for this task (though its important to note that it likely wouldn't continue to be since it doesn't scale well as the 
probelm size increases). The reason this performed the best and found a solution consistently was because it exhausted all the options to reach the end goal. 
Also, by adding a heuristic to the search, it is able to handle most of the larger problems in a reasonable amount of time since it prunes many of the useless
branches and focuses on the branches most likely to lead to the solution. 




## Figures and Data
### Fuel:
![Fuel Remaining Table](fuel_table.png)
![Fuel Remaining Graph](fuel_bar_graph.png)

### Game Time:
![Game Time Table](game_time_table.png)
![Game Time Graph](gtime_bar_graph.png)

### Run Time
![Run Time Table](sys_time_table.png)
![Run Time Graph](stime_bar_graph.png)
