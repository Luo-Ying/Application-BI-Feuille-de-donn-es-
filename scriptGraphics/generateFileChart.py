import os
import sys
import matplotlib.pyplot as plt


def generateFileChart(nom_fichier, filename, type):
    nom_fichier_sortie = f'fig\\{nom_fichier}\\{nom_fichier}_{filename}_{type}'
    isExist = os.path.exists(sys.path[0] + f'\\fig')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\fig')

    isExist = os.path.exists(sys.path[0] + f'\\fig\\{nom_fichier}')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\fig\\{nom_fichier}')
    plt.savefig(f'fig/{nom_fichier}/{nom_fichier}_{filename}_{type}')
    print(f"Résultats enregistrés dans {nom_fichier_sortie}")


def generateFileTab(nom_fichier, filename, content):
    # Enregistrer les résultats dans un fichier CSV
    extension = 'output'
    nom_fichier_sortie = f'Output\\{nom_fichier}\\{nom_fichier}_{filename}_{extension}.csv'

    isExist = os.path.exists(sys.path[0] + f'\\Output\\{nom_fichier}')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\Output\\{nom_fichier}')

    content.to_csv(sys.path[0] + f'\\{nom_fichier_sortie}', index=False)
    print(f"Résultats enregistrés dans {nom_fichier_sortie}")
