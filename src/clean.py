# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from collections import Counter

kb = pd.read_csv('././kb/tinykb.csv')
kb.columns = ['n1', 'rela', 'n2']

print('load KB finished')

paths = ['player','team','league','country','stadium']
needClean = [1,0,0,0,0]

def getRela(n1,n2):
    # n1 is the source node
    f = kb[(kb.n1 == str(n1)) & (kb.n2 == ' ' + str(n2))]
    if len(f) != 0:
        return f.rela.values[0]
    # n2 is the source node
    f = kb[(kb.n1 == str(n2)) & (kb.n2 == ' ' + str(n1))]
    if len(f) != 0:
        return f.rela.values[0]

# reusable
path = 'player'
df = pd.read_csv('././experiment/d/' + path + '_d.csv')

# find pattern
n_row = df.shape[0]
n_col = df.shape[1]

pattern = np.empty([n_col,n_col], dtype=np.object)
for i in range(0,n_col):
    for j in range(i+1,n_col):
        # one relationship
        for k, _ in df.iterrows():
            if (df.iloc[k,i] == 'dirty_data') | (df.iloc[k,j] == 'dirty_data'):
                continue
            n1 = df.iloc[k,i]
            n2 = df.iloc[k,j]
            r = getRela(n1,n2)
            if (r == None) & (k >= 2):
                break
            else:
                pattern[i,j] = r
                pattern[j,i] = r
                continue


# TODO: use crowd to find more edge in patten
# if an attribute column has no relationship with the other,
# we find the point with the highest degree( maybe N0.1,2,3 ) and ask crowd


def loopMatching(n2,rela):
    # n1 is the source node
    df = kb[(kb.n1.str.contains(n2)) & (kb.rela == rela)]
    if len(df) != 0:
        return df.n2.values[0]
    # n2 is the source node
    df = kb[(kb.n2 == ' ' + n2) & (kb.rela == rela)]
    if len(df) != 0:
        return df.n1.values[0]
    pass

def repair(n_list,rela_list):
    l = list()
    i = 0
    for r in rela_list:
        p = loopMatching(n_list[i],r)
        if p != None:
            l.append(p)
        i += 1

    #TODO: sth can do here. For example：Ask the crowd here
    rep = Counter(l).most_common(1)
    if len(rep) != 0:
        return rep[0][0]

print('cleaning...')
# cleaning
idx_r,idx_c = np.where(df=='dirty_data')
n = 0
for i in idx_r:
    # now we get the row number: i
    j = idx_c[n]
    a = pattern[:,j]

    r_l = list()
    n_l = list()
    s = 0
    for rela in a:
        if rela == None:
            s += 1
            continue
        r_l.append(rela)
        n_l.append(df.iloc[i,s])
        s += 1

    rep = repair(n_l, r_l)
    if rep != None:
        # print(rep)
        df.iloc[i,j] = 'FromKB' + rep

    n += 1
    print('\r' + path + '-cleaned:' + str(n) + ' / ' + str(len(idx_r)), end='', flush=True)

df.to_csv('././experiment/c/' + path + '_c.csv', index=False)