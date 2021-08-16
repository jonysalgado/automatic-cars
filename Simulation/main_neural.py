from params import *
import numpy as np
import random
import pandas as pd
import time

def load_neural(file_name, shapes_w, shapes_b):
    df = pd.read_csv(file_name)
    genes_w, genes_b = [], []
    for i in range(len(df)):
        genes = df["genes_w"][i].strip('][').split(' ')
        genes = [float(gene) for gene in genes if gene != '']
        genes = unflatten(np.array(genes), shapes_w)
        genes_w.append(genes)

        genes = df["genes_b"][i].strip('][').split(' ')
        genes = [float(gene) for gene in genes if gene != '']
        genes = unflatten(np.array(genes), shapes_b)
        genes_b.append(genes)

    return genes_w, genes_b

def save_neural(players):
    players = selection(players)
    players = players[:int(ELITISM)]
    genes_w = []
    genes_b = []
    for player in players:
        genes_w.append(np.concatenate([a.flatten() for a in player.neural_network.weights]))
        genes_b.append(np.concatenate([a.flatten() for a in player.neural_network.bias]))
    
    today = time.strftime("%d_%b_%Y_%H_%M_%S")
    df = pd.DataFrame({
        "genes_w": genes_w,
        "genes_b": genes_b
    })

    df.to_csv('csv\\best_players_' + today + '.csv')


def selection(players):
    return sorted(players, key=lambda player: player.distance, reverse=True) 

def unique_players(old_best_players, best_players):
    players = old_best_players + best_players
    players_number = [player.number for player in best_players]
    old_players_number = [player.number for player in old_best_players]
    old_not_actual_best = [number for number in old_players_number if number not in players_number]
    players_number = players_number + old_not_actual_best
    players = [player for player in players if player.number in players_number]
    print(len(players))
    if len(players) > ELITISM + 10:
        return selection(players)[:ELITISM + 10]
    return selection(players)

def unflatten(flattened,shapes):
    newarray = []
    index = 0
    for shape in shapes:
        size = np.product(shape)
        newarray.append(flattened[index : index + size].reshape(shape))
        index += size
    return newarray

def crossover(players):
    offspring_w = []
    offspring_b = []
    for _ in range((N_PLAYERS - len(players))//2):
        parent1 = players[0]
        parent2 = random.choice(players)
        
        shapes_w = [a.shape for a in parent1.neural_network.weights]
        shapes_b = [a.shape for a in parent1.neural_network.bias]
        
        genes_w1 = np.concatenate([a.flatten() for a in parent1.neural_network.weights])
        genes_w2 = np.concatenate([a.flatten() for a in parent2.neural_network.weights])

        genes_b1 = np.concatenate([a.flatten() for a in parent1.neural_network.bias])
        genes_b2 = np.concatenate([a.flatten() for a in parent2.neural_network.bias])

        split = np.random.randint(len(genes_w1), size=2)
        child1_genes_w = np.array(genes_w1[:split[0]].tolist() + genes_w2[split[0]:].tolist())
        child2_genes_w = np.array(genes_w1[:split[1]].tolist() + genes_w2[split[1]:].tolist())

        split = np.random.randint(len(genes_b1), size=2)
        child1_genes_b = np.array(genes_b1[:split[0]].tolist() + genes_b2[split[0]:].tolist())
        child2_genes_b = np.array(genes_b1[:split[1]].tolist() + genes_b2[split[1]:].tolist())

        weights1 = unflatten(child1_genes_w,shapes_w)
        weights2 = unflatten(child2_genes_w,shapes_w)

        bias1 = unflatten(child1_genes_b,shapes_b)
        bias2 = unflatten(child2_genes_b,shapes_b)
        
        offspring_w.append(weights1)
        offspring_w.append(weights2)

        offspring_b.append(bias1)
        offspring_b.append(bias2)
    
    return offspring_w, offspring_b

def mutation(players):
    for player in players:
        if random.uniform(0.0, 1.0) <= 0.1:
            weights = player.neural_network.weights
            shapes = [a.shape for a in weights]
            flattened = np.concatenate([a.flatten() for a in weights])
            size = np.random.randint(len(flattened)*0.5)
            randint = np.random.randint(len(flattened), size=size)
            for i in range(size):
                flattened[randint[i]] += np.random.randn() + 0.15
            newarray = []
            indeweights = 0
            for shape in shapes:
                size = np.product(shape)
                newarray.append(flattened[indeweights : indeweights + size].reshape(shape))
                indeweights += size
            player.neural_network.weights = newarray
            
            bias = player.neural_network.bias
            shapes = [a.shape for a in bias]
            flattened = np.concatenate([a.flatten() for a in bias])
            size = np.random.randint(4)
            randint = np.random.randint(len(flattened), size=size)
            for i in range(size):
                flattened[randint[i]] += np.random.randn() + 0.15
            newarray = []
            indebias = 0
            for shape in shapes:
                size = np.product(shape)
                newarray.append(flattened[indebias : indebias + size].reshape(shape))
                indebias += size
            player.neural_network.bias = newarray

    return players 

def copy_best_for_olds(best_players, old_players):
    best_number = len(best_players)
    index = 0
    for player in old_players:
        player.neural_network.weights = best_players[index].neural_network.weights
        player.neural_network.bias = best_players[index].neural_network.bias
        if index < best_number - 1:
            index += 1
        else:
            index = 0
    
    return old_players

def random_mutation(other_players):
    for player in other_players:
        weights = player.neural_network.weights
        shapes = [a.shape for a in weights]
        flattened = np.concatenate([a.flatten() for a in weights])
        mutations = np.random.randint(0, len(flattened))
        flattened = _random_mutation(mutations, flattened)
        newarray = []
        indeweights = 0
        for shape in shapes:
            size = np.product(shape)
            newarray.append(flattened[indeweights : indeweights + size].reshape(shape))
            indeweights += size
        player.neural_network.weights = newarray
        bias = player.neural_network.bias
        shapes = [a.shape for a in bias]
        flattened = np.concatenate([a.flatten() for a in bias])
        mutations = np.random.randint(0, len(flattened))
        flattened = _random_mutation(mutations, flattened)
        newarray = []
        indebias = 0
        for shape in shapes:
            size = np.product(shape)
            newarray.append(flattened[indebias : indebias + size].reshape(shape))
            indebias += size
        player.neural_network.bias = newarray

    return other_players 

def _random_mutation(mutations, flattened):
    for _ in range(mutations):
            type = np.random.randint(1, 3)
            index = np.random.randint(0, len(flattened))
            if type == 0: 
                factor = np.random.choice([-1,1])
                flattened[index] = factor * np.random.uniform(0, 1000)
            
            elif type == 1:
                factor = np.random.uniform(0.5, 1.5)
                flattened[index] *= factor

            else:
                factor = np.random.choice([-1,1])
                number = factor * np.random.uniform(0, 10)
                flattened[index] += number

    return flattened

            

def main_neural(players):
    players = selection(players)
    distances = [players[i].distance for i in range(ELITISM)]
    print('Elite distances: ', distances)
    print('N_POPULATION: ', N_PLAYERS)
    best_players = players[:int(ELITISM)]
    old_players = players[int(ELITISM):]
    old_players = copy_best_for_olds(best_players, old_players)
    old_players = random_mutation(old_players)

    return best_players + old_players


# def main_neural(players, generation):
#     if generation != 1:
#         old_best_players = players[:int(ELITISM)]
#     else:
#         old_best_players = []
#     players = selection(players)
#     best_players = players[:int(ELITISM)]
#     best_players = unique_players(old_best_players, best_players)
#     other_players = [player for player in players if player not in best_players]
#     distances = [players[i].distance for i in range(ELITISM)]
#     print('Elite distances: ', distances)
#     print('Sigma: ', SIGMA)
#     print('N_POPULATION: ', N_PLAYERS)
#     # new_weights, new_bias = crossover(best_players)
#     # old_players = players[int(ELITISM):]
#     # for player, weight, bias in zip(old_players, new_weights, new_bias):
#     #     player.neural_network.weights = weight
#     #     player.neural_network.bias = bias
#     # old_players = mutation(old_players)
#     other_players = random_mutation(best_players, other_players)
#     players = best_players + other_players

#     return players

# def main_neural(players):
#     players = selection(players)
#     distances = []
#     for i in range(10):
#         distances.append(players[i].distance)
#     print(distances)
#     best_players = players[:int(ELITISM)]
#     old_players = players[int(ELITISM):]
#     players = copy_best_for_olds(best_players, old_players)
#     old_players = players[int(ELITISM):]
#     old_players = random_mutation(old_players)

#     return best_players + old_players