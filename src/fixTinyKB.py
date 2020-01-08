# -*- coding: utf-8 -*-

import pandas as pd

kb = pd.read_csv('././kb/tinykb.csv')
kb.columns = ['n1', 'rela', 'n2']

for i, row in kb.iterrows():
    if '[' in str(row['n1']):
        kb.loc[i, 'n1'] = str(row['n1']).split('[',1)[0]
        # x = df.n1.str.split('[',1)
        # print(x[0][0])
        # df.n1 = x[0][0]

kb.to_csv('././kb/tinykb.csv', index=False)