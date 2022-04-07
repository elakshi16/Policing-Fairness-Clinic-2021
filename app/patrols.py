import random


def random_walk(walk_length, graph, start, arrest_rate):
    current_location = start
    path = []
    arrest_data = {node:0 for node in graph.nodes.keys()}
    for i in range(walk_length):
        # record location
        path.append(current_location)
        
        # flip a coin to make an arrest
        if random.random() < arrest_rate[current_location.ID]: 
            arrest_data[current_location.ID] = arrest_data.setdefault(current_location.ID, 0) + 1
            
        # choose where to go next
         
        next_ind = random.choice(graph.getNeighbors(current_location))

        current_location = graph.nodes[next_ind]
        # current_location = random.choice(graph.getNeighbors(current_location))
    return path, arrest_data

def random_walk_precinct(walk_length, graph, start, arrest_rate):
    current_location = start
    path = []
    arrest_data = {node:0 for node in graph.precincts[start.precinct_ID].keys()}
    for i in range(walk_length):
        # record location
        path.append(current_location)
        
        # flip a coin to make an arrest
        if random.random() < arrest_rate[current_location.ID]: 
            arrest_data[current_location.ID] = arrest_data.setdefault(current_location.ID, 0) + 1
            
        # choose where to go next
         
        next_ind = random.choice(graph.getNeighborsPrecinct(current_location))

        current_location = graph.nodes[next_ind]
        # current_location = random.choice(graph.getNeighbors(current_location))
    return path, arrest_data
