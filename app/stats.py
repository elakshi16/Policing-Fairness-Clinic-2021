from math import sqrt
import random
from scipy import spatial

def mysum(arrests, patrols):
  #Patrols should be number of precints (start_loc) * days (* possibly patrols per day (num_trips))
  #arrests = arrest_data from the la_patrol
    magic_number = 0.8
    average_arrests = magic_number * patrols
    lower_bound = .9 * average_arrests
    upper_bound = (.1 * average_arrests) + average_arrests
    sum_arrests = sum(arrests.values())
    if (sum_arrests > upper_bound) or (sum_arrests < lower_bound):
        return "Invalid Patrol"
    else:
        return "Valid Patrol with current parameters"



def sim_mean(arrests):
    total_arrests = sum(arrests.values())
    mean = total_arrests / len(arrests)
    return mean


def nodal_mean(list_of_simulations, node):
    total_arrests = 0
    for arrest in list_of_simulations:
        total_arrests += arrest[node] 
    mean = total_arrests / len(list_of_simulations) 
    return mean


def sim_stddev(arrests):
    mean = sim_mean(arrests)
    count = 0
    list_of_arrest_counts = arrests.values()
    for i in list_of_arrest_counts:
        count += ((i - mean) ** 2)
    result = sqrt(count/(len(arrests)-1))
    return result

def nodal_stddev(list_of_simulations, node):
    mean = nodal_mean(list_of_simulations, node)
    count = 0
    for i in list_of_simulations:
        count += ((i[node] - mean) ** 2)
    result = sqrt(count/(len(list_of_simulations)-1))
    return result


def result(list_of_simulations):
    store = {}
    for sim in list_of_simulations:
        for node in sim.keys():
            store.setdefault(node, {'mean': 0 , 'stddev': 0, 'values': []})
            store[node]['mean'] = nodal_mean(list_of_simulations, node)
            store[node]['stddev'] = nodal_stddev(list_of_simulations, node)
            store[node]['values'].append(sim[node])
    return store


def bounds (mean, interval, stddev, length):
    upperbound = mean + (interval * (stddev / sqrt(length)))
    lowerbound = mean - (interval * (stddev / sqrt(length)))
    
    return upperbound, lowerbound


def compare_means(store, real):
    # input result ^ and real-world data result
    # output dictionary key: node & value: [sim mean, real mean, confidence]
    # compare mean and stddev(should be used to determine confidence) between simulations and data
    # confidence is how accurately the real world data is represented (to be properly discussed)
    confidence_85 = 1.440
    confidence_95 = 1.960
    confidence_99 = 2.576
    confidence    = ''

    length = len(store)

    model_avg = {}
    for i in store:
        model_avg.setdefault(i, store[i]['mean']) 
    
    model_mean = sim_mean(model_avg)
    real_mean = sim_mean(real)

    model_stddev = sim_stddev(model_avg)

    if (real_mean >= bounds(model_mean, confidence_85, model_stddev, length)[1]) and (real_mean <= bounds(model_mean, confidence_85, model_stddev, length)[0]):
        if (real_mean >= bounds(model_mean, confidence_95, model_stddev, length)[1]) and (real_mean <= bounds(model_mean, confidence_95, model_stddev, length)[0]):
            if (real_mean >= bounds(model_mean, confidence_99, model_stddev, length)[1]) and (real_mean <= bounds(model_mean, confidence_99, model_stddev, length)[0]):
                confidence = '99%'
            else:
                confidence = '95%'
        else:
            confidence = '85%'
    else:
        confidence = '<85%'

    return f" We are {confidence} confident that the mean of our simulated data matches the mean of the real world data. "


def compare_sims(store, real):

    # Note the confidence interval numbers
    confidence_85 = 1.440
    confidence_95 = 1.960
    confidence_99 = 2.576
    randNode = random.choice(list(store.values()))
    length = len(randNode['values'])

    # number of nodes within each confidence interval
    count_85 = 0
    count_95 = 0
    count_99 = 0

    # Dictionary to store which nodes are in each confidence interval
    answer = {}
    for node in store:
        answer.setdefault(node, (False, False, False))     
    
    # Loop through the nodes
    for node_id, i in store.items():

        # Find out the upper and lower bound for each confidence interval
        upper_bound_85, lower_bound_85 = bounds(i['mean'], confidence_85, i['stddev'], length)
        upper_bound_95, lower_bound_95 = bounds(i['mean'], confidence_95, i['stddev'], length)
        upper_bound_99, lower_bound_99 = bounds(i['mean'], confidence_99, i['stddev'], length)

        #Check each bound
        if (lower_bound_99 <= real[node_id]) and (real[node_id] <= upper_bound_99):
            count_85 += 1
            count_95 += 1
            count_99 += 1
            answer[node_id] = (True, True, True)
        
        # elif (lower_bound_95 <= real[node_id]) and (real[node_id] <= upper_bound_95):
        #     count_85 += 1
        #     count_95 += 1
        #     answer[node_id] = (True, True, False)
        # elif (lower_bound_85 <= real[node_id]) and (real[node_id] <= upper_bound_85):
        #     count_85 += 1
        #     answer[node_id] = (True, False, False)

        else:
            pass

    return answer, (count_85, count_95, count_99)
    # return answer, count_99


def similarity_score(store, real):
    simList = []
    realList = []
    for node_id, i in store.items():
        simList.append(int(i['mean']))
        realList.append(int(real[node_id]))
    similarity = 1 - spatial.distance.cosine(simList, realList)
    return similarity


# import pickle


# with open('populated_nodes.pkl', 'rb') as f:
#     data = pickle.load(f)
#     print(data)
