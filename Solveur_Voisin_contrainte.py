import json

def nearest_neighbor_multi(json_file, nombre_vehicules):
    # Lit le fichier JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    nombre_villes = data["nombre_de_villes"]
    matrice_cout = data["matrice_cout"]

    # Remplace "Infinity" par float('inf')
    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if matrice_cout[i][j] == "Infinity" or matrice_cout[i][j] == "inf":
                matrice_cout[i][j] = float('inf')

    visited = [False] * nombre_villes
    visited[0] = True  # ville 0 est le point de départ pour tous

    chemins = [[] for _ in range(nombre_vehicules)]
    couts_totaux = [0 for _ in range(nombre_vehicules)]

    # Initialise tous les véhicules à la ville de départ
    positions = [0 for _ in range(nombre_vehicules)]
    for chemin in chemins:
        chemin.append(0)

    villes_a_visiter = nombre_villes - 1  # sauf la ville de départ

    while villes_a_visiter > 0:
        for v in range(nombre_vehicules):
            # Trouve la ville la plus proche pour ce véhicule
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

            if villes_a_visiter == 0:
                break

    # Retour à la ville de départ
    for v in range(nombre_vehicules):
        couts_totaux[v] += matrice_cout[positions[v]][0]
        chemins[v].append(0)

    for i in range(nombre_vehicules):
        print(f"Chemin véhicule {i+1} : {chemins[i]}")
        print(f"Coût total véhicule {i+1} : {couts_totaux[i]}")

if __name__ == "__main__":
    json_file = 'cas_reel.json'
    nombre_vehicules = int(input("Entrez le nombre de véhicules : "))
    nearest_neighbor_multi(json_file, nombre_vehicules)
