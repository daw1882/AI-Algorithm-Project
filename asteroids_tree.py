import tkinter as tk
import time 
import json
import tkinter
import time
import argparse
import copy
import pandas as pd
import asteroids_exp
import pdb
import heapq

class Agent:

    def __init__(self, args):
        self.args = asteroids_exp.parse_args(args)
        self.args['visual'] = True
        self.state, self.window_width, self.window_height  = asteroids_exp.init_asteroid_model(self.args)
        self.view = None

    def act(self,state,direction,time):
        xv, yv = self.get_move(direction)
        state = asteroids_exp.move(state, xv, yv, time, self.window_width, self.window_height, self.args, lambda x: asteroids_exp.render(self.view, x))
        return state

    def get_move(self,key):
        return asteroids_exp.MOVES[key]


class Search_Agent(Agent):
    class Strategy:
        # Changed to use a min-heap ordered by end_cost
        def __init__(self):
            self.heap  = []
        def next(self):
            return heapq.heappop(self.heap)
        def add(self, node):
            heapq.heappush(self.heap, (node.end_cost, node))

    class Node:
        def __init__(self, parent, state, move, path_cost, end_cost):
            self.parent = parent
            self.state = copy.deepcopy(state)
            self.move = move
            self.path_cost = path_cost
            self.end_cost = end_cost
            self.leaves = {}
            self.visited = {}
        
        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return True
            else:
                return False

        def expand(self, outer):
            # Uses path cost to determine how far along the screen the ship is
            # and uses end cost to keep track of how far the end still is as well
            # as fuel usage
            (direction, time) = self.move
            
            for action in ['d','c','s','e']:
                # note that 's' is also a legal move
                fuel_cost = 0
                move_cost = 0
                # Only continues for multiple s moves
                if self.parent and self.parent.move[0] == action == 's':
                    continue 
                if self.parent and action != self.parent.move[0]:
                    fuel_cost = 1
                
                to_end = outer.window_width - self.path_cost
                lower = 10
                if outer.window_width < 20:
                    lower = 1
                for time in range(50,lower, -1):
                    if action in ('d', 'e', 'c'):
                        move_cost = time
                    state = outer.act(self.state,action,time)
                    # Create the new node with the new costs
                    child = outer.Node(self,state,(action,time), self.path_cost+move_cost, to_end+fuel_cost-move_cost)
                    self.leaves[(action,time)] = child
            return self.leaves.values()
    
    def retrieve_path(self,node):
        if node.parent == None:
            return [node.move]
        else:
            path = self.retrieve_path(node.parent)
            path.append(node.move)
            return path

    def run(self):
        root = self.Node(None, self.state, ('s',0), 0, self.window_width)
        strategy = self.Strategy()
        strategy.add(root)
        try:
            while (True):
                current = strategy.next()[1]
                if current.state.goal == asteroids_exp.Goal.SUCCESS:
                    path = self.retrieve_path(current)
                    #print ("success!")
                    return path
                if current.state.goal == asteroids_exp.Goal.OK:
                    leaves = current.expand(self)
                    for leaf in leaves:
                        strategy.add(leaf)
        except IndexError:
            return []


if __name__ == "__main__":
    heuristic = Search_Agent(None)
    start_time = time.time()
    path = heuristic.run()
    end_time = time.time()
    df = pd.DataFrame(path, columns=['direction','time'])
    df.to_csv((".").join([heuristic.args['in'].split(".")[0],"csv"]),index = False)
    print(end_time-start_time)




       
