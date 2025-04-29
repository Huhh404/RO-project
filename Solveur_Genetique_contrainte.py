import json
import random
import time

def load_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    nombre_villes = data["nombre_de_villes"]
    matrice_cout = data["matrice_cout"]

    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if matrice_cout[i][j] in ("Infinity", "inf"):
                matrice_cout[i][j] = float('inf')
    return nombre_villes, matrice_cout

def cout_chemin_multi(chemins, matrice_cout):
    total = 0
    for chemin in chemins:
        if not chemin:
            continue
        cost = matrice_cout[0][chemin[0]]
        for i in range(len(chemin) - 1):
            cost += matrice_cout[chemin[i]][chemin[i+1]]
        cost += matrice_cout[chemin[-1]][0]
        total += cost
    return total

def creer_population(taille_population, nombre_villes, nombre_vehicules):
    population = []
    villes = list(range(1, nombre_villes))
    for _ in range(taille_population):
        random.shuffle(villes)
        chemins = [[] for _ in range(nombre_vehicules)]
        for idx, ville in enumerate(villes):
            chemins[idx % nombre_vehicules].append(ville)
        population.append(chemins)
    return population

def selection_tournoi(population, matrice_cout, taille_tournoi=5):
    nouveaux_parents = []
    for _ in range(len(population) // 2):
        tournoi = random.sample(population, taille_tournoi)
        meilleur = min(tournoi, key=lambda ch: cout_chemin_multi(ch, matrice_cout))
        nouveaux_parents.append(meilleur)
    return nouveaux_parents

def croisement(parent1, parent2):
    villes = []
    for chemin in parent1:
        villes.extend(chemin)

    used = set()
    enfant = [[] for _ in range(len(parent1))]
    index = 0
    for chemin in parent2:
        for ville in chemin:
            if ville not in used:
                enfant[index % len(enfant)].append(ville)
                used.add(ville)
                index += 1

    # Ajouter les villes manquantes
    for ville in villes:
        if ville not in used:
            enfant[index % len(enfant)].append(ville)
            index += 1
    return enfant

def mutation(chemins, taux_mutation=0.02):
    # Intra-chemin mutation
    for chemin in chemins:
        if len(chemin) > 1 and random.random() < taux_mutation:
            i, j = random.sample(range(len(chemin)), 2)
            chemin[i], chemin[j] = chemin[j], chemin[i]

    # Inter-chemin mutation
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(chemins)), 2)
        if chemins[i] and chemins[j]:
            vi = random.choice(chemins[i])
            vj = random.choice(chemins[j])
            chemins[i][chemins[i].index(vi)] = vj
            chemins[j][chemins[j].index(vj)] = vi
    return chemins

def algorithme_genetique_multi(matrice_cout, nombre_villes, nombre_vehicules, generations=1000, taille_population=200):
    population = creer_population(taille_population, nombre_villes, nombre_vehicules)
    meilleur_cout = float('inf')
    meilleur_chemin = None

    for gen in range(generations):
        population = selection_tournoi(population, matrice_cout)
        enfants = []
        while len(enfants) < taille_population:
            parent1, parent2 = random.sample(population, 2)
            enfant = croisement(parent1, parent2)
            taux_mut = 0.05 if gen < generations * 0.5 else 0.01  # Mutation plus élevée au début
            enfant = mutation(enfant, taux_mut)
            enfants.append(enfant)

        population = enfants
        candidat = min(population, key=lambda ch: cout_chemin_multi(ch, matrice_cout))
        cout = cout_chemin_multi(candidat, matrice_cout)
        if cout < meilleur_cout:
            meilleur_cout = cout
            meilleur_chemin = candidat

    return meilleur_chemin, meilleur_cout

if __name__ == "__main__":
    json_file = 'test.json'
    nombre_villes, matrice_cout = load_data(json_file)
    nombre_vehicules = int(input("Entrez le nombre de véhicules : "))

    start_time = time.time()
    chemin, cout = algorithme_genetique_multi(matrice_cout, nombre_villes, nombre_vehicules)
    
    for i, parcours in enumerate(chemin):
        print(f"Chemin véhicule {i+1} : [0] -> {parcours} -> [0]")
    print("Coût total :", cout)
    print(f"Temps d'exécution : {time.time() - start_time:.2f} secondes")
