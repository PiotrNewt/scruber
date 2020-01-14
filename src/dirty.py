# -*- coding: utf-8 -*-

import pandas as pd
import random
import math
import pickle

# country   18 * 6
# league    5 * 6
# player    740 * 9
# stadium   56 * 5
# team      50 * 7

paths = ['player','team','league','country','stadium']
ps = [0.1,0.3,0,0,0]

i = 0
for path in paths:
    p = ps[i]
    if p <= 0:
        i += 1
        continue

    df = pd.read_csv('././experiment/s/' + path + '.csv')
    n_row = df.shape[0]
    n_col = df.shape[1] - 1 # do not dirty the id (-1)

    s = n_row * n_col
    rand_list = random.sample(range(0,s), math.ceil(s * p))

    dirty_idx = []
    for idx in rand_list:
        r = math.ceil(idx / n_col)
        c = idx - n_col * (r - 1) + 1
        dirty_idx.append([r-1,c-1])

    for idx_p in dirty_idx:
        df.iloc[idx_p[0],idx_p[1]] = 'dirty_data'

    df.to_csv('././experiment/d/' + path + '_d.csv', index=False)
    f = open('././experiment/d/' + path + '_rand.bin','wb')
    pickle.dump(dirty_idx,f)
    f.close()
    i += 1