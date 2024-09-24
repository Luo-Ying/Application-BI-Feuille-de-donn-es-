# Application BI - Fouille de données
[Lien Github](https://github.com/Luo-Ying/Application-BI-Feuille-de-donn-es-)

C'est une application d'analyse des données dans le domaine commercial, permettant d'analyser les flux de communication tant sur le plan commercial que financier. Les données proviennent des marchés publics de la France et sont les données collectées des années 2010 à 2020.

Il y a des questionnements qui sont posés dans le but d'y répondre tout au long du travail sur le projet:

- Quelles entreprises communiquent le plus avec quelles autres entreprises ?
- Quelles entreprises ont le plus de flux monétaire sortants/entrants. Y a-t-il des PME parmi elles ?
- D'où provient l'argent qui arrive/sort en plus grande quantité ? (en terme de département français)
- Quelles sont les activités les plus actives ou les plus lucratives en terme de code CPV ?

Le but du script est de lancer une fois le programme. Il va d'abord lire les données, puis dessiner les graphiques basés sur les données brutes dans le but de visualiser les données pour qu'on puisse voir s'il y a des problème des données. Ensuite, la partie du script de nettoyage sera directement appliquée pour nettoyer les données en utilisant les algorithmes qui ont déjà été discutés en interne par l'équipe du projet. Une fois le nettoyage appliqué, les script des générations des graphiques serons relancé pour sortir les graphiques propre basés sur les données nettoyés. En suite, la dernière partie est de générer les sortie (des graphiques et des fichiers) pour répondre aux question posé le début du projet.

Le rapport réalisé : [Rapport](./rapport.pdf)

# Organisation

Les éléments nécessaire:

- `requirements.txt`: La liste des packages Python nécessaires pour l'ensemble du programme.
- Dossier `References`: Les fichiers nécessaire `departements-20180101.*` à la création de la carte français. Le fichier `int_courts_naf_rev_2.xls` sert à référencier les informations des entreprises.
- `main.py`: Python script pour lancer toutes les fonctions du programme.

Ce projet se compose de trois grandes parties :

- Génération des graphiques (basés sur les données brutes et les données nettoyées)
- Nettoyage des données
- Génération des graphiques et des fichiers en répondant aux questions

Avec les répertoires qui contiennent les fichiers de sortie à la fin de l'exécution du programme :

- Le dossier [fig](./fig) contient tous les graphiques générés. (Les dossiers qu'il contient correspondent aux différents tableaux des données, à l'exception du dossier [Flux](./fig/Flux) qui contient les graphiques répondant aux questions posées).
  - Fin du prgramme, dans le dossier [Flux](./fig/Flux), il aura des graphiques générer pour répondre des questions:
    - [Flux_Top_50_des_acheteurs_qui_communiquent_le_plus.png](./fig/Flux/Flux_Top_50_des_acheteurs_qui_communiquent_le_plus_hist.png)
    - [Flux_Top_50_des_acheteurs_qui_communiquent_le_plus.png](./fig/Flux/Flux_Top_50_des_acheteurs_qui_communiquent_le_plus_hist.png)
    - [Flux_Top_50_des_acheteurs_et_des_fournisseurs_qui_communiquent_entre_eux_le_plus.png](./fig/Flux/Flux_Top_50_des_acheteurs_et_des_fournisseurs_qui_communiquent_entre_eux_le_plus_hist.png)
    - [Flux_Top_50_des_acheteurs_avec_le_plus_de_flux_d'agent_sortant.png](./fig/Flux/Flux_Top_50_des_acheteurs_avec_le_plus_de_flux_d'agent_sortant_hist_with_log.png)
    - [Flux_Top_50_des_fournisseurs_avec_le_plus_de_flux_d'agent_entrant.png](./fig/Flux/Flux_Top_50_des_fournisseurs_avec_le_plus_de_flux_d'agent_entrant_hist_with_log.png)
    - [Flux_Top_50_des_département_avec_le_plus_de_flux_d'agent_sortant.png](./fig/Flux/Flux_Top_50_des_département_avec_le_plus_de_flux_d'agent_sortant_hist_with_log.png)
    - [map_France_département_achètent_le_plus.png](./fig/Flux/Flux_Les_département_qui_achètent_le_plus_hist_pivot.png)
    - [Flux_Top_50_des_département_avec_le_plus_de_flux_d'agent_entrant.png](./fig/Flux/Flux_Top_50_des_département_avec_le_plus_de_flux_d'agent_entrant_hist_with_log.png)
    - [map_France_département_fournissent_le_plus.png](./fig/Flux/Flux_Les_département_qui_fournissent_le_plus_hist_pivot.png)
    - [Flux_Top_50_CPV_le_plus_actives.png](./fig/Flux/Flux_Top_50_CPV_flux_hist.png)
    - [Flux_Top_50_CPV_pour_les_acheteurs_qui_génèrent_le_plus_d'argent.png](./fig/Flux/Flux_Top_50_CPV_pour_les_acheteurs_qui_génèrent_le_plus_d'argent_hist_with_log.png)
- Le dossier [Output](./Output) contient les résultats des fichiers répondant aux questions.
  - Fin du prgramme, dans le dossier [Output](./Output), il aura des fichiers générer pour compléter des informations d'entreprise obetenu de l'étape précédents:
    - [Top50_des_acheteurs_qui_communiquent_le_plus_output.csv](./Output/Top50/Top50_des_acheteurs_qui_communiquent_le_plus_output.csv)
    - [Top50_des_fourniseurs_qui_communiquent_le_plus_output.csv](./Output/Top50/Top50_des_fourniseurs_qui_communiquent_le_plus_output.csv)
    - [Top50_des_acheterus_et_fourniseurs_qui_communiquent_entre_eux_le_plus_output.csv](./Output/Top50/Top50_des_acheterus_et_fourniseurs_qui_communiquent_entre_eux_le_plus_output.csv)
    - [Top50_des_acheterus_avec_le_plus_de_flux_argent_sortant_output.csv](./Output/Top50/Top50_des_acheterus_avec_le_plus_de_flux_argent_sortant_output.csv)
    - [Top50_des_fourniseurs_avec_le_plus_de_flux_argent_entrant_output.csv](./Output/Top50/Top50_des_fourniseurs_avec_le_plus_de_flux_argent_entrant_output.csv)


## Installation

Pour lancer le programme:

1. Excécuter `python -m pip install -r requirements.txt` pour installer tous les packages necessaire du programme.
2. S'inscrire sur le site de l'[INSEE](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/sign-up.jag) pour pouvoir utiliser l'API SIREN avec le Bearer Token personnel, dans l'étape de compléter les fichiers CSV avec les informations des entreprises.
3. Créer une fichier `varsEnv.py` dans le racine du projet et y ajouter une variable BEARER_TOKEN, en lui donnant la valeur du Bearer Token personnel obtenu à l'étape précédente.

## Run

Pour lancer le programme:

`python main.py [chemin de la base de donnée]`

## Dépendences

Le programme a testé en version de Python: 3.9.1, avec les packages suivant:

- `sqlite3`: version 3.41.2
- `beautifulsoup4`: version 4.12.3
- `lxml`: version 5.2.1
- `matplotlib`: version 3.8.4
- `numpy`: version1.26.4
- `pandas`: version 2.2.1
- `Requests`: version 2.31.0
- `seaborn`: version 0.13.2
- `tabulate`: version 0.9.0
- `geopandas`: version 0.14.3
- `xlrd`: version 2.0.1


## Données

Le fichier de la base de données a été corrigé avec les données les plus récentes et bonnes, grâce à l'API TED. Le fichier téléchargeable de la base de données avec la version corrigé: [Foppa_cloned.db](https://drive.google.com/file/d/1plHB8bFOZoYeutf7NwbE1q4vqFN9kOal/view?usp=drive_link).

Remarque : si le fichier provient d'une base de données originale, il faut décommenter la fonction `correctedData(conn)` danns le fichier `main.py` afin que le programme puisse se connecter à l'API et corriger les données.

Attention : Veuillez noter que le programme de correction des données via l'API de TED peut être très long!
