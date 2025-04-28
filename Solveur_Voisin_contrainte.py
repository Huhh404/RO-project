import time
from utils import cout_chemin_multi

def run_voisin(matrice_cout, nombre_villes, nombre_vehicules):
    historique_couts = []
    historique_temps = []

    visited = [False] * nombre_villes
    visited[0] = True

    chemins = [[] for _ in range(nombre_vehicules)]
    couts_totaux = [0 for _ in range(nombre_vehicules)]
    positions = [0 for _ in range(nombre_vehicules)]

    for chemin in chemins:
        chemin.append(0)

    villes_a_visiter = nombre_villes - 1
    start = time.perf_counter()

    while villes_a_visiter > 0:
        for v in range(nombre_vehicules):
            current_city = positions[v]
            next_city = None
            min_cost = float('inf')

            for city in range(nombre_villes):
                if not visited[city] and matrice_cout[current_city][city] < min_cost:
                    min_cost = matrice_cout[current_city][city]
                    next_city = city

            if next_city is not None:
                chemins[v].append(next_city)
                couts_totaux[v] += min_cost
                visited[next_city] = True
                positions[v] = next_city
                villes_a_visiter -= 1

                total_cost_now = sum(couts_totaux)
                historique_couts.append(total_cost_now)
                historique_temps.append(time.perf_counter() - start)

            if villes_a_visiter == 0:
                break

    return historique_couts, historique_temps
