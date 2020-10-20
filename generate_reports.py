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
    """
    Get the statistics for genetic algorithm run

    Returns
    -------
    ga_fuel : List
        Fuel left for each game.
    ga_game_time : List
        Game run time for each game.
    ga_sys_time : List
        System run time for each game.

    """
    ga_fuel = []
    ga_game_time = []
    ga_sys_time = []
    for i in range(25):
        print("Game #" + str(i) + ": ", end='')
        #for j in range(5):
            
        GA = asteroids_ga.GA_Agent(line_args.format(i))
        start = time.time()
        GA_path = GA.run()
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(GA_path, args)
            
            # if not np.isnan(fuel_left) or i == 9:
            #     break
        if not np.isnan(fuel_left):
            print("success")
        else:
            print("failure")
        ga_fuel.append(fuel_left)
        ga_game_time.append(game_time)
        ga_sys_time.append(round(end-start, 4))
            
        
    return ga_fuel, ga_game_time, ga_sys_time


def get_sa_stats():
    """
    Get the statistics for simulated annealing algorithm run

    Returns
    -------
    sa_fuel : List
        Fuel left for each game.
    sa_game_time : List
        Game run time for each game.
    sa_sys_time : List
        System run time for each game.

    """
    sa_fuel = []
    sa_game_time = []
    sa_sys_time = []
    for i in range(25):
        print("Game #" + str(i) + ": ", end='')
        #for j in range(5):
            
        SA = asteroids_sa.SA_Agent(line_args.format(i))
        start = time.time()
        SA_path = SA.run()
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(SA_path, args)
            
            # if not np.isnan(fuel_left) or i == 9:
            #     break
        if not np.isnan(fuel_left):
            print("success")
        else:
            print("failure")
            
        sa_fuel.append(fuel_left)
        sa_game_time.append(game_time)
        sa_sys_time.append(round(end-start, 4))
        
        
    return sa_fuel, sa_game_time, sa_sys_time


def get_tree_stats():
    """
    Get the statistics for tree search algorithm run

    Returns
    -------
    tree_fuel : List
        Fuel left for each game.
    tree_game_time : List
        Game run time for each game.
    tree_sys_time : List
        System run time for each game.

    """
    tree_fuel = []
    tree_game_time = []
    tree_sys_time = []
    for i in range(25):
        print("Game #" + str(i) + ": ", end='')
        #for j in range(5):
        tree = asteroids_tree.Search_Agent(line_args.format(i))
        start = time.time()
        tree_path = tree.run()
        end = time.time()
        
        args = asteroids_exp.parse_args(line_args.format(i))
        game_time, fuel_left = asteroids_exp.check_soln(tree_path, args)
            
            # if not np.isnan(fuel_left) or i == 9:
            #     break
        if not np.isnan(fuel_left):
            print("success")
        else:
            print("failure")
            
        tree_fuel.append(fuel_left)
        tree_game_time.append(game_time)
        run_time = end-start
        tree_sys_time.append(round(run_time, 4))
        
    return tree_fuel, tree_game_time, tree_sys_time

def one_iteration():
    """
    Goes through the single iteration statistic gathering and saves the
    values to a csv file.

    Returns
    -------
    None.

    """
    print("----- GENETIC START -----")
    fuel, g_time, s_time = get_ga_stats()
    print("----- GENETIC DONE -----")
    fuel_table = {'Game #': indices, 'Genetic Algorithms': fuel}
    game_table = {'Game #': indices, 'Genetic Algorithms': g_time}
    sys_table = {'Game #': indices, 'Genetic Algorithms': s_time}
    
    print()
    print("----- ANNEALING START -----")
    fuel, g_time, s_time = get_sa_stats()
    print("----- ANNEALING DONE -----")
    fuel_table['Simulated Annealing'] = fuel
    game_table['Simulated Annealing'] = g_time
    sys_table['Simulated Annealing'] = s_time
    
    print()
    print("----- TREE SEARCH START -----")
    fuel, g_time, s_time = get_tree_stats()
    print("----- TREE SEARCH DONE -----")
    fuel_table['Tree Search'] = fuel
    game_table['Tree Search'] = g_time
    sys_table['Tree Search'] = s_time
    
    print()
    print("------ RESULTS -------")
    
    fuel_table = pd.DataFrame(fuel_table)
    game_table = pd.DataFrame(game_table)
    sys_table = pd.DataFrame(sys_table)
    
    print("FUEL:")
    print(fuel_table)
    
    print()
    print("GAME TIME:")
    print(game_table)
    
    print()
    print("RUNTIME:")
    print(sys_table)
    
    
    fuel_table.to_csv('fuel_table.csv', index=False)
    game_table.to_csv('game_time_table.csv', index=False)
    sys_table.to_csv('sys_time_table.csv', index=False)
    
    
# Starter code for the box and whiskers: (didn't leave myself enough time to
# run it so instead I worked on improving Genetic Algorithm)
    
# def set_box_color(bp, color):
#     plt.setp(bp['boxes'], color=color)
#     plt.setp(bp['whiskers'], color=color)
#     plt.setp(bp['caps'], color=color)
#     plt.setp(bp['medians'], color=color)
    
# def create_box_whisker(algos, output):
#     #ticks = [1, 2, 3, 4, 5]
#     # Create single boxplot
#     plt.figure()
#     for i in range(1):
#         bpl = plt.boxplot(algos[0][i], positions=[i*3-0.4], sym='', widths=0.2)
#         #bpr = plt.boxplot(algos[1][i], positions=[i*3], sym='', widths=0.2)
#         #bpm = plt.boxplot(algos[2][i], positions=[i*3+0.4], sym='', widths=0.2)
#         set_box_color(bpl, 'tab:blue') 
#         #set_box_color(bpr, 'tab:orange')
#         #set_box_color(bpm, 'tab:green')
        
#     plt.xticks(range(0, len(indices) * 3, 3), indices)
#     plt.xlim(-2, len(indices)*3)
    
#     plt.plot([], c='tab:blue', label='Genetic Algorithm')
#     plt.plot([], c='tab:orange', label='Simulated Annealing')
#     plt.plot([], c='tab:green', label='Tree Search')
#     plt.legend()
    
#     plt.tight_layout()
#     plt.savefig(output, dpi=150)
#     plt.show()
    
# def twenty_iterations():
#     # Need list of fuel values for each game for each algo
    
#     # all fuels for 20 iteration of a game for each algo:
#     fuels = [[],[],[]]
#     game_times = [[],[],[]]
#     sys_times = [[],[],[]]
    
#     for i in range(1):
#         print("ITERATION " + str(i+1) +":")
#         fuel, g_time, s_time = get_tree_stats()
#         #fuel = pd.DataFrame(fuel)
#         fuel = [i for i in fuel if not np.isnan(i)]
#         fuel = [i for i in fuel if not np.isnan(i)]
#         fuel = [i for i in fuel if not np.isnan(i)]
#         fuels[0].append(fuel)
#         game_times[0].append(g_time)
        
    
#     print(fuels)
#     create_box_whisker(fuels, 'test.png')
    
    
#     # for i in range(20):
#     #     print("Iteration " + str(i) +": ")
        
        


def create_tbl_img(file, output, title):
    """
    Makes an image of the data table

    Parameters
    ----------
    file : string
        csv file to create image from.
    output : string
        file name to output in.
    title : string
        title of the table.

    Returns
    -------
    None.

    """
    df = pd.read_csv(file, delimiter=',')
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
    """
    Makes an image of the bar graph for the statistics

    Parameters
    ----------
    file : string
        csv file to create graph from.
    output : string
        file name to output in.
    title : string
        title of the graph.
    y_label : string
        label of the y axis.

    Returns
    -------
    None.

    """
    df = pd.read_csv(file, delimiter=',')
    plt.plot()

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
    
    
def simple_data():
    """
    Create all of the images for the data gathered from one iteration

    Returns
    -------
    None.

    """
    create_tbl_img("fuel_table.csv", "fuel_table.png", "Fuel Remaining at End of Game")
    create_tbl_img("game_time_table.csv", "game_time_table.png", "Time Steps to Get to Solution")
    create_tbl_img("sys_time_table.csv", "sys_time_table.png", "Run Time of Algorithm")
    
    create_bar("fuel_table.csv", "fuel_bar_graph.png", "Fuel Remaining at End of Game", "Fuel Left")
    create_bar("game_time_table.csv", "gtime_bar_graph.png", "Time Steps to Get to Solution", "# Time Steps")
    create_bar("sys_time_table.csv", "stime_bar_graph.png", "Run Time of Algorithm", "Runtime (seconds)")



if __name__ == "__main__":
    one_iteration()
    # Uncomment to regenerate the tables
    #simple_data()
    





