"""
File: asteroids_sa.py
Desc: Uses simulated annealing to find a path through an asteroid field

@author Dade Wood
"""
import tkinter as tk
import time as t
import json
import tkinter
import time as t
import argparse
import random
import copy
import math
import pandas as pd
import asteroids_exp
import pdb


class SA_Agent():

    def __init__(self):
        """
        Initialize environment and intial solution

        Returns
        -------
        None.

        """
        self.args = asteroids_exp.parse_args()
        self.args['visual'] = True
        self.env_state, self.window_width, self.window_height  = asteroids_exp.init_asteroid_model(self.args)
        self.view = None
        self.solution = []
        self.init_state = [('s', 0), ('d', self.window_width)]
        
     
    def init_env_state(self):
        """
        Re-initialize the environment to reset items like the fuel used

        Returns
        -------
        None.

        """
        self.env_state, self.window_width, self.window_height  = asteroids_exp.init_asteroid_model(self.args)
        
     
    class Node:
        """
        Creates a Node to hold a full solution state and its performance value
        """
        
        def __init__(self, state, outer):
            self.state = state
            self.perf_val = self.act(outer)
     
        
        """simulate a solution, return a reward value (10 points) """

        def act(self, outer):
            """
            Determine the states performance score by stepping through each move
            in the state.

            Parameters
            ----------
            outer : SA_Agent
                The simulated annealing agent the node is inside of.

            Returns
            -------
            integer
                Numerical value for a performance measure. Higher is better.

            """
            outer.init_env_state()
            for move in self.state:
                direction = move[0]
                xv, yv = self.get_move(direction)
                outer.env_state = asteroids_exp.move(outer.env_state, xv, yv, move[1], outer.window_width, outer.window_height, outer.args, lambda x: asteroids_exp.render(outer.view, x))
                if outer.env_state.goal == asteroids_exp.Goal.FAIL:
                    return outer.env_state.ship.x + outer.env_state.ship.fuel
                if outer.env_state.goal == asteroids_exp.Goal.SUCCESS:
                    return outer.env_state.ship.x + outer.env_state.ship.fuel - len(self.state) + 10000
            return outer.env_state.ship.x + outer.env_state.ship.fuel - len(self.state)
        
        
        def get_move(self, key):
            """
            Get the tuple of move values for a given key

            Parameters
            ----------
            key : char
                Character that was pressed to mvoe.

            Returns
            -------
            TYPE
                Tuple of integers.

            """
            return asteroids_exp.MOVES[key]
        
        
        """choose a new random solution, via a local edit of current solution (10 points) """
        
        def get_successor(self, state, outer):
            """
            Return a random successor state by removing or adding a move within
            the state.

            Parameters
            ----------
            state : List
                Contains all the moves in the current state.
            outer : SA_Agent
                Agent that this Node is contained in.

            Returns
            -------
            new_node : Node
                A new node with the random successor to state.

            """
            op_type = random.randrange(2)
            new_state = copy.deepcopy(state)
            
            if op_type == 0 and len(new_state) > 2:
                remove_idx = random.randrange(1, len(new_state))
                new_state.pop(remove_idx)
            else:
                move_types = ['s','d','e','c']
                make_move = move_types[random.randrange(4)]
                time_block = random.randrange(1, outer.window_width)
                start_idx = random.randint(1, len(new_state)+1)
                new_state.insert(start_idx, (make_move, time_block))
                
            new_node = outer.Node(new_state, outer)
            return new_node
                
                        
                    
        
     
    def schedule(self, time):
        """
        The scheduling function used to determine temperature

        Parameters
        ----------
        time : integer
            Number of the current loop.

        Returns
        -------
        TYPE
            0 if there has been 10000 loops, 1/time otherwise.

        """
        if time > 5000:
            return 0
        return 1/time
    


    """run high-level simulated annealing algorithm (30 points)"""
    """determine whether to move to new state or remain in same place (10 points) """

    def run(self):
        """
        Runs the full simulated annealing algorithm

        Returns
        -------
        current : Node
            The node that we are currently using as the solution.

        """
        i = 1
        current = self.Node(self.init_state, self)

        while True:
            temp = self.schedule(i)
            if temp == 0:
                self.solution = current.state
                return current
            next = current.get_successor(current.state, self)
            performance = next.perf_val - current.perf_val
            if performance > 0:
                current = next
            else:
                decision = random.random()
                probability = math.exp(performance/temp)
                if decision <= probability:
                    current = next
            i += 1
            
            
    def check_sol(self):
        """
        Goes through the solution state for this agent and checks to see if it is a failure
        or a success

        Returns
        -------
        None.

        """
        self.init_env_state()
        for move in self.solution:
            direction = move[0]
            xv, yv = asteroids_exp.MOVES[direction]
            self.env_state = asteroids_exp.move(self.env_state, xv, yv, move[1], self.window_width, self.window_height, self.args, lambda x: asteroids_exp.render(self.view, x))
            if self.env_state.goal == asteroids_exp.Goal.FAIL:
                print("failure")
                return
            if self.env_state.goal == asteroids_exp.Goal.SUCCESS:
                print("success")
                return
        
            

a = SA_Agent()

# run the algorithm, print the time it took
start = t.time()
a.run()
end = t.time()
#print(a.solution) # Uncomment for solution list to print
print("Time to Solution:", end-start)
a.check_sol()

# a.solution is a list of ordered pairs of (direction, steps)
df = pd.DataFrame(a.solution, columns=['direction','time'])
df.to_csv((".").join([a.args['in'].split(".")[0],"csv"]),index = False)
