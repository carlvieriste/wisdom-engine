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
#   Désavantages:   - Imprécisions dûes au stemming
#                   - Pas de relation entre les mots (embeddings)

import keras.preprocessing.text

# 1. Representation =================================================
#   1.1 Porter stemming     TODO relation mot -> remplacement
#   1.2 TF-IDF              importance de chaque mot : obtenir vecteur "importance selon doc" pour chaque mot,
#                           garder les D mots avec la plus grande norme
#   1.3 Afficher les D mots les plus importants du corpus

D = 512

# Charger dataset: liste de questions, liste de reponses, assoc rep -> quest
raw_questions = []
raw_answers = []
raw_all_texts = raw_questions + raw_answers
tokenizer = keras.preprocessing.text.Tokenizer(nb_words=D)
tokenizer.fit_on_texts(raw_all_texts)
questions_repr = tokenizer.texts_to_matrix(raw_questions, 'tfidf')  # TODO est-ce bon?
answers_repr = tokenizer.texts_to_matrix(raw_answers, 'tfidf')

