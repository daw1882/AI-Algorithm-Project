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
import operator


class Chromosome(object):
        
    def __init__(self, moves, outer):
        self.num_moves = 15
        self.moves = moves
        self.fitness = self.score_fitness(outer)
        

    
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
    
    # Have fitness func as actual method??? params(member of pop)  
    # should return higher vals for better states
    # possibly: how far state gets across board with 0 collisions + fuel left 
    # at the end
    def score_fitness(self, outer):
        env = outer.init_env_state()
        how_far = 0
        for move in self.moves:
            direction = move[0]
            xv, yv = self.get_move(direction)
            env = asteroids_exp.move(env, xv, yv, move[1], outer.window_width, outer.window_height, outer.args, lambda x: asteroids_exp.render(outer.view, x))
            if env.num_collisions > 0:
                return env.ship.fuel + how_far
            else:
                how_far += env.ship.x
        return env.ship.fuel + how_far

    # Mutate function params:(child) <- mutate child if random probability
    # DO LAST
    def mutate(self):
        for i in range(20):
            time = random.randint(1, 100)
            move_types = ['s','d','e','c']
            move_type = move_types[random.randrange(4)]
            idx = random.randint(0, self.num_moves-1)
            #print("length:", len(self.moves))
            self.moves[idx] = (move_type, time)
        return self

    # Reproduce function params(parent1, parent2) <- taken from pop
    # by random selection
    def reproduce(self, mate, outer):
        cutoff = random.randint(1, self.num_moves-1)
        moves = self.moves[:cutoff] + mate.moves[cutoff:]
        return Chromosome(moves, outer)

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
        
    def init_env_state(self):
        """
        Re-initialize the environment to reset items like the fuel used

        Returns
        -------
        None.

        """
        self.env_state, self.window_width, self.window_height  = asteroids_exp.init_asteroid_model(self.args)
        return self.env_state
        
        
    # maybe have class here for a member of the population (soln representation)
    
        
    def init_moves(self):
        moves = []
        for i in range(15):
            time = random.randint(1, self.window_width)
            move_types = ['s','d','e','c']
            move_type = move_types[random.randrange(4)]
            moves.append((move_type, time))
            
        return moves
        
    # initialize the first population
    def init_pop(self):
        population = []
        for i in range(100):
            moves = self.init_moves()
            population.append(Chromosome(moves, self))
        return population
    
    def find_fittest(self, pop):
        #print(pop)
        sort_pop = sorted(pop, key=operator.attrgetter('fitness'), reverse=True)
        return sort_pop[0]
    
    # Random Selection function params:(population, fitness func)
    # probability for each state is percentage of total sum of fitness scores
    def rand_select(self, population):
        total_fit = 0.0
        for chromosome in population:
            total_fit += chromosome.fitness
        probs = [0]
        for i in range(len(population)):
            probs.append(population[i].fitness/total_fit + probs[i])
        probs.pop(0)
            
        selection = random.random()
        for i in range(len(probs)):
            if selection <= probs[i]:
                return population[i]
    
    # run GA on a pop params(population, fitness func)
        # follow algo in book for steps
        
    def run(self):
        pop = self.init_pop()
        
        i = 0
        while(i < 100):
            new_pop = []
            for j in range(len(pop)):
                x = self.rand_select(pop)
                y = self.rand_select(pop)
                child = x.reproduce(y, self)
                if random.random() < .1:
                    child = child.mutate()
                new_pop.append(child)
            pop = new_pop
            print(len(pop), i)
            i += 1
        # change this to best from population
        return self.find_fittest(pop).moves



# How to represent population:
    # 1) have a long string of moves, each move repping a single unit of time
    #    and slice between to create new ones (alternatively, have string of
    #    moves with time in 3 digits after it, harder to do)
    
    # 2) Have list of moves (direction, time) and slice the list like a string
    #    to generate new ones. length of list will be 100

genetic = GA_Agent()
path = genetic.run()
#print(path)
df = pd.DataFrame(path, columns=['direction','time'])
df.to_csv((".").join([genetic.args['in'].split(".")[0],"csv"]),index = False)


