# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

kb = pd.read_csv('././kb/7kb.csv')
kb.columns = ['n1', 'rela', 'n2']
print('load KB finished')

paths = ['country','league','player','stadium','team']
tables = []
shape = []

c = 0
for path in paths:
    df = pd.read_csv('././experiment/d/' + path + '_d.csv')
    c += df.shape[1]
    tables.append(df)
    shape.append([df.shape[0],df.shape[1]])


def findIdx(i):
    i += 1
    x = 0
    for s in shape:
        col = s[1]
        if i <= col:
            return x,i-1
        i -= col
        x += 1

def getRela(n1,n2):
    # n1 is the source node
    f = kb[(kb.n1 == str(n1)) & (kb.n2 == ' ' + str(n2))]
    if len(f) != 0:
        return f.rela.values[0]
    # n2 is the source node
    f = kb[(kb.n1 == str(n2)) & (kb.n2 == ' ' + str(n1))]
    if len(f) != 0:
        return f.rela.values[0]

def getSingleTableRela(t,c1,c2):
    df = tables[t]
    r = ''
    for k, _ in df.iterrows():
            if (df.iloc[k,c1] == 'dirty_data') & (df.iloc[k,c2] == 'dirty_data'):
                continue
            n1 = df.iloc[k,i]
            n2 = df.iloc[k,j]
            r = getRela(n1,n2)
            if k >= 2:
                return r

def getTwoTableRela(t1,t2,c1,c2):
    # TODO: Two tables rela
    # is
    pass

# find patten
pattern = np.empty([c,c], dtype=np.object)

for i in range(0,c):
    for j in range(i+1,c):
        t1,c1 = findIdx(i)
        t2,c2 = findIdx(j)
        if t1 == t2:
            r = getSingleTableRela(t1,c1,c2)
        else:
            r = getTwoTableRela(t1,t2,c1,c2)
        pattern[i,j] = r
        pattern[j,i] = r

# repair
def repairTable(df):
    pass

for df in tables:
    repairTable(df)


# write back