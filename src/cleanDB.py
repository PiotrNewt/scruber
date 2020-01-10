# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import pickle
import math
from collections import Counter

kb = pd.read_csv('././kb/tinykb.csv')
kb.columns = ['n1', 'rela', 'n2']
print('load KB finished')

paths = ['player','team','league','country','stadium']
needClean = [1,1,0,0,0]
tables = []
shape = []

c = 0
i = -1
for path in paths:
    i += 1
    df = pd.DataFrame()
    if needClean[i] == 1:
        df = pd.read_csv('././experiment/d/' + path + '_d.csv')
    else:
        df = pd.read_csv('././experiment/s/' + path + '.csv')
    c += df.shape[1]
    tables.append(df)
    shape.append([df.shape[0],df.shape[1]])

i = -1

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
        n1 = df.iloc[k,c1]
        n2 = df.iloc[k,c2]
        r = getRela(n1,n2)
        if k >= 10:
            return r
    return r

def getIdx(t,i):
    idx = 0
    for n in range(0,len(shape)):
        if n == t:
            idx += i
            return idx
        idx += shape[n][1]

def findClosetPattern(t1,t2,r1,r2,c1,c2):
    df1 = tables[t1]
    df2 = tables[t2]
    for i in range(0,shape[t1][1]):
        if i == c1:
            continue
        for j in range(shape[t2][1]):
            if j == c2:
                continue

            if str(df1.iloc[r1,i]) == str(df2.iloc[r2,j]):
                h1 = getIdx(t1,i)
                h2 = getIdx(t2,j)
                return h1,h2
    return -1,-1

def getTwoTableRela(t1,t2,c1,c2):
    df1 = tables[t1]
    df2 = tables[t2]
    count = 0
    for r1, _ in df1.iterrows():
        if (df1.iloc[r1,c1] == 'dirty_data'):
                continue
        for r2, _ in df2.iterrows():
            if (df2.iloc[r2,c2] == 'dirty_data'):
                continue
            n1 = df1.iloc[r1,c1]
            n2 = df2.iloc[r2,c2]
            r = getRela(n1,n2)
            if r != None:
                # 3 pair means well done
                count += 1
                if count > 3:
                    h1,h2 = findClosetPattern(t1,t2,r1,r2,c1,c2)
                    # if t1 == 0 and t2 == 1 and c1 == 1 and c2 == 1:
                    #     print(r,h1,h2)
                    return r,h1,h2

            # loop control
            if r2 >= len(df2):
                break
            if r1 >= 10:
                return None,-1,-1

    return None,-1,-1

'''
# find patten
pattern = np.empty([c,c], dtype=np.object)
n = 0
for i in range(0,c):
    for j in range(i+1,c):
        n += 1
        t1,c1 = findIdx(i)
        t2,c2 = findIdx(j)
        if t1 == t2:
            r = getSingleTableRela(t1,c1,c2)
        else:
            r,h1,h2 = getTwoTableRela(t1,t2,c1,c2)
            if h1 != -1 and h2 != -1 and h1 != h2:
                # t2 link id and attribute column
                pattern[j,h2] = 'link'
                pattern[h2,j] = 'link'
                # encode the outter key
                pattern[i,h1] = str(c1) + '_' + str(t2) + '_' + str(c2)
                pattern[h1,i] = str(c1) + '_' + str(t2) + '_' + str(c2)
                # column h1 is column h2
                pattern[h1,h2] = 'is'
                pattern[h2,h1] = 'is'
            else:
                r = None

        if r != None:
            pattern[i,j] = r
            pattern[j,i] = r
        print('\r' + 'find pattern:' + str(n) + ' / ' + str(math.ceil(c*c/2)), end='', flush=True)

# print(pattern)
# pa = pd.DataFrame(pattern)
# pa.to_csv('././experiment/pattern.csv', index=False)

f = open('././experiment/pattern.bin','wb')
pickle.dump(pattern,f)
f.close()
'''


f = open('././experiment/pattern.bin', "rb")
pattern = pickle.load(f)

# TODO: here to load pattern
# pattern_df = pd.read_csv('././experiment/pattern.csv')
# pattern = pattern_df.values

# repair
# findIdxRange find the idx range by the t idx in tables
def findIdxRange(t):
    i = -1
    a = 0
    b = 0
    for s in shape:
        i += 1
        if i == t:
            b = a + s[1]
            break
        a += s[1]

    # a+1 means we don't need consider id
    return range(a+1,b)

def loopMatch(n2,rela):
    # n1 is the source node
    df = kb[(kb.n1.str.contains(n2)) & (kb.rela == rela)]
    if len(df) != 0:
        return df.n2.values[0]
    # n2 is the source node
    df = kb[(kb.n2 == ' ' + n2) & (kb.rela == rela)]
    if len(df) != 0:
        return df.n1.values[0]

def complexMatch(t1,c1,r_arr,r1,t2,c2):
    df = tables[t1]
    h1 = getIdx(t1,c1)
    h2 = getIdx(t2,c2)
    rela = pattern[h1,h2]
    rep = loopMatch(df.iloc[r1,c1],rela)
    if rep == None:
        return None

    rep = rep.replace(' ', '')

    # find the 'is' one
    i = -1
    for r in r_arr:
        i += 1
        if r == 'is':
            df2 = tables[t2]
            c_name = df2.columns.values[c2]
            rdf = df2.loc[df2[c_name] == rep]
            _,c = findIdx(i)
            vs = rdf.iloc[:,c].values
            if len(vs) != 0:
                return vs[0]

def repairOne(t_idx, r_idx, r_arr):
    df = tables[t_idx]
    idxRange = findIdxRange(t_idx)
    l = list()
    rc = -1
    first = -1
    for rela in r_arr:
        rc += 1
        if rela == None:
            continue

        first += 1
        if rc not in idxRange:
            continue

        i_l = rela.split('_')
        # this datum need be find in another table
        if len(i_l) == 3 and first == 0:
            t1 = t_idx
            t2 = int(i_l[1])
            c1 = int(i_l[0])
            c2 = int(i_l[2])
            rep = complexMatch(t1,c1,r_arr,r_idx,t2,c2)
            return rep, False

        fi = findIdx(rc)
        if fi[0] != t_idx:
            print('find idx error: t-{}, e-{}'.format(t_idx,fi[0]))
            return None, False

        p = loopMatch(df.iloc[r_idx,fi[1]],rela)
        if p != None:
            l.append(p)

    rep = Counter(l).most_common(1)
    if len(rep) != 0:
        return rep[0][0], True

    return None, False


def repairTable(idx):
    df = tables[idx]
    idx_r,idx_c = np.where(df=='dirty_data')
    # print(idx_r,idx_c)
    n = -1
    for i in idx_r:
        # i is the dirty data row number
        n += 1
        j = idx_c[n]
        h = getIdx(idx,j)

        # get the col in pattern
        a = pattern[:,h]

        rep, fromKB = repairOne(idx, i, a)
        if rep != None and fromKB == True:
            df.iloc[i,j] = 'FromKB' + rep
        else:
            df.iloc[i,j] = rep

        print('\r' + paths[idx] + '-cleaned:' + str(n+1) + ' / ' + str(len(idx_r)), end='', flush=True)

i = len(paths)
for nc in needClean[::-1]:
    i -= 1
    if nc == 0:
        continue
    repairTable(i)

# write back
i = -1
for path in paths:
    i += 1
    if needClean[i] == 0:
        continue
    df = tables[i]
    df.to_csv('././experiment/c/' + path + '_mc.csv', index=False)