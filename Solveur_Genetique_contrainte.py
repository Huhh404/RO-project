import json
import random

def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    nombre_villes = data["nombre_de_villes"]
    matrice_cout = data["matrice_cout"]

    # Remplace "Infinity" par float('inf')
    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if matrice_cout[i][j] == "Infinity" or matrice_cout[i][j] == "inf":
                matrice_cout[i][j] = float('inf')

    return nombre_villes, matrice_cout

def cout_chemin_multi(chemins, matrice_cout):
    total = 0
    for chemin in chemins:
        if len(chemin) == 0:
            continue
        cost = 0
        current_city = 0  # départ
        for ville in chemin:
            cost += matrice_cout[current_city][ville]
            current_city = ville
        cost += matrice_cout[current_city][0]  # retour au départ
        total += cost
    return total

def creer_population(taille_population, nombre_villes, nombre_vehicules):
    population = []
    villes = list(range(1, nombre_villes))  # Sauf ville 0
    for _ in range(taille_population):
        random.shuffle(villes)
        chemins = [[] for _ in range(nombre_vehicules)]
        for idx, ville in enumerate(villes):
            chemins[idx % nombre_vehicules].append(ville)
        population.append(chemins)
    return population

def selection(population, matrice_cout):
    population = sorted(population, key=lambda chemins: cout_chemin_multi(chemins, matrice_cout))
    return population[:len(population)//2]

def croisement(parent1, parent2):
    villes = []
    for chemin in parent1:
        villes.extend(chemin)
    random.shuffle(villes)
    nombre_vehicules = len(parent1)
    enfant = [[] for _ in range(nombre_vehicules)]
    for idx, ville in enumerate(villes):
        enfant[idx % nombre_vehicules].append(ville)
    return enfant

def mutation(chemins, taux_mutation=0.02):
    for chemin in chemins:
        if len(chemin) > 1 and random.random() < taux_mutation:
            i, j = random.sample(range(len(chemin)), 2)
            chemin[i], chemin[j] = chemin[j], chemin[i]
    return chemins

def algorithme_genetique_multi(matrice_cout, nombre_villes, nombre_vehicules, generations=500, taille_population=100):
    population = creer_population(taille_population, nombre_villes, nombre_vehicules)

    for generation in range(generations):
        population = selection(population, matrice_cout)
        
        enfants = []
        while len(enfants) < taille_population:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            enfant = croisement(parent1, parent2)
            enfant = mutation(enfant)
            enfants.append(enfant)
        
        population = enfants

    meilleur_chemin = min(population, key=lambda chemins: cout_chemin_multi(chemins, matrice_cout))
    cout_final = cout_chemin_multi(meilleur_chemin, matrice_cout)
    return meilleur_chemin, cout_final

if __name__ == "__main__":
    json_file = 'cas_reel.json'
    nombre_villes, matrice_cout = load_data(json_file)

    nombre_vehicules = int(input("Entrez le nombre de véhicules : "))
    chemin, cout = algorithme_genetique_multi(matrice_cout, nombre_villes, nombre_vehicules, generations=1000, taille_population=200)

    for i, parcours in enumerate(chemin):
        print(f"Chemin véhicule {i+1} : [0] -> {parcours} -> [0]")
    print("Coût total :", cout)
