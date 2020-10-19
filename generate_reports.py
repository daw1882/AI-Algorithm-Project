import os
import time
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
import numpy as np

import asteroids_ga
import asteroids_tree
import asteroids_sa
import asteroids_exp

indices = [i for i in range(25)]
line_args = "-i asteroid_game_{:d}.json"


def get_ga_stats():
    ga_fuel = []
    ga_game_time = []
    ga_sys_time = []
    for i in range(25):
        print("Iteration " + str(i) + ": ", end='')
        GA = asteroids_ga.GA_Agent(line_args.format(i))
        start = time.time()
        GA_path = GA.run()
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(GA_path, args)
        
        ga_fuel.append(fuel_left)
        ga_game_time.append(game_time)
        ga_sys_time.append(round(end-start, 4))
        
    return ga_fuel, ga_game_time, ga_sys_time


def get_sa_stats():
    sa_fuel = []
    sa_game_time = []
    sa_sys_time = []
    for i in range(25):
        print("Iteration " + str(i) + ": ", end='')
        SA = asteroids_sa.SA_Agent(line_args.format(i))
        start = time.time()
        SA_path = SA.run()
        #print(SA_path)
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(SA_path, args)
        
        sa_fuel.append(fuel_left)
        sa_game_time.append(game_time)
        sa_sys_time.append(round(end-start, 4))
        
    return sa_fuel, sa_game_time, sa_sys_time


def get_tree_stats():
    tree_fuel = []
    tree_game_time = []
    tree_sys_time = []
    for i in range(25):
        print("Iteration " + str(i) + ": ", end='')
        tree = asteroids_tree.Search_Agent(line_args.format(i))
        start = time.time()
        tree_path = tree.run()
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(tree_path, args)
        
        tree_fuel.append(fuel_left)
        tree_game_time.append(game_time)
        run_time = end-start
        tree_sys_time.append(round(run_time, 4))
        
    return tree_fuel, tree_game_time, tree_sys_time

def one_iteration():
    # print("----- GENETIC START -----")
    # fuel, g_time, s_time = get_ga_stats()
    # print("----- GENETIC DONE -----")
    # fuel_table = {'Game #': indices, 'Genetic Algorithms': fuel}
    # game_table = {'Game #': indices, 'Genetic Algorithms': g_time}
    # sys_table = {'Game #': indices, 'Genetic Algorithms': s_time}
    #print(pd.DataFrame(fuel_table))
    
    print()
    print("----- ANNEALING START -----")
    fuel, g_time, s_time = get_sa_stats()
    print("----- ANNEALING DONE -----")
    # fuel_table['Simulated Annealing'] = fuel
    # game_table['Simulated Annealing'] = g_time
    # sys_table['Simulated Annealing'] = s_time
    
    # print()
    # print("----- TREE SEARCH START -----")
    # fuel, g_time, s_time = get_tree_stats()
    # print("----- TREE SEARCH DONE -----")
    # fuel_table['Tree Search'] = fuel
    # game_table['Tree Search'] = g_time
    # sys_table['Tree Search'] = s_time
    
    # print()
    # print("------ RESULTS -------")
    # fuel_table = pd.DataFrame(fuel_table)
    # game_table = pd.DataFrame(game_table)
    # sys_table = pd.DataFrame(sys_table)
    # print("FUEL:")
    # print(fuel_table)
    
    # print()
    # print("GAME TIME:")
    # print(game_table)
    
    # print()
    # print("RUNTIME:")
    # print(sys_table)
    
    
    # fuel_table.to_csv('fuel_table.csv', index=False)
    # game_table.to_csv('game_time_table.csv', index=False)
    # sys_table.to_csv('sys_time_table.csv', index=False)

def create_tbl_img(file, output, title):
    df = pd.read_csv(file, delimiter=',')
    #print(df)
    fig = plt.figure()
    cell_text = []
    for row in range(len(df)):
        cell_text.append(df.iloc[row])
    plt.table(cellText=cell_text, colLabels=df.columns, loc='center', cellLoc='center')
    plt.axis('off')
    plt.title(title, loc='center', y=1.0, pad=55)
    
    fig.savefig(output, bbox_inches='tight', dpi=150)
    plt.show()
    
def create_bar(file, output, title, y_label):
    df = pd.read_csv(file, delimiter=',')
    plt.plot()
    #print(df)

    x = df['Game #']
    plt.xticks(x)
    plt.tick_params(axis='x', labelrotation=90, labelsize=9)
    ga = plt.bar(x-0.2, df['Genetic Algorithms'], width=0.2, color='tab:blue', align='center')
    sa = plt.bar(x,     df['Simulated Annealing'], width=0.2, color='tab:green', align='center')
    ts = plt.bar(x+0.2, df['Tree Search'], width=0.2, color='tab:orange', align='center')
    plt.legend(handles=[ga,sa,ts], labels=['Genetic Algorithms', 'Simulated Annealing', 'Tree Search'])
    plt.title(title)
    plt.xlabel("Game #")
    plt.ylabel(y_label)
    
    plt.savefig(output, dpi=150)
    plt.show()
    
    


if __name__ == "__main__":
    one_iteration()
    one_iteration()
    one_iteration()
    # create_tbl_img("fuel_table.csv", "fuel_table.png", "Fuel Remaining at End of Game")
    # create_tbl_img("game_time_table.csv", "game_time_table.png", "Time Steps to Get to Solution")
    # create_tbl_img("sys_time_table.csv", "sys_time_table.png", "Run Time of Algorithm")
    
    # create_bar("fuel_table.csv", "fuel_bar_graph.png", "Fuel Remaining at End of Game", "Fuel Left")
    # create_bar("game_time_table.csv", "gtime_bar_graph.png", "Time Steps to Get to Solution", "# Time Steps")
    # create_bar("sys_time_table.csv", "stime_bar_graph.png", "Run Time of Algorithm", "Runtime (seconds)")



#TODO try and fix GA to have more successes
    # Modify SA algorithm for 7, 8, 9 fails
    # Whisker plot extra credit?
    # See if we can modify Tree to include the 'x' move




