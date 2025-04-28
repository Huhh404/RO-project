import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import json
from AffichageGraphe import afficher_graphe

def generer_instance_aleatoire(n, proba_interdit=0.05):
    """
    Génère une instance aléatoire d'un problème de tournée de livraison avec des contraintes de routes.

    :param n: Nombre de villes
    :param proba_interdit: Probabilité qu'une arête soit interdite
    :return: Graphe pondéré avec contraintes
    """
    G = nx.Graph()
    G.add_nodes_from(range(n))

    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < proba_interdit:
                weight = float('inf')
            else:
                weight = random.randint(1, 100)
            G.add_edge(u, v, weight=weight)

    return G

def enregistrer_donnees(G, fichier):
    """
    Enregistre les données du graphe dans un fichier JSON.

    :param G: Graphe à enregistrer
    :param fichier: Nom du fichier de sortie
    """
    n = len(G.nodes)
    matrice_cout = np.full((n, n), float('inf'))

    for (u, v) in G.edges():
        matrice_cout[u][v] = G[u][v]['weight']
        matrice_cout[v][u] = G[u][v]['weight']

    matrice_cout = matrice_cout.tolist()

    donnees = {
        'nombre_de_villes': n,
        'matrice_cout': matrice_cout
    }

    with open(fichier, 'w') as f:
        json.dump(donnees, f, indent=4)

# Exemple d'utilisation
nombre_de_villes = 15
graphe = generer_instance_aleatoire(nombre_de_villes, proba_interdit=0.05)
enregistrer_donnees(graphe, 'donnees_tournee.json')
afficher_graphe(graphe)
