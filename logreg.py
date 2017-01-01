# Méthode simple:
#   Représentation: BOW avec les meilleurs mots selon TF-IDF
#   Régression:     Régression logistique
#   Méthode:    1.  Représenter le dataset (et les paragraphes de la litt.)
#                   On obtient Q' et R'.
#               2.  Entraîner une reg. log.
#                   On obtient R'_est = f(Q')
#               3.  Inférence:  - Représenter la question avec Q'
#                               - Trouver R'_est = f(Q')
#                               - Trouver les KNN de R'_est -> voici les fragments philosophiques recherchés.

