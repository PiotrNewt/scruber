# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

kb_df = pd.read_csv('./7kb.csv')
kb_df.columns = ['n1', 'rela', 'n2']

# player
# id,name,nationality,birthplace,birthday,height,weight,team_id,position
team_df = pd.read_csv('./rough_tables/t.csv')
idx = 0
p_r_df = pd.DataFrame(columns=['id','name','nationality','birthplace','birthday','height','weight','team_id','position'])
player_pair = [[' 中文名','name'],[' 国籍','nationality'],[' 出生地','birthplace'],[' 出生日期','birthday'],[' 身高','height'],[' 体重','weight'],[' 场上位置','position']]
count_limit = 55

for i,row in team_df.iterrows():
    team_name = row['name']
    ps_df = kb_df[(kb_df.rela ==' 所属运动队') & (kb_df.n2 == ' '+ team_name)]
    ps_name = ps_df['n1'].values
    ps_name = np.unique(ps_name)
    count = 0
    for name in ps_name:
        if count >= count_limit:
            break

        p_df = kb_df[kb_df.n1 == name]
        p_r_df.loc[idx] = None
        pr = p_r_df.loc[idx]

        b_flag = False
        for pp in player_pair:
            v = p_df[p_df.rela == pp[0]]['n2'].values
            if len(v) != 0:
                if type(v[0]) == str:
                    pr[pp[1]] = v[0][1:]
                else:
                    pr[pp[1]] = v[0]
            else:
                b_flag = True
                break

        if b_flag == True:
            continue

        pr.id = idx + 1
        pr.team_id = i + 1
        idx += 1
        print('\r' + 'team:' + str(i+1) + ', player: ' + str(idx), end='', flush=True)
        count += 1

p_r_df.to_csv('./player_r.csv', index=False)


#---Reusable---#
def completeTable(path,rpath,pair):
    df = pd.read_csv(path)
    r_df = pd.DataFrame()
    for i, _ in df.iterrows():
        d = df.loc[[i]]
        entity_df = kb_df[kb_df.n1 == d.name.values[0]]

        for p in pair:
            v = entity_df[entity_df.rela == p[0]]['n2'].values
            if len(v) != 0:
                if type(v[0]) == str:
                    d[p[1]] = v[0][1:]
                else:
                    d[p[1]] = v[0]

        r_df = pd.concat([r_df, d], axis=0)

    r_df.to_csv(rpath, index=False)

'''
# stadium
pair = [[' 位置','location'],[' 竣工时间','completion_time'],[' 容量','num_seats']]
completeTable('./rough_tables/stadium.csv','./stadium_r.csv',pair)
# team
pair = [[' 角逐赛事','league_id'],[' 所属地区','location'],[' 成立时间','established'],[' 主场馆','stadium_id'],[' 现任主教练','coach'],[' 现任队长','captain']]
completeTable('./rough_tables/team.csv','./team_r.csv',pair)
# country
pair = [[' 国家代码','code'],[' 首都','capital'],[' 官方语言','language'],[' 货币','currency']]
completeTable('./rough_tables/country.csv','./country.csv',pair)
# league_r
pair = [[' 国家','country'],[' 成立年份','year_established'],[' 球队数目','num_teams'],[' 所属协会','association']]
completeTable('./rough_tables/league.csv','./league_r.csv',pair)
'''

