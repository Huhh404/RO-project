import random
import time
from utils import cout_chemin_multi

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

def run_genetique(matrice_cout, nombre_villes, nombre_vehicules, generations=2500, taille_population=100):
    historique_couts = []
    historique_temps = []

    population = creer_population(taille_population, nombre_villes, nombre_vehicules)
    start = time.perf_counter()

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
        cout_actuel = cout_chemin_multi(meilleur_chemin, matrice_cout)

        historique_couts.append(cout_actuel)
        historique_temps.append(time.perf_counter() - start)

    return historique_couts, historique_temps
