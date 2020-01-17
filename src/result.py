# -*- coding: utf-8 -*-

import pandas as pd
import math
import pickle

paths = ['player','team','league','country','stadium']
c_bool = [1,0,0,0,0]

i = 0
result = []
for path in paths:
    c = c_bool[i]
    if c != 1:
        i += 1
        continue

    n = 0
    df_c = pd.read_csv('././experiment/c/' + path + '_mc.csv')
    df_s = pd.read_csv('././experiment/s/' + path + '.csv')

    if df_c.shape[0] != df_s.shape[0]:
        print('Data shape error: {}'.format(path))
        i += 1
        continue

    f = open('././experiment/d/' + path + '_rand.bin', "rb")
    dirty_idx = pickle.load(f)

    for idx in dirty_idx:
        rstr = str(df_c.iloc[idx[0],idx[1]])
        if rstr.startswith('FromKB'):
            n += 1
            continue
        if df_c.iloc[idx[0],idx[1]] == df_s.iloc[idx[0],idx[1]]:
            n += 1

    print('{} : num_dd = {}, repaired = {}, rate = {}'.format(path, len(dirty_idx), n, (n/len(dirty_idx))))
    i += 1