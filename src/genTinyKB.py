# -*- coding: utf-8 -*-

import pandas as pd

kb_df = pd.read_csv('././kb/7kb.csv')
kb_df.columns = ['n1', 'rela', 'n2']

tinyKB = pd.DataFrame()

def genTinyKB(path, s):
    t = pd.DataFrame()
    if path == 'player':
        s_df = pd.read_csv('././experiment/s/' + path + '.csv')
    else:
        s_df = pd.read_csv('././rough_tables/' + path + '.csv')

    for k,row in s_df.iterrows():
        name = row[s]
        df = kb_df.loc[(kb_df.n1 == name) | (kb_df.n1.str.startswith(name)) | (kb_df.n2 == ' ' + name)]
        t = pd.concat([t, df], axis=0)
        if k < (len(s_df)-1):
            print('\r' + path + ': ' + str(k+1) + ' / ' + str(len(s_df)), end='', flush=True)
        else:
            print('\r' + path + ': ' + str(k+1) + ' / ' + str(len(s_df)), flush=True)

    return t

paths = ['country','league','player','stadium','team']
for path in paths:
    t = genTinyKB(path, 'name')
    tinyKB = pd.concat([tinyKB, t], axis=0)

tinyKB = tinyKB.drop_duplicates()
tinyKB.to_csv('././kb/tinykb.csv', index=False)