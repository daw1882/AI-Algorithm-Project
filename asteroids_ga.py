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


class GA_Agent():

    def __init__(self):
        """
        Initialize environment

        Returns
        -------
        None.

        """
        self.args = asteroids_exp.parse_args()
        self.args['visual'] = True
        self.env_state, self.window_width, self.window_height  = asteroids_exp.init_asteroid_model(self.args)
        self.view = None
        
        
    # maybe have class here for a member of the population (soln representation)
    class Chromosome():
        
        def __init__(self):
            self.num_moves = 100
            self.moves = self.init_moves()
            self.fitness = self.score_fitness()
            
            
        def init_moves(self):
            moves = []
            for i in range(self.num_moves):
                time = random.randint(1, 100)
                move_types = ['s','d','e','c']
                move_type = move_types[random.randrange(4)]
                moves.append((move_type, time))
            return moves
        
        # Have fitness func as actual method??? params(member of pop)  
        # should return higher vals for better states
        # possibly: how far state gets across board with 0 collisions + fuel left 
        # at the end
        def score_fitness(self):
            return 0  #DO THIS NEXT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
        # Mutate function params:(child) <- mutate child if random probability
        # DO LAST
        def mutate(self):
            return self
    
        # Reproduce function params(parent1, parent2) <- taken from pop
        # by random selection
        def reproduce(self, mate):
            cutoff = random.randint(1, self.num_moves)
            return self.moves[:cutoff] + mate.moves[cutoff+1:]
        
        
    # initialize the first population
    def init_pop(self):
        population = []
        for i in range(100):
            population.append(self.Chromosome())
        return population
    
    # Random Selection function params:(population, fitness func)
    # probability for each state is percentage of total sum of fitness scores
    def rand_select(self, population):
        return # DO THIS SECOND!!!!!!!!!!!!!!!!!!!!!!!!
    
    # run GA on a pop params(population, fitness func)
        # follow algo in book for steps
        
    def run(self):
        pop = self.init_pop()
        
        i = 0
        while(i < 100):
            new_pop = []
            for i in range(len(pop)):
                x = self.rand_select(pop)
                y = self.rand_select(pop)
                child = x.reproduce(y)
                if random.random() < .1:
                    child.mutate()
                new_pop.append(child)
            pop = new_pop
            i += 1
        # change this to best from population
        return pop[0]



# How to represent population:
    # 1) have a long string of moves, each move repping a single unit of time
    #    and slice between to create new ones (alternatively, have string of
    #    moves with time in 3 digits after it, harder to do)
    
    # 2) Have list of moves (direction, time) and slice the list like a string
    #    to generate new ones. length of list will be 100

test = GA_Agent()

