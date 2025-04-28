import json
import numpy as np
import networkx as nx

def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    nombre_villes = data["nombre_de_villes"]
    matrice_cout = data["matrice_cout"]

    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if matrice_cout[i][j] == "Infinity" or matrice_cout[i][j] == "inf":
                matrice_cout[i][j] = float('inf')

    return nombre_villes, matrice_cout

def lire_donnees_graph(json_file):
    with open(json_file, 'r') as f:
        donnees = json.load(f)

    n = donnees['nombre_de_villes']
    matrice_cout = np.array(donnees['matrice_cout'])

    G = nx.Graph()
    G.add_nodes_from(range(n))

    for u in range(n):
        for v in range(u + 1, n):
            if matrice_cout[u][v] != float('inf'):
                G.add_edge(u, v, weight=matrice_cout[u][v])

    return G, n

def cout_chemin_multi(chemins, matrice_cout):
    total = 0
    for chemin in chemins:
        if len(chemin) == 0:
            continue
        cost = 0
        current_city = 0
        for ville in chemin:
            cost += matrice_cout[current_city][ville]
            current_city = ville
        cost += matrice_cout[current_city][0]
        total += cost
    return total

def cout_chemin_multi_graph(G, chemins):
    total = 0
    for chemin in chemins:
        if len(chemin) == 0:
            continue
        cost = 0
        current_city = 0
        for ville in chemin:
            if G.has_edge(current_city, ville):
                cost += G[current_city][ville]['weight']
            else:
                return float('inf')
            current_city = ville
        if G.has_edge(current_city, 0):
            cost += G[current_city][0]['weight']
        else:
            return float('inf')
        total += cost
    return total
