from AffichageGraphe import afficher_graphe
from Solveur import lire_donnees, calculer_cout
import random
import numpy as np



def recuit_simule(G, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-3, max_iter=10000):
    """
    Recuit simulé pour optimiser une tournée sur un graphe pondéré avec interdictions.

    :param G: Graphe NetworkX
    :param initial_temp: Température initiale
    :param cooling_rate: Taux de refroidissement
    :param stopping_temp: Température d'arrêt
    :param max_iter: Nombre maximal d'itérations
    :return: Meilleure tournée trouvée
    """
    def generate_neighbor(tour):
        """Génère un voisin en inversant deux villes."""
        a, b = random.sample(range(len(tour)), 2)
        tour[a], tour[b] = tour[b], tour[a]
        return tour

    nodes = list(G.nodes)
    current_solution = nodes[:]
    random.shuffle(current_solution)
    current_cost = calculer_cout(G, current_solution)
    best_solution = current_solution[:]
    best_cost = current_cost

    temperature = initial_temp
    iteration = 0

    while temperature > stopping_temp and iteration < max_iter:
        candidate_solution = current_solution[:]
        candidate_solution = generate_neighbor(candidate_solution)
        candidate_cost = calculer_cout(G, candidate_solution)

        cost_diff = candidate_cost - current_cost

        if cost_diff < 0 or random.random() < np.exp(-cost_diff / temperature):
            current_solution = candidate_solution
            current_cost = candidate_cost

            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

        temperature *= cooling_rate
        iteration += 1

    return best_solution

graphe_from_json = lire_donnees('donnees_tournee.json')
tour_optimise_recuit = recuit_simule(graphe_from_json)
print("Tournée optimisée (Recuit Simulé) :", tour_optimise_recuit)
afficher_graphe(graphe_from_json, tour_optimise_recuit)