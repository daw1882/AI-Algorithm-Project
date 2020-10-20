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

POPSIZE = 10
ITERATIONS = 750
NUM_MOVES = 20
MUTATE_NUM = 7
#TIME_BOUND = window_width



class Chromosome(object):
        
    def __init__(self, moves, outer):
        """
        Initialize a chromosome

        Parameters
        ----------
        moves : List
            all the moves to make for this chromosome.
        outer : GA_Agent
            GA_Agent to access info from.

        Returns
        -------
        None.

        """
        self.outer = outer
        self.num_moves = NUM_MOVES
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
        """
        Give a fitness score for the Chromosome

        Parameters
        ----------
        outer : GA_Agent

        Returns
        -------
        integer
            Fitness score for the Chromosome.

        """
        env = outer.init_env_state()
        how_far = 0
        for move in self.moves:
            direction = move[0]
            xv, yv = self.get_move(direction)
            env = asteroids_exp.move(env, xv, yv, move[1], outer.window_width, outer.window_height, outer.args, lambda x: asteroids_exp.render(outer.view, x))
            if env.goal == asteroids_exp.Goal.FAIL:
                #print("fail")
                return how_far #env.ship.fuel + 
            elif env.ship.x > outer.window_width and env.goal == asteroids_exp.Goal.SUCCESS:
                return  outer.window_width+1001 + env.ship.fuel*100 
            else:
                #print("ok")
                how_far = env.ship.x
            #print(env.ship.fuel)
        return how_far*10 + env.ship.fuel*10

    # Mutate function params:(child) <- mutate child if random probability
    # DO LAST
    def mutate(self):
        """
        Change a Chromosome slightly to alter the population.

        Returns
        -------
        Chromosome
            Modified chromosome.

        """
        for i in range(MUTATE_NUM):
            time = random.randint(1, int(self.outer.window_width/2))
            move_types = ['s','d','e','c']
            move_type = move_types[random.randrange(4)]
            idx = random.randint(0, self.num_moves-1)
            #print("length:", len(self.moves))
            self.moves[idx] = (move_type, time)
        return self

    # Reproduce function params(parent1, parent2) <- taken from pop
    # by random selection
    def reproduce(self, mate, outer):
        """
        Generate an offspring for the new population

        Parameters
        ----------
        mate : Chromosome
            second Chromosome to reproduce with.
        outer : GA_Agent
            Agent to get info from for the environment.

        Returns
        -------
        Chromosome
            Child of the two Chromosome's given.

        """
        cutoff = random.randint(1, self.num_moves-1)
        moves = self.moves[:cutoff] + mate.moves[cutoff:]
        return Chromosome(moves, outer)

class GA_Agent():

    def __init__(self, args):
        """
        Initialize environment
        Returns
        -------
        None.
        """
        self.args = asteroids_exp.parse_args(args)
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
        """
        Create an initial set of moves for a population member.

        Returns
        -------
        moves : List
            List of moves to make to try and reach goal.

        """
        moves = []
        for i in range(NUM_MOVES):
            time = random.randint(1, int(self.window_width/2))
            move_types = ['s','d','e','c']
            move_type = move_types[random.randrange(4)]
            moves.append((move_type, time))
            
        return moves
        
    # initialize the first population
    def init_pop(self):
        """
        Generate's initial population'

        Returns
        -------
        population : List
            list of Chromosomes.

        """
        population = []
        for i in range(POPSIZE):
            moves = self.init_moves()
            population.append(Chromosome(moves, self))
        return population
    
    def find_fittest(self, pop):
        """
        Search the population for the highest scoring (fittest) member

        Parameters
        ----------
        pop : List
            list of Chromosomes.

        Returns
        -------
        Chromosome
            The fittest member of the pop.

        """
        #print(pop)
        sort_pop = sorted(pop, key=operator.attrgetter('fitness'), reverse=True)
        return sort_pop[0]
    
    # Random Selection function params:(population, fitness func)
    # probability for each state is percentage of total sum of fitness scores
    def rand_select(self, population):
        """
        Select member of population to reproduce based of probability.

        Parameters
        ----------
        population : List
            List of pop members.

        Returns
        -------
        Chromosome
            Chromosome chosen for reproduction.

        """
        total_fit = 1
        for chromosome in population:
            total_fit += chromosome.fitness
        #print(total_fit)
        probs = [0]
        for i in range(len(population)):
            probs.append(population[i].fitness/total_fit + probs[i])
        probs.pop(0)
            
        selection = random.random()
        for i in range(len(probs)):
            if selection <= probs[i] or i == len(probs)-1:
                return population[i]
    
    # run GA on a pop params(population, fitness func)
        # follow algo in book for steps
        
    def run(self):
        """
        Runs the entire Genetic Algorithm

        Returns
        -------
        List
            The best list of moves to make that the algorithm found in 
            given time.

        """
        pop = self.init_pop()
        
        i = 0
        while(i < ITERATIONS):
            new_pop = []
            for j in range(len(pop)):
                x = self.rand_select(pop)
                y = self.rand_select(pop)
                child = x.reproduce(y, self)
                if random.random() < .1:
                    child = child.mutate()
                new_pop.append(child)
            pop = new_pop
            #print(len(pop), i)
            i += 1
        #print(self.find_fittest(pop).fitness)
        return self.find_fittest(pop).moves


if __name__ == "__main__":
    genetic = GA_Agent(None)
    path = genetic.run()
    df = pd.DataFrame(path, columns=['direction','time'])
    df.to_csv((".").join([genetic.args['in'].split(".")[0],"csv"]),index = False)
    

