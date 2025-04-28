import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from AffichageGraphe import afficher_graphe
from Solveur import lire_donnees


def calculer_cout_complet(G, tour):
    """
    Calcule le coût total d'une tournée complète (y compris le retour au point de départ).

    :param G: Graphe
    :param tour: Liste des nœuds dans l'ordre de la tournée
    :return: Coût total de la tournée
    """
    if not tour:
        return float('inf')

    cost = 0
    # Vérifier les arêtes entre les villes consécutives
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if G.has_edge(u, v):
            cost += G[u][v]['weight']
        else:
            return float('inf')  # Si une arête est interdite, le coût est infini

    # Ajouter le coût de retour à la ville de départ
    if G.has_edge(tour[-1], tour[0]):
        cost += G[tour[-1]][tour[0]]['weight']
    else:
        return float('inf')  # Si le retour est impossible, le coût est infini

    return cost


def est_tournee_valide(G, tour):
    """
    Vérifie si une tournée est valide (toutes les arêtes existent).

    :param G: Graphe
    :param tour: Liste des nœuds dans l'ordre de la tournée
    :return: True si la tournée est valide, False sinon
    """
    for i in range(len(tour) - 1):
        if not G.has_edge(tour[i], tour[i + 1]):
            return False

    # Vérifier l'arête de retour
    if not G.has_edge(tour[-1], tour[0]):
        return False

    return True


def algorithme_genetique_ameliore(G, population_size=50, generations=100, mutation_rate=0.05,
                                  selection_pressure=0.3, elitism_rate=0.1, timeout=60):
    """
    Algorithme génétique amélioré pour optimiser la tournée de livraison.

    :param G: Graphe
    :param population_size: Taille de la population
    :param generations: Nombre maximal de générations
    :param mutation_rate: Taux de mutation
    :param selection_pressure: Pression de sélection (plus elle est élevée, plus on favorise les meilleurs)
    :param elitism_rate: Taux d'élitisme (proportion des meilleurs individus à conserver)
    :param timeout: Temps maximum d'exécution en secondes
    :return: Tuple (meilleur tour, coût, historique des coûts, temps d'exécution)
    """
    start_time = time.time()

    def generate_initial_population(size):
        """
        Génère une population initiale de tournées valides.
        """
        population = []
        nodes = list(G.nodes)
        max_attempts = 100  # Limiter le nombre de tentatives pour éviter une boucle infinie

        while len(population) < size and max_attempts > 0:
            random.shuffle(nodes)
            tour = nodes[:]
            if est_tournee_valide(G, tour):
                population.append(tour)
            max_attempts -= 1

        # Si on n'a pas assez de tournées valides, on complète avec des tournées partielles
        if len(population) < size:
            # Utiliser un algorithme glouton pour trouver des tournées valides
            for _ in range(size - len(population)):
                tour = generer_tournee_gloutonne(G)
                if tour:
                    population.append(tour)

        return population

    def generer_tournee_gloutonne(G):
        """
        Génère une tournée valide en utilisant une approche gloutonne.
        """
        nodes = list(G.nodes)
        start_node = random.choice(nodes)
        tour = [start_node]
        remaining = set(nodes) - {start_node}

        current = start_node
        while remaining:
            # Trouver le nœud le plus proche qui est accessible
            valid_neighbors = [(v, G[current][v]['weight']) for v in remaining if G.has_edge(current, v)]
            if not valid_neighbors:
                # Si on arrive dans une impasse, on essaie de trouver une solution alternative
                alternative_paths = []
                for node in remaining:
                    for node_in_tour in tour:
                        if G.has_edge(node_in_tour, node):
                            alternative_paths.append((node_in_tour, node, G[node_in_tour][node]['weight']))

                if not alternative_paths:
                    # Aucune solution trouvée
                    return None

                # Choisir le meilleur chemin alternatif
                best_path = min(alternative_paths, key=lambda x: x[2])
                insertion_idx = tour.index(best_path[0])
                tour.insert(insertion_idx + 1, best_path[1])
                remaining.remove(best_path[1])
                current = best_path[1]
            else:
                next_node = min(valid_neighbors, key=lambda x: x[1])[0]
                tour.append(next_node)
                remaining.remove(next_node)
                current = next_node

        # Vérifier si on peut retourner au point de départ
        if not G.has_edge(tour[-1], tour[0]):
            return None

        return tour

    def crossover_pmx(parent1, parent2):
        """
        Croisement PMX (Partially Mapped Crossover) qui génère des enfants valides.
        """
        size = len(parent1)
        # Choisir deux points de croisement
        p1, p2 = sorted(random.sample(range(size), 2))

        # Initialiser les enfants
        child1 = [None] * size
        child2 = [None] * size

        # Copier le segment entre les points de croisement
        child1[p1:p2] = parent1[p1:p2]
        child2[p1:p2] = parent2[p1:p2]

        # Créer les mappings
        mapping1 = {parent1[i]: parent2[i] for i in range(p1, p2)}
        mapping2 = {parent2[i]: parent1[i] for i in range(p1, p2)}

        # Remplir le reste des enfants
        for i in range(size):
            if p1 <= i < p2:
                continue

            # Pour child1
            item1 = parent2[i]
            while item1 in child1[p1:p2]:
                item1 = mapping1[item1]
            child1[i] = item1

            # Pour child2
            item2 = parent1[i]
            while item2 in child2[p1:p2]:
                item2 = mapping2[item2]
            child2[i] = item2

        return child1, child2

    def mutate_swap(tour):
        """
        Mutation par échange de deux villes, avec vérification de validité.
        """
        original_tour = tour.copy()
        max_attempts = 10  # Limiter le nombre de tentatives

        if random.random() < mutation_rate:
            for _ in range(max_attempts):
                mutated_tour = tour.copy()
                i, j = random.sample(range(len(tour)), 2)
                mutated_tour[i], mutated_tour[j] = mutated_tour[j], mutated_tour[i]

                if est_tournee_valide(G, mutated_tour):
                    return mutated_tour

        return original_tour

    def tournament_selection(population, costs, k=3):
        """
        Sélection par tournoi.
        """
        selected = random.sample(range(len(population)), k)
        selected_costs = [costs[i] for i in selected]
        winner_idx = selected[selected_costs.index(min(selected_costs))]
        return population[winner_idx]

    # Générer la population initiale
    population = generate_initial_population(population_size)

    # Si on n'a pas pu générer de population valide, retourner une erreur
    if not population:
        return None, float('inf'), [], time.time() - start_time

    # Initialisation pour le suivi des performances
    best_tour = None
    best_cost = float('inf')
    cost_history = []

    # Nombre d'individus élites à conserver
    num_elites = int(population_size * elitism_rate)

    for generation in range(generations):
        # Vérifier le timeout
        if time.time() - start_time > timeout:
            print(f"Timeout atteint après {generation} générations")
            break

        # Évaluer la population
        costs = [calculer_cout_complet(G, tour) for tour in population]

        # Mettre à jour le meilleur tour
        min_cost_idx = costs.index(min(costs))
        current_best_cost = costs[min_cost_idx]
        current_best_tour = population[min_cost_idx]

        cost_history.append(current_best_cost)

        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_tour = current_best_tour.copy()
            print(f"Génération {generation}: Nouveau meilleur coût = {best_cost}")

        # Trier la population par coût
        sorted_indices = sorted(range(len(costs)), key=lambda i: costs[i])
        sorted_population = [population[i] for i in sorted_indices]

        # Conservation des élites
        elites = sorted_population[:num_elites]

        # Créer une nouvelle population
        new_population = elites.copy()

        # Remplir le reste de la population avec des enfants
        while len(new_population) < population_size:
            # Sélection des parents
            parent1 = tournament_selection(population, costs)
            parent2 = tournament_selection(population, costs)

            # Croisement
            child1, child2 = crossover_pmx(parent1, parent2)

            # Mutation
            child1 = mutate_swap(child1)
            child2 = mutate_swap(child2)

            # Ajouter à la nouvelle population si valides
            if est_tournee_valide(G, child1):
                new_population.append(child1)
            if len(new_population) < population_size and est_tournee_valide(G, child2):
                new_population.append(child2)

        # Mise à jour de la population
        population = new_population[    :population_size]  # S'assurer que la taille est correcte

    execution_time = time.time() - start_time
    return best_tour, best_cost, cost_history, execution_time


graphe_from_json = lire_donnees('donnees_tournee.json')
tour_optimise_recuit = recuit_simule(graphe_from_json)
print("Tournée optimisée (Recuit Simulé) :", tour_optimise_recuit)
afficher_graphe(graphe_from_json, tour_optimise_recuit)