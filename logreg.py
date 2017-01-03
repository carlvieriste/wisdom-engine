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

import numpy as np
import sklearn.feature_extraction.text
import yaml


def load_yaml(filename):
    yaml_data = {}
    with open(filename, 'r') as file:
        try:
            yaml_data = yaml.load(file)
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    return yaml_data


def extract_qa_ama(filename):
    yaml_data = load_yaml(filename)
    raw_questions = []
    raw_answers = []
    for q in yaml_data['comments']:
        raw_questions.append(q['body'])
        raw_answers.append(q['__replies'][0]['body'])
    return raw_questions, raw_answers


def extract_qa(filename):
    yaml_data = load_yaml(filename)
    raw_questions = []
    raw_answers = []
    for q in yaml_data:
        if len(q['selftext']) == 0:
            continue
        raw_questions.append(q['selftext'])
        for a in q['__comments']:
            raw_answers.append(a['body'])
    return raw_questions, raw_answers


# 1. Representation =================================================
#   1.1 TODO Stemming       relation mot -> remplacement
#   1.2 TF-IDF              importance de chaque mot : obtenir matrice tfdif(i,j) = importance de j dans i
#   1.3 Afficher les D mots les plus importants du corpus

D = 512

# Preparer dataset
print('Loading data')
# raw_questions, raw_answers = extract_qa_ama('data/3jd7hj.yaml')
# confucianism_1482268487.045067  taoism_1482257353.98838
raw_questions, raw_answers = extract_qa('data/confucianism_1482268487.045067.yaml')

# Texts to matrix of representations
print('Analyzing corpus')
raw_all_texts = raw_questions  # raw_questions + raw_answers
vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(stop_words='english')
all_repr = vectorizer.fit_transform(raw_all_texts)
all_repr = all_repr.toarray()
index_to_word = {}
for word, idx in vectorizer.vocabulary_.items():
    index_to_word[idx] = word

# Keep best words
print('Finding best words')
word_importance = np.linalg.norm(all_repr, axis=0, ord=2)  # np.sum(all_repr, axis=0)
best_words = np.argsort(word_importance)[::-1][:D]
for widx in best_words:
    print("{:>20} {}".format(index_to_word[widx], word_importance[widx]))

