import random
import time

import numpy as np

from utils import cout_chemin_multi_graph

def run_recuit(G, nombre_villes, nombre_vehicules, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-3, max_iter=2500):
    historique_couts = []
    historique_temps = []

    villes = list(range(1, nombre_villes))
    current_solution = [[] for _ in range(nombre_vehicules)]

    random.shuffle(villes)
    for idx, ville in enumerate(villes):
        current_solution[idx % nombre_vehicules].append(ville)

    current_cost = cout_chemin_multi_graph(G, current_solution)
    best_cost = current_cost
    start = time.perf_counter()

    temperature = initial_temp
    iteration = 0

    def generate_neighbor(chemins):
        chemins_copy = [list(route) for route in chemins]
        v1, v2 = random.sample(range(nombre_vehicules), 2)
        if chemins_copy[v1] and chemins_copy[v2]:
            c1 = random.choice(chemins_copy[v1])
            c2 = random.choice(chemins_copy[v2])
            i1 = chemins_copy[v1].index(c1)
            i2 = chemins_copy[v2].index(c2)
            chemins_copy[v1][i1], chemins_copy[v2][i2] = chemins_copy[v2][i2], chemins_copy[v1][i1]
        return chemins_copy

    while temperature > stopping_temp and iteration < max_iter:
        candidate_solution = generate_neighbor(current_solution)
        candidate_cost = cout_chemin_multi_graph(G, candidate_solution)

        if candidate_cost < current_cost or random.random() < np.exp(-(candidate_cost - current_cost) / temperature):
            current_solution = candidate_solution
            current_cost = candidate_cost

            if current_cost < best_cost:
                best_cost = current_cost

        historique_couts.append(best_cost)
        historique_temps.append(time.perf_counter() - start)

        temperature *= cooling_rate
        iteration += 1

    return historique_couts, historique_temps
