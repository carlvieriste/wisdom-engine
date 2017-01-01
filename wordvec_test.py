import numpy as np
import sklearn.neighbors.kd_tree

idx_to_word = []
word_to_idx = {}
embeddings_str = []

D = 300
count = 0

# Get word to index relation, load data as str
with open('glove/glove.6B.{}d.txt'.format(D), 'r') as file:
    for line in file.readlines():
        sep = line.index(' ')
        word = line[:sep]
        emb_str = line[sep+1:].strip()

        idx_to_word.append(word)
        word_to_idx[word] = len(word_to_idx)
        embeddings_str.append(emb_str)

        count += 1
        if count >= 10000:
            print(len(word_to_idx))
            count = 0

count = 0

# Load embeddings
N = len(word_to_idx)
embeddings = np.zeros((N, D))
for i, v in enumerate(embeddings_str):
    embeddings[i] = np.fromstring(v, sep=' ')

    count += 1
    if count >= 10000:
        print(i)
        count = 0

del embeddings_str

tree = sklearn.neighbors.KDTree(embeddings)


def wv(word):
    return embeddings[word_to_idx[word]]


def vec2word(vec):
    dist, ind = tree.query([vec], k=7)
    dist = dist[0]
    ind = ind[0]
    pairs = zip(ind, dist)
    for idx, dist in pairs:
        print(idx_to_word[idx] + '  ' + str(dist))


def ana2(a, b, c):
    excl = [a, b, c, a + 's', b + 's', c + 's',
            a.replace('y', 'ies'), b.replace('y', 'ies'), c.replace('y', 'ies')]
    d = wv(c) + wv(b) - wv(a)
    dist, ind = tree.query([d], k=7)
    dist = dist[0]
    ind = ind[0]
    pairs = zip(ind, dist)
    ans = "OOPS"
    for idx, dist in pairs:
        w = idx_to_word[idx]
        if w in excl:
            continue
        ans = w
        break
        # print(w + '  ' + str(dist))
        # break  # Only show first
    print(a + ' is to ' + b + ' as ' + c + ' is to ' + ans)


def ana3():
    entree = input()
    a, b, c = entree.split(' ')
    ana2(a, b, c)


def analogies():
    while True:
        print("\nAnalogy - (1) is to (2) as (3) is to...")
        entree = input()
        if len(entree.strip()) == 0:
            break
        a, b, c = entree.split(' ')
        ana2(a, b, c)


def ana(a, b, c):
    return vec2word(wv(c) + wv(b) - wv(a))
