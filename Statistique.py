import matplotlib.pyplot as plt
from utils import load_data, lire_donnees_graph
from Solveur_Genetique_contrainte import run_genetique
from Solveur_Voisin_contrainte import run_voisin
from Solveur_Recuit_Simule import run_recuit

def main():
    json_file = 'cas_reel.json'
    nombre_vehicules = int(input("Entrez le nombre de véhicules : "))
    nombre_villes, matrice_cout = load_data(json_file)
    G, _ = lire_donnees_graph(json_file)

    couts_genetique, temps_genetique = run_genetique(matrice_cout, nombre_villes, nombre_vehicules)
    couts_voisin, temps_voisin = run_voisin(matrice_cout, nombre_villes, nombre_vehicules)
    couts_recuit, temps_recuit = run_recuit(G, nombre_villes, nombre_vehicules)

    # Tracer
    plt.figure(figsize=(12,6))
    plt.plot(range(len(couts_genetique)), couts_genetique, label="Génétique")
    plt.plot(range(len(couts_voisin)), couts_voisin, label="Plus Proche Voisin")
    plt.plot(range(len(couts_recuit)), couts_recuit, label="Recuit Simulé")
    plt.xlabel("Itérations")
    plt.ylabel("Coût total (distance parcourue)")
    plt.title("Évolution du coût total")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12,6))
    plt.plot(range(len(temps_genetique)), temps_genetique, label="Génétique")
    plt.plot(range(len(temps_voisin)), temps_voisin, label="Plus Proche Voisin")
    plt.plot(range(len(temps_recuit)), temps_recuit, label="Recuit Simulé")
    plt.xlabel("Itérations")
    plt.ylabel("Temps cumulé (secondes)")
    plt.title("Évolution du temps cumulé")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
