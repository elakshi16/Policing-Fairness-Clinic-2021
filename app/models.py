import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import random

from graph import Graph
from graph import Node

import fiona
import pandas as pd
import pickle

#-----------------------------------------------------
# RUN IN TERMINAL BEFORE THE REST OF THE CODE
# myGraph = Graph()
# myGraph.createNodes(save_file="./out/nodes.pkl")
#-----------------------------------------------------

# Get nodes from existing pickle file
la_graph = Graph()
la_graph.createNodes(from_file = './out/nodes.pkl')

# visualizes LAPD arrest data - just a check
def testPlot():
    x = []
    y = []
    arrCnt = []
    for key, node in la_graph.nodes.items():
        x.append(key[0])
        y.append(key[1])
        arrCnt.append(0.5*len(node.pd_reports)) # PROPERTY TO VARY HERE

    # plot
    fig, ax = plt.subplots()
    fig.set_size_inches(20,20)
    ax.scatter(x, y, c=arrCnt) # can use colormap instea of size&alpha
    ax.set(xlim=(0, 350), xticks=np.arange(1, 8),
        ylim=(0, 475), yticks=np.arange(1, 8))

    plt.show()

#-----------------------------------------------------
#                ARREST RATE MODELS
#-----------------------------------------------------

# uniform rate of arrest for all nodes
def uniformArrest(graph):
    return {node: 0.5 for node in graph.nodes.values()}

# rate of arrest adjusted for population per node
def populationArrest(graph):
    for node in graph:
        
        node.population
    return 0

''' nodes with higher concentrations of people in precinct are more favored

    nodes with higher arrest rates are favored

    after arrest update surrounding nodes 

    get neighbors versus get neighbors precincts
    is there a way to calculate all nodes in a precinct without going through the entire graph?
'''

#-----------------------------------------------------
#                    WALK MODELS
#-----------------------------------------------------

# finds and returns valid neighbors inside precinct
def precinctNeighbors(graph, node):
    neighbors = graph.getNeighbors(node)
    precinct = node.precinct_ID
    valid_neighbors = []
    
    for coords in neighbors:
        n = graph.nodes[coords]
        if n.precinct_ID == precinct:
            valid_neighbors.append(n)
    
    return valid_neighbors

# walk by neighbor
def patrol(walk_length, graph, start, arrest_rate):
    current_location = start
    path = []
    arrest_data = {node:0 for node in graph.nodes.values()}
    for i in range(walk_length):
        # record location
        path.append(current_location)
        
        # flip a coin to make an arrest
        if random.random() < arrest_rate[current_location]: 
            arrest_data[current_location] += 1
        
        # choose where to go next 
        current_location = random.choice(precinctNeighbors(graph, current_location))
    return path, arrest_data


#-----------------------------------------------------
#                  MAIN FUNCTION
#-----------------------------------------------------

# In this cell, we run the simulation on the neighborhood
def main():
    arrest_rate = uniformArrest(la_graph)
    arrest_concentration = {node:0 for node in la_graph.nodes.values()}

    paths = []
    for day in range(365):
        start = random.choice(list(la_graph.nodes.values()))
        path, arrest_data = patrol(20, la_graph,start, arrest_rate)
        for key in arrest_concentration:
            arrest_concentration[key] += arrest_data[key]
        paths.append(path)

    # now, visualize the patrol
    x = []
    y = []
    arrCnt = []
    for key, node in la_graph.nodes.items():
        x.append(key[0])
        y.append(key[1])
        arrCnt.append(arrest_concentration[node]) # PROPERTY TO VARY HERE

    fig, ax = plt.subplots()
    fig.set_size_inches(20,20)
    ax.scatter(x, y, c=arrCnt) # can use colormap instea of size&alpha
    ax.set(xlim=(0, 350), xticks=np.arange(1, 8),
        ylim=(0, 475), yticks=np.arange(1, 8))

    plt.show()

    # save data to a pickle file
